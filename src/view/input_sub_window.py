from PyQt5.QtWidgets import QDialog, QLineEdit, QPushButton, QVBoxLayout


class InputDialog(QDialog):
    def __init__(self, parent = None):
        super().__init__(parent)
        self.setWindowTitle('Input Dialog')

        self.layout = QVBoxLayout(self)
        self.input = QLineEdit(self)
        self.button = QPushButton('Confirm', self)

        self.layout.addWidget(self.input)
        self.layout.addWidget(self.button)

        self.button.clicked.connect(self.accept)

    def accept(self):
        self.result = self.input.text()
        super().accept()
