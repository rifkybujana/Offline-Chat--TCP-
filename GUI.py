# GUI Components
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

# UI Components
import qtawesome as qta

# Needed to access some system data
import sys
import os

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
    border: 1px hidden white;
    border-radius: 3px;
}
*:hover {
    background-color: #d9d8eb;
    border: 1px solid #d9d8eb;
}
*:pressed {
    background-color: #c4c3d9;
    border: 1px solid #c4c3d9;
}
"""
BUBBLE_INCOME_STYLE = """
* {
    background-color: white;
    border: 1px solid #e6e6f0;
    border-radius: 10px;
}
"""
BUBBLE_OUTCOME_STYLE = """
* {
    background-color: #e6e6f0;
    border: 1px solid #d1d1e3;
    border-radius: 10px;
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

OTHER_WINDOW = []

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
            QPixmap(LOGO_PATH_PNG).scaledToWidth(250)
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

        self.listMessage = QListWidget()
        self.listMessage.setStyleSheet("* { border: none; }")
        self.listMessage.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.listMessage.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)

        
        # example        
        self.addIncomeItem("badrul", "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.")
        self.addOutcomeItem("udin", "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.")

        self.addIncomeImageBubble("badrul", os.path.join(RESOURCE_PATH, "example2.jpg"))
        self.addOutcomeImageBubble("udin", os.path.join(RESOURCE_PATH, "example.png"))
        # example

        
        layout.addWidget(self.listMessage, 9)
        
        self.message_input = QLineEdit()
        self.message_input.setFont(DEFAULT_FONT)
        self.message_input.setPlaceholderText("Type message")
        self.message_input.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.message_input.setStyleSheet(LINEEDIT_STYLE)
        self.message_input.returnPressed.connect(lambda: print(self.message_input.text()))
        # self.message_input.installEventFilter(self)

        layout.addWidget(self.message_input, 1)

        component_layout.addSpacing(10)

        def add_component_button(action, icon, tooltip):
            button = QPushButton(icon, "")
            button.setFont(DEFAULT_FONT_BOLD)
            button.setFixedSize(32, 32)
            button.setStyleSheet(COMPONENT_BUTTON_STYLE)
            button.setIconSize(QSize(16, 16))
            button.setToolTip(tooltip)

            button.pressed.connect(action)

            component_layout.addWidget(button, 1)

            return button

        gdocs_button = add_component_button(
            lambda: print("test"), 
            qta.icon("mdi.file-document-outline"),
            "gdocs"
        )
        math_button = add_component_button(
            lambda: print("test"), 
            qta.icon("mdi.math-integral"),
            "math solver"
        )
        image_button = add_component_button(
            lambda: print("test"), 
            qta.icon("fa.file-image-o"),
            "send image"
        )
        file_button = add_component_button(
            lambda: print("test"), 
            qta.icon("ri.attachment-line"),
            "send attachment"
        )

        component_layout.addWidget(Color("purple"), 10)
        
        component_layout.addSpacing(10)

        layout.addLayout(component_layout, 1)

        self.setLayout(layout)

        self.message_input.setFocus()

    def addIncomeItem(self, username, message):
        message = IncomeChatBubble(username, message)
        widgetItem = QListWidgetItem(self.listMessage)
        widgetItem.setSizeHint(message.sizeHint())
        self.listMessage.addItem(widgetItem)
        self.listMessage.setItemWidget(widgetItem, message)

    def addOutcomeItem(self, username, message):
        message = OutcomeChatBubble(username, message)
        widgetItem = QListWidgetItem(self.listMessage)
        widgetItem.setSizeHint(message.sizeHint())
        self.listMessage.addItem(widgetItem)
        self.listMessage.setItemWidget(widgetItem, message)

    def addIncomeImageBubble(self, username, image):
        message = IncomeImageBubble(username, image)
        widgetItem = QListWidgetItem(self.listMessage)
        widgetItem.setSizeHint(message.sizeHint())
        self.listMessage.addItem(widgetItem)
        self.listMessage.setItemWidget(widgetItem, message)
        
    def addOutcomeImageBubble(self, username, image):
        message = OutcomeImageBubble(username, image)
        widgetItem = QListWidgetItem(self.listMessage)
        widgetItem.setSizeHint(message.sizeHint())
        self.listMessage.addItem(widgetItem)
        self.listMessage.setItemWidget(widgetItem, message)


class IncomeChatBubble(QWidget):
    def __init__(self, username, message, *args, **kwargs):
        super(IncomeChatBubble, self).__init__(*args, **kwargs)

        frame = QFrame()
        frame.setFrameShape(QFrame.StyledPanel)
        frame.setLineWidth(1)
        frame.setLayout(QVBoxLayout())
        frame.setStyleSheet(BUBBLE_INCOME_STYLE)
        
        frame_h_layout = QHBoxLayout()
        frame_h_layout.addWidget(frame, 0)
        frame_h_layout.addWidget(Color("red"), 5)

        layout = QVBoxLayout()

        self.username = QLabel(username)
        self.username.setFont(DEFAULT_FONT_BOLD)
        self.username.setStyleSheet("* { background-color: transparent; }")
        layout.addWidget(self.username, 0, alignment=Qt.AlignTop | Qt.AlignLeft)
        
        layout.addLayout(frame_h_layout, 3)
        
        self.message = QLabel(message)
        self.message.setFont(DEFAULT_FONT)
        self.message.setWordWrap(True)
        self.message.setStyleSheet("* { background-color: transparent; border: none; }")
        frame.layout().addWidget(self.message, alignment=Qt.AlignTop | Qt.AlignLeft)

        self.setLayout(layout)

    def __str__(self) -> str:
        return self.message.text()


