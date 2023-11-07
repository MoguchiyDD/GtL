# Developer && Owner: МогучийДД (MoguchiyDD)
# LICENSE: MIT License which is located in the text file LICENSE
#
# Goal: Create a CONTENT TEMPLATE with Ready-Made Working Filling
# Result: Providing a CONTENT TEMPLATE
#
# Past Modification: Update TEXT
# Last Modification: Editing The «Content» CLASS (FINISH)
# Modification Date: 2023.11.07, 05:19 PM
#
# Create Date: 2023.10.24, 05:39 PM


from PySide6.QtCore import Qt, Slot
from PySide6.QtGui import QFont
from PySide6.QtWidgets import (
    QWidget,
    QFrame,
    QHBoxLayout,
    QVBoxLayout,
    QLabel,
    QTextEdit,
    QProgressBar,
    QPushButton
)

from .filesystem import FileSystem
from .values import StringsValues
from .messages import MessageBox

from re import split


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
    - box_with_text(attribute_name: str, object_name: str, is_enabled: bool) ->
    QFrame : Responsible for The TEXT BLOCK
    - box_with_progress() -> QFrame : Responsible for The PROGRESS BLOCK
    - box_with_buttons() -> QFrame : Responsible for The BUTTONS BLOCK
    ---
    SLOTS:
    - activate_btn_finish() -> None : Runs PROCESSING TEXT
    """

    def __init__(
        self,
        parent: QWidget | None = None,
        flags: Qt.WindowType = Qt.WindowType.Widget
    ) -> None:
        super(Content, self).__init__(parent, flags)
        self.setParent(parent)
        self.parent = parent

        self.str_val = StringsValues()

        template = self.page()
        self.parent.main_layout.addWidget(
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
        self.textbox_creative_mess = self.box_with_text(
            "ru_content_textbox_creative_mess", "creative_mess", True
        )
        self.textbox_ready_text = self.box_with_text(
            "ru_content_textbox_ready_text", "ready_text", False
        )
        textbox_layout.addWidget(self.textbox_creative_mess)
        textbox_layout.addWidget(self.textbox_ready_text)

        # RIGHT
        self.progressbox = self.box_with_progress()
        buttonsbox = self.box_with_buttons()
        progress_layout.addWidget(
            self.progressbox, alignment=Qt.AlignmentFlag.AlignTop
        )
        progress_layout.addWidget(
            buttonsbox, alignment=Qt.AlignmentFlag.AlignBottom
        )

        main_layout.addLayout(textbox_layout)
        main_layout.addLayout(progress_layout)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(25)

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

        text = self.str_val.string_values(attribute_name)
        title = QLabel(text.upper())
        title.setObjectName("content_title_textbox")
        title.setFont(QFont("Lora"))

        textbox = QTextEdit()
        textbox.setObjectName(object_name)
        textbox.setFont(QFont("Ubuntu"))
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
        frame.setFixedWidth(300)

        layout = QVBoxLayout()

        text_for_title = self.str_val.string_values("ru_content_progress")
        title = QLabel(text_for_title)
        title.setObjectName("content_title_progress")
        title.setFont(QFont("Lora"))

        self.text_for_status = self.str_val.string_values("ru_content_ready")
        status = QLabel(self.text_for_status.upper())
        status.setObjectName("content_status")
        status.setFont(QFont("Ubuntu"))

        self.progress = QProgressBar()
        self.progress.setObjectName("content_progress_bar")
        self.progress.setValue(0)
        self.progress.setFont(QFont("Ubuntu"))

        layout.addWidget(title, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(status)
        layout.addWidget(self.progress)

        frame.setLayout(layout)
        return frame

    def box_with_buttons(self) -> QFrame:
        """
        Responsible for The BUTTONS BLOCK

        ---
        RESULT: The FRAME with LAYOUT inside WIDGETS
        """

        frame = QFrame()
        frame.setObjectName("content_buttons")

        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(15)

        text_for_finish = self.str_val.string_values("ru_content_start_app")
        btn_finish = QPushButton(text_for_finish.upper())
        btn_finish.setObjectName("content_btn_finish")
        btn_finish.clicked.connect(self.activate_btn_finish)

        text_for_copy = self.str_val.string_values(
            "ru_content_copy_two_textbox"
        )
        btn_copy = QPushButton(text_for_copy.upper())
        btn_copy.setObjectName("content_btn_copy")

        layout.addWidget(btn_finish)
        layout.addWidget(btn_copy)

        frame.setLayout(layout)
        return frame

    @Slot()
    def activate_btn_finish(self) -> None:
        """
        Runs PROCESSING TEXT
        """

        def __validation_length_text(length: int) -> bool:
            """
            Checks that The TEXT has been Given

            ---
            PARAMETERS:
            - length: int -> Length of TEXT
            ---
            RESULT: True (length >= 1) || False (length == 0)
            """

            result = False
            if length >= 1:
                result = True

            return result

        _cnt_valid_false = 0

        textbox_creative_mess = self.textbox_creative_mess
        text_create = textbox_creative_mess.findChild(QTextEdit).toPlainText()

        # LENGTH TEXT
        valid_text_create = __validation_length_text(len(text_create))
        if valid_text_create is False:
            _cnt_valid_false += 1

            # ERROR
            text_for_error_msg_valid_len_title = self.str_val.string_values(
                "ru_error_msg_valid_length_title"
            )
            text_for_error_msg_valid_len_text = self.str_val.string_values(
                "ru_error_msg_valid_length_text"
            )
            MessageBox(
                "app/icons/error.svg",
                text_for_error_msg_valid_len_title,
                text_for_error_msg_valid_len_text,
                self
            )

        # SETTINGS FILE
        if (_cnt_valid_false == 0) and (valid_text_create is True):
            filesystem = FileSystem(self.parent.basedir)
            valid_keys = filesystem._valid_true_keys(
                list(self.parent.data_settings_file.keys())
            )
            if valid_keys is False:
                _cnt_valid_false += 1

                filesystem.write_file_settings()
                self.parent.data_settings_file = filesystem.TEMPLATE

                # INFO
                text_for_info_msg_data_title = self.str_val.string_values(
                    "ru_info_msg_data_title"
                )
                text_for_info_msg_data_text = self.str_val.string_values(
                    "ru_info_msg_data_text"
                )
                MessageBox(
                    "app/icons/info.svg",
                    text_for_info_msg_data_title,
                    text_for_info_msg_data_text,
                    self
                )

# ---------------------------------
