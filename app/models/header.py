# Developer && Owner: МогучийДД (MoguchiyDD)
# LICENSE: MIT License which is located in the text file LICENSE
#
# Goal: Create a HEADER TEMPLATE with Ready-Made Working Filling
# Result: Providing a HEADER TEMPLATE
#
# Past Modification: Checking CODE The PEP8
# Last Modification: Editing The «Header» CLASS («page»)
# Modification Date: 2023.10.24, 04:32 PM
#
# Create Date: 2023.10.23, 06:45 PM


from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import (
    QWidget,
    QFrame,
    QHBoxLayout,
    QLabel,
    QPushButton
)

from .values import string_values


# ------------ HEADER ------------

class Header(QWidget):
    """
    Providing a HEADER TEMPLATE

    ---
    PARAMETER:
    - parent: QWidget | None = None -> Widget PARENT for this CLASS
    (AFTER THAT, THIS CURRENT CLASS WILL BECOME A CHILD OF THE PARENT)
    - f: Qt.WindowType = Qt.WindowType.Widget -> Window-System (Widget)
    ---
    FUNCTIONS:
    - page() -> QFrame : Create 1 HEADER FRAME
    """

    def __init__(
        self,
        parent: QWidget | None = None,
        flags: Qt.WindowType = Qt.WindowType.Widget
    ) -> None:
        super(Header, self).__init__(parent, flags)
        self.setParent(parent)

        template = self.page()
        parent.main_layout.addWidget(
            template, alignment=Qt.AlignmentFlag.AlignTop
        )

    def page(self) -> QFrame:
        """
        Create 1 HEADER TEMPLATE

        ---
        RESULT: HEADER TEMPLATE
        """

        frame = QFrame()
        frame.setObjectName("header")

        layout = QHBoxLayout()
        layout.setSpacing(8)

        text = string_values("header_title")
        title = QLabel(text)

        btn_settings = QPushButton()
        btn_settings.setObjectName("header_btn_settings")
        btn_settings.setIcon(QIcon("app/icons/settings.svg"))
        btn_settings.setFixedWidth(40)

        btn_license = QPushButton()
        btn_license.setObjectName("header_btn_license")
        btn_license.setIcon(QIcon("app/icons/license.svg"))
        btn_license.setFixedWidth(40)

        layout.addWidget(title, alignment=Qt.AlignmentFlag.AlignLeft)
        layout.addWidget(btn_settings, alignment=Qt.AlignmentFlag.AlignRight)
        layout.addWidget(btn_license)

        frame.setLayout(layout)
        return frame

# --------------------------------
