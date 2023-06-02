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

        self.labelPreviewFileDictionary = QLabel("预览", self)
        self.labelPreviewFileName = QLabel("预览", self)

        self.lineEditHost = LineEdit(self)
        self.lineEditPort = LineEdit(self)
        self.lineEditPort.setValidator(QIntValidator())
        self.lineEditUsername = LineEdit(self)
        self.lineEditPassword = LineEdit(self)
        self.lineEditDownloadPath = LineEdit(self)
        self.lineEditFileDictionary = LineEdit(self)
        self.lineEditFileName = LineEdit(self)

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
        hBoxLayout1.addWidget(self.lineEditHost)
        hBoxLayout1.addStretch()

        hBoxLayout2 = QHBoxLayout(self)
        hBoxLayout2.setSpacing(20)
        hBoxLayout2.addWidget(self.labelPortTip)
        hBoxLayout2.addWidget(self.lineEditPort)
        hBoxLayout2.addStretch()

        hBoxLayout3 = QHBoxLayout(self)
        hBoxLayout3.setSpacing(20)
        hBoxLayout3.addWidget(self.labelUsernameTip)
        hBoxLayout3.addWidget(self.lineEditUsername)
        hBoxLayout3.addStretch()

        hBoxLayout4 = QHBoxLayout(self)
        hBoxLayout4.setSpacing(20)
        hBoxLayout4.addWidget(self.labelPasswordTip)
        hBoxLayout4.addWidget(self.lineEditPassword)
        hBoxLayout4.addStretch()

        hBoxLayout5 = QHBoxLayout(self)
        hBoxLayout5.setSpacing(20)
        hBoxLayout5.addWidget(self.labelDownloadPathTip)
        hBoxLayout5.addWidget(self.lineEditDownloadPath)
        hBoxLayout5.addStretch()

        hBoxLayout6 = QHBoxLayout(self)
        hBoxLayout6.setSpacing(20)
        hBoxLayout6.addWidget(self.labelFileDictionaryTip)
        hBoxLayout6.addWidget(self.lineEditFileDictionary)
        hBoxLayout6.addWidget(self.labelPreviewFileDictionary)
        hBoxLayout6.addStretch()

        hBoxLayout7 = QHBoxLayout(self)
        hBoxLayout7.setSpacing(20)
        hBoxLayout7.addWidget(self.labelFileNameTip)
        hBoxLayout7.addWidget(self.lineEditFileName)
        hBoxLayout7.addWidget(self.labelPreviewFileName)
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

        self.lineEditFileDictionary.setMaximumWidth(308)
        self.lineEditFileDictionary.setMinimumWidth(308)
        self.lineEditFileName.setMaximumWidth(308)
        self.lineEditFileName.setMinimumWidth(308)

    def initEvent(self):
        self.buttonSaveData.clicked.connect(self.buttonSaveDown)
        self.buttonReturnDefault.clicked.connect(self.buttonReturnDefaultDown)

        self.lineEditFileDictionary.textChanged.connect(self.lineEditFileDictionaryChanged)
        self.lineEditFileName.textChanged.connect(self.lineEditFileNameChanged)

    def freshLineEdit(self):
        qbittorrentSetting = FileUnit.readQbittorrentSettingFile(self.dataPath)
        self.lineEditHost.setText(qbittorrentSetting['host'])
        self.lineEditPort.setText(str(qbittorrentSetting['port']))
        self.lineEditUsername.setText(qbittorrentSetting['userName'])
        self.lineEditPassword.setText(qbittorrentSetting['password'])
        self.lineEditDownloadPath.setText(qbittorrentSetting['downloadPath'])
        self.lineEditFileDictionary.setText(qbittorrentSetting['animeDictionary'])
        self.lineEditFileName.setText(qbittorrentSetting['animeFile'])

    def buttonSaveDown(self):
        if self.lineEditHost.text() == "" or self.lineEditPort.text() == "" \
                or self.lineEditUsername.text() == "" or self.lineEditPassword.text() == "" \
                or self.lineEditDownloadPath.text() == "" or self.lineEditFileDictionary.text() == "" \
                or self.lineEditFileName.text() == "":
            errorBox = MessageBox('错误', '保存失败，所有设置不得为空', self)
            errorBox.exec()
            return
        qbittorrentSetting = FileUnit.readQbittorrentSettingFile(self.dataPath)
        qbittorrentSetting['host'] = self.lineEditHost.text()
        qbittorrentSetting['port'] = int(self.lineEditPort.text())
        qbittorrentSetting['userName'] = self.lineEditUsername.text()
        qbittorrentSetting['password'] = self.lineEditPassword.text()
        qbittorrentSetting['downloadPath'] = self.lineEditDownloadPath.text()
        qbittorrentSetting['animeDictionary'] = self.lineEditFileDictionary.text()
        qbittorrentSetting['animeFile'] = self.lineEditFileName.text()
        FileUnit.freshQbittorrentSettingFile(self.dataPath, qbittorrentSetting)
        self.freshLineEdit()

    def buttonReturnDefaultDown(self):
        FileUnit.deleteFile(f'{self.dataPath}/qbittorrent.yaml')
        FileUnit.initQbittorrentSetting(self.dataPath)
        self.freshLineEdit()

    def lineEditFileDictionaryChanged(self):
        name = 'けいおん！'
        name_cn = '轻音少女'
        year = '2009'
        month = '04'
        day = '02'
        episode = '01'
        previewText = self.lineEditFileDictionary.text().replace('[name]', name)
        previewText = previewText.replace('[name_cn]', name_cn)
        previewText = previewText.replace('[year]', year)
        previewText = previewText.replace('[month]', month)
        previewText = previewText.replace('[day]', day)
        previewText = previewText.replace('[episode]', episode)

        self.labelPreviewFileDictionary.setText(f"示例：{previewText}")

    def lineEditFileNameChanged(self):
        name = 'けいおん！'
        name_cn = '轻音少女'
        year = '2009'
        month = '04'
        day = '02'
        episode = '01'
        previewText = self.lineEditFileName.text().replace('[name]', name)
        previewText = previewText.replace('[name_cn]', name_cn)
        previewText = previewText.replace('[year]', year)
        previewText = previewText.replace('[month]', month)
        previewText = previewText.replace('[day]', day)
        previewText = previewText.replace('[episode]', episode)

        self.labelPreviewFileName.setText(f"示例：{previewText}.mp4")
