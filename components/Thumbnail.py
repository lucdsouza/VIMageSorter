from PySide6.QtWidgets import QWidget, QSizePolicy, QHBoxLayout, QVBoxLayout, QLabel
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt
from components.ThumbTag import ThumbTag


class Thumbnail(QWidget):
    def __init__(self, pixmap, filename, thumb_id, tags, parent=None):
        super().__init__(parent)
        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.setFixedSize(180, 220)

        pixmap = pixmap.scaled(180, 160, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        img_width = pixmap.width()
        img_height = pixmap.height()

        self._container = QWidget(self)
        self._container.setFixedSize(img_width, img_height)
        self._container.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        # Thumbnail image.
        self._image_label = QLabel(self._container)
        self._image_label.setPixmap(pixmap)
        self._image_label.setGeometry(0, 0, img_width, img_height)

        # Bottom overlay for tags.
        overlay_height = 22
        self._btag_overlay = QWidget(self._container)
        self._btag_overlay.setGeometry(0, img_height-overlay_height, img_width, overlay_height-2)
        self._btag_overlay.setStyleSheet("background-color: rgba(0, 0, 0, 0);")

        tag_layout = QHBoxLayout(self._btag_overlay)
        tag_layout.setContentsMargins(5, 0, 5, 0)
        tag_layout.setSpacing(8)

        tag_layout.addWidget(ThumbTag(thumb_id))
        for tag in tags:
            tag_layout.addWidget(tag)

        tag_layout.addStretch()

        # Filename.
        self._filename_label = QLabel(filename, self)
        self._filename_label.setAlignment(Qt.AlignCenter)
        self._filename_label.setStyleSheet("font-size: 9pt;")
        self._filename_label.setGeometry(0, min(img_height, 160), self.width(), 30)


