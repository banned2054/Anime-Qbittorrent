import asyncio

import aiohttp as aiohttp
import yaml
# coding:utf-8
from PyQt5.QtCore import QUrl, Qt
from PyQt5.QtGui import QDesktopServices, QStandardItem, QStandardItemModel
from PyQt5.QtWidgets import QApplication, QMenu, QSizePolicy, QSpacerItem, QVBoxLayout
from qasync import asyncSlot
from qfluentwidgets import MessageBox, SearchLineEdit, TableView

from src.view.base_view import Widget


class MyModel(QStandardItemModel):
    def __init__(self, row, column):
        super().__init__(row, column)
        self._data = []

    def columnCount(self, parent = None):
        # 这里返回4，因为你要的是4列
        return 4

    def headerData(self, section, orientation, role = Qt.DisplayRole):
        if role == Qt.DisplayRole and orientation == Qt.Horizontal:
            return ["Name", "Name CN", "Date", "URL"][section]


class MyTable(TableView):
    def __init__(self, parent = None):
        super(MyTable, self).__init__(parent)
        self.model = MyModel(0, 4)
        self.setModel(self.model)
        self.setColumnWidth(0, 250)
        self.setColumnWidth(1, 200)
        self.setColumnWidth(2, 100)
        self.setColumnWidth(3, 250)
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.verticalHeader().setVisible(False)
        self.customContextMenuRequested.connect(self.show_context_menu)

    def show_context_menu(self, position):
        menu = QMenu(self)
        copy_action = menu.addAction("Copy URL")
        copy_action.triggered.connect(self.copy_url)
        menu.exec_(self.mapToGlobal(position))

    def copy_url(self):
        index = self.currentIndex()
        if index.isValid():
            text = index.data()
            QApplication.clipboard().setText(text)

    def add_row(self, data):
        items = [QStandardItem(str(d)) for d in data]
        self.model.appendRow(items)

    def mouseDoubleClickEvent(self, event):
        index = self.currentIndex()
        if index.column() == 3 and index.isValid():
            url = index.data()
            QDesktopServices.openUrl(QUrl(url))

    def update_data(self, data):
        self.model.clear()  # 清除旧的数据

        for index, row in enumerate(data):
            now_name = row['name']
            now_name_cn = row['name_cn']
            now_date = row['date']
            now_url = row['url']
            standardItem1 = QStandardItem(now_name)
            standardItem1.setToolTip(now_name)
            standardItem2 = QStandardItem(now_name_cn)
            standardItem2.setToolTip(now_name_cn)
            standardItem3 = QStandardItem(now_date)
            standardItem3.setToolTip(now_date)
            standardItem4 = QStandardItem(now_url)
            standardItem4.setToolTip(now_url)
            self.model.appendRow([standardItem1, standardItem2, standardItem3, standardItem4])

        self.setColumnWidth(0, 250)
        self.setColumnWidth(1, 200)
        self.setColumnWidth(2, 100)
        self.setColumnWidth(3, 250)


# class EnterSearchFilter(QObject):
# enterPressed = pyqtSignal()
#
# def eventFilter(self, obj, event):
#     if event.type() == QEvent.KeyPress and obj is SearchLineEdit:
#         if event.key() == Qt.Key_Return or event.key() == Qt.Key_Enter:
#             self.enterPressed.emit()
#             return True
#     return QObject.eventFilter(self, obj, event)


class SearchWidget(Widget):
    def __init__(self, parent = None):
        super().__init__(parent = parent)
        self.setObjectName("search-widget")
        self.lock = asyncio.Lock()
        self.vBoxLayout = QVBoxLayout(self)
        self.vBoxLayout.setSpacing(50)
        self.lineEdit = SearchLineEdit(self)
        self.lineEdit.searchButton.clicked.connect(self.async_search)
        # self.lineEdit.installEventFilter(EnterSearchFilter())
        self.lineEdit.setClearButtonEnabled(True)
        self.lineEdit.setPlaceholderText('Search icon')
        self.dataTable = MyTable()

        spacerItem = QSpacerItem(20, 50, QSizePolicy.Minimum, QSizePolicy.Fixed)
        self.vBoxLayout.addItem(spacerItem)
        self.vBoxLayout.addWidget(self.lineEdit)
        self.vBoxLayout.addWidget(self.dataTable)

    @asyncSlot()
    async def async_search(self):
        search_keyword = self.lineEdit.text()
        if search_keyword == "":
            return
        self.lineEdit.searchButton.setEnabled(False)
        async with self.lock:
            with open('C:\\Code\\Python\\Anime-Qbittorrent\\src\\data\\bangumi.yaml', 'r') as file:
                data = yaml.safe_load(file)

            bangumi_token = data['bangumi_token']
            version = data['version']
            result = await self.get_anime_info(version, search_keyword, bangumi_token)
            if isinstance(result, str):
                self.lineEdit.searchButton.setEnabled(True)
                w = MessageBox(
                        '错误',
                        '搜索失败，请检查是网络问题还是搜索词不对',
                        self
                )
                w.exec()
                return
            self.dataTable.update_data(result)
        self.lineEdit.searchButton.setEnabled(True)

    async def get_anime_info(self, version, keyword, access_token):

        params = {
            'type': 2
        }
        headers = {
            "User-Agent"   : f"banned/Anime-Qbittorrent/{version} (https://github.com/banned2054/Anime-Qbittorrent)",
            "Authorization": f"Bearer {access_token}"
        }

        url = f"https://api.bgm.tv/search/subject/{keyword}"
        data = await self.get_request(url, headers, params)
        result = await self.analysis_search_result(data, version, access_token)
        return result

    @staticmethod
    async def get_request(url, headers, params = None):
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers = headers, params = params) as response:
                if response.status == 200:
                    try:
                        data = await response.json()
                        return data
                    except aiohttp.ClientResponseError:
                        return "Failed to parse JSON"
                else:
                    return f"Error: {response.status}"

    async def analysis_search_result(self, data, version, access_token):
        if isinstance(data, str):
            return data
        headers = {
            "User-Agent"   : f"banned/Anime-Qbittorrent/{version} (https://github.com/banned2054/Anime-Qbittorrent)",
            "Authorization": f"Bearer {access_token}"
        }
        if data.get("results") > 0:
            results = []
            for item in data.get("list", []):
                result = {
                    "url"    : item.get("url"),
                    "name"   : item.get("name"),
                    "name_cn": item.get("name_cn")
                }

                # Get subject id from url
                subject_id = result["url"].split("/")[-1]

                subject_url = f"https://api.bgm.tv/v0/subjects/{subject_id}"
                subject_data = await self.get_request(subject_url, headers)
                results = self.analysis_subject_result(subject_data, results, result)
            return results
        else:
            return "No results found"

    @staticmethod
    def analysis_subject_result(data, results, result):
        if isinstance(data, str):
            return data
        result["date"] = data.get("date")
        results.append(result)
        return results
