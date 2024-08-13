import os
import shutil
import sys
from multiprocessing import Process, Queue

from PyQt6.QtCore import QTimer
from PyQt6.QtWidgets import (
    QApplication,
    QCheckBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from constants import DOWNLOAD_TMP_DIR
from download import Downloader


class DownloadProcess:
    def __init__(self, queue, downloader):
        self.queue = queue
        self.downloader = downloader
        self.audio_only = False

    def run(self):
        try:
            self.downloader.cleanup()
            if self.audio_only:
                self.downloader.audio_download()
            else:
                self.downloader.full_download()
            self.queue.put("finished")
        except Exception as e:
            self.queue.put(f"error:{str(e)}")


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

        # Cancel button
        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.clicked.connect(self.cancel_download)
        self.cancel_button.setEnabled(False)
        layout.addWidget(self.cancel_button)

        self.setLayout(layout)

    def start_download(self):
        url = self.url_field.text()
        resolution = (
            self.resolution_field.text()
            if self.resolution_field.text()
            else "720"
        )
        audio_only = self.audio_only_checkbox.isChecked()

        if not url:
            QMessageBox.warning(self, "Input Error", "URL cannot be empty.")
            return

        self.queue = Queue()
        self.download_process = Process(
            target=DownloadProcess(
                self.queue, Downloader(url=url, resolution=resolution)
            ).run
        )
        self.download_process.audio_only = audio_only
        self.download_process.start()

        self.download_button.setEnabled(False)
        self.cancel_button.setEnabled(True)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.check_queue)
        self.timer.start(100)

    def cancel_download(self):
        try:
            self.download_process.kill()
        finally:
            self.download_button.setEnabled(True)
            self.cancel_button.setEnabled(False)

    def check_queue(self):
        if not self.queue.empty():
            message = self.queue.get()
            if message == "finished":
                QMessageBox.information(
                    self,
                    "Download Complete",
                    "Download completed successfully.",
                )
            elif message.startswith("error:"):
                QMessageBox.critical(self, "Download Error", message[6:])
            self.download_button.setEnabled(True)
            self.cancel_button.setEnabled(False)
            self.timer.stop()

    def cleanup(self):
        if os.path.exists(DOWNLOAD_TMP_DIR):
            shutil.rmtree(DOWNLOAD_TMP_DIR)


def main():
    app = QApplication(sys.argv)
    downloader_window = DownloaderWindow()
    downloader_window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
