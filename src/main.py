import sys

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QFrame, QHBoxLayout, QLabel, QVBoxLayout
from qfluentwidgets import PushButton, SearchLineEdit, TableWidget


class Widget(QFrame):

    def __init__(self, parent = None):
        super().__init__(parent = parent)


class TorrentWidget(Widget):
    def __init__(self, parent = None):
        super().__init__(parent = parent)

        self.v_layout = QVBoxLayout(self)
        self.h_layout = QHBoxLayout()

        self.selectFileButton = PushButton("选择torrent文件")
        self.filePathLabel = QLabel("请选择文件")

        self.h_layout.addWidget(self.filePathLabel)
        self.h_layout.addWidget(self.selectFileButton)

        self.tableView = TableWidget(self)
        self.v_layout.addLayout(self.h_layout)
        self.v_layout.addWidget(self.tableView)

        self.setLayout(self.v_layout)


class SearchWidget(Widget):
    def __init__(self, parent = None):
        super().__init__(parent = parent)
        self.hBoxLayout = QHBoxLayout(self)
        self.lineEdit = SearchLineEdit(self)
        self.button = PushButton('Search', self)

        self.hBoxLayout.setAlignment(Qt.AlignCenter)
        self.hBoxLayout.addWidget(self.lineEdit, 0, Qt.AlignCenter)
        self.hBoxLayout.addWidget(self.button, 0, Qt.AlignCenter)

        self.lineEdit.setClearButtonEnabled(True)
        self.lineEdit.setPlaceholderText('Search icon')


app = QApplication(sys.argv)
ex = SearchWidget()
ex.show()
sys.exit(app.exec_())
