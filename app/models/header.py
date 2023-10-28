# Developer && Owner: МогучийДД (MoguchiyDD)
# LICENSE: MIT License which is located in the text file LICENSE
#
# Goal: Create a HEADER TEMPLATE with Ready-Made Working Filling
# Result: Providing a HEADER TEMPLATE
#
# Past Modification: Adding The «HeaderModal» CLASS (LICENSE)
# Last Modification: Checking CODE The PEP8
# Modification Date: 2023.10.29, 01:56 AM
#
# Create Date: 2023.10.23, 06:45 PM


from PySide6.QtCore import Qt, Slot
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import (
    QWidget,
    QFrame,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton
)

from .values import string_values


# --------------- HEADER ---------------

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
    ---
    SLOTS:
    - activate_btn_license() -> None : Opens 1 MODAL WINDOW for The LICENSE
    """

    def __init__(
        self,
        parent: QWidget | None = None,
        flags: Qt.WindowType = Qt.WindowType.Widget
    ) -> None:
        super(Header, self).__init__(parent, flags)
        self.setParent(parent)
        self.parent = parent

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
        btn_license.clicked.connect(self.activate_btn_license)

        layout.addWidget(title, alignment=Qt.AlignmentFlag.AlignLeft)
        layout.addWidget(btn_settings, alignment=Qt.AlignmentFlag.AlignRight)
        layout.addWidget(btn_license)

        frame.setLayout(layout)
        return frame

    @Slot()
    def activate_btn_license(self) -> None:
        """
        Opens 1 MODAL WINDOW for The LICENSE
        """

        HeaderModal("license", self)

# --------------------------------------


# ------------ MODAL WINDOW ------------

class HeaderModal(QWidget):
    """
    Opens 1 MODAL WINDOW

    ---
    PARAMETERS:
    - mode: str -> Mode «settings» or «license»
    - parent: QWidget | None = None -> Widget PARENT for this CLASS
    (AFTER THAT, THIS CURRENT CLASS WILL BECOME A CHILD OF THE PARENT)
    - f: Qt.WindowType = Qt.WindowType.Widget -> Window-System (Widget)
    ---
    FUNCTIONS:
    - page_license() -> QFrame : Create 1 LICENSE TEMPLATE
    """

    def __init__(
        self,
        mode: str,
        parent: QWidget | None = None,
        f: Qt.WindowType = Qt.WindowType.Widget
    ) -> None:
        super(HeaderModal, self).__init__(parent, f)
        self.setParent(parent)

        self.setWindowFlags(Qt.WindowType.Dialog)
        self.setStyleSheet("background-color: #404040;")

        template = QFrame()
        match(mode):
            case "settings":
                pass
            case "license":
                template = self.page_license()

        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(template, alignment=Qt.AlignmentFlag.AlignCenter)

        self.setLayout(layout)
        self.show()

    def page_license(self) -> QFrame:
        """
        Create 1 LICENSE TEMPLATE

        ---
        RESULT: LICENSE TEMPLATE
        """

        # STRINGS
        text_for_title = string_values("ru_license_part_one")
        text_for_copyright = string_values("license_part_zero")
        text_for_zero = string_values("ru_license_part_two")
        text_for_one = string_values("ru_license_part_three")
        text_for_two = string_values("ru_license_part_four")

        # MODAL WINDOW
        self.setWindowTitle(text_for_title)
        self.setFixedSize(675, 500)

        frame = QFrame()
        frame.setObjectName("header_modal_license")

        layout = QVBoxLayout()

        # TITLE
        title_license = QLabel(text_for_title)
        title_license.setObjectName("license_title")

        # COPYRIGHT
        copyright_license = QLabel(text_for_copyright)
        copyright_license.setObjectName("license_copyright")

        # TEXT #0
        text_zero_license = QLabel(text_for_zero)
        text_zero_license.setObjectName("license_text_zero")
        text_zero_license.setWordWrap(True)

        # TEXT #1
        text_one_license = QLabel(text_for_one)
        text_one_license.setObjectName("license_text_one")
        text_one_license.setWordWrap(True)

        # TEXT #2
        text_two_license = QLabel(text_for_two)
        text_two_license.setObjectName("license_text_two")
        text_two_license.setWordWrap(True)

        layout.addWidget(title_license, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(copyright_license)
        layout.addWidget(text_zero_license)
        layout.addWidget(text_one_license)
        layout.addWidget(text_two_license)

        frame.setLayout(layout)
        return frame

# --------------------------------------
