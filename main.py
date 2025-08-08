import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QLabel, QStackedWidget
from PySide6.QtGui import QFont, QPixmap
from PySide6.QtCore import Qt

from components import TopBar, OmniBar, ThumbTag, Thumbnail


font = QFont("Consolas", 12)
mcolor = "#ADD8E6"
bg_color = "#000000"


app = QApplication(sys.argv)
app.setStyleSheet(f"""
    QWidget {{
        background-color: {bg_color};
        color: {mcolor};
    }}
""")
app.setFont(font)


class MainWindow(QMainWindow):
    def __init__(self, mcolor):
        super().__init__()
        
        self.mcolor = mcolor

        self.setWindowTitle("VIMageSorter")

        central = QWidget()
        self.setCentralWidget(central)
        self._central = QVBoxLayout(central)
        self._central.setSpacing(2)
        self._central.setContentsMargins(2, 2, 2, 2)

        # Top bar to display progress and info.
        self._topbar = TopBar(self)
        self._central.addWidget(self._topbar)

        self._topbar.set_folder("/inbox/downloads", 37430000, 102, 1)
        
        # Content.
        self._main_stacked = QStackedWidget()

        pixmap = QPixmap("/home/auggie/library/downloads/wallpaper.jpg")
        thumb_folder = ThumbTag("Trash", color="lightcoral")
        gallery = Thumbnail(pixmap, "wallpaper.jpg", "AA", [thumb_folder])
        people = QLabel("People Gallery Screen")
        screens = [gallery, people]

        for screen in screens:
            # screen.setAlignment(Qt.AlignCenter)
            self._main_stacked.addWidget(screen)

        self._central.addWidget(self._main_stacked, 1)

        # OmniBar
        self._omnibar = OmniBar(self, self.mcolor)
        self._omnibar.notify("Press ':' to enter commands.", "info")
        self._central.addWidget(self._omnibar)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Colon:
            # Start command mode
            self._omnibar.show_input()

        elif event.key() == Qt.Key_Escape:
            # Cancel command mode
            self._omnibar.hide_input()

        else:
            super().keyPressEvent(event)


if __name__ == "__main__":
    window = MainWindow(mcolor)
    window.show()

    app.exec()

