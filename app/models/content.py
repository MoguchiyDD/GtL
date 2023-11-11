# Developer && Owner: МогучийДД (MoguchiyDD)
# LICENSE: MIT License which is located in the text file LICENSE
#
# Goal: Create a CONTENT TEMPLATE with Ready-Made Working Filling
# Result: Providing a CONTENT TEMPLATE
#
# Past Modification: Editing The «Content» CLASS («__finish» : TITLE)
# Last Modification: Editing The «Content» CLASS («__finish» : LIST)
# Modification Date: 2023.11.11, 08:32 PM
#
# Create Date: 2023.10.24, 05:39 PM


from PySide6.QtCore import (
    Qt,
    Slot,
    QTimer,
    QPropertyAnimation,
    QSequentialAnimationGroup
)
from PySide6.QtGui import QGuiApplication, QTextCursor, QFont
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
from time import sleep


# ------------------- CONTENT -------------------

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
    - activate_btn_copy(text: str) -> None : Copies The 2nd BLOCK of TEXT to
    The CLIPBOARD
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
        self.current_percent_progress = 0
        self.text_for_copy = ""

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

        text_for_status = self.str_val.string_values("ru_content_ready")
        self.status = QLabel(text_for_status.upper())
        self.status.setObjectName("content_status")
        self.status.setFont(QFont("Ubuntu"))
        self.status.setWordWrap(True)

        self.progress = QProgressBar()
        self.progress.setObjectName("content_progress_bar")
        self.progress.setValue(0)
        self.progress.setFont(QFont("Ubuntu"))

        layout.addWidget(title, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.status)
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
        btn_copy.clicked.connect(
            lambda clicked: self.activate_btn_copy(self.text_for_copy)
        )

        layout.addWidget(btn_finish)
        layout.addWidget(btn_copy)

        frame.setLayout(layout)
        return frame

    def __finish(
        self,
        data: dict[str, any],
        percent: float,
        status: str,
        text: list[str],
        text_ready: QTextEdit,
        progress: QProgressBar
    ) -> None:
        """
        Builds BEAUTIFUL TEXT from The 1st TEXTBOX into The 2nd TEXTBOX

        ---
        PARAMETERS:
        - data: dict[str, any] -> The DATA from The RAM
        - percent: float -> The Percentage of The Number of LINES
        - status: str -> The STATUS of The PROGRESS
        - text: list[str] -> The LIST 1st TEXTBOX without NEW LINES
        - text_ready: QTextEdit -> The TEXT 1nd TEXTBOX
        - progress: QProgressBar -> The PROGRESS
        """

        def _title(_num_line: int, line: str, is_title: bool) -> bool:
            """
            Line to be TESTED with TITLE

            ---
            PARAMETERS:
            - _num_line: int -> Number of The LINE
            - line: str -> Line to CHECK
            - is_title: bool -> Meeting The TITLE (True || False)
            ---
            RESULT: is_title
            """

            if line[:2] == "//":
                is_title = True

                line = line[2:].strip()
                if _num_line == 2:
                    text_ready.setText(text_ready.toPlainText() + line)
                else:
                    text_ready.setText(
                        text_ready.toPlainText() + "\n\n" + line
                    )

                text_ready.setText(text_ready.toPlainText() + "\n\n")

            return is_title

        def _list(
            line: list[str], is_list: bool, is_add_text: bool
        ) -> tuple[bool]:
            """
            Line to be TESTED with LIST

            ---
            PARAMETERS:
            - line: list[str] -> Line to CHECK
            - is_list: bool -> Meeting The LIST (True || False)
            - is_add_text: bool -> The LINE has been Added (True || False)
            ---
            RESULT: (is_list, is_add_text)
            """

            if line[-1][-1] == ";":
                is_list = True
                is_add_text = True
                text_ready.setText(
                    text_ready.toPlainText() + "\t" + " ".join(line) + "\n"
                )
            else:
                is_list = False
                is_add_text = False

            result = (is_list, is_add_text)
            return result

        def _dash(word: str, is_dash: bool, is_add_text: bool) -> tuple[bool]:
            """
            Word to be TESTED with DASH

            ---
            PARAMETERS:
            - word: str -> Word to CHECK
            - is_dash: bool -> Meeting The DASH (True || False)
            - is_add_text: bool -> The LINE has been Added (True || False)
            ---
            RESULT: (is_dash, is_add_text)
            """

            if word[-1] in ("-", "–", "—", "‒", "﹘"):
                is_dash = True
                is_add_text = True
                text_ready.setText(text_ready.toPlainText() + word[:-1])

            result = (is_dash, is_add_text)
            return result

        def _block(word: str, is_add_text) -> bool:
            """
            Word to be TESTED with PUNCTUATIONS

            ---
            PARAMETERS:
            - word: str -> Word to CHECK
            - is_add_text: bool -> The LINE has been Added (True || False)
            ---
            RESULT: is_add_text
            """

            if word[-1] in block:
                is_add_text = True
                text_ready.setText(text_ready.toPlainText() + word)
                if text[-1] != line:
                    text_ready.setText(text_ready.toPlainText() + "\n")

            return is_add_text

        # DATA
        title = data["title"]
        lists = data["list"]
        dash = data["dash"]
        block = data["block"]

        # DOTS
        is_title = False
        is_list = False
        is_dash = False
        is_add_text = False

        _num_lines = 1
        for line in text:  # Line
            self.status.setText(status + str(_num_lines))
            _num_lines += 1

            if len(line) == 0:
                continue

            if title is True:  # TITLE
                is_title = _title(_num_lines, line, is_title)
                if is_title is True:
                    is_title = False
                    continue

            words = split(r"\s", line)
            if is_list is True:  # LIST
                def_list = _list(words, is_list, is_add_text)
                is_list = def_list[0]
                is_add_text = def_list[1]
                if is_list is True:
                    continue

            for word in words[:-1]:  # Word
                text_ready.setText(text_ready.toPlainText() + word + " ")

            if dash is True:  # DASH
                def_dash = _dash(words[-1], is_dash, is_add_text)
                is_dash = def_dash[0]
                is_add_text = def_dash[1]

            if is_dash is False:  # BLOCK && LIST
                if (lists is True) and (words[-1][-1] == ":"):  # LIST
                    is_list = True
                    is_add_text = True
                    text_ready.setText(
                        text_ready.toPlainText() + words[-1] + "\n"
                    )
                if (lists is False) or (is_list is False):  # BLOCK
                    is_add_text = _block(words[-1], is_add_text)
            else:
                is_dash = False

            if is_add_text is False:  # OTHER WORDS
                text_ready.setText(text_ready.toPlainText() + words[-1] + " ")
            else:
                is_add_text = False

            if progress.value() < 100:  # PROGRESS
                self.current_percent_progress += percent
                progress.setValue(int(self.current_percent_progress))

            sleep(0.1)

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

        def __count_percent_progress(lines: list[str]) -> float:
            """
            Calculates The Percentage of 1 LINE from a List of LINES

            ---
            PARAMETERS:
            - lines: list[str] -> The List of LINES with WORDS
            ---
            RESULTS: Percentage of The Number of LINES
            """

            len_lines = len(lines)
            percent = 100 / len_lines
            return percent

        _cnt_valid_false = 0
        self.current_percent_progress = 0

        # STRINGS for PROGRESS
        text_for_progress_start = self.str_val.string_values(
            "ru_content_ready"
        )
        text_for_progress_line_number = self.str_val.string_values(
            "ru_content_line_number"
        )
        text_for_progress_end = self.str_val.string_values(
            "ru_content_end_app"
        )

        # PROGRESS BAR
        progress = self.progressbox.findChild(QProgressBar)
        progress.setValue(0)
        self.status.setText(text_for_progress_start)

        # TEXTBOXES
        text_create = self.textbox_creative_mess.findChild(
            QTextEdit
        ).toPlainText().strip()
        text_ready = self.textbox_ready_text.findChild(QTextEdit)
        text_ready.setText("")

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

        # FINISH
        if (_cnt_valid_false == 0) and (valid_keys is True):
            text_create_without_new_lines = text_create.split("\n")
            percent_progress = __count_percent_progress(
                text_create_without_new_lines
            )
            data = self.parent.data_settings_file

            self.__finish(
                data,
                percent_progress,
                text_for_progress_line_number,
                text_create_without_new_lines,
                text_ready,
                progress
            )

            if progress.value() < 100:  # PROGRESS
                progress.setValue(100)

            self.status.setText(text_for_progress_end)
            self.text_for_copy = text_ready.toPlainText()

            # SUCCESS MESSAGE BOX
            text_for_success_msg_finish_title = self.str_val.string_values(
                "ru_success_msg_finish_title"
            )
            text_for_success_msg_finish_text = self.str_val.string_values(
                "ru_success_msg_finish_text"
            )
            MessageBox(
                "app/icons/success.svg",
                text_for_success_msg_finish_title,
                text_for_success_msg_finish_text,
                self
            )

            # Animation 2nd Textbox
            self.anim_text_ready = AnimationText(text_ready)
            self.anim_text_ready.timer_text.start()
            self.anim_text_ready.animation()

    @Slot()
    def activate_btn_copy(self, text: str) -> None:
        """
        Copies The 2nd BLOCK of TEXT to The CLIPBOARD

        ---
        PARAMETERS:
        - text: str -> The 2nd BLOCK of TEXT
        """

        try:
            clipboard = QGuiApplication.clipboard()
            clipboard.setText(text, clipboard.Mode.Clipboard)

            mdg_icon = "app/icons/success.svg"
            mdg_title = "ru_success_msg_copy_second_block_title"
            mdg_text = "ru_success_msg_copy_second_block_text"
        except:
            mdg_icon = "app/icons/error.svg"
            mdg_title = "ru_error_msg_copy_second_block_title"
            mdg_text = "ru_error_msg_copy_second_block_text"

        # SUCCESS or ERROR MESSAGE BOX
        text_for_msg_copy_2nd_block_title = self.str_val.string_values(
            mdg_title
        )
        text_for_msg_copy_2nd_block_text = self.str_val.string_values(
            mdg_text
        )
        MessageBox(
            mdg_icon,
            text_for_msg_copy_2nd_block_title,
            text_for_msg_copy_2nd_block_text,
            self
        )

