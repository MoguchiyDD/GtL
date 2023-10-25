# Developer && Owner: МогучийДД (MoguchiyDD)
# LICENSE: MIT License which is located in the text file LICENSE
#
# Goal: Create a CONTENT TEMPLATE with Ready-Made Working Filling
# Result: Providing a CONTENT TEMPLATE
#
# Past Modification: Checking CODE The PEP8
# Last Modification: Editing The «Content» CLASS (PROGRESS BLOCK)
# Modification Date: 2023.10.25, 03:19 PM
#
# Create Date: 2023.10.24, 05:39 PM


from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QWidget,
    QFrame,
    QHBoxLayout,
    QVBoxLayout,
    QLabel,
    QTextEdit,
    QProgressBar
)

from .values import string_values


# ------------ CONTENT ------------

class Content(QWidget):
    """
    Providing a CONTENT TEMPLATE

    ---
    PARAMETER:
    - parent: QWidget | None = None -> Widget PARENT for this CLASS
    (AFTER THAT, THIS CURRENT CLASS WILL BECOME A CHILD OF THE PARENT)
    - f: Qt.WindowType = Qt.WindowType.Widget -> Window-System (Widget)
    ---
    FUNCTIONS:
    - page() -> QFrame : Create 1 CONTENT FRAME
    """

    def __init__(
        self,
        parent: QWidget | None = None,
        flags: Qt.WindowType = Qt.WindowType.Widget
    ) -> None:
        super(Content, self).__init__(parent, flags)
        self.setParent(parent)

        template = self.page()
        parent.main_layout.addWidget(
            template, alignment=Qt.AlignmentFlag.AlignBottom
        )

    def page(self) -> QFrame:
        """
        Create 1 CONTENT TEMPLATE

        ---
        RESULT: CONTENT TEMPLATE
        """

        frame = QFrame()
        frame.setObjectName("content")

        main_layout = QHBoxLayout()
        textbox_layout = QVBoxLayout()  # LEFT
        progress_layout = QVBoxLayout()  # RIGHT

        # LEFT
        textbox_creative_mess = self.box_with_text(
            "ru_content_textbox_creative_mess", "creative_mess", True
        )
        textbox_ready_text = self.box_with_text(
            "ru_content_textbox_ready_text", "ready_text", False
        )
        textbox_layout.addWidget(textbox_creative_mess)
        textbox_layout.addWidget(textbox_ready_text)

        # RIGHT
        progressbox = self.box_with_progress()
        progress_layout.addWidget(
            progressbox, alignment=Qt.AlignmentFlag.AlignTop
        )

        main_layout.addLayout(textbox_layout)
        main_layout.addLayout(progress_layout)

        frame.setLayout(main_layout)
        return frame

    def box_with_text(
        self,
        attribute_name: str,
        object_name: str,
        is_enabled: bool
    ) -> QFrame:
        """
        Responsible for The TEXT BLOCK

        ---
        PARAMETERS:
        - attribute_name: str -> ATTRIBUTE with The NAME (for TEXTBOX)
        - object_name: str -> NAME for OBJECT
        - is_enabled: bool -> OPEN or CLOSE Textbox
        ---
        RESULT: The FRAME with LAYOUT inside WIDGETS
        """

        object_name = "content_textbox_" + object_name

        frame = QFrame()
        frame.setObjectName("content_textbox")

        layout = QVBoxLayout()

        text = string_values(attribute_name)
        title = QLabel(text)
        title.setObjectName("content_title_textbox")

        textbox = QTextEdit()
        textbox.setObjectName(object_name)
        if is_enabled is False:
            textbox.setEnabled(is_enabled)

        layout.addWidget(title)
        layout.addWidget(textbox)

        frame.setLayout(layout)
        return frame

    def box_with_progress(self) -> QFrame:
        """
        Responsible for The PROGRESS BLOCK

        ---
        RESULT: The FRAME with LAYOUT inside WIDGETS
        """

        frame = QFrame()
        frame.setObjectName("content_progress")

        layout = QVBoxLayout()

        text_for_title = string_values("ru_content_progress")
        title = QLabel(text_for_title)
        title.setObjectName("content_title_progress")

        self.text_for_status = string_values("ru_content_ready")
        status = QLabel(self.text_for_status)
        status.setObjectName("content_status")

        self.progress = QProgressBar()
        self.progress.setObjectName("content_progress_bar")
        self.progress.setValue(0)

        layout.addWidget(title, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(status)
        layout.addWidget(self.progress)

        frame.setLayout(layout)
        return frame

# ---------------------------------
