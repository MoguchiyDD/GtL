# Developer && Owner: МогучийДД (MoguchiyDD)
# LICENSE: MIT License which is located in the text file LICENSE
#
# Goal: Create a FOOTER TEMPLATE with Ready-Made Working Filling
# Result: Providing a FOOTER TEMPLATE
#
# Past Modification: Update MESSAGE BOX
# Last Modification: Editing The «Footer» CLASS (LOGGER)
# Modification Date: 2024.02.02, 04:46 PM
#
# Create Date: 2023.10.24, 05:17 PM


from PySide6.QtCore import Qt, Slot
from PySide6.QtGui import QFont
from PySide6.QtWidgets import QWidget, QFrame, QHBoxLayout, QLabel, QPushButton

from .filesystem import Logger
from .values import StringsValues
from .messages import activate_message_box

from webbrowser import open


# ------------ FOOTER ------------

class Footer(QWidget):
    """
    Providing a FOOTER TEMPLATE

    ---
    PARAMETERS:
    - language_char: str -> The Characters of LANGUAGE
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
        language_char: str,
        parent: QWidget | None = None,
        flags: Qt.WindowType = Qt.WindowType.Widget
    ) -> None:
        super(Footer, self).__init__(parent, flags)
        self.setParent(parent)

        self.language_char = language_char.lower() + "_"
        self.basedir = parent.basedir
        self.str_val = StringsValues(self.basedir)
        self.logs = Logger()

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
            activate_message_box(  # ERROR
                self.basedir,
                self.language_char + "error_msg_url_title",
                self.language_char + "error_msg_url_text",
                "error.svg",
                self
            )
            self.logs.write_logger(
                self.logs.LoggerLevel.LOGGER_ERROR,
                "URL did not open: " + text_git
            )

# --------------------------------
