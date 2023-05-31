from src.view.base_view import Widget


class SettingWidget(Widget):
    def __init__(self, parent = None):
        super().__init__(parent = parent)
        self.setObjectName("setting-widget")
