# coding:utf-8
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QHBoxLayout, QLabel, QVBoxLayout
from qfluentwidgets import PushButton, TableWidget

from src.view.base_view import Widget


class TorrentWidget(Widget):
    def __init__(self, parent = None):
        super().__init__(parent = parent)
        self.setObjectName("torrent-widget")

        self.v_layout = QVBoxLayout(self)
        self.h_layout = QHBoxLayout()

        self.selectFileButton = PushButton("选择torrent文件")
        self.filePathLabel = QLabel("请选择文件")

        self.h_layout.addWidget(self.filePathLabel)
        self.h_layout.addWidget(self.selectFileButton)

        self.tableView = TableWidget(self)
        self.v_layout.addWidget(QLabel(), Qt.AlignCenter)
        self.v_layout.addLayout(self.h_layout, Qt.AlignCenter)
        self.v_layout.addWidget(self.tableView, Qt.AlignCenter)

        self.setLayout(self.v_layout)