# -----------------------------------------------


# ------------ ANIMATION 2ND TEXTBOX ------------

class AnimationText(QWidget):
    """
    Responsible for The ANIMATION of TEXT in 1 TEXTBOX

    ---
    PARAMETERS:
    - textbox: QTextEdit -> The TEXTBOX
    ---
    FUNCTIONS:
    - animation(self) -> None : RUNS to an ANIMATION
    """

    def __init__(self, textbox: QTextEdit) -> None:
        super(AnimationText, self).__init__()

        self.textbox = textbox
        self.doc_textbox = textbox.document()

        # START ANIMATION
        self.s_anim_text = QPropertyAnimation(
            self.textbox, b"move_start_to_end", self
        )
        self.s_anim_text.valueChanged.connect(self.__move)
        self.s_anim_text = self.__start_animation()

        # END ANIMATION
        self.e_anim_text = QPropertyAnimation(
            self.textbox, b"move_end_to_start", self
        )
        self.e_anim_text.valueChanged.connect(self.__move)
        self.e_anim_text = self.__end_animation()

        # TOTAL ANIMATIONS
        self.animations_group = QSequentialAnimationGroup()
        self.animations_group.addAnimation(self.s_anim_text)
        self.animations_group.addAnimation(self.e_anim_text)

        # DURATION : START && END
        durations = self.s_duration_anim_text + self.e_duration_anim_text

        self.timer_text = QTimer()
        self.timer_text.setInterval(durations)
        self.timer_text.timeout.connect(self.animation)

    def __start_animation(self) -> None:
        """
        An ANIMATION that goes from TEXT POSITION 0 to The LAST POSITION
        """

        self.s_anim_text.stop()

        self.s_duration_anim_text = self.doc_textbox.blockCount() * 1000 / 2

        self.s_anim_text.setStartValue(0)
        self.s_anim_text.setEndValue(self.doc_textbox.blockCount())
        self.s_anim_text.setDuration(self.s_duration_anim_text)

        return self.s_anim_text

    def __end_animation(self) -> None:
        """
        An ANIMATION that goes from TEXT POSITION The LAST POSITION to 0
        """

        self.e_anim_text.stop()

        self.e_duration_anim_text = self.doc_textbox.blockCount() * 10 / 2

        self.e_anim_text.setStartValue(self.doc_textbox.blockCount())
        self.e_anim_text.setEndValue(0)
        self.e_anim_text.setDuration(self.e_duration_anim_text)

        return self.e_anim_text

    def animation(self) -> None:
        """
        RUNS to an ANIMATION
        """

        self.animations_group.stop()
        self.animations_group.start()

    @Slot()
    def __move(self, pos: int) -> None:
        """
        Moves TEXT According to POSITION NUMBER

        ---
        PARAMETERS:
        - pos: int -> The POSITION NUMBER
        """

        cursor = QTextCursor(self.doc_textbox.findBlockByLineNumber(pos))
        self.textbox.setTextCursor(cursor)

# -----------------------------------------------
