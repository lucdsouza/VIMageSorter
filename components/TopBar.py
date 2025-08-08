from PySide6.QtWidgets import QWidget, QHBoxLayout, QLabel
from utils import format_bytes


class TopBar(QWidget):
    def __init__(self, parent):
        super().__init__(parent)

        self.folder_path = "/"
        self.folder_size = "0 B"
        self.image_count = 0
        self.video_count = 0
        
        self.layout = QHBoxLayout(self)
        self.layout.setContentsMargins(2, 2, 2, 2)

        # Label to display current folder.
        self._folder_label = QLabel("")
        self._folder_label.setVisible(True)
        self.layout.addWidget(self._folder_label)

        # Space Between.
        self.layout.addStretch(1)

        # Label to Display count and size.
        self._folder_info_label = QLabel("")
        self._folder_info_label.setVisible(True)
        self.layout.addWidget(self._folder_info_label)

        self._update_labels()

    def _update_labels(self):
        self._folder_label.setText(self.folder_path)

        file_count = "0 files"
        if self.image_count and self.video_count:
            file_count = f"{self.image_count} images  {self.video_count} videos"
        
        elif self.image_count:
            file_count = f"{self.image_count} images"

        elif self.video_count:
            file_count = f"{self.video_count} videos"

        self._folder_info_label.setText(f"{file_count}  {self.folder_size}")

    def set_folder(self, folder_path, folder_size, image_count=0, video_count=0):
        self.folder_path = folder_path
        self.folder_size = format_bytes(folder_size)
        self.image_count = image_count
        self.video_count = video_count

        self._update_labels()
