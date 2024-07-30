#Run python browser.py in the same folder as this file and the bookmarks file, if no bookmarks file esxistsitll make a new one

import sys
import csv
from PyQt5.QtWidgets import QApplication, QMainWindow, QLineEdit, QPushButton, QVBoxLayout, QWidget, QHBoxLayout, QListWidget
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl

class SimpleBrowser(QMainWindow):
    def __init__(self):
        super().__init__()
        self.browser = QWebEngineView()
        self.url_bar = QLineEdit()
        self.back_button = QPushButton('Back')
        self.forward_button = QPushButton('Forward')
        self.bookmark_button = QPushButton('Bookmark')
        self.bookmark_list = QListWidget()
        self.bookmarks = []

        self.init_ui()
        self.load_bookmarks()

    def init_ui(self):
        self.browser.setUrl(QUrl("http://www.google.com"))

        self.url_bar.returnPressed.connect(self.load_url)
        self.back_button.clicked.connect(self.browser.back)
        self.forward_button.clicked.connect(self.browser.forward)
        self.bookmark_button.clicked.connect(self.add_bookmark)

        self.bookmark_list.itemClicked.connect(self.load_bookmark_from_list)

        nav_bar = QHBoxLayout()
        nav_bar.addWidget(self.back_button)
        nav_bar.addWidget(self.forward_button)
        nav_bar.addWidget(self.url_bar)
        nav_bar.addWidget(self.bookmark_button)

        bookmark_layout = QVBoxLayout()
        bookmark_layout.addWidget(self.bookmark_list)
        bookmark_widget = QWidget()
        bookmark_widget.setLayout(bookmark_layout)
        bookmark_widget.setFixedWidth(200)

        layout = QHBoxLayout()
        layout.addWidget(self.browser)
        layout.addWidget(bookmark_widget)

        main_layout = QVBoxLayout()
        main_layout.addLayout(nav_bar)
        main_layout.addLayout(layout)

        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

        self.browser.urlChanged.connect(self.update_url_bar)

        self.setWindowTitle('Simple Web Browser')
        self.setGeometry(100, 100, 1200, 800)
        self.show()

    def load_url(self):
        url = QUrl(self.url_bar.text())
        if not url.isValid():
            url = QUrl("http://" + self.url_bar.text())
        self.browser.setUrl(url)

    def update_url_bar(self, q):
        self.url_bar.setText(q.toString())

    def add_bookmark(self):
        url = self.url_bar.text()
        if url and url not in self.bookmarks:
            self.bookmarks.append(url)
            self.bookmark_list.addItem(url)
            self.save_bookmarks()

    def load_bookmarks(self):
        try:
            with open('bookmarks.csv', 'r', newline='') as file:
                reader = csv.reader(file)
                for row in reader:
                    if row:
                        self.bookmarks.append(row[0])
                        self.bookmark_list.addItem(row[0])
        except FileNotFoundError:
            pass

    def save_bookmarks(self):
        with open('bookmarks.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            for bookmark in self.bookmarks:
                writer.writerow([bookmark])

    def load_bookmark_from_list(self, item):
        url = item.text()
        self.url_bar.setText(url)
        self.browser.setUrl(QUrl(url))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    browser = SimpleBrowser()
    sys.exit(app.exec_())
