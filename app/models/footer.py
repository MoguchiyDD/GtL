# Developer && Owner: МогучийДД (MoguchiyDD)
# LICENSE: MIT License which is located in the text file LICENSE
#
# Goal: Create a FOOTER TEMPLATE with Ready-Made Working Filling
# Result: Providing a FOOTER TEMPLATE
#
# Past Modification: Editing The «Footer» CLASS (TEXT + URL)
# Last Modification: Editing The «Footer» CLASS (PATH)
# Modification Date: 2023.12.22, 05:09 PM
#
# Create Date: 2023.10.24, 05:17 PM


from PySide6.QtCore import Qt, Slot
from PySide6.QtGui import QFont
from PySide6.QtWidgets import QWidget, QFrame, QHBoxLayout, QLabel, QPushButton

from .values import StringsValues
from .messages import MessageBox

from webbrowser import open
from os import path


# ------------ FOOTER ------------

class Footer(QWidget):
    """
    Providing a FOOTER TEMPLATE

    ---
    PARAMETERS:
    - parent: QWidget | None = None -> Widget PARENT for this CLASS
    (AFTER THAT, THIS CURRENT CLASS WILL BECOME A CHILD OF THE PARENT)
    - f: Qt.WindowType = Qt.WindowType.Widget -> Window-System (Widget)
    ---
    FUNCTIONS:
    - page() -> QFrame : Create 1 FOOTER FRAME
    ---
    SLOTS:
    - open_url() -> None : Opens The URL in The BROWSER
    """

    def __init__(
        self,
        parent: QWidget | None = None,
        flags: Qt.WindowType = Qt.WindowType.Widget
    ) -> None:
        super(Footer, self).__init__(parent, flags)
        self.setParent(parent)

        self.basedir = parent.basedir
        self.str_val = StringsValues(self.basedir)

        template = self.page()
        parent.main_layout.addWidget(
            template, alignment=Qt.AlignmentFlag.AlignBottom
        )

    def page(self) -> QFrame:
        """
        Create 1 FOOTER TEMPLATE

        ---
        RESULT: FOOTER TEMPLATE
        """

        # STRINGS
        text_zero = self.str_val.string_values("footer_title_zero")
        text_one = self.str_val.string_values("footer_title_one")
        text_two = self.str_val.string_values("footer_title_two")

        frame = QFrame()
        frame.setObjectName("footer")

        title_zero = QLabel(text_zero)
        title_zero.setFont(QFont("Lora"))

        title_one = QPushButton(text_one)
        title_one.setFont(QFont("Lora"))
        title_one.setFixedWidth(172)
        title_one.clicked.connect(self.open_url)

        title_two = QLabel(text_two)
        title_two.setFont(QFont("Lora"))

        layout = QHBoxLayout()
        layout.setSpacing(1)

        layout.addWidget(title_zero, alignment=Qt.AlignmentFlag.AlignRight)
        layout.addWidget(title_one)
        layout.addWidget(title_two, alignment=Qt.AlignmentFlag.AlignLeft)

        frame.setLayout(layout)
        return frame

    @Slot()
    def open_url(self) -> None:
        """
        Opens The URL in The BROWSER
        """

        try:
            text_git = self.str_val.string_values("app_git")
            open(text_git)
        except:
            text_error_msg_url_title = self.str_val.string_values(
                "ru_error_msg_url_title"
            )
            text_error_msg_url_text = self.str_val.string_values(
                "ru_error_msg_url_text"
            )
            MessageBox(  # ERROR
                path.join(self.basedir, "icons", "error.svg"),
                text_error_msg_url_title,
                text_error_msg_url_text,
                self
            )


# --------------------------------
