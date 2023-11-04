# Developer && Owner: МогучийДД (MoguchiyDD)
# LICENSE: MIT License which is located in the text file LICENSE
#
# Goal: Message DIALOG BOX
# Result: Shows The Generated Message DIALOG BOX
#
# Past Modification: Adding The «MessageBox» CLASS
# Last Modification: Editing The «MessageBox» CLASS (TEMPLATE)
# Modification Date: 2023.11.04, 04:22 PM
#
# Create Date: 2023.11.04, 01:11 PM


from PySide6.QtCore import Qt
from PySide6.QtGui import QFont, QPixmap, QScreen
from PySide6.QtWidgets import (
    QApplication,
    QDialog,
    QWidget,
    QFrame,
    QVBoxLayout,
    QHBoxLayout,
    QLabel
)


# ------------ MESSAGE BOX ------------

class MessageBox(QDialog):
    """
    Generates 1 MODAL WINDOW with 1 MESSAGE

    ---
    PARAMETERS:
    - icon: str -> The ICON for MESSAGE BODY
    - title: str -> The TITLE for MESSAGE WINDOW
    - text: str -> The TEXT for MESSAGE BODY
    - parent: QWidget | None = None -> Widget PARENT for this CLASS
    (AFTER THAT, THIS CURRENT CLASS WILL BECOME A CHILD OF THE PARENT)
    - f: Qt.WindowType = Qt.WindowType.Widget -> Window-System (Widget)
    ---
    FUNCTIONS:
    - page(icon: str, text: str) -> QFrame : Create 1 MESSAGE TEMPLATE
    """

    WIDTH = 430

    def __init__(
        self,
        icon: str, title: str, text: str,
        parent: QWidget | None = None,
        f: Qt.WindowType = Qt.WindowType.Widget
    ) -> None:
        super(MessageBox, self).__init__(parent, f)
        self.setParent(parent)

        self.setWindowFlags(Qt.WindowType.Dialog)
        self.setWindowTitle(title)

        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        template = self.page(icon, text)
        layout.addWidget(template, alignment=Qt.AlignmentFlag.AlignCenter)

        self.setFixedSize(self.WIDTH, layout.heightForWidth(self.WIDTH))

        # CENTER WINDOW
        center = QScreen.availableGeometry(
            QApplication.primaryScreen()
        ).center()
        geo = self.frameGeometry()
        geo.moveCenter(center)
        self.move(geo.topLeft())

        self.setLayout(layout)
        self.exec()

    def page(self, icon: str, text: str) -> QFrame:
        """
        Create 1 MESSAGE TEMPLATE

        ---
        PARAMETERS;
        - icon: str -> The ICON for MESSAGE
        - text: str -> The TEXT for MESSAGE
        ---
        RESULT: MESSAGE TEMPLATE
        """

        frame = QFrame()
        frame.setObjectName("message")

        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(17)

        w_icon = QLabel()
        w_icon.setObjectName("message_icon")
        w_icon.setPixmap(QPixmap(icon).scaled(67, 64))

        w_text = QLabel(text)
        w_text.setObjectName("message_text")
        w_text.setFont(QFont("Ubuntu"))
        w_text.setWordWrap(True)

        layout.addWidget(w_icon, alignment=Qt.AlignmentFlag.AlignLeft)
        layout.addWidget(w_text, alignment=Qt.AlignmentFlag.AlignTop)

        frame.setLayout(layout)
        return frame

# -------------------------------------
