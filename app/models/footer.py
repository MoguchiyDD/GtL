# Developer && Owner: МогучийДД (MoguchiyDD)
# LICENSE: MIT License which is located in the text file LICENSE
#
# Goal: Create a FOOTER TEMPLATE with Ready-Made Working Filling
# Result: Providing a FOOTER TEMPLATE
#
# Past Modification: Install FONTS
# Last Modification: Update TEXT
# Modification Date: 2023.10.30, 02:34 PM
#
# Create Date: 2023.10.24, 05:17 PM


from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from PySide6.QtWidgets import QWidget, QFrame, QVBoxLayout, QLabel

from .values import StringsValues


# ------------ FOOTER ------------

class Footer(QWidget):
    """
    Providing a FOOTER TEMPLATE

    ---
    PARAMETER:
    - parent: QWidget | None = None -> Widget PARENT for this CLASS
    (AFTER THAT, THIS CURRENT CLASS WILL BECOME A CHILD OF THE PARENT)
    - f: Qt.WindowType = Qt.WindowType.Widget -> Window-System (Widget)
    ---
    FUNCTIONS:
    - page() -> QFrame : Create 1 FOOTER FRAME
    """

    def __init__(
        self,
        parent: QWidget | None = None,
        flags: Qt.WindowType = Qt.WindowType.Widget
    ) -> None:
        super(Footer, self).__init__(parent, flags)
        self.setParent(parent)

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

        frame = QFrame()
        frame.setObjectName("footer")

        text = StringsValues().string_values("footer_title")
        title = QLabel(text)
        title.setFont(QFont("Lora"))

        layout = QVBoxLayout()
        layout.addWidget(title, alignment=Qt.AlignmentFlag.AlignCenter)

        frame.setLayout(layout)
        return frame

# --------------------------------
