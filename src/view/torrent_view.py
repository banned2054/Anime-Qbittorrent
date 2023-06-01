from datetime import datetime

from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QFileDialog, QHBoxLayout, QLabel, QSizePolicy, QSpacerItem, QVBoxLayout
from qasync import asyncSlot
from qfluentwidgets import ComboBox, Dialog, PushButton

from src.unit.bangumi_unit import BangumiUnit
from src.unit.file_unit import FileUnit
from src.unit.sql_unit import SqlUnit
from src.view.base_view import Widget
from src.view.input_sub_window import InputDialog, InputIntValidatorDialog


class TorrentWidget(Widget):
    def __init__(self, dataPath: str, parent = None):
        super().__init__(parent = parent)
        self.setObjectName("torrent-widget")
        self.dataPath = dataPath

        self.vBoxLayout = QVBoxLayout(self)

        self.labelFilePath = QLabel("请选择文件", self)
        self.buttonChooseTorrentFile = PushButton("选择文件", self)

        self.comboBoxAnimeName = ComboBox(self)
        self.buttonAddAnime = PushButton("添加动画", self)

        self.comboBoxTags = ComboBox(self)
        self.buttonAddTags = PushButton("添加tag", self)

        self.qbittorrentSettingData = None

        self.initLayout()
        self.initItemSize()
        self.initEvent()

        self.freshAnimeComboBox()
        self.freshTagComboBox()

    def initLayout(self):
        hBoxLayout_1 = QHBoxLayout(self)
        hBoxLayout_1.setSpacing(20)
        hBoxLayout_1.addWidget(self.labelFilePath)
        hBoxLayout_1.addWidget(self.buttonChooseTorrentFile)
        hBoxLayout_1.addStretch()

        hBoxLayout_2 = QHBoxLayout(self)
        hBoxLayout_2.setSpacing(20)
        hBoxLayout_2.addWidget(self.comboBoxAnimeName)
        hBoxLayout_2.addWidget(self.buttonAddAnime)
        hBoxLayout_2.addStretch()

        hBoxLayout_3 = QHBoxLayout(self)
        hBoxLayout_3.setSpacing(20)
        hBoxLayout_3.addWidget(self.comboBoxTags)
        hBoxLayout_3.addWidget(self.buttonAddTags)
        hBoxLayout_3.addStretch()

        spacerItem = QSpacerItem(20, 50, QSizePolicy.Minimum, QSizePolicy.Fixed)
        self.vBoxLayout.setSpacing(20)
        self.vBoxLayout.addItem(spacerItem)
        self.vBoxLayout.addLayout(hBoxLayout_1)
        self.vBoxLayout.addLayout(hBoxLayout_2)
        self.vBoxLayout.addLayout(hBoxLayout_3)
        self.vBoxLayout.addStretch()

    def initItemSize(self):
        self.buttonChooseTorrentFile.setMaximumWidth(200)
        self.buttonAddAnime.setMaximumWidth(200)
        self.buttonAddTags.setMaximumWidth(200)

        self.labelFilePath.setMaximumWidth(400)
        self.labelFilePath.setMinimumWidth(400)

        self.comboBoxAnimeName.setMaximumWidth(400)
        self.comboBoxTags.setMaximumWidth(400)

    def initEvent(self):
        timer1 = QTimer()
        timer1.timeout.connect(self.freshAnimeComboBox)
        timer1.start(1000)

        timer2 = QTimer()
        timer2.timeout.connect(self.freshTagComboBox)
        timer2.start(1000)

        self.buttonAddAnime.clicked.connect(self.buttonAddAnimeDown)
        self.buttonAddTags.clicked.connect(self.buttonAddTagDown)
        self.buttonChooseTorrentFile.clicked.connect(self.buttonChooseTorrentFileDown)

    def freshAnimeComboBox(self):
        animeDatas = SqlUnit.getAllData(self.dataPath)
        self.comboBoxAnimeName.clear()
        for animeData in animeDatas:
            self.comboBoxAnimeName.addItem(str(animeData[0]))
        if len(animeDatas) > 0:
            self.comboBoxAnimeName.setCurrentIndex(0)

    def freshTagComboBox(self):
        self.comboBoxTags.clear()
        self.qbittorrentSettingData = FileUnit.readQbittorrentSettingFile(self.dataPath)
        tags = self.qbittorrentSettingData['tags']
        for tag in tags:
            self.comboBoxTags.addItem(str(tag))

        if len(self.qbittorrentSettingData['tags']) > 0:
            self.comboBoxTags.setCurrentIndex(0)

    def buttonAddTagDown(self):
        dialog = InputDialog("输入新tag", self)
        if dialog.exec_():
            newTag = dialog.result
            if newTag != "":
                if newTag in self.qbittorrentSettingData['tags']:
                    errorDialog = Dialog("error", 'tag已存在', self)
                    errorDialog.open()
                    return
                self.qbittorrentSettingData['tags'].append(newTag)
                FileUnit.freshQbittorrentSettingFile(self.qbittorrentSettingData, self.dataPath)

    @asyncSlot()
    async def buttonAddAnimeDown(self):
        dialog = InputIntValidatorDialog("输入新动画的bangumi id", self)
        if dialog.exec_():
            newAnimeBangumiId = dialog.result
            if newAnimeBangumiId == "":
                return
            animeByBangumiId = SqlUnit.getDataByBangumiId(self.dataPath, newAnimeBangumiId)
            if len(animeByBangumiId) > 0:
                return
            newAnimeInfo = await BangumiUnit.getAnimeInfoByBangumiId(self.dataPath, newAnimeBangumiId)
            if isinstance(newAnimeInfo, str):
                # todo
                return
            animeDate = datetime.strptime(newAnimeInfo['date'], '%Y-%m-%d')
            SqlUnit.insertSqlNewLine(
                    self.dataPath,
                    newAnimeBangumiId,
                    newAnimeInfo['name'],
                    newAnimeInfo['name_cn'],
                    int(animeDate.year),
                    int(animeDate.month),
                    int(animeDate.day)
            )
            self.freshAnimeComboBox()

    def buttonChooseTorrentFileDown(self):
        file_path = QFileDialog.getOpenFileName(None, "Open .torrent File", ".", "Torrent Files (*.torrent)")[0]
        if file_path:
            self.labelFilePath.setText(file_path)
            self.labelFilePath.setToolTip(file_path)
