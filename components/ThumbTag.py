from PySide6.QtWidgets import QLabel


class ThumbTag(QLabel):
    def __init__(self, text, parent=None, color="#3498DB"):
        super().__init__(text, parent)
        
        self.bg_color = color
        self.setStyleSheet(f"""
            QLabel {{
                background-color: {self.bg_color};
                color: white;
                padding: 2px 6px;
                border-radius: 10px;
                font-size: 10pt;
            }}
        """)

