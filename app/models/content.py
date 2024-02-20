# Developer && Owner: МогучийДД (MoguchiyDD)
# LICENSE: MIT License which is located in the text file LICENSE
#
# Goal: Create a CONTENT TEMPLATE with Ready-Made Working Filling
# Result: Providing a CONTENT TEMPLATE
#
# Past Modification: Editing The «Content» CLASS (RINGTONE)
# Last Modification: Editing The «Content» CLASS (RINGTONE for OS Windows)
# Modification Date: 2024.02.19, 05:29 PM
#
# Create Date: 2023.10.24, 05:39 PM


from PySide6.QtCore import Qt, Slot, Signal, QObject
from PySide6.QtGui import QGuiApplication, QFont, QIcon
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

from .filesystem import FileSystem, Logger
from .values import StringsValues
from .messages import activate_message_box
from .animations import AnimationTextEdit

from threading import Thread
from mutagen import MutagenError
from mutagen.wave import WAVE
from playsound import PlaysoundException

from re import split
from time import sleep

from sys import platform
from os import name, path

if (platform == "linux") or (name == "posix"):
    from playsound import playsound, PlaysoundException
elif (platform == "win32") or (name == "nt"):
    from winsound import PlaySound, SND_ASYNC


# ---------------- CONTENT ----------------

