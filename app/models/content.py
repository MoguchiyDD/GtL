# Developer && Owner: МогучийДД (MoguchiyDD)
# LICENSE: MIT License which is located in the text file LICENSE
#
# Goal: Create a CONTENT TEMPLATE with Ready-Made Working Filling
# Result: Providing a CONTENT TEMPLATE
#
# Past Modification: Checking CODE The PEP8
# Last Modification: Editing The «TextProcessing» CLASS (DASH)
# Modification Date: 2023.12.21, 01:27 AM
#
# Create Date: 2023.10.24, 05:39 PM


from PySide6.QtCore import (
    Qt,
    Slot,
    QTimer,
    Signal,
    QObject,
    QThread,
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
    - language_char: str -> The Characters of LANGUAGE
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
        language_char: str,
        parent: QWidget | None = None,
        flags: Qt.WindowType = Qt.WindowType.Widget
    ) -> None:
        super(Content, self).__init__(parent, flags)
        self.setParent(parent)
        self.parent = parent

        self.language_char = language_char.lower() + "_"
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
            self.language_char + "content_textbox_creative_mess",
            "creative_mess",
            True
        )
        textbox_ready_text = self.box_with_text(
            self.language_char + "content_textbox_ready_text",
            "ready_text",
            False
        )
        self.text_ready = textbox_ready_text.findChild(QTextEdit)
        textbox_layout.addWidget(self.textbox_creative_mess)
        textbox_layout.addWidget(textbox_ready_text)

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

        text_for_title = self.str_val.string_values(
            self.language_char + "content_progress"
        )
        title = QLabel(text_for_title)
        title.setObjectName("content_title_progress")
        title.setFont(QFont("Lora"))

        text_for_status = self.str_val.string_values(
            self.language_char + "content_ready"
        )
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

        text_for_finish = self.str_val.string_values(
            self.language_char + "content_start_app"
        )
        btn_finish = QPushButton(text_for_finish.upper())
        btn_finish.setObjectName("content_btn_finish")
        btn_finish.clicked.connect(self.activate_btn_finish)

        text_for_copy = self.str_val.string_values(
            self.language_char + "content_copy_two_textbox"
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

    def __finish(self, data: dict[str, any], text: list[str]) -> None:
        """
        Builds BEAUTIFUL TEXT from The 1st TEXTBOX into The 2nd TEXTBOX

        ---
        PARAMETERS:
        - data: dict[str, any] -> The DATA from The RAM
        - text: list[str] -> The LIST 1st TEXTBOX without NEW LINES
        """

        text_processing = TextProcessing(data, text, self)
        text_processing.start()

    @Slot()
    def _update_text_ready(self, text: str) -> None:
        """
        Updates The 2nd BLOCK with TEXT

        ---
        PARAMETERS:
        - text: str -> The Processed TEXT
        """

        self.text_ready.setText(self.text_ready.toPlainText() + text)

    @Slot()
    def _update_status(self, num_line: str) -> None:
        """
        Updates The STATUS of TEXT Processing

        ---
        PARAMETERS:
        - num_line: str -> The LINE NUMBER that The TEXT is Currently being
        Processed
        """

        text_for_progress_line_number = self.str_val.string_values(
            self.language_char + "content_line_number"
        )
        self.status.setText(text_for_progress_line_number + num_line)

    @Slot()
    def _update_percent(self, percent: float) -> None:
        """
        Updates The PROGRESS of TEXT Processing Performed

        ---
        PARAMETERS:
        - percent: float -> The STEP for text Processing
        """

        progress = self.progressbox.findChild(QProgressBar)
        self.current_percent_progress += round(percent, 2)
        if (progress.value() < 100) and (self.current_percent_progress < 100):
            progress.setValue(int(self.current_percent_progress))

    @Slot()
    def _finished_processing(self) -> None:
        """
        The TEXT that comes out when The TEXT has Finished Processing
        """

        # PROGRESS BAR
        text_for_progress_end = self.str_val.string_values(
            self.language_char + "content_end_app"
        )
        progress = self.progressbox.findChild(QProgressBar)
        if progress.value() < 100:
            self.current_percent_progress = 100
            progress.setValue(self.current_percent_progress)

        self.current_percent_progress = 0
        self.status.setText(text_for_progress_end)
        self.text_for_copy = self.text_ready.toPlainText()

        # SUCCESS MESSAGE BOX
        text_for_success_msg_finish_title = self.str_val.string_values(
            self.language_char + "success_msg_finish_title"
        )
        text_for_success_msg_finish_text = self.str_val.string_values(
            self.language_char + "success_msg_finish_text"
        )
        MessageBox(
            "app/icons/success.svg",
            text_for_success_msg_finish_title,
            text_for_success_msg_finish_text,
            self
        )

        # Animation 2nd Textbox
        self.anim_text_ready = AnimationText(self.text_ready)
        self.anim_text_ready.timer_text.start()
        self.anim_text_ready.animation()

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
        self.current_percent_progress = 0

        # PROGRESS BAR
        text_for_progress_start = self.str_val.string_values(
            self.language_char + "content_ready"
        )
        progress = self.progressbox.findChild(QProgressBar)
        progress.setValue(self.current_percent_progress)
        self.status.setText(text_for_progress_start)

        # TEXTBOXES
        text_create = self.textbox_creative_mess.findChild(
            QTextEdit
        ).toPlainText().strip()
        self.text_ready.setText("")

        # LENGTH TEXT
        valid_text_create = __validation_length_text(len(text_create))
        if valid_text_create is False:
            _cnt_valid_false += 1

            # ERROR
            text_for_error_msg_valid_len_title = self.str_val.string_values(
                self.language_char + "error_msg_valid_length_title"
            )
            text_for_error_msg_valid_len_text = self.str_val.string_values(
                self.language_char + "error_msg_valid_length_text"
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
                    self.language_char + "info_msg_data_title"
                )
                text_for_info_msg_data_text = self.str_val.string_values(
                    self.language_char + "info_msg_data_text"
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
            data = self.parent.data_settings_file
            self.__finish(data, text_create_without_new_lines)

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

            msg_icon = "app/icons/success.svg"
            msg_title = self.language_char
            msg_title += "success_msg_copy_second_block_title"
            msg_text = self.language_char
            msg_text += "success_msg_copy_second_block_text"
        except:
            msg_icon = "app/icons/error.svg"
            msg_title = self.language_char
            msg_title += "error_msg_copy_second_block_title"
            msg_text = self.language_char
            msg_text += "error_msg_copy_second_block_text"

        # SUCCESS or ERROR MESSAGE BOX
        text_for_msg_copy_2nd_block_title = self.str_val.string_values(
            msg_title
        )
        text_for_msg_copy_2nd_block_text = self.str_val.string_values(
            msg_text
        )
        MessageBox(
            msg_icon,
            text_for_msg_copy_2nd_block_title,
            text_for_msg_copy_2nd_block_text,
            self
        )

# -----------------------------------------------


# --------------- Text Processing ---------------

class TextProcessingSignals(QObject):
    """
    Connection between a GRAPHICAL SOFTWARE and a THREAD

    ---
    SIGNALS:
    - signal_text_ready : str -> Signal with TEXT from The 2nd TEXT BLOCK
    - signal_status : str -> Signal with STATUS of Current Work Location
    - signal_percent : float -> Signal with PERCENT of Current Work Completed
    - signal_finished -> Signal Indicating The END of Che Current Job
    """

    signal_text_ready = Signal(str)
    signal_status = Signal(str)
    signal_percent = Signal(float)
    signal_finished = Signal()


class TextProcessing(QThread):
    """
    The THREAD Responsible for The TEXT PROCESSING Process

    ---
    PARAMETERS:
    - data: dict[str, any] -> The DATA from The RAM
    - text: list[str] -> The LIST 1st TEXTBOX without NEW LINES
    - parent: QObject | None = None -> Object PARENT for this CLASS
    (AFTER THAT, THIS CURRENT CLASS WILL BECOME A CHILD OF THE PARENT)
    ---
    FUNCTIONS:
    - run() -> None : Starting a THREAD
    """

    def __init__(
        self,
        data: dict[str, any],
        text: list[str],
        parent: QObject | None = None
    ) -> None:
        super().__init__(parent)
        self.text = text
        self.percent = self.__count_percent_progress(self.text)

        # DATA
        self.title = data["title"]
        self.lists = data["list"]
        self.dash = data["dash"]
        self.block = data["block"]

        # DOTS
        self.is_dash = False
        self.is_add_text = False

        # Signals
        self.signals = TextProcessingSignals()
        self.signals.signal_text_ready.connect(parent._update_text_ready)
        self.signals.signal_status.connect(parent._update_status)
        self.signals.signal_percent.connect(parent._update_percent)
        self.signals.signal_finished.connect(parent._finished_processing)

    def __count_percent_progress(self, lines: list[str]) -> float:
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

    def run(self) -> None:
        """
        Starting a THREAD
        """

        def __signal_ready_text(text: str) -> str:
            """
            Send TEXT from a THREAD to a GRAPHICAL SOFTWARE, and SLEEP and
            CLEAN UP TEXT
            ---
            PARAMETERS:
            - text: str -> The TEXT from The 2nd TEXT BLOCK
            ---
            RESULT: ""
            """

            self.signals.signal_text_ready.emit(text)
            sleep(0.1)

            text = ""
            return text

        def _title(_num_line: int, line: str) -> str:
            """
            Line to be TESTED with TITLE

            ---
            PARAMETERS:
            - _num_line: int -> Number of The LINE
            - line: str -> Line to CHECK
            ---
            RESULT: PROCESSED TEXT
            """

            line = line[2:].strip()

            text = ""
            if _num_line == 2:
                text += line
            else:
                text += "\n\n" + line
            text += "\n\n"

            return text

        def _list(
            num: int,
            words: list[str],
            is_list: bool,
            is_dash: bool
        ) -> tuple[str, bool, bool]:
            """
            Line to be TESTED with LIST

            ---
            PARAMETERS:
            - num: int -> The LINE NUMBER that The TEXT is Currently being
            - words: list[str] -> Words to CHECK
            - is_list: bool -> Meeting The LIST (True || False)
            - is_dash: bool ->  (True || False)
            ---
            RESULT: (PROCESSED TEXT, is_list, is_dash)
            """

            top_word = False  # For *
            end_word = False  # For |||
            dash_word = ""  # For -
            text = ""

            # DASH
            if self.dash is True:
                res_dash = _dash(words[-1])
                if res_dash != "":
                    is_dash = True
                    dash_word += res_dash

            if words[0] == "*":  # *
                top_word = True

                if num >= 2:  # Count *
                    text += "\n"

                num += 1

            if words[-1] == "|||":  # End LIST
                end_word = True

            match top_word:
                case True:  # With *
                    text += "\t" + " ".join(words[1:])
                    if dash_word != "":  # Have -
                        text = text[:-1]
                case False:  # Without *
                    text += " ".join(words)
                    if dash_word != "":  # Have -
                        text = text[:-1]

            if is_dash:  # For MERGE TEXT, if have -
                is_dash = False
            else:
                text += " "

            if end_word:  # End LIST
                text = text[:-4] + "\n"
                is_list = False

            result = (num, text, is_list, is_dash)
            return result

        def _dash(word: str) -> str:
            """
            Word to be TESTED with DASH

            ---
            PARAMETERS:
            - word: str -> Word to CHECK
            ---
            RESULT: PROCESSED TEXT
            """

            text = ""
            if word[-1] in ("-", "–", "—", "‒", "﹘"):
                text += word[:-1]

            return text

        def _block(word: str, is_add_text) -> bool:
            """
            Word to be TESTED with PUNCTUATIONS

            ---
            PARAMETERS:
            - word: str -> Word to CHECK
            - is_add_text: bool -> The LINE has been Added (True || False)
            ---
            RESULT: (is_add_text, processed text)
            """

            text = ""
            if word[-1] in self.block:
                is_add_text = True

                text += word
                if text[-1] != line:
                    text += "\n"

            result = (is_add_text, text)
            return result

        is_list = False
        is_list_dash = False
        is_dash = False
        _num_lines = 1
        _num_lists = 1
        dash_word = ""
        ready_text = ""

        for line in self.text:  # Line
            line = line.strip()
            replace_words_dash = line.replace("-\xad", "-")
            words_without_spaces = split(r"\s", replace_words_dash)
            words = list(filter(lambda w: w != "", words_without_spaces))
            current_line = " ".join(words)

            self.signals.signal_status.emit(str(_num_lines))  # NEW STATUS
            self.signals.signal_percent.emit(self.percent)
            _num_lines += 1

            if len(line) == 0:  # SELF-DEFENSE AGAINST PACIFIERS
                continue

            # TITLE
            if (self.title is True) and (line[:3] == "// "):
                res_title = _title(_num_lines, current_line)
                if res_title != "":
                    ready_text += res_title
                    ready_text = __signal_ready_text(ready_text)
                    continue

            # LIST
            if self.lists is True:
                if is_list is True:
                    res_list = _list(_num_lists, words, is_list, is_list_dash)
                    _num_lists = res_list[0]
                    text = res_list[1]
                    is_list = res_list[2]
                    is_list_dash = res_list[3]
                    if text != "":
                        ready_text += text
                        ready_text = __signal_ready_text(ready_text)
                        continue
                elif words[-1][-1] == ":":
                    ready_text += current_line + "\n"
                    is_list = True
                    _num_lists = 1
                if is_list is True:
                    ready_text = __signal_ready_text(ready_text)
                    continue

            # DASH
            if self.dash is True:
                res_dash = _dash(words[-1])
                if res_dash != "":
                    dash_word += res_dash
                    is_dash = True

            ready_text += " ".join(words[:-1])
            if dash_word != "":
                ready_text += " " + dash_word
                dash_word = ""

            ready_text = __signal_ready_text(ready_text)

        self.signals.signal_finished.emit()

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
