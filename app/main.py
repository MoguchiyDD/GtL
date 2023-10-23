# Developer && Owner: МогучийДД (MoguchiyDD)
# LISENCE: MIT License which is located in the text file LICENSE
#
# Goal: Launch Working SOFTWARE
# Result: Opens The Finished SOFTWARE in The ACTIVE WINDOW
#
# Past Modification: Adding «MainWindow» CLASS
# Last Modification: Checking CODE The PEP8
# Modification Date: 2023.10.23, 12:26 PM
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

        self.setWindowTitle("QtL : Guide to Letters")  # TITLE
        self.setMinimumSize(self.MIN_WIDTH, self.MIN_HEIGHT)  # SIZE

        # CENTER WINDOW
        center = QScreen.availableGeometry(
            QApplication.primaryScreen()
        ).center()
        geo = self.frameGeometry()
        geo.moveCenter(center)
        self.move(geo.topLeft())

        self.main_layout = QVBoxLayout()  # CONTENT

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
