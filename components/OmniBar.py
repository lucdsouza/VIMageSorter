from PySide6.QtWidgets import QWidget, QHBoxLayout, QLabel, QLineEdit


class OmniBar(QWidget):
    def __init__(self, parent, mcolor):
        super().__init__(parent)

        self.mcolor = mcolor

        self.layout = QHBoxLayout(self)
        self.layout.setContentsMargins(2, 2, 2, 2)

        # Label to display messages.
        self._msg_label = QLabel("")
        self._msg_label.setVisible(True)
        self._msg_label.setStyleSheet(f"color: {self.mcolor};")
        self.layout.addWidget(self._msg_label)

        # Input to enter commands.
        self._input = QLineEdit()
        self._input.setVisible(False)
        self._input.setStyleSheet("""
            QLineEdit {
                border: none;
                outline: none;
            }
            QLineEdit:focus {
                border: none;
                outline: none;
            }
        """)
        self.layout.addWidget(self._input)
        self._input.returnPressed.connect(self._process_cmd)
        self._input.editingFinished.connect(self.hide_input)

    def show_input(self):
        self._msg_label.setVisible(False)
        self._input.setVisible(True)
        self._msg_label.setText("")
        self._input.setText(":")
        self._input.setFocus()

        self._input.setCursorPosition(1)

    def hide_input(self):
        self._input.setVisible(False)
        self._msg_label.setVisible(True)
        self._input.setText("")
        self._input.clearFocus()

    def notify(self, text, notification_type="info"):
        color = {
                "info": self.mcolor,
                "error": "lightcoral",
                "success": "lightgreen",
        }.get(notification_type, self.mcolor)

        self._msg_label.setText(text)
        self._msg_label.setStyleSheet(f"color: {color};")

    def _process_cmd(self):
        cmd = self._input.text()
        if cmd.startswith(":"):
            cmd = cmd.lstrip(":").strip()

            self.notify(f"Executed: {cmd}", "success")

        else:
            self.notify("No command entered", "error")

        self.hide_input()

