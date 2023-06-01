import yaml
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QHBoxLayout
from qfluentwidgets import ComboBox, Dialog, PushButton

from src.view.base_view import Widget
from src.view.input_sub_window import InputDialog


class TorrentSubWidget(Widget):
    def __init__(self, parent = None):
        super().__init__(parent = parent)
        self.data = None
        self.tagComboBox = ComboBox(self)
        self.tagComboBox.setFixedWidth(300)
        self.freshTagComboBox()
        timer = QTimer()
        timer.timeout.connect(self.freshTagComboBox)  # 连接定时器的 timeout 信号到 timer_func
        timer.start(1000)  # 启动定时器，设置间隔为 1000 毫秒（1秒）

        self.addTagButton = PushButton("添加tag", self)
        self.addTagButton.setMaximumWidth(200)
        self.addTagButton.clicked.connect(self.open_dialog)

        self.hBoxLayout = QHBoxLayout()
        self.hBoxLayout.addWidget(self.tagComboBox)
        self.hBoxLayout.addWidget(self.addTagButton)

        self.setLayout(self.hBoxLayout)

    def freshTagComboBox(self):
        self.tagComboBox.clear()
        with open('src/data/qbittorrent.yaml', 'r') as file:
            self.data = yaml.safe_load(file)
            tags = self.data['tags']
            for tag in tags:
                self.tagComboBox.addItem(str(tag))
        if len(self.data['tags']) > 0:
            self.tagComboBox.setCurrentIndex(0)

    def open_dialog(self):
        dialog = InputDialog("输入新tag", self)
        if dialog.exec_():
            if dialog.result != "":
                if dialog.result in self.data['tags']:
                    errorDialog = Dialog('error', 'tag已存在', self)
                    errorDialog.open()
                    return
                self.data['tags'].append(dialog.result)
                with open('src/data/qbittorrent.yaml', 'w') as file:
                    yaml.safe_dump(self.data, file)
                self.freshTagComboBox()

# app = QApplication([])
# w = TorrentSubWidget()
# w.show()
# app.exec_()
