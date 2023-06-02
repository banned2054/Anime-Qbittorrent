import asyncio

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QHBoxLayout, QStackedWidget
from qasync import QEventLoop
from qfluentwidgets import FluentIcon, NavigationInterface, NavigationItemPosition, Theme, isDarkTheme, \
    qrouter, setTheme
from qframelesswindow import FramelessWindow

from src.unit.file_unit import FileUnit
from src.view.base_view import CustomTitleBar
from src.view.search_view import SearchWidget
from src.view.setting_view import SettingWidget
from src.view.torrent_view import TorrentWidget


class Window(FramelessWindow):

    def __init__(self):
        super().__init__()

        self.setTitleBar(CustomTitleBar(self))

        # use dark theme mode
        setTheme(Theme.DARK)

        self.hBoxLayout = QHBoxLayout(self)
        self.navigationInterface = NavigationInterface(self, showMenuButton = True, showReturnButton = True)
        self.stackWidget = QStackedWidget(self)

        self.searchInterface = SearchWidget("src/data", self)
        self.torrentInterface = TorrentWidget("src/data", self)
        self.settingInterface = SettingWidget("src/data", self)

        # initialize layout
        self.init_layout()

        # add items to navigation interface
        self.init_navigation()

        self.initWindow()

    def init_layout(self):
        self.hBoxLayout.setSpacing(0)
        self.hBoxLayout.setContentsMargins(0, 0, 0, 0)
        self.hBoxLayout.addWidget(self.navigationInterface)
        self.hBoxLayout.addWidget(self.stackWidget)
        self.hBoxLayout.setStretchFactor(self.stackWidget, 1)

        self.titleBar.raise_()
        self.navigationInterface.displayModeChanged.connect(self.titleBar.raise_)

    def init_navigation(self):
        self.add_sub_interface(self.searchInterface, FluentIcon.SEARCH, 'Search')
        self.add_sub_interface(self.torrentInterface, FluentIcon.FOLDER, 'Torrent')

        self.navigationInterface.addSeparator()
        self.add_sub_interface(self.settingInterface, FluentIcon.SETTING, 'Settings', NavigationItemPosition.BOTTOM)

        qrouter.setDefaultRouteKey(self.stackWidget, self.searchInterface.objectName())

        self.stackWidget.currentChanged.connect(self.on_current_interface_changed)

    def initWindow(self):
        self.resize(900, 700)
        self.setWindowIcon(QIcon('resource/logo.png'))
        self.titleBar.setAttribute(Qt.WA_StyledBackground)

        desktop = QApplication.desktop().availableGeometry()
        w, h = desktop.width(), desktop.height()
        self.move(w // 2 - self.width() // 2, h // 2 - self.height() // 2)

        self.set_qss()

    def set_qss(self):
        color = 'dark' if isDarkTheme() else 'light'
        with open(f'resource/{color}/demo.qss', encoding = 'utf-8') as f:
            self.setStyleSheet(f.read())

    def add_sub_interface(self, interface, icon, text: str, position = NavigationItemPosition.TOP):
        """ add sub interface """
        self.stackWidget.addWidget(interface)
        self.navigationInterface.addItem(
                routeKey = interface.objectName(),
                icon = icon,
                text = text,
                onClick = lambda: self.switch_to(interface),
                position = position,
                tooltip = text
        )

    def switch_to(self, widget):
        self.stackWidget.setCurrentWidget(widget)

    def on_current_interface_changed(self, index):
        widget = self.stackWidget.widget(index)
        self.navigationInterface.setCurrentItem(widget.objectName())
        qrouter.push(self.stackWidget, widget.objectName())


if __name__ == '__main__':
    QApplication.setHighDpiScaleFactorRoundingPolicy(Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)

    FileUnit.initQbittorrentSetting('src/data')

    app = QApplication([])
    loop = QEventLoop(app)
    asyncio.set_event_loop(loop)
    w = Window()
    w.show()
    with loop:
        loop.run_forever()
