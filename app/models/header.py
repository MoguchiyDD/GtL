# Developer && Owner: МогучийДД (MoguchiyDD)
# LICENSE: MIT License which is located in the text file LICENSE
#
# Goal: Create a HEADER TEMPLATE with Ready-Made Working Filling
# Result: Providing a HEADER TEMPLATE
#
# Past Modification: Editing The «Header» and «HeaderModal» CLASSES (PATH)
# Last Modification: Editing The «HeaderModal» CLASSES (ICON to BOXES)
# Modification Date: 2023.12.22, 06:50 PM
#
# Create Date: 2023.10.23, 06:45 PM


from PySide6.QtCore import Qt, Slot
from PySide6.QtGui import QFont, QIcon
from PySide6.QtWidgets import (
    QWidget,
    QFrame,
    QVBoxLayout,
    QHBoxLayout,
    QGroupBox,
    QScrollArea,
    QLabel,
    QTextEdit,
    QCheckBox,
    QRadioButton,
    QPushButton
)

from .run import run
from .filesystem import FileSystem
from .values import StringsValues
from .messages import MessageBox

from webbrowser import open
from os import path


# --------------- HEADER ---------------

class Header(QWidget):
    """
    Providing a HEADER TEMPLATE

    ---
    PARAMETERS:
    - language_char: str -> The Characters of LANGUAGE
    - language_text: str -> The Title of LANGUAGE
    - parent: QWidget | None = None -> Widget PARENT for this CLASS
    (AFTER THAT, THIS CURRENT CLASS WILL BECOME A CHILD OF THE PARENT)
    - f: Qt.WindowType = Qt.WindowType.Widget -> Window-System (Widget)
    ---
    FUNCTIONS:
    - page() -> QFrame : Create 1 HEADER FRAME
    ---
    SLOTS:
    - activate_btn_settings() -> None : Opens 1 MODAL WINDOW for The SETTINGS
    - activate_btn_information() -> None : Opens 1 MODAL WINDOW for
    The INFORMATION
    - activate_btn_license() -> None : Opens 1 MODAL WINDOW for The LICENSE
    """

    def __init__(
        self,
        language_char: str,
        language_text: str,
        parent: QWidget | None = None,
        flags: Qt.WindowType = Qt.WindowType.Widget
    ) -> None:
        super(Header, self).__init__(parent, flags)
        self.setParent(parent)
        self.parent = parent

        self.language_char = language_char.lower() + "_"
        self.language_text = language_text

        self.basedir = self.parent.basedir
        self.str_val = StringsValues(self.basedir)

        self.__settings = HeaderModal("settings", self)
        self.__information = HeaderModal("information", self)
        self.__license = HeaderModal("license", self)

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

        text = self.str_val.string_values("header_title")
        title = QLabel(text)
        title.setFont(QFont("Lora"))

        self.btn_settings = QPushButton()
        self.btn_settings.setObjectName("header_btn_settings")
        self.btn_settings.setIcon(
            QIcon(path.join(self.basedir, "icons", "settings.svg"))
        )
        self.btn_settings.setFixedWidth(40)
        self.btn_settings.clicked.connect(self.activate_btn_settings)

        btn_information = QPushButton()
        btn_information.setObjectName("header_btn_information")
        btn_information.setIcon(
            QIcon(path.join(self.basedir, "icons", "information.svg"))
        )
        btn_information.setFixedWidth(40)
        btn_information.clicked.connect(self.activate_btn_information)

        btn_license = QPushButton()
        btn_license.setObjectName("header_btn_license")
        btn_license.setIcon(
            QIcon(path.join(self.basedir, "icons", "license.svg"))
        )
        btn_license.setFixedWidth(40)
        btn_license.clicked.connect(self.activate_btn_license)

        layout.addWidget(title, alignment=Qt.AlignmentFlag.AlignLeft)
        layout.addWidget(
            self.btn_settings, alignment=Qt.AlignmentFlag.AlignRight
        )
        layout.addWidget(btn_information)
        layout.addWidget(btn_license)

        frame.setLayout(layout)
        return frame

    def __activate(self, mode: str) -> None:
        """
        Opens and Clodes 1 MODAL WINDOW

        ---
        PARAMETERS:
        - mode: str -> Mode «settings», «information» or «license»
        """

        self.__settings.hide()
        self.__information.hide()
        self.__license.hide()

        match mode:
            case "settings":
                self.__settings.show()
            case "information":
                self.__information.show()
            case "license":
                self.__license.show()

    @Slot()
    def activate_btn_settings(self) -> None:
        """
        Opens 1 MODAL WINDOW for The SETTINGS
        """

        self.__activate("settings")

    @Slot()
    def activate_btn_information(self) -> None:
        """
        Opens 1 MODAL WINDOW for The INFORMATION
        """

        self.__activate("information")

    @Slot()
    def activate_btn_license(self) -> None:
        """
        Opens 1 MODAL WINDOW for The LICENSE
        """

        self.__activate("license")

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
    - page_settings() -> QFrame : Create 1 SETTINGS TEMPLATE
    - page_information() -> QFrame : Create 1 INFORMATION TEMPLATE
    - page_license() -> QFrame : Create 1 LICENSE TEMPLATE
    ---
    SLOTS:
    - save_settings() -> None : Saving NEW DATA to 1 SETTINGS FILE
    - open_url() -> None : Opens The URL in The BROWSER
    """

    def __init__(
        self,
        mode: str,
        parent: QWidget | None = None,
        f: Qt.WindowType = Qt.WindowType.Widget
    ) -> None:
        super(HeaderModal, self).__init__(parent, f)
        self.setParent(parent)
        self.parent = parent

        # LANGUAGE
        self.language_char = self.parent.language_char
        self.language_text = self.parent.language_text

        self.text_for_language_ru = self.parent.str_val.string_values(
            "ru_lang"
        )
        self.text_for_language_en = self.parent.str_val.string_values(
            "en_lang"
        )
        self.dir_language_char = {
            self.text_for_language_ru: "RU",
            self.text_for_language_en: "EN"
        }
        self.dir_language_text = {
            "RU": self.text_for_language_ru,
            "EN": self.text_for_language_en
        }

        self.setWindowFlags(Qt.WindowType.Dialog)

        template = QFrame()
        match(mode):
            case "settings":
                template = self.page_settings()
            case "information":
                template = self.page_information()
            case "license":
                template = self.page_license()

        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(template, alignment=Qt.AlignmentFlag.AlignTop)

        self.setLayout(layout)

    def page_settings(self) -> QFrame:
        """
        Create 1 SETTINGS TEMPLATE

        ---
        RESULT: SETTINGS TEMPLATE
        """

        # STRINGS
        text_for_title = self.parent.str_val.string_values(
            self.language_char + "settings_title"
        )
        text_for_btn_save = self.parent.str_val.string_values(
            self.language_char + "settings_btn_save"
        )

        # DATA from SETTINGS FILE
        filesystem = FileSystem(self.parent.basedir)
        valid_keys = filesystem._valid_true_keys(
            list(self.parent.parent.data_settings_file.keys())
        )
        if valid_keys is False:
            filesystem.write_file_settings()
            self.parent.parent.data_settings_file = filesystem.TEMPLATE

            # INFO
            text_for_info_msg_data_title = self.parent.str_val.string_values(
                self.language_char + "info_msg_data_title"
            )
            text_for_info_msg_data_text = self.parent.str_val.string_values(
                self.language_char + "info_msg_data_text"
            )
            MessageBox(
                path.join(self.parent.basedir, "icons", "info.svg"),
                text_for_info_msg_data_title,
                text_for_info_msg_data_text,
                self
            )

        data = self.parent.parent.data_settings_file
        main_data_title = data["title"]
        main_data_list = data["list"]
        main_data_dash = data["dash"]
        main_data_textbox = data["block"]
        language_data = data["language"]

        # MODAL WINDOW
        self.setWindowTitle(text_for_title)
        self.setFixedSize(568, 469)

        frame = QFrame()
        frame.setObjectName("header_modal_settings")

        layout = QVBoxLayout()

        # TITLE
        title = QLabel(text_for_title)
        title.setObjectName("settings_title")
        title.setFont(QFont("Lora"))

        # GROUPS
        group_layout = QHBoxLayout()
        group_layout.setContentsMargins(0, 0, 0, 0)

        self.main_group = self.__settings_main_group(
            main_data_title,
            main_data_list,
            main_data_dash,
            " ".join(main_data_textbox)
        )
        self.language_group = self.__settings_language_group(language_data)

        group_layout.addWidget(self.main_group)
        group_layout.addWidget(self.language_group)

        # BUTTON
        btn_save = QPushButton(text_for_btn_save.upper())
        btn_save.setObjectName("settings_btn_save")
        btn_save.setFont(QFont("Ubuntu"))
        btn_save.clicked.connect(self.save_settings)

        layout.addWidget(title, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addLayout(group_layout)
        layout.addWidget(btn_save)

        frame.setLayout(layout)
        return frame

    def page_information(self) -> QFrame:
        """
        Create 1 INFORMATION TEMPLATE

        ---
        RESULT: INFORMATION TEMPLATE
        """

        def __title(name: str, object_name: str) -> QLabel:
            """
            Makes up a SIMPLE TITLE

            ---
            PARAMETERS:
            - name: str -> The TEXT for The TITLE
            - object_name: str -> The OBJECT NAME of The TITLE
            ---
            RESULT: The TITLE
            """

            title = QLabel(name)
            title.setObjectName(object_name)
            title.setFont(QFont("Lora"))

            return title

        def __group(group_title: str, label: str) -> QGroupBox:
            """
            Makes 1 GROUP with 1 TEMPLATE inside

            ---
            PARAMETERS:
            - group_title: str -> The TITLE for GROUP Block
            - label: str -> The TITLE for TEMPLATE
            ---
            RESULT: The GROUP Block
            """

            group = QGroupBox()

            label_group = QLabel(group_title.upper())
            label_group.setObjectName("information_group_title")
            label_group.setFont(QFont("Ubuntu"))
            label_group.setFixedHeight(23)

            layout_group = QVBoxLayout()
            layout_group.setContentsMargins(0, 0, 0, 0)
            layout_group.addWidget(label_group)

            frame = QFrame()
            frame.setObjectName("information_group")
            frame.setContentsMargins(0, 0, 0, 0)

            frame_layout = QVBoxLayout()
            frame_layout.setContentsMargins(0, 0, 0, 0)

            template = QLabel(str(label))
            template.setObjectName("information_group_template")
            template.setFont(QFont("Ubuntu"))
            template.setWordWrap(True)

            frame_layout.addWidget(template)
            frame.setLayout(frame_layout)
            layout_group.addWidget(frame)
            group.setLayout(layout_group)

            return group

        def __block(
            name: str,
            template_before: str,
            template_after: str
        ) -> QFrame:
            """
            Block with DETAILED DESCRIPTION

            ---
            PARAMETERS:
            - name: str -> The TITLE for Block
            - template_before: str -> The TEXT for LEFT CONTENT
            - template_after: str -> The TEXT for RIGHT CONTENT
            ---
            RESULT: BLOCK TEMPLATE
            """

            frame = QFrame()
            frame.setObjectName("information_block")

            main_layout = QVBoxLayout()
            main_layout.setContentsMargins(0, 0, 0, 0)

            second_layout = QHBoxLayout()
            second_layout.setContentsMargins(0, 0, 0, 0)
            second_layout.setSpacing(10)

            title = __title(name, "information_second_title")
            before = __group(text_for_group_before, template_before)
            after = __group(text_for_group_after, template_after)

            second_layout.addWidget(before)
            second_layout.addWidget(after)
            main_layout.addWidget(title)
            main_layout.addLayout(second_layout)

            frame.setLayout(main_layout)
            return frame

        # STRINGS
        text_for_lost_and_found = self.parent.str_val.string_values(
            self.language_char + "information_lost_and_found"
        )
        text_for_title = self.parent.str_val.string_values(
            self.language_char + "information_title"
        )
        text_for_main = self.parent.str_val.string_values(
            self.language_char + "information_main"
        )
        text_for_main_url = self.parent.str_val.string_values(
            self.language_char + "information_main_url"
        )
        text_for_group_before = self.parent.str_val.string_values(
            self.language_char + "information_group_before"
        )
        text_for_group_after = self.parent.str_val.string_values(
            self.language_char + "information_group_after"
        )
        text_for_second_title = self.parent.str_val.string_values(
            self.language_char + "information_second_title"
        )
        text_for_second_title_before = self.parent.str_val.string_values(
            self.language_char + "information_second_title_before"
        )
        text_for_second_title_after = self.parent.str_val.string_values(
            self.language_char + "information_second_title_after"
        )
        text_for_second_list = self.parent.str_val.string_values(
            self.language_char + "information_second_list"
        )
        text_for_second_list_before = self.parent.str_val.string_values(
            self.language_char + "information_second_list_before"
        )
        text_for_second_list_after = self.parent.str_val.string_values(
            self.language_char + "information_second_list_after"
        )
        text_for_second_dash = self.parent.str_val.string_values(
            self.language_char + "information_second_dash"
        )
        text_for_second_dash_before = self.parent.str_val.string_values(
            self.language_char + "information_second_dash_before"
        )
        text_for_second_dash_after = self.parent.str_val.string_values(
            self.language_char + "information_second_dash_after"
        )

        # MODAL WINDOW
        self.setWindowTitle(text_for_lost_and_found)
        self.setFixedSize(720, 480)

        frame = QFrame()
        frame.setObjectName("header_modal_information")
        frame.setContentsMargins(0, 0, 0, 0)
        frame.setFixedWidth(720)

        layout = QVBoxLayout()

        # TITLE
        main_title = __title(text_for_title, "information_title")

        # SCROLL
        scroll = QScrollArea()
        scroll.setContentsMargins(0, 0, 0, 0)
        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        scroll.setHorizontalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        )
        scroll.setWidgetResizable(True)

        frame_scroll = QFrame()
        frame_scroll.setObjectName("header_modal_information_scroll")
        frame_scroll.setContentsMargins(0, 0, 0, 0)

        layout_scroll = QVBoxLayout()
        layout_scroll.setContentsMargins(0, 0, 0, 0)
        layout_scroll.setSpacing(0)

        # SCROLL : MAIN
        main_text = QLabel(text_for_main)
        main_text.setObjectName("information_main")
        main_text.setFont(QFont("Ubuntu"))
        main_text.setWordWrap(True)

        # SCROLL : MAIN URL
        btn_url = QPushButton(text_for_main_url)
        btn_url.setObjectName("information_main_url")
        btn_url.setFont(QFont("Ubuntu"))
        btn_url.clicked.connect(self.open_url)

        # SCROLL : TITLE && LIST && DASH
        second_title = __block(
            text_for_second_title,
            text_for_second_title_before,
            text_for_second_title_after
        )
        second_list = __block(
            text_for_second_list,
            text_for_second_list_before,
            text_for_second_list_after
        )
        second_dash = __block(
            text_for_second_dash,
            text_for_second_dash_before,
            text_for_second_dash_after
        )

        layout_scroll.addWidget(main_text)
        layout_scroll.addWidget(btn_url, alignment=Qt.AlignmentFlag.AlignLeft)
        layout_scroll.addWidget(second_title)
        layout_scroll.addWidget(second_list)
        layout_scroll.addWidget(second_dash)
        frame_scroll.setLayout(layout_scroll)
        scroll.setWidget(frame_scroll)

        layout.addWidget(main_title, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(scroll)

        frame.setLayout(layout)
        return frame

    def page_license(self) -> QFrame:
        """
        Create 1 LICENSE TEMPLATE

        ---
        RESULT: LICENSE TEMPLATE
        """

        WIDTH = 675
        HEIGHT = [500 if self.language_char == "ru_" else 420][0]

        # STRINGS
        text_for_title = self.parent.str_val.string_values(
            self.language_char + "license_part_one"
        )
        text_for_copyright = self.parent.str_val.string_values(
            "license_part_zero"
        )
        text_for_zero = self.parent.str_val.string_values(
            self.language_char + "license_part_two"
        )
        text_for_one = self.parent.str_val.string_values(
            self.language_char + "license_part_three"
        )
        text_for_two = self.parent.str_val.string_values(
            self.language_char + "license_part_four"
        )

        # MODAL WINDOW
        self.setWindowTitle(text_for_title)
        self.setFixedSize(WIDTH, HEIGHT)

        frame = QFrame()
        frame.setObjectName("header_modal_license")
        frame.setFixedHeight(HEIGHT)

        layout = QVBoxLayout()

        # TITLE
        title_license = QLabel(text_for_title)
        title_license.setObjectName("license_title")
        title_license.setFont(QFont("Lora"))

        # COPYRIGHT
        copyright_license = QLabel(text_for_copyright)
        copyright_license.setObjectName("license_copyright")
        copyright_license.setFont(QFont("Ubuntu"))

        # TEXT #0
        text_zero_license = QLabel(text_for_zero)
        text_zero_license.setObjectName("license_text_zero")
        text_zero_license.setWordWrap(True)
        text_zero_license.setFont(QFont("Ubuntu"))

        # TEXT #1
        text_one_license = QLabel(text_for_one)
        text_one_license.setObjectName("license_text_one")
        text_one_license.setWordWrap(True)
        text_one_license.setFont(QFont("Ubuntu"))

        # TEXT #2
        text_two_license = QLabel(text_for_two)
        text_two_license.setObjectName("license_text_two")
        text_two_license.setWordWrap(True)
        text_two_license.setFont(QFont("Ubuntu"))

        layout.addWidget(title_license, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(copyright_license)
        layout.addWidget(text_zero_license)
        layout.addWidget(text_one_license)
        layout.addWidget(text_two_license)

        frame.setLayout(layout)
        return frame

    def __settings_group_checkboxes(
        self, checked: bool, *text: str
    ) -> QHBoxLayout:
        """
        Creates 1 HORIZONTAL LAYOUT with CHECKBOX and TEXT Together

        ---
        PARAMETERS:
        - checked: bool -> The Boolean from CHECKBOX
        - *text: str -> The LIST with TEXT
        ---
        RESULT: HORIZONTAL LAYOUT
        """

        icon_checkbox_path = path.join(
            self.parent.basedir, "icons", "c_checked.svg"
        )
        icon_checkbox = "QFrame#header_modal_settings QCheckBox::indicator"
        icon_checkbox += ":checked { image: url(%s); }" % icon_checkbox_path

        checkbox_layout = QHBoxLayout()
        checkbox_layout.setContentsMargins(0, 0, 0, 0)
        checkbox_layout.setSpacing(0)
        checkbox_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)

        checkbox = QCheckBox()
        checkbox.setObjectName("settings_checkboxes")
        checkbox.setFont(QFont("Ubuntu"))
        checkbox.setChecked(checked)
        checkbox.setStyleSheet(icon_checkbox)
        checkbox_layout.addWidget(checkbox)

        for tt in text:
            part = QLabel(tt[0])
            part.setObjectName(tt[1])
            part.setFont(QFont("Ubuntu"))
            checkbox_layout.addWidget(part)

        return checkbox_layout

    def __settings_main_group(self, *data: any) -> QGroupBox:
        """
        CREATE 1 MAIN GROUP for SETTINGS TEMPLATE

        ---
        PARAMETERS:
        - *data: any -> The DATA from RAM with SETTINGS FILE
        ---
        RESULT: MAIN GROUP
        """

        # STRINGS
        text_for_main_group = self.parent.str_val.string_values(
            self.language_char + "settings_main"
        )
        text_for_main_title = self.parent.str_val.strings_values_idx(
            self.language_char + "settings_main_title", 3
        )
        text_for_main_list = self.parent.str_val.strings_values_idx(
            self.language_char + "settings_main_list", 3
        )
        text_for_main_dash = self.parent.str_val.strings_values_idx(
            self.language_char + "settings_main_dash",
            [1 if self.language_char == "ru_" else 2][0]
        )
        text_for_title_punctuations = self.parent.str_val.string_values(
            self.language_char + "settings_main_title_punctuations"
        )
        text_for_hint_punctuations = self.parent.str_val.string_values(
            self.language_char + "settings_main_hint_punctuations"
        )

        # MAIN GROUP
        main_group = QGroupBox()
        main_group.setTitle(text_for_main_group.upper())
        main_group.setFont(QFont("Lora"))

        main_group_layout = QVBoxLayout()
        main_group_layout.setContentsMargins(0, 0, 0, 0)

        main_frame = QFrame()
        main_frame.setObjectName("settings_main_group")

        main_frame_layout = QVBoxLayout()
        main_frame_layout.setContentsMargins(0, 0, 0, 0)

        # CHECKBOXES
        title_checkbox_layout = self.__settings_group_checkboxes(  # TITLE
            data[0],  # title
            (text_for_main_title[1], "settings_checkboxes_one_part"),
            (text_for_main_title[0][0], "settings_checkboxes_find")
        )
        list_checkbox_layout = self.__settings_group_checkboxes(  # LIST
            data[1],  # list
            (text_for_main_list[1], "settings_checkboxes_one_part"),
            (text_for_main_list[0][0], "settings_checkboxes_find")
        )
        dash_checkbox_layout = self.__settings_group_checkboxes(  # DASH
            data[2],  # dash
            (text_for_main_dash[1], "settings_checkboxes_one_part"),
            (text_for_main_dash[0][0], "settings_checkboxes_find"),
            (text_for_main_dash[2], "settings_checkboxes_two_part")
        )

        # TITLE PUNCTUATIONS
        title_punctuations = QLabel(text_for_title_punctuations)
        title_punctuations.setObjectName("settings_title_edits")
        title_punctuations.setFont(QFont("Ubuntu"))

        # PUNCTUATIONS
        self.punctuations = QTextEdit()
        self.punctuations.setObjectName("settings_edits")
        self.punctuations.setText(data[3])  # block
        self.punctuations.setFont(QFont("Ubuntu"))
        self.punctuations.setFixedHeight(73)

        # HINT PUNCTUATIONS
        hint_punctuations = QLabel(text_for_hint_punctuations)
        hint_punctuations.setObjectName("settings_hint_edits")
        hint_punctuations.setFont(QFont("Lora"))
        hint_punctuations.setWordWrap(True)

        main_frame_layout.addLayout(title_checkbox_layout)
        main_frame_layout.addLayout(list_checkbox_layout)
        main_frame_layout.addLayout(dash_checkbox_layout)
        main_frame_layout.addWidget(title_punctuations)
        main_frame_layout.addWidget(self.punctuations)
        main_frame_layout.addWidget(hint_punctuations)
        main_frame.setLayout(main_frame_layout)

        main_group_layout.addWidget(main_frame)
        main_group.setLayout(main_group_layout)
        return main_group

    def __settings_language_group(self, language: str) -> QGroupBox:
        """
        CREATE 1 LANGUAGE GROUP for LANGUAGE TEMPLATE

        ---
        PARAMETERS:
        - language: str -> The LANGUAGE from RAM with SETTINGS FILE
        ---
        RESULT: LANGUAGE GROUP
        """

        __language = self.dir_language_text[language]

        # STRINGS
        text_for_language_group = self.parent.str_val.string_values(
            self.language_char + "settings_language"
        )

        # LANGUAGE GROUP
        language_group = QGroupBox()
        language_group.setTitle(text_for_language_group.upper())
        language_group.setFont(QFont("Lora"))

        language_group_layout = QVBoxLayout()
        language_group_layout.setContentsMargins(0, 0, 0, 0)

        language_frame = QFrame()
        language_frame.setObjectName("settings_language_group")
        language_frame.setFixedWidth(170)

        language_frame_layout = QVBoxLayout()
        language_frame_layout.setContentsMargins(0, 0, 0, 0)

        # RU && EN : ICON for QRadioBox
        icon_radiobox_path = path.join(
            self.parent.basedir, "icons", "r_checked.svg"
        )
        icon_radiobox = "QFrame#header_modal_settings QRadioButton::indicator"
        icon_radiobox += ":checked { image: url(%s); }" % icon_radiobox_path

        # RADIOBUTTONS : RU
        ru_lang = QRadioButton(self.text_for_language_ru, self)
        ru_lang.setFont(QFont("Ubuntu"))
        [
            ru_lang.setChecked(True) if ru_lang.text() == __language
            else ru_lang.setChecked(False)
        ]
        ru_lang.setStyleSheet(icon_radiobox)

        # RADIOBUTTONS : EN
        en_lang = QRadioButton(self.text_for_language_en, self)
        en_lang.setFont(QFont("Ubuntu"))
        [
            en_lang.setChecked(True) if en_lang.text() == __language
            else en_lang.setChecked(False)
        ]
        en_lang.setStyleSheet(icon_radiobox)

        language_frame_layout.addWidget(ru_lang)
        language_frame_layout.addWidget(
            en_lang, alignment=Qt.AlignmentFlag.AlignTop
        )
        language_frame.setLayout(language_frame_layout)

        language_group_layout.addWidget(
            language_frame, alignment=Qt.AlignmentFlag.AlignTop
        )
        language_group.setLayout(language_group_layout)
        return language_group

    @Slot()
    def save_settings(self) -> None:
        """
        Saving NEW DATA to 1 SETTINGS FILE
        """

        # STRINGS
        text_for_success_msg_save_title = self.parent.str_val.string_values(
            self.language_char + "success_msg_save_settings_title"
        )
        text_for_success_msg_save_text = self.parent.str_val.string_values(
            self.language_char + "success_msg_save_settings_text"
        )

        # MAIN GROUP
        main_frame = self.main_group.findChild(QFrame, "settings_main_group")
        main_checkboxes = main_frame.findChildren(
            QCheckBox, "settings_checkboxes"
        )
        main_title = main_checkboxes[0]
        main_list = main_checkboxes[1]
        main_dash = main_checkboxes[2]
        main_textbox = main_frame.findChild(QTextEdit, "settings_edits")
        main_textbox_set_list = list(set(main_textbox.toPlainText().split()))

        # LANGUAGE GROUP
        language_frame = self.language_group.findChildren(QRadioButton)
        language_radio = [
            lang.text() for lang in language_frame if lang.isChecked()
        ][0]

        new_data = {
            "title": main_title.isChecked(),
            "list": main_list.isChecked(),
            "dash": main_dash.isChecked(),
            "block": main_textbox_set_list,
            "language": self.dir_language_char[language_radio]
        }
        stop_old_language = self.parent.parent.data_settings_file["language"]

        filesystem = FileSystem(self.parent.basedir)
        filesystem.write_file_settings(new_data)
        self.parent.parent.data_settings_file = new_data
        self.punctuations.setText(" ".join(main_textbox_set_list))

        MessageBox(  # SUCCESS
            path.join(self.parent.basedir, "icons", "success.svg"),
            text_for_success_msg_save_title,
            text_for_success_msg_save_text,
            self
        )

        self.hide()

        if stop_old_language != self.dir_language_char[language_radio]:
            self.parent.parent.close()
            run()

    @Slot()
    def open_url(self) -> None:
        """
        Opens The URL in The BROWSER
        """

        try:
            text_readme = self.parent.str_val.string_values("app_readme")
            open(text_readme)
        except:
            text_error_msg_url_title = self.parent.str_val.string_values(
                self.language_char + "error_msg_url_title"
            )
            text_error_msg_url_text = self.parent.str_val.string_values(
                self.language_char + "error_msg_url_text"
            )
            MessageBox(  # ERROR
                path.join(self.parent.basedir, "icons", "error.svg"),
                text_error_msg_url_title,
                text_error_msg_url_text,
                self
            )

# --------------------------------------
