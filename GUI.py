# GUI Components
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

# Needed to access some system data
import sys
import os

import time

# STYLESHEET
WINDOW_STYLE = """
* {
    background-color: white;
}
"""
LINEEDIT_STYLE = """
* {
    border: 1px solid #ECC8C8;
    border-radius: 5px;
    padding-left: 10px;
}
*:focus {
    border: 1px solid #ECC8C8;
    border-radius: 5px;
    border-bottom: 2px solid #5e5eff;
}
"""
SEARCH_BAR_STYLE = """
* {
    border-style: none none solid none;
    border-bottom-width: 1px;
    border-bottom-color: #ECC8C8;
}
*:focus {
    border-bottom-width: 2px;
    border-bottom-color: #5e5eff;
}
"""
SUBMIT_BUTTON_STYLE = """
* {
    color: white;
    background-color: #9b49de;
    border: 1px solid #ECC8C8;
    border-radius: 5px
}
*:hover {
    background-color: #6f16b8;
}
*:pressed {
    background-color: #4e0887;
}
"""
COMPONENT_BUTTON_STYLE = """
* {
    background-color: transparent;
    border: none;
}
"""

# FONTS
DEFAULT_FONT_FAMILY = "MS Shell Dlg 2"
DEFAULT_FONT = QFont(DEFAULT_FONT_FAMILY, 9)
DEFAULT_FONT_BOLD = QFont(DEFAULT_FONT_FAMILY, 9)
DEFAULT_FONT_BOLD.setBold(True)

# PATHS
RESOURCE_PATH = os.path.join(os.getcwd(), "resource")
LOGO_PATH_PNG = os.path.join(RESOURCE_PATH, "logo.png")
LOGO_PATH_ICO = os.path.join(RESOURCE_PATH, "logo.ico")

# WINDOW SETTINGS
WINDOW_SIZE = QSize(600, 450)
WINDOW_TITLE = "Megalitikum Robotikum"


class Color(QWidget):
    """Widget to check layout"""
    def __init__(self, color):
        super(Color, self).__init__()
        self.setAutoFillBackground(True)

        palette = self.palette()
        palette.setColor(QPalette.Window, QColor(color))
        self.setPalette(palette)


class AuthWidget(QWidget):
    def __init__(self, *args, **kwargs):
        super(AuthWidget, self).__init__(*args, **kwargs)

        layout = QVBoxLayout()

        layout.addSpacing(50)

        image_label = QLabel()
        image_label.setPixmap(
            QPixmap(LOGO_PATH_PNG).
            scaledToHeight(500).
            scaledToWidth(250)
        )

        layout.addWidget(image_label, stretch=5, alignment=Qt.AlignCenter)

        self.ip_addr = QLineEdit()
        self.ip_addr.setFont(DEFAULT_FONT)
        self.ip_addr.setPlaceholderText("192.168.1.4")
        self.ip_addr.setFixedSize(300, 30)
        self.ip_addr.setAlignment(Qt.AlignCenter)
        self.ip_addr.setStyleSheet(LINEEDIT_STYLE)

        layout.addWidget(self.ip_addr, stretch=1, alignment=Qt.AlignCenter)

        self.username = QLineEdit()
        self.username.setFont(DEFAULT_FONT)
        self.username.setPlaceholderText("Username")
        self.username.setFixedSize(300, 30)
        self.username.setAlignment(Qt.AlignCenter)
        self.username.setStyleSheet(LINEEDIT_STYLE)

        layout.addWidget(self.username, stretch=1, alignment=Qt.AlignCenter)

        submit_button = QPushButton("Connect")
        submit_button.setFont(DEFAULT_FONT_BOLD)
        submit_button.setFixedSize(300, 30)
        submit_button.setStyleSheet(SUBMIT_BUTTON_STYLE)

        layout.addWidget(submit_button, stretch=1, alignment=Qt.AlignCenter)
        
        self.ip_addr.returnPressed.connect(self.username.setFocus)
        self.username.returnPressed.connect(self.connect)
        submit_button.pressed.connect(self.connect)

        layout.addSpacing(50)

        widget = QWidget()
        widget.setLayout(layout)
        
        self.setLayout(layout)

    def connect(self):
        if len(self.ip_addr.text()) <= 0 or len(self.username.text()) <= 0:
            return

        super().parent().showWidget(LoadingWidget)
        self.deleteLater()