class Content(QWidget):
    """
    Providing a CONTENT TEMPLATE

    ---
    PARAMETERS:
    - language_char: str -> The Characters of LANGUAGE
    - header: QWidget -> Link of HEADER TEMPLATE
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
        header: QWidget,
        parent: QWidget | None = None,
        flags: Qt.WindowType = Qt.WindowType.Widget
    ) -> None:
        super(Content, self).__init__(parent, flags)
        self.setParent(parent)
        self.parent = parent
        self.header = header

        self.language_char = language_char.lower() + "_"
        self.basedir = self.parent.basedir
        self.str_val = StringsValues(self.basedir)
        self.logs = Logger(self.basedir)
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
        self.btn_finish = QPushButton(text_for_finish.upper())
        self.btn_finish.setObjectName("content_btn_finish")
        self.btn_finish.clicked.connect(self.activate_btn_finish)

        text_for_copy = self.str_val.string_values(
            self.language_char + "content_copy_two_textbox"
        )
        self.btn_copy = QPushButton(text_for_copy.upper())
        self.btn_copy.setObjectName("content_btn_copy")
        self.btn_copy.clicked.connect(
            lambda clicked: self.activate_btn_copy(self.text_for_copy)
        )

        layout.addWidget(self.btn_finish)
        layout.addWidget(self.btn_copy)

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

        self.anim_text_ready = None
        self.btn_finish.setEnabled(False)
        self.btn_copy.setEnabled(False)
        self.header._Header__settings.hide()
        self.header.btn_settings.setEnabled(False)
        self.header.btn_settings.setIcon(
            QIcon(path.join(self.basedir, "icons", "d_settings.svg"))
        )

        text_processing = TextProcessing(data, text, self)
        self.thread_text_processing = Thread(
            target=text_processing.run,
            name="THREAD_TEXT_PROCESSING",
            args=(),
            daemon=True
        )
        self.thread_text_processing.start()

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

        def set_notification(notification: bool) -> None:
            """
            Displays 1 MESSAGE BOX or Starts 1 RINGTONE

            ---
            PARAMETERS:
            - notification: bool -> The DATA from RAM with SETTINGS FILE from
            «notification» KEY
            """

            if notification is False:  # MESSAGE BOX
                activate_message_box(  # SUCCESS
                    self.basedir,
                    self.language_char + "success_msg_finish_title",
                    self.language_char + "success_msg_finish_text",
                    "success.svg",
                    self
                )
            else:  # RINGTONE
                ringtone = RingtoneThread(self)
                self.thread_text_processing = Thread(
                    target=ringtone.run,
                    name="THREAD_RINGTONE",
                    args=(),
                    daemon=True
                )
                self.thread_text_processing.start()

            self.logs.write_logger(
                self.logs.LoggerLevel.LOGGER_SUCCESS,
                "Successfully processed text"
            )

        def set_animation(animation: bool) -> None:
            """
            Enables or disables The ANIMATION of The 2nd TEXT BLOCK

            ---
            PARAMETERS:
            - animation: bool -> The DATA from RAM with SETTINGS FILE from
            «animation» KEY
            """

            self.anim_text_ready = AnimationTextEdit(self.text_ready)
            if animation is False:  # Turn On
                if len(self.text_ready.toPlainText()) >= 1:
                    self.anim_text_ready.timer_text.start()
            else:  # Turn Off
                self.anim_text_ready.timer_text.stop()
                self.anim_text_ready.timer_text.timeout.disconnect()
                self.anim_text_ready.animations_group.stop()

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

        data = self.parent.data_settings_file  # DATA

        # Notification
        notification = data["notification"]
        set_notification(notification)

        # Animation 2nd Textbox
        animation = data["animation"]
        set_animation(animation)

        self.btn_finish.setEnabled(True)
        self.btn_copy.setEnabled(True)
        self.header.btn_settings.setEnabled(True)
        self.header.btn_settings.setIcon(
            QIcon(path.join(self.basedir, "icons", "settings.svg"))
        )

    @Slot()
    def activate_btn_finish(self) -> None:
        """
        Runs PROCESSING TEXT
        """

        def valid_length_text(len_errors: int, text: str) -> tuple[bool, int]:
            """
            Checks that The TEXT has been Given

            ---
            PARAMETERS:
            - len_errors: int -> The Number of The ERRORS
            - text: str -> The TEXT from The 1st TEXTBOX
            ---
            RESULT: (True (LENGTH >= 1) || False (LENGTH <= 0),
            The Number of The ERRORS)
            """

            result = True

            len_text = len(text)
            if len_text <= 0:  # ERROR
                len_errors += 1
                result = False

                activate_message_box(
                    self.basedir,
                    self.language_char + "error_msg_valid_length_title",
                    self.language_char + "error_msg_valid_length_text",
                    "error.svg",
                    self
                )
                self.logs.write_logger(
                    self.logs.LoggerLevel.LOGGER_ERROR,
                    "Launched the program without text"
                )

            return (result, len_errors)

        def data_from_settings(
            len_errors: int, valid_text: bool
        ) -> tuple[bool, int]:
            """
            Checks ALL KEYS for their Existence in The FILE SYSTEM

            ---
            PARAMETERS:
            - len_errors: int -> The Number of The ERRORS
            - valid_text: bool -> Reply from The «valid_length_text» FUNCTION
            ---
            RESULT: (True (OK with KEYS from FILE SYSTEM) ||
            False (not OK with KEYS  from FILE SYSTEM),
            The Number of The ERRORS)
            """

            valid_keys = False
            if (len_errors == 0) and (valid_text is True):
                filesystem = FileSystem(self.parent.basedir)
                valid_keys = filesystem._valid_true_keys(
                    list(self.parent.data_settings_file.keys())
                )
                if valid_keys is False:  # ERROR
                    len_errors += 1

                    filesystem.write_file_settings()
                    self.parent.data_settings_file = filesystem.TEMPLATE
                    filesystem.write_file_language(
                        self.parent.data_settings_file["language"]
                    )

                    activate_message_box(  # INFO
                        self.basedir,
                        self.language_char + "info_msg_data_title",
                        self.language_char + "info_msg_data_text",
                        "info.svg",
                        self
                    )
                    self.logs.write_logger(
                        self.logs.LoggerLevel.LOGGER_INFO,
                        "Fixing a damaged program settings file"
                    )

            return (valid_keys, len_errors)

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

        valid_text_create = valid_length_text(  # LENGTH TEXT
            _cnt_valid_false, text_create
        )
        valid_keys = data_from_settings(  # SETTINGS FILE
            valid_text_create[1], valid_text_create[0]
        )
        _cnt_valid_false = valid_keys[1]

        # FINISH
        if (_cnt_valid_false == 0) and (valid_keys[0] is True):
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

            logger = "success"
            msg_icon = "success.svg"
            msg_title = "success_msg_copy_second_block_title"
            msg_text = "success_msg_copy_second_block_text"
        except:
            logger = "error"
            msg_icon = "error.svg"
            msg_title = "error_msg_copy_second_block_title"
            msg_text = "error_msg_copy_second_block_text"

        activate_message_box(  # SUCCESS || ERROR
            self.basedir,
            self.language_char + msg_title,
            self.language_char + msg_text,
            msg_icon,
            self
        )

        match logger:
            case "success":
                self.logs.write_logger(
                    self.logs.LoggerLevel.LOGGER_SUCCESS,
                    "Successfully copied text from the 2nd text block"
                )
            case "error":
                self.logs.write_logger(
                    self.logs.LoggerLevel.LOGGER_ERROR,
                    "Failed to copy text from the 2nd text block"
                )

    @Slot()
    def activate_ringtone(self) -> None:
        """
        Launches 1 RINGTONE if Found, Otherwise Opens 1 MESSAGE BOX
        with an ERROR for The USER
        """

        url = path.join(self.basedir, "ringtone", "success.wav")
        try:
            if int(WAVE(url).info.length) == 1:
                if (platform == "linux") or (name == "posix"):
                    playsound(url, False)
                elif (platform == "win32") or (name == "nt"):
                    PlaySound(url, SND_ASYNC)
            else:  # ERROR
                activate_message_box(
                    self.basedir,
                    self.language_char + "error_msg_ringtone_time_title",
                    self.language_char + "error_msg_ringtone_time_text",
                    "ringtone.svg",
                    self
                )
                self.logs.write_logger(
                    self.logs.LoggerLevel.LOGGER_ERROR,
                    "New ringtone plays for more than 1 second"
                )
        except PlaysoundException and MutagenError:
            activate_message_box(
                self.basedir,
                self.language_char + "error_msg_ringtone_title",
                self.language_char + "error_msg_ringtone_text",
                "ringtone.svg",
                self
            )
            self.logs.write_logger(
                self.logs.LoggerLevel.LOGGER_ERROR,
                "Didn't find a ringtone on the way"
            )

# -----------------------------------------


# --------------- Ringtone ----------------

class RingtoneThread(QObject):
    """
    Responsible for The RINGTONE through The THREAM
    """

    signal_play = Signal()

    def __init__(self, parent: QWidget) -> None:
        super().__init__(parent)
        self.signal_play.connect(parent.activate_ringtone)

    def run(self) -> None:
        """
        Sends 1 SIGNAL to Start 1 RINGTONE
        """

        self.signal_play.emit()

# -----------------------------------------


# ------------ Text Processing ------------

class TextProcessing(QObject):
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

    signal_text_ready = Signal(str)
    signal_status = Signal(str)
    signal_percent = Signal(float)
    signal_finished = Signal()

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
        self.signal_text_ready.connect(parent._update_text_ready)
        self.signal_status.connect(parent._update_status)
        self.signal_percent.connect(parent._update_percent)
        self.signal_finished.connect(parent._finished_processing)

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

            self.signal_text_ready.emit(text)
            sleep(0.2)

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

        def _block(word: str) -> bool:
            """
            Word to be TESTED with FUNCTUATIONS

            ---
            PARAMETERS:
            - word: str -> Word to CHECK
            ---
            RESULT: WORD with NEWLINE
            """

            text = ""
            if word[-1] in self.block:
                text += word + "\n"

            return text

        is_list = False
        is_list_dash = False
        is_dash = False
        _num_lines = 1
        _num_lists = 1
        ready_text = ""

        for line in self.text:  # Line
            line = line.strip()
            replace_words_dash = line.replace("-\xad", "-")
            words_without_spaces = split(r"\s", replace_words_dash)
            words = list(filter(lambda w: w != "", words_without_spaces))
            current_line = " ".join(words)

            self.signal_status.emit(str(_num_lines))  # NEW STATUS
            self.signal_percent.emit(self.percent)
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
                dash_word = _dash(words[-1])
                if dash_word != "":
                    is_dash = True

            # BLOCK
            if is_dash is False:
                block_word = _block(words[-1])

            ready_text += " ".join(words[:-1]) + " "
            match(is_dash):
                case True:
                    ready_text += dash_word
                    is_dash = False
                case False:
                    if block_word != "":
                        ready_text += block_word
                    else:
                        ready_text += words[-1] + " "

            ready_text = __signal_ready_text(ready_text)

        self.signal_finished.emit()

# -----------------------------------------
