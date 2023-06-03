import os
from datetime import datetime

from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QFileDialog, QHBoxLayout, QLabel, QSizePolicy, QSpacerItem, QVBoxLayout
from qasync import asyncSlot
from qfluentwidgets import CheckBox, ComboBox, Dialog, MessageBox, PushButton

from src.unit.bangumi_unit import BangumiUnit
from src.unit.file_unit import FileUnit
from src.unit.qbittorrent_unit import QbittorrentUnit
from src.unit.sql_unit import SqlUnit
from src.view.base_view import Widget
from src.view.input_view import InputDialog, InputIntValidatorDialog


class TorrentWidget(Widget):
    def __init__(self, dataPath: str, parent = None):
        super().__init__(parent = parent)
        self.setObjectName("torrent-widget")
        self.finalPath = "最终下载路径"
        self.dataPath = dataPath
        self.extension = ""
        self.currentBangumiId = 0

        self.vBoxLayout = QVBoxLayout(self)

        self.labelFilePath = QLabel("请选择文件", self)
        self.buttonChooseTorrentFile = PushButton("选择文件", self)

        self.comboBoxAnimeName = ComboBox(self)
        self.buttonAddAnime = PushButton("添加动画", self)

        self.comboBoxTags = ComboBox(self)
        self.buttonAddTags = PushButton("添加tag", self)

        self.labelEpisodeTip1 = QLabel("第", self)
        self.comboBoxEpisodes = ComboBox(self)
        self.labelEpisodeTip2 = QLabel("集", self)

        self.checkBox = CheckBox("删除torrent文件", self)

        self.labelPreviewTargetPath = QLabel("最终下载路径", self)

        self.buttonStartTorrentDownload = PushButton("开始下载", self)

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
        hBoxLayout_2.setSpacing(120)
        hBoxLayout_2.addWidget(self.comboBoxAnimeName)
        hBoxLayout_2.addWidget(self.buttonAddAnime)
        hBoxLayout_2.addStretch()

        hBoxLayout_3 = QHBoxLayout(self)
        hBoxLayout_3.setSpacing(120)
        hBoxLayout_3.addWidget(self.comboBoxTags)
        hBoxLayout_3.addWidget(self.buttonAddTags)
        hBoxLayout_3.addStretch()

        hBoxLayout_4 = QHBoxLayout(self)
        hBoxLayout_4.setSpacing(20)
        hBoxLayout_4.addWidget(self.labelEpisodeTip1)
        hBoxLayout_4.addWidget(self.comboBoxEpisodes)
        hBoxLayout_4.addWidget(self.labelEpisodeTip2)
        hBoxLayout_4.addStretch()

        spacerItem = QSpacerItem(20, 50, QSizePolicy.Minimum, QSizePolicy.Fixed)
        self.vBoxLayout.setSpacing(20)
        self.vBoxLayout.addItem(spacerItem)
        self.vBoxLayout.addLayout(hBoxLayout_1)
        self.vBoxLayout.addLayout(hBoxLayout_2)
        self.vBoxLayout.addLayout(hBoxLayout_3)
        self.vBoxLayout.addLayout(hBoxLayout_4)
        self.vBoxLayout.addWidget(self.checkBox)
        self.vBoxLayout.addWidget(self.labelPreviewTargetPath)
        self.vBoxLayout.addWidget(self.buttonStartTorrentDownload)
        self.vBoxLayout.addStretch()

    def initItemSize(self):
        self.buttonChooseTorrentFile.setMaximumWidth(150)
        self.buttonChooseTorrentFile.setMinimumWidth(150)
        self.buttonAddAnime.setMaximumWidth(150)
        self.buttonAddAnime.setMinimumWidth(150)
        self.buttonAddTags.setMaximumWidth(150)
        self.buttonAddTags.setMinimumWidth(150)
        self.buttonStartTorrentDownload.setMaximumWidth(150)
        self.buttonStartTorrentDownload.setMinimumWidth(150)

        self.labelFilePath.setMaximumWidth(500)
        self.labelFilePath.setMinimumWidth(500)
        self.labelPreviewTargetPath.setMaximumWidth(600)
        self.labelPreviewTargetPath.setMinimumWidth(600)

        self.comboBoxAnimeName.setMaximumWidth(400)
        self.comboBoxAnimeName.setMinimumWidth(400)
        self.comboBoxTags.setMaximumWidth(400)
        self.comboBoxTags.setMinimumWidth(400)

    def initEvent(self):
        timer1 = QTimer()
        timer1.timeout.connect(self.freshAnimeComboBox)
        timer1.start(10000)

        timer2 = QTimer()
        timer2.timeout.connect(self.freshTagComboBox)
        timer2.start(10000)

        self.buttonAddAnime.clicked.connect(self.buttonAddAnimeDown)
        self.buttonAddTags.clicked.connect(self.buttonAddTagDown)
        self.buttonChooseTorrentFile.clicked.connect(self.buttonChooseTorrentFileDown)
        self.buttonStartTorrentDownload.clicked.connect(self.buttonStartTorrentDownloadDown)

        self.comboBoxAnimeName.currentIndexChanged.connect(self.comboBoxAnimeTextChanged)
        self.comboBoxEpisodes.currentIndexChanged.connect(self.comboBoxChanged)

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
        self.buttonAddTags.setEnabled(False)
        dialog = InputDialog("输入新tag", self)
        if dialog.exec_():
            newTag = dialog.result
            if newTag != "":
                if newTag in self.qbittorrentSettingData['tags']:
                    errorDialog = Dialog("error", 'tag已存在', self)
                    errorDialog.open()
                    self.buttonAddTags.setEnabled(True)
                    return
                self.qbittorrentSettingData['tags'].append(newTag)
                FileUnit.freshMikanSettingFile(self.dataPath, self.qbittorrentSettingData)
                self.buttonAddTags.setEnabled(True)

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
            self.buttonAddAnime.setEnabled(False)
            newAnimeInfo = await BangumiUnit.getAnimeInfoByBangumiId(self.dataPath, newAnimeBangumiId)
            if isinstance(newAnimeInfo, str):
                self.buttonAddAnime.setEnabled(True)
                errorBox = MessageBox('错误', '搜索失败，请检查是网络问题还是搜索词不对', self)
                errorBox.exec()
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
            self.buttonAddAnime.setEnabled(True)
            self.freshAnimeComboBox()

    def buttonChooseTorrentFileDown(self):
        filePath = QFileDialog.getOpenFileName(None, "Open .torrent File", ".", "Torrent Files (*.torrent)")[0]
        if filePath:
            self.labelFilePath.setText(filePath)
            self.labelFilePath.setToolTip(filePath)
            fileName = FileUnit.getTorrentOneFileName(filePath)
            self.extension = os.path.splitext(fileName)[1]
            self.comboBoxChanged()

    @asyncSlot()
    async def comboBoxAnimeTextChanged(self):
        nowAnimeName = self.comboBoxAnimeName.currentText()
        animeInfo = SqlUnit.getDataByAnimeName(self.dataPath, nowAnimeName)[0]
        self.currentBangumiId = animeInfo[5]
        await self.freshEpisodeComboBox()
        self.comboBoxChanged()

    def comboBoxChanged(self):
        qbittorrentSetting = FileUnit.readQbittorrentSettingFile(self.dataPath)
        finalPath = f"{qbittorrentSetting['animeDictionary']}/{qbittorrentSetting['animeFile']}"
        nowAnimeName = self.comboBoxAnimeName.currentText()
        animeInfo = SqlUnit.getDataByAnimeName(self.dataPath, nowAnimeName)[0]
        finalPath = finalPath.replace('[name]', f"{animeInfo[0]}")
        finalPath = finalPath.replace('[name_cn]', f"{animeInfo[1]}")
        finalPath = finalPath.replace('[year]', f"{animeInfo[2]}")
        finalPath = finalPath.replace('[month]', f"{animeInfo[3]:02d}")
        finalPath = finalPath.replace('[day]', f"{animeInfo[4]}:02d")

        episode = self.comboBoxEpisodes.currentText()
        if episode.isdigit():
            episode = int(episode)
            self.finalPath = finalPath.replace('[episode]', f"{episode:02d}")
        else:
            self.finalPath = finalPath.replace('[episode]', "01")

        if self.extension != "":
            self.finalPath = f"{self.finalPath}{self.extension}"
        self.labelPreviewTargetPath.setText(self.finalPath)
        self.labelPreviewTargetPath.setToolTip(self.finalPath)

    async def freshEpisodeComboBox(self):
        if self.currentBangumiId == 0:
            return
        self.comboBoxEpisodes.clear()
        episodes = await BangumiUnit.getAnimeEpisodeInfoByBangumiId(self.dataPath, self.currentBangumiId)
        for episode in episodes:
            self.comboBoxEpisodes.addItem(str(episode))
        if len(episodes) > 0:
            self.comboBoxEpisodes.setCurrentIndex(0)

    @asyncSlot()
    async def buttonStartTorrentDownloadDown(self):
        self.buttonStartTorrentDownload.setEnabled(False)
        await QbittorrentUnit.downloadOneFile(self.dataPath,
                                              self.labelFilePath.text(),
                                              self.finalPath,
                                              self.comboBoxTags.currentText())
        if self.checkBox.isChecked():
            FileUnit.deleteFile(self.labelFilePath.text())
            self.checkBox.setChecked(False)
        self.buttonStartTorrentDownload.setEnabled(True)
