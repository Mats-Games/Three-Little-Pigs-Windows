import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtNetwork import QNetworkAccessManager, QNetworkRequest, QNetworkReply

class WebBrowser(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Three Little Pigs")  # Set window title
        self.browser = QWebEngineView()
        self.browser.page().profile().downloadRequested.connect(self.download_requested)
        self.browser.page().iconUrlChanged.connect(self.update_favicon)  # Connect to iconUrlChanged signal
        url = QUrl("https://tlpigs.net")
        self.browser.setUrl(url)

        self.setCentralWidget(self.browser)

        self.network_manager = QNetworkAccessManager()  # Initialize the network manager

    def download_requested(self, download_item):
        download_path, _ = QFileDialog.getSaveFileName(self, "Save File", download_item.path())
        if download_path:
            download_item.setPath(download_path)
            download_item.accept()

    def save_file(self, reply, file_path):
        if reply.error() == QNetworkReply.NoError:
            with open(file_path, 'wb') as f:
                f.write(reply.readAll())
        else:
            print("Download error:", reply.errorString())
        reply.deleteLater()

    def set_window_icon(self, pixmap):
        if isinstance(pixmap, QPixmap) and not pixmap.isNull():
            icon = QIcon(pixmap)
            self.setWindowIcon(icon)

    def update_favicon(self, url):
        icon_url = self.browser.iconUrl()
        if icon_url.isValid():
            request = QNetworkRequest(icon_url)
            reply = self.network_manager.get(request)
            reply.finished.connect(lambda: self.process_icon_reply(reply))

    def process_icon_reply(self, reply):
        if reply.error() == QNetworkReply.NoError:
            pixmap = QPixmap()
            pixmap.loadFromData(reply.readAll())
            self.set_window_icon(pixmap)
        reply.deleteLater()

def main():
    app = QApplication(sys.argv)

    default_width = 1280
    default_height = 1024

    pyqt_window = WebBrowser()
    pyqt_window.resize(default_width, default_height)
    pyqt_window.show()

    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
