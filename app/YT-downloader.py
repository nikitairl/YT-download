import sys
from PyQt6.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QCheckBox,
    QPushButton,
    QMessageBox,
)
from download import Downloader


class DownloaderWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setWindowTitle("Downloader")
        self.setMinimumSize(400, 200)

        layout = QVBoxLayout()

        # URL field
        url_layout = QHBoxLayout()
        url_label = QLabel("URL:")
        self.url_field = QLineEdit()
        url_layout.addWidget(url_label)
        url_layout.addWidget(self.url_field)
        layout.addLayout(url_layout)

        # Resolution field
        resolution_layout = QHBoxLayout()
        resolution_label = QLabel("Resolution (default if empty: 720):")
        self.resolution_field = QLineEdit()
        resolution_layout.addWidget(resolution_label)
        resolution_layout.addWidget(self.resolution_field)
        layout.addLayout(resolution_layout)

        # Audio only checkbox
        self.audio_only_checkbox = QCheckBox("Audio Only")
        layout.addWidget(self.audio_only_checkbox)

        # Download button
        self.download_button = QPushButton("Download")
        self.download_button.clicked.connect(self.start_download)
        layout.addWidget(self.download_button)
        self
        self.setLayout(layout)

    def start_download(self):
        url = self.url_field.text()
        resolution = (
            self.resolution_field.text()
            if self.resolution_field.text()
            else "1080"
        )
        audio_only = self.audio_only_checkbox.isChecked()

        if not url:
            QMessageBox.warning(self, "Input Error", "URL cannot be empty.")
            return

        try:
            downloader = Downloader(url=url, resolution=resolution)
            if audio_only:
                downloader.audio_download()
            else:
                downloader.full_download()

            QMessageBox.information(
                self, "Download Complete", "Download completed successfully."
            )
        except Exception as e:
            QMessageBox.critical(self, "Download Error", str(e))


def main():
    app = QApplication(sys.argv)
    downloader_window = DownloaderWindow()
    downloader_window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
