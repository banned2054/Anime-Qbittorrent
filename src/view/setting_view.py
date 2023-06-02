from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QIntValidator
from PyQt5.QtWidgets import QHBoxLayout, QLabel, QSizePolicy, QSpacerItem, QVBoxLayout
from qfluentwidgets import LineEdit, MessageBox, PushButton

from src.unit.file_unit import FileUnit
from src.view.base_view import Widget


class SettingWidget(Widget):
    def __init__(self, dataPath: str, parent = None):
        super().__init__(parent = parent)
        self.dataPath = dataPath
        self.setObjectName("setting-widget")

        self.vBoxLayout = QVBoxLayout(self)

        self.labelHostTip = QLabel("qbittorrent地址", self)
        self.labelPortTip = QLabel("qbittorrent端口", self)
        self.labelUsernameTip = QLabel("qb-web 用户名", self)
        self.labelPasswordTip = QLabel("qb-web 密  码", self)
        self.labelDownloadPathTip = QLabel("下载目录", self)
        self.labelFileDictionaryTip = QLabel("下载动画文件夹", self)
        self.labelFileNameTip = QLabel("下载动画名", self)

        self.lineEditHostTip = LineEdit(self)
        self.lineEditPortTip = LineEdit(self)
        self.lineEditPortTip.setValidator(QIntValidator())
        self.lineEditUsernameTip = LineEdit(self)
        self.lineEditPasswordTip = LineEdit(self)
        self.lineEditDownloadPathTip = LineEdit(self)
        self.lineEditFileDictionaryTip = LineEdit(self)
        self.lineEditFileNameTip = LineEdit(self)

        self.buttonSaveData = PushButton("保存设置", self)
        self.buttonReturnDefault = PushButton("恢复默认设置", self)

        self.init_layout()
        self.initItemSize()
        self.initEvent()
        self.freshLineEdit()

    def init_layout(self):
        hBoxLayout1 = QHBoxLayout(self)
        hBoxLayout1.setSpacing(20)
        hBoxLayout1.addWidget(self.labelHostTip)
        hBoxLayout1.addWidget(self.lineEditHostTip)
        hBoxLayout1.addStretch()

        hBoxLayout2 = QHBoxLayout(self)
        hBoxLayout2.setSpacing(20)
        hBoxLayout2.addWidget(self.labelPortTip)
        hBoxLayout2.addWidget(self.lineEditPortTip)
        hBoxLayout2.addStretch()

        hBoxLayout3 = QHBoxLayout(self)
        hBoxLayout3.setSpacing(20)
        hBoxLayout3.addWidget(self.labelUsernameTip)
        hBoxLayout3.addWidget(self.lineEditUsernameTip)
        hBoxLayout3.addStretch()

        hBoxLayout4 = QHBoxLayout(self)
        hBoxLayout4.setSpacing(20)
        hBoxLayout4.addWidget(self.labelPasswordTip)
        hBoxLayout4.addWidget(self.lineEditPasswordTip)
        hBoxLayout4.addStretch()

        hBoxLayout5 = QHBoxLayout(self)
        hBoxLayout5.setSpacing(20)
        hBoxLayout5.addWidget(self.labelDownloadPathTip)
        hBoxLayout5.addWidget(self.lineEditDownloadPathTip)
        hBoxLayout5.addStretch()

        hBoxLayout6 = QHBoxLayout(self)
        hBoxLayout6.setSpacing(20)
        hBoxLayout6.addWidget(self.labelFileDictionaryTip)
        hBoxLayout6.addWidget(self.lineEditFileDictionaryTip)
        hBoxLayout6.addStretch()

        hBoxLayout7 = QHBoxLayout(self)
        hBoxLayout7.setSpacing(20)
        hBoxLayout7.addWidget(self.labelFileNameTip)
        hBoxLayout7.addWidget(self.lineEditFileNameTip)
        hBoxLayout7.addStretch()

        spacerItem = QSpacerItem(20, 50, QSizePolicy.Minimum, QSizePolicy.Fixed)
        self.vBoxLayout.setSpacing(20)
        self.vBoxLayout.addItem(spacerItem)
        self.vBoxLayout.addLayout(hBoxLayout1)
        self.vBoxLayout.addLayout(hBoxLayout2)
        self.vBoxLayout.addLayout(hBoxLayout3)
        self.vBoxLayout.addLayout(hBoxLayout4)
        self.vBoxLayout.addLayout(hBoxLayout5)
        self.vBoxLayout.addLayout(hBoxLayout6)
        self.vBoxLayout.addLayout(hBoxLayout7)
        self.vBoxLayout.addWidget(self.buttonSaveData)
        self.vBoxLayout.addWidget(self.buttonReturnDefault)
        self.vBoxLayout.addStretch()

    def initItemSize(self):
        self.labelHostTip.setMinimumWidth(200)
        self.labelHostTip.setMaximumWidth(200)
        self.labelPortTip.setMinimumWidth(200)
        self.labelPortTip.setMaximumWidth(200)
        self.labelUsernameTip.setMinimumWidth(200)
        self.labelUsernameTip.setMaximumWidth(200)
        self.labelPasswordTip.setMinimumWidth(200)
        self.labelPasswordTip.setMaximumWidth(200)
        self.labelDownloadPathTip.setMinimumWidth(200)
        self.labelDownloadPathTip.setMaximumWidth(200)
        self.labelFileDictionaryTip.setMinimumWidth(200)
        self.labelFileDictionaryTip.setMaximumWidth(200)
        self.labelFileNameTip.setMinimumWidth(200)
        self.labelFileNameTip.setMaximumWidth(200)

    def initEvent(self):
        timer1 = QTimer()
        timer1.timeout.connect(self.freshLineEdit)
        timer1.start(10000)
        self.buttonSaveData.clicked.connect(self.buttonSaveDown)
        self.buttonReturnDefault.clicked.connect(self.buttonReturnDefaultDown)

    def freshLineEdit(self):
        qbittorrentSetting = FileUnit.readQbittorrentSettingFile(self.dataPath)
        self.lineEditHostTip.setText(qbittorrentSetting['host'])
        self.lineEditPortTip.setText(str(qbittorrentSetting['port']))
        self.lineEditUsernameTip.setText(qbittorrentSetting['userName'])
        self.lineEditPasswordTip.setText(qbittorrentSetting['password'])
        self.lineEditDownloadPathTip.setText(qbittorrentSetting['downloadPath'])
        self.lineEditFileDictionaryTip.setText(qbittorrentSetting['animeDictionary'])
        self.lineEditFileNameTip.setText(qbittorrentSetting['animeFile'])

    def buttonSaveDown(self):
        if self.lineEditHostTip.text() == "" or self.lineEditPortTip.text() == "" \
                or self.lineEditUsernameTip.text() == "" or self.lineEditPasswordTip.text() == "" \
                or self.lineEditDownloadPathTip.text() == "" or self.lineEditFileDictionaryTip.text() == "" \
                or self.lineEditFileNameTip.text() == "":
            errorBox = MessageBox('错误', '保存失败，所有设置不得为空', self)
            errorBox.exec()
            return
        qbittorrentSetting = FileUnit.readQbittorrentSettingFile(self.dataPath)
        qbittorrentSetting['host'] = self.lineEditHostTip.text()
        qbittorrentSetting['port'] = int(self.lineEditPortTip.text())
        qbittorrentSetting['userName'] = self.lineEditUsernameTip.text()
        qbittorrentSetting['password'] = self.lineEditPasswordTip.text()
        qbittorrentSetting['downloadPath'] = self.lineEditDownloadPathTip.text()
        qbittorrentSetting['animeDictionary'] = self.lineEditFileDictionaryTip.text()
        qbittorrentSetting['animeFile'] = self.lineEditFileNameTip.text()
        FileUnit.freshQbittorrentSettingFile(self.dataPath, qbittorrentSetting)
        self.freshLineEdit()

    def buttonReturnDefaultDown(self):
        FileUnit.deleteFile(f'{self.dataPath}/qbittorrent.yaml')
        FileUnit.initQbittorrentSetting(self.dataPath)
        self.freshLineEdit()
