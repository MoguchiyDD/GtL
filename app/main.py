# Developer && Owner: МогучийДД (MoguchiyDD)
# LICENSE: MIT License which is located in the text file LICENSE
#
# Goal: Launch Working SOFTWARE
# Result: Opens The Finished SOFTWARE in The ACTIVE WINDOW
#
# Past Modification: Editing «MainWindow» CLASS (WINDOW TITLE)
# Last Modification: Editing «MainWindow» CLASS (HEADER)
# Modification Date: 2023.10.23, 08:49 PM
#
# Create Date: 2023.10.23, 11:28 AM


from PySide6.QtCore import Qt
from PySide6.QtGui import QScreen
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout
)

from models.values import string_values
from models.header import Header

from sys import argv, exit


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

		# TITLE
        window_title = string_values("app_title")
        self.setWindowTitle(window_title)

        self.setMinimumSize(self.MIN_WIDTH, self.MIN_HEIGHT)  # SIZE

        # CENTER WINDOW
        center = QScreen.availableGeometry(
            QApplication.primaryScreen()
        ).center()
        geo = self.frameGeometry()
        geo.moveCenter(center)
        self.move(geo.topLeft())

        # CONTENT
        self.main_layout = QVBoxLayout()
        Header(self)

        # INSTALL
        widget = QWidget()
        widget.setLayout(self.main_layout)
        self.setCentralWidget(widget)

# ----------------------------------


if __name__ == "__main__":
    app = QApplication(argv)

    window = MainWindow()
    window.show()

    exit(app.exec())
