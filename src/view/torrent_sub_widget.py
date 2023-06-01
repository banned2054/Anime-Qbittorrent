import yaml
from PyQt5.QtCore import QTimer
from qfluentwidgets import ComboBox

from src.view.base_view import Widget
from src.view.input_sub_window import InputDialog


class TorrentSubWidget(Widget):
    def __init__(self, parent = None):
        super().__init__(parent = parent)
        self.data = None
        self.tagComboBox = ComboBox()
        timer = QTimer()
        timer.timeout.connect(self.freshTagComboBox)  # 连接定时器的 timeout 信号到 timer_func
        timer.start(1000)  # 启动定时器，设置间隔为 1000 毫秒（1秒）

    def freshTagComboBox(self):
        self.tagComboBox.clear()
        with open('src/data/qbittorrent.yaml', 'r') as file:
            self.data = yaml.safe_load(file)
            tags = self.data['tags']
            for tag in tags:
                self.tagComboBox.addItem(str(tag))
            self.tagComboBox.addItem('添加新的tag')

    def open_dialog(self):
        dialog = InputDialog(self)
        if dialog.exec_():
            if dialog.result != "":
                self.data['tags'].append(dialog.result)
                with open('src/data/qbittorrent.yaml', 'w') as file:
                    yaml.safe_dump(self.data, file)
                self.freshTagComboBox()
