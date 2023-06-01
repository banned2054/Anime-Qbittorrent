from PyQt5.QtGui import QIntValidator
from PyQt5.QtWidgets import QDialog, QVBoxLayout
from qfluentwidgets import LineEdit, PushButton


class InputDialog(QDialog):
    def __init__(self, title: str, parent = None):
        super().__init__(parent)
        self.setWindowTitle(title)

        self.layout = QVBoxLayout(self)
        self.input = LineEdit(self)
        self.button = PushButton('确定', self)

        self.layout.addWidget(self.input)
        self.layout.addWidget(self.button)

        self.button.clicked.connect(self.accept)
        self.result = ""

    def accept(self):
        self.result = self.input.text()
        super().accept()


class InputIntValidatorDialog(InputDialog):
    def __init__(self, title: str, parent = None):
        super().__init__(title, parent)
        self.input.setValidator(QIntValidator())
