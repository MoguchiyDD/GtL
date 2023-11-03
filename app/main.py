# Developer && Owner: МогучийДД (MoguchiyDD)
# LICENSE: MIT License which is located in the text file LICENSE
#
# Goal: Launch Working SOFTWARE
# Result: Opens The Finished SOFTWARE in The ACTIVE WINDOW
#
# Past Modification: Adding The «MainWindow» CLASS (basedir)
# Last Modification: Adding The «MainWindow» CLASS (RAM (Settings File))
# Modification Date: 2023.11.03, 12:49 AM
#
# Create Date: 2023.10.23, 11:28 AM


from PySide6.QtCore import Qt
from PySide6.QtGui import QScreen, QFontDatabase
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout

from models.filesystem import FyleSystem
from models.values import StringsValues
from models.header import Header
from models.content import Content
from models.footer import Footer

from sys import argv, exit
from os import path

basedir = path.dirname(__file__)


# ------------ SOFTWARE ------------

class MainWindow(QMainWindow):
    """
    The MAIN CLASS that Runs The All SOFTWARE

    ---
    PARAMETER:
    - parent: QWidget | None = None -> Widget PARENT for this CLASS
    (AFTER THAT, THIS CURRENT CLASS WILL BECOME A CHILD OF THE PARENT)
    - f: Qt.WindowType = Qt.WindowType.Window -> Window-System (Window)
    """

    MIN_WIDTH = 1024
    MIN_HEIGHT = 600

    def __init__(
        self,
        parent: QWidget | None = None,
        flags: Qt.WindowType = Qt.WindowType.Window
    ) -> None:
        super(MainWindow, self).__init__(parent, flags)

        global basedir
        self.basedir = basedir

        # RAM (Settings File)
        filesystem = FyleSystem(self.basedir)
        self.data_from_settings_file = filesystem.read_file_settings()

        # TITLE
        window_title = StringsValues().string_values("app_title")
        self.setWindowTitle(window_title)

        self.setMinimumSize(self.MIN_WIDTH, self.MIN_HEIGHT)  # SIZE

        # CENTER WINDOW
        center = QScreen.availableGeometry(
            QApplication.primaryScreen()
        ).center()
        geo = self.frameGeometry()
        geo.moveCenter(center)
        self.move(geo.topLeft())

        # FONTS
        QFontDatabase.addApplicationFont("app/fonts/Lora/Lora-Bold.ttf")
        QFontDatabase.addApplicationFont("app/fonts/Lora/Lora-Regular.ttf")
        QFontDatabase.addApplicationFont("app/fonts/Ubuntu/Ubuntu-B.ttf")
        QFontDatabase.addApplicationFont("app/fonts/Ubuntu/Ubuntu-R.ttf")

        # CONTENT
        self.main_layout = QVBoxLayout()
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        Header(self)
        Content(self)
        Footer(self)

        # INSTALL
        widget = QWidget()
        widget.setLayout(self.main_layout)
        self.setCentralWidget(widget)

# ----------------------------------


if __name__ == "__main__":
    app = QApplication(argv)

    with open(path.join(basedir, "qss", "main.qss"), "r") as qss_file:
        app.setStyleSheet(qss_file.read())

    window = MainWindow()
    window.show()

    exit(app.exec())