class LoadingWidget(QWidget):
    def __init__(self, *args, **kwargs):
        super(LoadingWidget, self).__init__(*args, **kwargs)
        
        self._animation = QMovie(os.path.join(RESOURCE_PATH, "spinner.gif"))
        self._animation.setScaledSize(QSize(50, 50))

        layout = QVBoxLayout()

        self._label = QLabel()
        self._label.setMovie(self._animation)

        layout.addWidget(self._label, alignment=Qt.AlignCenter)

        self.setLayout(layout)

        self.start()

    def start(self):
        self._animation.start()

    def stop(self):
        self._animation.stop()


class MessageWidget(QWidget):
    def __init__(self, *args, **kwargs):
        super(MessageWidget, self).__init__(*args, **kwargs)
        
        layout = QVBoxLayout()
        component_layout = QHBoxLayout()

        self.search = QLineEdit()
        self.search.setFont(DEFAULT_FONT)
        self.search.setPlaceholderText("Search (blom jadi)")
        self.search.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.search.setStyleSheet(SEARCH_BAR_STYLE)

        layout.addWidget(self.search, 1)

        layout.addWidget(Color("green"), 9)
        
        self.message_input = QLineEdit()
        self.message_input.setFont(DEFAULT_FONT)
        self.message_input.setPlaceholderText("Type message")
        self.message_input.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.message_input.setStyleSheet(LINEEDIT_STYLE)

        layout.addWidget(self.message_input, 1)

        component_layout.addSpacing(10)

        def add_component_button(action, text):
            button = QPushButton(text)
            button.setFont(DEFAULT_FONT_BOLD)
            button.setFixedSize(20, 20)
            button.setStyleSheet(COMPONENT_BUTTON_STYLE)
            button.setIconSize(QSize(20, 20))

            button.pressed.connect(action)

            component_layout.addWidget(button, 1)

            return button

        gdocs_button = add_component_button(
            lambda: print("test"), 
            "1"
        )
        math_button = add_component_button(
            lambda: print("test"), 
            "2"
        )
        image_button = add_component_button(
            lambda: print("test"), 
            "3"
        )
        file_button = add_component_button(
            lambda: print("test"), 
            "4"
        )

        component_layout.addWidget(Color("purple"), 10)
        
        component_layout.addSpacing(10)

        layout.addLayout(component_layout, 1)

        self.setLayout(layout)


class MainWindow(QMainWindow):
    """
    Window for user to connect to the server
    """

    def __init__(self):
        super().__init__()

        # Window setup
        self.setWindowTitle(WINDOW_TITLE)
        self.setWindowIcon(QIcon(LOGO_PATH_ICO))
        self.setFixedSize(WINDOW_SIZE)
        self.setStyleSheet(WINDOW_STYLE)
        
        # ask user the Host/server IP address
        self.showWidget(MessageWidget)

        # Show window, windows are hidden by default.
        self.show()

    def showWidget(self, widget, *args):
        self.currentWidget = widget(self)
        self.setCentralWidget(self.currentWidget)


if __name__ == "__main__":
    # Only need one QApplication instance per application.
    # Pass in sys.argv to allow command line arguments for your app.
    # If you know you won't use command line arguments QApplication([]) works too.
    app = QApplication(sys.argv)

    # Create a Qt main window, which will be our window.
    window = MainWindow()

    # Start the event loop.
    app.exec_()


    # Application won't reach here until you exit and the event
    # loop has stopped.