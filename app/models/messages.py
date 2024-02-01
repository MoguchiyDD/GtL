# Developer && Owner: МогучийДД (MoguchiyDD)
# LICENSE: MIT License which is located in the text file LICENSE
#
# Goal: Message DIALOG BOX
# Result: Shows The Generated Message DIALOG BOX
#
# Past Modification: Adding The «activate_message_box» FUNCTION («MESSAGE BOX»)
# Last Modification: Editing The «MessageBox» CLASS (PRIVATE)
# Modification Date: 2024.02.01, 01:56 PM
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

from .values import StringsValues

from os import path


# ------------ MESSAGE BOX ------------

class __MessageBox(QDialog):
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

    HEIGHT = 107
    WIDTH = 430
    WIDTH_ICON = 90
    WIDTH_TEXT = WIDTH - 130

    def __init__(
        self,
        icon: str, title: str, text: str,
        parent: QWidget | None = None,
        f: Qt.WindowType = Qt.WindowType.Widget
    ) -> None:
        super(__MessageBox, self).__init__(parent, f)
        self.setParent(parent)

        self.setWindowFlags(Qt.WindowType.Dialog)
        self.setWindowTitle(title)

        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        template = self.page(icon, text)
        layout.addWidget(template, alignment=Qt.AlignmentFlag.AlignCenter)

        self.setFixedSize(self.WIDTH, self.HEIGHT)

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
        frame.setFixedSize(self.WIDTH, self.HEIGHT)

        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        w_icon = QLabel()
        w_icon.setObjectName("message_icon")
        w_icon.setPixmap(QPixmap(icon).scaled(67, 64))
        w_icon.setFixedWidth(self.WIDTH_ICON)

        w_text = QLabel(text)
        w_text.setObjectName("message_text")
        w_text.setFont(QFont("Ubuntu"))
        w_text.setWordWrap(True)
        w_text.setAlignment(Qt.AlignmentFlag.AlignJustify)
        w_text.setFixedWidth(self.WIDTH_TEXT)

        layout.addWidget(w_icon, alignment=Qt.AlignmentFlag.AlignRight)
        layout.addWidget(w_text)

        frame.setLayout(layout)
        return frame


def activate_message_box(
    basedir: str, title: str, text: str, icon: str, parent: QWidget
) -> None:
    """
    ---
    PARAMETERS:
    - basedir: str -> Link to CODE HOME DIRECTORY
    - title: str -> FULL NAME of The ARGUMENT from The XML FILE with STRINGS
    (HEADER)
    - text: str -> FULL NAME of The ARGUMENT from The XML FILE with STRINGS
    (CONTENT)
    - icon: str -> NAME of The ICON with FORMAT
    - parent: QWidget -> Widget PARENT for this MESSAGES
    """

    msg_title = StringsValues(basedir).string_values(title)
    msg_text = StringsValues(basedir).string_values(text)
    __MessageBox(
        path.join(basedir, "icons", icon), msg_title, msg_text, parent
    )

# -------------------------------------
