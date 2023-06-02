import asyncio

# coding:utf-8
from PyQt5.QtCore import QUrl, Qt
from PyQt5.QtGui import QDesktopServices, QStandardItem, QStandardItemModel
from PyQt5.QtWidgets import QApplication, QMenu, QSizePolicy, QSpacerItem, QVBoxLayout
from qasync import asyncSlot
from qfluentwidgets import MessageBox, SearchLineEdit, TableView

from src.unit.bangumi_unit import BangumiUnit
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
        self.setColumnsWidth()
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.verticalHeader().setVisible(False)
        self.customContextMenuRequested.connect(self.show_context_menu)

    def show_context_menu(self, position):
        menu = QMenu(self)
        copy_action = menu.addAction("复制bangumi id")
        copy_action.triggered.connect(self.copy_url)
        menu.exec_(self.mapToGlobal(position))

    def copy_url(self):
        index = self.currentIndex()
        if index.isValid():
            last_cell_index = index.sibling(index.row(), 3)
            text = last_cell_index.data().split("/")[-1]
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
            now_url = f'https://bgm.tv/subject/{row["subject_id"]}'
            standardItem1 = QStandardItem(now_name)
            standardItem1.setToolTip(now_name)
            standardItem2 = QStandardItem(now_name_cn)
            standardItem2.setToolTip(now_name_cn)
            standardItem3 = QStandardItem(now_date)
            standardItem3.setToolTip(now_date)
            standardItem4 = QStandardItem(now_url)
            standardItem4.setToolTip(now_url)
            self.model.appendRow([standardItem1, standardItem2, standardItem3, standardItem4])
            self.setColumnsWidth()

    def setColumnsWidth(self):
        self.setColumnWidth(0, 250)
        self.setColumnWidth(1, 200)
        self.setColumnWidth(2, 100)
        self.setColumnWidth(3, 250)


class SearchWidget(Widget):
    def __init__(self, dataPath: str, parent = None):
        super().__init__(parent = parent)
        self.dataPath = dataPath
        self.setObjectName("search-widget")
        self.lock = asyncio.Lock()

        self.vBoxLayout = QVBoxLayout(self)
        self.lineEdit = SearchLineEdit(self)
        self.dataTable = MyTable()
        spacerItem = QSpacerItem(20, 50, QSizePolicy.Minimum, QSizePolicy.Fixed)

        self.lineEdit.setClearButtonEnabled(True)
        self.lineEdit.setPlaceholderText('Search icon')
        self.lineEdit.setMaximumWidth(300)
        self.dataTable.setMaximumWidth(800)

        self.lineEdit.searchButton.clicked.connect(self.searchButtonDown)

        self.vBoxLayout.setSpacing(20)
        self.vBoxLayout.addItem(spacerItem)
        self.vBoxLayout.addWidget(self.lineEdit)
        self.vBoxLayout.addWidget(self.dataTable)

    @asyncSlot()
    async def searchButtonDown(self):
        search_keyword = self.lineEdit.text()
        if search_keyword == "":
            return
        self.lineEdit.searchButton.setEnabled(False)
        bangumiList = await BangumiUnit.searchAnimeByKeyword(self.dataPath, search_keyword)
        result = await BangumiUnit.getAnimeInfoByMultiBangumiId(self.dataPath, bangumiList)
        if isinstance(result, str):
            self.lineEdit.searchButton.setEnabled(True)
            errorBox = MessageBox('错误', '搜索失败，请检查是网络问题还是搜索词不对', self)
            errorBox.exec()
            return
        self.dataTable.update_data(result)
