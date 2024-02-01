# Developer && Owner: МогучийДД (MoguchiyDD)
# LICENSE: MIT License which is located in the text file LICENSE
#
# Goal: Create a HEADER TEMPLATE with Ready-Made Working Filling
# Result: Providing a HEADER TEMPLATE
#
# Past Modification: Editing The «HeaderModal» CLASS (TEXTBOX ANIMATION)
# Last Modification: Checking CODE The PEP8
# Modification Date: 2024.02.01, 05:20 PM
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
from .messages import activate_message_box

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
    - version: str -> New VERSION Number of The SOFTWARE
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
    - open_url() -> None : Opens The URL in The BROWSER
    """

    def __init__(
        self,
        language_char: str,
        language_text: str,
        version: str,
        parent: QWidget | None = None,
        flags: Qt.WindowType = Qt.WindowType.Widget
    ) -> None:
        super(Header, self).__init__(parent, flags)
        self.setParent(parent)
        self.parent = parent

        self.language_char = language_char.lower() + "_"
        self.language_text = language_text
        self.version = version

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

        def btn(
            object_name: str, icon_name: str, connect: object
        ) -> QPushButton:
            """
            Creates and Returns 1 QPushButton

            ---
            PARAMETERS:
            - object_name: str -> ID for The QPushButton
            - icon_name: str -> NAME of The ICON for The QPushButton
            - connect: object -> Function that will Work After ACTIVATING
            The QPushButton
            ---
            RESULT: QPushButton
            """

            btn = QPushButton()
            btn.setObjectName(object_name)
            btn.setIcon(
                QIcon(path.join(self.basedir, "icons", icon_name))
            )
            btn.setFixedWidth(40)
            btn.clicked.connect(connect)

            return btn

        frame = QFrame()
        frame.setObjectName("header")

        layout = QHBoxLayout()
        layout.setSpacing(8)

        text = self.str_val.string_values("header_title")
        title = QLabel(text)
        title.setObjectName("header_title")
        title.setFont(QFont("Lora"))

        text_version = self.str_val.string_values("app_version")
        text_version += "/" + self.version
        self.btn_updates = btn(
            "header_btn_updates",
            "updates.svg",
            lambda _: self.open_url(
                text_version, "error_msg_url_text_version"
            )
        )
        if len(self.version) == 0:
            self.btn_updates.hide()

        self.btn_settings = btn(
            "header_btn_settings",
            "settings.svg",
            self.activate_btn_settings
        )
        btn_information = btn(
            "header_btn_information",
            "information.svg",
            self.activate_btn_information
        )
        btn_license = btn(
            "header_btn_license",
            "license.svg",
            self.activate_btn_license
        )

        layout.addWidget(title, alignment=Qt.AlignmentFlag.AlignLeft)
        layout.addWidget(
            self.btn_updates, alignment=Qt.AlignmentFlag.AlignRight
        )
        layout.addWidget(self.btn_settings)
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

    @Slot()
    def open_url(self, url: str, text_url: str) -> None:
        """
        Opens The URL in The BROWSER

        ---
        PARAMETERS:
        - url: str -> URL-Address
        - text_url: str -> Text from The «strings.xml» File
        """

        try:
            open(url)
        except:
            activate_message_box(  # ERROR
                self.basedir,
                self.language_char + "error_msg_url_title",
                self.language_char + text_url,
                "error.svg",
                self
            )

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

        def data_from_settings() -> None:
            """
            Checks ALL KEYS for their Existence in The FILE SYSTEM
            """

            filesystem = FileSystem(self.parent.basedir)
            valid_keys = filesystem._valid_true_keys(
                list(self.parent.parent.data_settings_file.keys())
            )
            if valid_keys is False:
                filesystem.write_file_settings()
                self.parent.parent.data_settings_file = filesystem.TEMPLATE
                activate_message_box(  # INFO
                    self.parent.basedir,
                    self.language_char + "info_msg_data_title",
                    self.language_char + "info_msg_data_text",
                    "info.svg",
                    self
                )

        def main_group(data: dict[any]) -> QGroupBox:
            """
            CREATE 1 MAIN GROUP for SETTINGS TEMPLATE

            ---
            PARAMETERS:
            - *data: dict[any] -> The DATA from RAM with SETTINGS FILE
            ---
            RESULT: MAIN GROUP
            """

            data_title = data["title"]
            data_list = data["list"]
            data_dash = data["dash"]
            data_textbox = data["block"]

            group = self.__settings_main_group(
                data_title, data_list, data_dash, " ".join(data_textbox)
            )
            return group

        def language_group(data: dict[any]) -> QGroupBox:
            """
            CREATE 1 LANGUAGE GROUP for SETTINGS TEMPLATE

            ---
            PARAMETERS:
            - *data: dict[any] -> The DATA from RAM with SETTINGS FILE
            ---
            RESULT: LANGUAGE GROUP
            """

            data_language = data["language"]
            group = self.__settings_language_group(data_language)
            return group

        def other_group(data: dict[any]) -> QGroupBox:
            """
            CREATE 1 OTHER GROUP for SETTINGS TEMPLATE

            ---
            PARAMETERS:
            - *data: dict[any] -> The DATA from RAM with SETTINGS FILE
            ---
            RESULT: OTHER GROUP
            """

            data_notification = data["notification"]
            data_animation = data["animation"]

            group = self.__settings_other_group(
                data_notification, data_animation
            )
            return group

        # STRINGS
        text_for_title = self.parent.str_val.string_values(
            self.language_char + "settings_title"
        )
        text_for_btn_save = self.parent.str_val.string_values(
            self.language_char + "settings_btn_save"
        )

        # DATA from SETTINGS FILE
        data_from_settings()  # Checking
        data = self.parent.parent.data_settings_file

        # CREATE GROUPS
        self.main_group = main_group(data)  # MAIN
        self.language_group = language_group(data)  # LANGUAGE
        self.other_group = other_group(data)  # OTHER

        # MODAL WINDOW
        self.setWindowTitle(text_for_title)
        self.setFixedSize(688, 469)

        frame = QFrame()
        frame.setObjectName("header_modal_settings")

        layout = QVBoxLayout()

        # TITLE
        title = QLabel(text_for_title)
        title.setObjectName("settings_title")
        title.setFont(QFont("Lora"))

        # LAYOUT VERTICAL GROUP
        vgroup_layout = QVBoxLayout()
        vgroup_layout.setContentsMargins(0, 0, 0, 0)
        vgroup_layout.addWidget(self.language_group)
        vgroup_layout.addWidget(self.other_group)

        # LAYOUT HORIZONTAL GROUP
        hgroup_layout = QHBoxLayout()
        hgroup_layout.setContentsMargins(0, 0, 0, 0)
        hgroup_layout.addWidget(self.main_group)
        hgroup_layout.addLayout(vgroup_layout)

        # BUTTON
        btn_save = QPushButton(text_for_btn_save.upper())
        btn_save.setObjectName("settings_btn_save")
        btn_save.setFont(QFont("Ubuntu"))
        btn_save.clicked.connect(self.save_settings)

        layout.addWidget(title, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addLayout(hgroup_layout)
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

            frame_layout.addWidget(
                template,
                alignment=Qt.AlignmentFlag.AlignTop
            )
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
        main_text.setAlignment(Qt.AlignmentFlag.AlignJustify)
        main_text.setWordWrap(True)

        # SCROLL : MAIN URL
        text_readme = self.parent.str_val.string_values("app_readme")
        btn_url = QPushButton(text_for_main_url)
        btn_url.setObjectName("information_main_url")
        btn_url.setFont(QFont("Ubuntu"))
        btn_url.clicked.connect(
            lambda btn: self.parent.open_url(
                text_readme, "error_msg_url_text_gtl"
            )
        )

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
        HEIGHT = [520 if self.language_char == "ru_" else 440][0]

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
        text_zero_license.setFont(QFont("Ubuntu"))
        text_zero_license.setAlignment(Qt.AlignmentFlag.AlignJustify)
        text_zero_license.setWordWrap(True)

        # TEXT #1
        text_one_license = QLabel(text_for_one)
        text_one_license.setObjectName("license_text_one")
        text_one_license.setFont(QFont("Ubuntu"))
        text_one_license.setAlignment(Qt.AlignmentFlag.AlignJustify)
        text_one_license.setWordWrap(True)

        # TEXT #2
        text_two_license = QLabel(text_for_two)
        text_two_license.setObjectName("license_text_two")
        text_two_license.setFont(QFont("Ubuntu"))
        text_two_license.setAlignment(Qt.AlignmentFlag.AlignJustify)
        text_two_license.setWordWrap(True)

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

        checkbox_layout = QHBoxLayout()
        checkbox_layout.setContentsMargins(0, 0, 0, 0)
        checkbox_layout.setSpacing(0)
        checkbox_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)

        checkbox = QCheckBox()
        checkbox.setObjectName("settings_checkboxes")
        checkbox.setFont(QFont("Ubuntu"))
        checkbox.setChecked(checked)
        checkbox_layout.addWidget(
            checkbox, alignment=Qt.AlignmentFlag.AlignTop
        )

        len_text = len(text)
        for tt in range(len_text):
            part = QLabel(text[tt][0])
            part.setObjectName(text[tt][1])
            part.setFont(QFont("Ubuntu"))
            if (len_text - 1) == 0:
                part.setWordWrap(True)
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
        language_frame.setFixedHeight(102)

        language_frame_layout = QVBoxLayout()
        language_frame_layout.setContentsMargins(0, 0, 0, 0)

        # RADIOBUTTONS : RU
        ru_lang = QRadioButton(self.text_for_language_ru, self)
        ru_lang.setFont(QFont("Ubuntu"))
        [
            ru_lang.setChecked(True) if ru_lang.text() == __language
            else ru_lang.setChecked(False)
        ]

        # RADIOBUTTONS : EN
        en_lang = QRadioButton(self.text_for_language_en, self)
        en_lang.setFont(QFont("Ubuntu"))
        [
            en_lang.setChecked(True) if en_lang.text() == __language
            else en_lang.setChecked(False)
        ]

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

    def __settings_other_group(self, *data: any) -> QGroupBox:
        """
        CREATE 1 OTHER GROUP for SETTINGS TEMPLATE

        ---
        PARAMETERS:
        - *data: any -> The DATA from RAM with SETTINGS FILE
        ---
        RESULT: OTHER GROUP
        """

        # STRINGS
        text_for_other_group = self.parent.str_val.string_values(
            self.language_char + "settings_other"
        )
        text_for_other_notification = self.parent.str_val.string_values(
            self.language_char + "settings_other_notification"
        )
        text_for_other_animation = self.parent.str_val.string_values(
            self.language_char + "settings_other_animation"
        )

        # OTHER GROUP
        other_group = QGroupBox()
        other_group.setTitle(text_for_other_group.upper())
        other_group.setFont(QFont("Lora"))

        other_group_layout = QVBoxLayout()
        other_group_layout.setContentsMargins(0, 0, 0, 0)

        other_frame = QFrame()
        other_frame.setObjectName("settings_other_group")

        other_frame_layout = QVBoxLayout()
        other_frame_layout.setContentsMargins(0, 0, 0, 0)

        # CHECKBOXES
        notification_checkbox_layout = self.__settings_group_checkboxes(
            data[0],  # notification
            (text_for_other_notification, "settings_checkboxes_one_part")
        )
        animation_checkbox_layout = self.__settings_group_checkboxes(
            data[1],  # animation
            (text_for_other_animation, "settings_checkboxes_one_part")
        )

        other_frame_layout.addLayout(notification_checkbox_layout)
        other_frame_layout.addLayout(animation_checkbox_layout)
        other_frame.setLayout(other_frame_layout)

        other_group_layout.addWidget(other_frame)
        other_group.setLayout(other_group_layout)
        return other_group

    @Slot()
    def save_settings(self) -> None:
        """
        Saving NEW DATA to 1 SETTINGS FILE
        """

        def main_group() -> None:
            """
            Receives DATA from The MAIN GROUP

            ---
            RESULT: {"title": bool, "list": bool, "dash": bool,
            "textbox_set_list": list[set]}
            """

            frame = self.main_group.findChild(QFrame, "settings_main_group")
            checkboxes = frame.findChildren(QCheckBox, "settings_checkboxes")

            title = checkboxes[0]
            _list = checkboxes[1]
            dash = checkboxes[2]
            textbox = frame.findChild(QTextEdit, "settings_edits")
            textbox_set_list = list(set(textbox.toPlainText().split()))

            result = {
                "title": title,
                "list": _list,
                "dash": dash,
                "textbox_set_list": textbox_set_list,
            }
            return result

        def language_group() -> None:
            """
            Receives DATA from The LANGUAGE GROUP

            ---
            RESULT: {"language": "RU" || "EN"}
            """

            frame = self.language_group.findChildren(QRadioButton)
            radio = [lang.text() for lang in frame if lang.isChecked()][0]

            result = {"language": self.dir_language_char[radio]}
            return result

        def other_group() -> None:
            """
            Receives DATA from The OTHER GROUP

            ---
            RESULT: {"notification": bool, "animation": bool}
            """

            frame = self.other_group.findChild(QFrame, "settings_other_group")
            checkboxes = frame.findChildren(QCheckBox, "settings_checkboxes")

            notification = checkboxes[0]
            animation = checkboxes[1]

            result = {
                "notification": notification,
                "animation": animation
            }
            return result

        def set_animation(animation: bool) -> None:
            """
            Enables or disables The ANIMATION of The 2nd TEXT BLOCK

            ---
            PARAMETERS:
            - animation: bool -> The DATA from RAM with SETTINGS FILE from
            «animation» KEY
            """

            content = self.parent.parent.content
            if animation is False:  # Turn On
                if len(content.text_ready.toPlainText()) >= 1:
                    content.anim_text_ready.timer_text.start()
                    content.anim_text_ready.timer_text.timeout.connect(
                        content.anim_text_ready.animation
                    )
                    content.anim_text_ready.animations_group.start()
            else:  # Turn Off
                try:
                    content.anim_text_ready.timer_text.stop()
                    content.anim_text_ready.timer_text.timeout.disconnect()
                    content.anim_text_ready.animations_group.stop()
                except AttributeError:
                    pass
                except RuntimeError:
                    pass

        # GROUPS
        main_group_data = main_group()  # MAIN
        language_group_data = language_group()  # LANGUAGE
        other_group_data = other_group()  # OTHER

        new_data = {
            "title": main_group_data["title"].isChecked(),
            "list": main_group_data["list"].isChecked(),
            "dash": main_group_data["dash"].isChecked(),
            "block": main_group_data["textbox_set_list"],
            "language": language_group_data["language"],
            "notification": other_group_data["notification"].isChecked(),
            "animation": other_group_data["animation"].isChecked()
        }
        stop_old_language = self.parent.parent.data_settings_file["language"]

        # SAVING
        filesystem = FileSystem(self.parent.basedir)
        filesystem.write_file_settings(new_data)
        self.parent.parent.data_settings_file = new_data
        self.punctuations.setText(
            " ".join(main_group_data["textbox_set_list"])
        )

        activate_message_box(  # SUCCESS
            self.parent.basedir,
            self.language_char + "success_msg_save_settings_title",
            self.language_char + "success_msg_save_settings_text",
            "success.svg",
            self
        )
        self.hide()

        # Animation 2nd Textbox
        data_animation = self.parent.parent.data_settings_file["animation"]
        set_animation(data_animation)

        if stop_old_language != language_group_data["language"]:
            self.parent.parent.close()  # Window
            try:  # Schedule
                self.parent.parent.schedule.is_activate = False
            except AttributeError:
                pass
            run()  # New Window

# --------------------------------------