class OutcomeChatBubble(QWidget):
    def __init__(self, username, message, *args, **kwargs):
        super(OutcomeChatBubble, self).__init__(*args, **kwargs)

        frame = QFrame()
        frame.setFrameShape(QFrame.StyledPanel)
        frame.setLineWidth(1)
        frame.setLayout(QVBoxLayout())
        frame.setStyleSheet(BUBBLE_OUTCOME_STYLE)
        
        frame_h_layout = QHBoxLayout()
        frame_h_layout.addWidget(Color("red"), 5)
        frame_h_layout.addWidget(frame, 0)

        layout = QVBoxLayout()

        self.username = QLabel(username)
        self.username.setFont(DEFAULT_FONT_BOLD)
        self.username.setStyleSheet("* { background-color: transparent; }")
        layout.addWidget(self.username, 0, alignment=Qt.AlignTop | Qt.AlignRight)
        
        layout.addLayout(frame_h_layout, 3)
        
        self.message = QLabel(message)
        self.message.setFont(DEFAULT_FONT)
        self.message.setWordWrap(True)
        self.message.setStyleSheet("* { background-color: transparent; border: none; }")
        frame.layout().addWidget(self.message, alignment=Qt.AlignTop | Qt.AlignRight)

        self.setLayout(layout)

    def __str__(self) -> str:
        return self.message.text()


class ImageViewer(QWidget):
    def __init__(self, image, *args, **kwargs):
        super(ImageViewer, self).__init__(*args, **kwargs)

        pixmap = QPixmap(image)
        pixmap = pixmap.scaled(
            QSize(
                min(
                    pixmap.width(),
                    800
                ),
                min(
                    pixmap.height(),
                    600
                )
            ),
            Qt.KeepAspectRatio,
            Qt.SmoothTransformation
        )

        self.image_label = QLabel(self)
        self.image_label.setScaledContents(True)
        self.image_label.setBackgroundRole(QPalette.Base)
        self.image_label.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
        self.image_label.setPixmap(pixmap)

        self.setFixedSize(pixmap.size())


class IncomeImageBubble(QWidget):
    def __init__(self, username, image, *args, **kwargs):
        super(IncomeImageBubble, self).__init__(*args, **kwargs)

        self.image = image

        layout = QVBoxLayout()

        self.username = QLabel(username)
        self.username.setFont(DEFAULT_FONT_BOLD)
        self.username.setStyleSheet("* { background-color: transparent; }")
        layout.layout().addWidget(self.username, 0, alignment=Qt.AlignTop | Qt.AlignLeft)

        image_layout = QHBoxLayout()

        self.image_label = QLabel()
        self.image_label.setMaximumHeight(200)
        self.image_label.setMaximumWidth(300)
        original_pixmap = QPixmap(self.image)
        original_pixmap = original_pixmap.scaled(
            QSize(
                min(
                    original_pixmap.width(),
                    self.image_label.maximumWidth()
                ),
                min(
                    original_pixmap.height(),
                    self.image_label.maximumHeight()
                )
            ),
            Qt.KeepAspectRatio,
            Qt.SmoothTransformation
        )

        pixmap = QPixmap(original_pixmap.size())
        pixmap.fill(QColor("transparent"))

        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setBrush(QBrush(original_pixmap))
        painter.setPen(Qt.NoPen)
        painter.drawRoundedRect(original_pixmap.rect(), 10, 10)

        self.image_label.setPixmap(pixmap)
        self.image_label.mousePressEvent = self.openImage
        
        del painter

        image_layout.addWidget(self.image_label, 0)
        image_layout.addWidget(Color("red"), 5)

        layout.addLayout(image_layout)

        self.setLayout(layout)

    def openImage(self, event):
        global OTHER_WINDOW
        self.w = ImageViewer(self.image)
        self.w.show()

        OTHER_WINDOW.append(self.w)


class OutcomeImageBubble(QWidget):
    def __init__(self, username, image, *args, **kwargs):
        super(OutcomeImageBubble, self).__init__(*args, **kwargs)

        self.image = image

        layout = QVBoxLayout()

        self.username = QLabel(username)
        self.username.setFont(DEFAULT_FONT_BOLD)
        self.username.setStyleSheet("* { background-color: transparent; }")
        layout.layout().addWidget(self.username, 0, alignment=Qt.AlignTop | Qt.AlignRight)

        image_layout = QHBoxLayout()

        self.image_label = QLabel()
        self.image_label.setMaximumHeight(200)
        self.image_label.setMaximumWidth(300)
        original_pixmap = QPixmap(self.image)
        original_pixmap = original_pixmap.scaled(
            QSize(
                min(
                    original_pixmap.width(),
                    self.image_label.maximumWidth()
                ),
                min(
                    original_pixmap.height(),
                    self.image_label.maximumHeight()
                )
            ),
            Qt.KeepAspectRatio,
            Qt.SmoothTransformation
        )

        pixmap = QPixmap(original_pixmap.size())
        pixmap.fill(QColor("transparent"))

        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setBrush(QBrush(original_pixmap))
        painter.setPen(Qt.NoPen)
        painter.drawRoundedRect(original_pixmap.rect(), 10, 10)

        self.image_label.setPixmap(pixmap)
        self.image_label.mousePressEvent = self.openImage
        
        del painter

        image_layout.addWidget(Color("red"), 5)
        image_layout.addWidget(self.image_label, 0)

        layout.addLayout(image_layout)

        self.setLayout(layout)

    def openImage(self, event):
        global OTHER_WINDOW
        self.w = ImageViewer(self.image)
        self.w.show()

        OTHER_WINDOW.append(self.w)


class MainWindow(QMainWindow):
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

    def closeEvent(self, event):
        global OTHER_WINDOW
        for window in OTHER_WINDOW:
            window.close()
            
        event.accept()

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