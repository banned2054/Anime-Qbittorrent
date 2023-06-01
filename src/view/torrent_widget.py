# coding:utf-8
import sqlite3

from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QHBoxLayout, QLabel, QSizePolicy, QSpacerItem, QVBoxLayout
from qfluentwidgets import ComboBox, PushButton

from src.view.base_view import Widget


class TorrentWidget(Widget):
    def __init__(self, parent = None):
        super().__init__(parent = parent)
        self.setObjectName("torrent-widget")

        self.vBoxLayout = QVBoxLayout(self)
        self.vBoxLayout.setSpacing(20)

        self.hBoxLayout = QHBoxLayout()
        self.selectFileButton = PushButton("选择torrent文件")
        self.filePathLabel = QLabel("请选择文件")

        self.hBoxLayout.addWidget(self.filePathLabel)
        self.hBoxLayout.addWidget(self.selectFileButton)

        self.animeNameComboBox = ComboBox(self)

        spacerItem = QSpacerItem(20, 50, QSizePolicy.Minimum, QSizePolicy.Fixed)
        self.vBoxLayout.addItem(spacerItem)
        self.vBoxLayout.addLayout(self.hBoxLayout)
        self.vBoxLayout.addWidget(self.animeNameComboBox)
        self.vBoxLayout.addStretch()

        self.initUiSize()

        self.setLayout(self.vBoxLayout)
        self.sqlGetData()

    def initUiSize(self):
        self.selectFileButton.setMaximumWidth(200)
        self.filePathLabel.setMaximumWidth(400)
        self.animeNameComboBox.setFixedWidth(300)
        self.freshComboBox()
        timer = QTimer()
        timer.timeout.connect(self.freshComboBox)  # 连接定时器的 timeout 信号到 timer_func
        timer.start(1000)  # 启动定时器，设置间隔为 1000 毫秒（1秒）

    def freshComboBox(self):
        sqlData = self.sqlGetData()
        self.animeNameComboBox.clear()
        for data in sqlData:
            print(data)
            self.animeNameComboBox.addItem(str(data[0]))
        self.animeNameComboBox.addItem("添加新动画")
        if len(sqlData) > 0:
            self.animeNameComboBox.setCurrentIndex(0)

    @staticmethod
    def sqlGetData():
        connection = sqlite3.connect('src/data/anime.db')
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM anime')
        rows = cursor.fetchall()
        connection.close()
        return rows
