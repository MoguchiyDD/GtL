# Developer && Owner: МогучийДД (MoguchiyDD)
# LICENSE: MIT License which is located in the text file LICENSE
#
# Goal: Create a HEADER TEMPLATE with Ready-Made Working Filling
# Result: Providing a HEADER TEMPLATE
#
# Past Modification: Editing The «HeaderModal» CLASS (MAIN GROUP)
# Last Modification: Adding The «HeaderModal» and The «Header» CLASS (BTN INFO)
# Modification Date: 2023.11.12, 11:43 PM
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
    QLabel,
    QTextEdit,
    QCheckBox,
    QPushButton
)

from .filesystem import FileSystem
from .values import StringsValues
from .messages import MessageBox


# --------------- HEADER ---------------

class Header(QWidget):
    """
    Providing a HEADER TEMPLATE

    ---
    PARAMETER:
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
        parent: QWidget | None = None,
        flags: Qt.WindowType = Qt.WindowType.Widget
    ) -> None:
        super(Header, self).__init__(parent, flags)
        self.setParent(parent)
        self.parent = parent

        self.str_val = StringsValues()

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

        btn_settings = QPushButton()
        btn_settings.setObjectName("header_btn_settings")
        btn_settings.setIcon(QIcon("app/icons/settings.svg"))
        btn_settings.setFixedWidth(40)
        btn_settings.clicked.connect(self.activate_btn_settings)

        btn_information = QPushButton()
        btn_information.setObjectName("header_btn_information")
        btn_information.setIcon(QIcon("app/icons/information.svg"))
        btn_information.setFixedWidth(40)
        btn_information.clicked.connect(self.activate_btn_information)

        btn_license = QPushButton()
        btn_license.setObjectName("header_btn_license")
        btn_license.setIcon(QIcon("app/icons/license.svg"))
        btn_license.setFixedWidth(40)
        btn_license.clicked.connect(self.activate_btn_license)

        layout.addWidget(title, alignment=Qt.AlignmentFlag.AlignLeft)
        layout.addWidget(btn_settings, alignment=Qt.AlignmentFlag.AlignRight)
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
        layout.addWidget(template, alignment=Qt.AlignmentFlag.AlignCenter)

        self.setLayout(layout)

    def page_settings(self) -> QFrame:
        """
        Create 1 SETTINGS TEMPLATE

        ---
        RESULT: SETTINGS TEMPLATE
        """

        # STRINGS
        text_for_title = self.parent.str_val.string_values("ru_settings_title")
        text_for_btn_save = self.parent.str_val.string_values(
            "ru_settings_btn_save"
        )

        # DATA from SETTINGS FILE
        filesystem = FileSystem(self.parent.parent.basedir)
        valid_keys = filesystem._valid_true_keys(
            list(self.parent.parent.data_settings_file.keys())
        )
        if valid_keys is False:
            filesystem.write_file_settings()
            self.parent.parent.data_settings_file = filesystem.TEMPLATE

            # INFO
            text_for_info_msg_data_title = self.parent.str_val.string_values(
                "ru_info_msg_data_title"
            )
            text_for_info_msg_data_text = self.parent.str_val.string_values(
                "ru_info_msg_data_text"
            )
            MessageBox(
                "app/icons/info.svg",
                text_for_info_msg_data_title,
                text_for_info_msg_data_text,
                self
            )

        data = self.parent.parent.data_settings_file
        main_data_title = data["title"]
        main_data_list = data["list"]
        main_data_dash = data["dash"]
        main_data_textbox = data["block"]

        # MODAL WINDOW
        self.setWindowTitle(text_for_title)
        self.setFixedSize(384, 469)

        frame = QFrame()
        frame.setObjectName("header_modal_settings")

        layout = QVBoxLayout()

        # TITLE
        title = QLabel(text_for_title)
        title.setObjectName("settings_title")
        title.setFont(QFont("Lora"))

        # GROUPS
        self.main_group = self.__settings_main_group(
            main_data_title,
            main_data_list,
            main_data_dash,
            " ".join(main_data_textbox)
        )

        # BUTTON
        btn_save = QPushButton(text_for_btn_save.upper())
        btn_save.setObjectName("settings_btn_save")
        btn_save.setFont(QFont("Ubuntu"))
        btn_save.clicked.connect(self.save_settings)

        layout.addWidget(title, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.main_group)
        layout.addWidget(btn_save)

        frame.setLayout(layout)
        return frame

    def page_information(self) -> QFrame:
        """
        Create 1 INFORMATION TEMPLATE

        ---
        RESULT: INFORMATION TEMPLATE
        """

        # STRINGS
        text_for_lost_and_found = self.parent.str_val.string_values(
            "ru_information_lost_and_found"
        )
        text_for_title = self.parent.str_val.string_values(
            "ru_information_title"
        )

        # MODAL WINDOW
        self.setWindowTitle(text_for_lost_and_found)
        self.setStyleSheet("background-color: #404040;")
        self.setFixedSize(720, 540)

        frame = QFrame()
        frame.setObjectName("header_modal_information")

        layout = QVBoxLayout()

        # TITLE
        title_information = QLabel(text_for_title)
        title_information.setObjectName("information_title")
        title_information.setFont(QFont("Lora"))

        layout.addWidget(
            title_information, alignment=Qt.AlignmentFlag.AlignTop
        )

        frame.setLayout(layout)
        return frame

    def page_license(self) -> QFrame:
        """
        Create 1 LICENSE TEMPLATE

        ---
        RESULT: LICENSE TEMPLATE
        """

        # STRINGS
        text_for_title = self.parent.str_val.string_values(
            "ru_license_part_one"
        )
        text_for_copyright = self.parent.str_val.string_values(
            "license_part_zero"
        )
        text_for_zero = self.parent.str_val.string_values(
            "ru_license_part_two"
        )
        text_for_one = self.parent.str_val.string_values(
            "ru_license_part_three"
        )
        text_for_two = self.parent.str_val.string_values(
            "ru_license_part_four"
        )

        # MODAL WINDOW
        self.setWindowTitle(text_for_title)
        self.setStyleSheet("background-color: #404040;")
        self.setFixedSize(675, 500)

        frame = QFrame()
        frame.setObjectName("header_modal_license")

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

        checkbox_layout = QHBoxLayout()
        checkbox_layout.setContentsMargins(0, 0, 0, 0)
        checkbox_layout.setSpacing(0)
        checkbox_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)

        checkbox = QCheckBox()
        checkbox.setObjectName("settings_checkboxes")
        checkbox.setFont(QFont("Ubuntu"))
        checkbox.setChecked(checked)
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
            "ru_settings_main"
        )
        text_for_main_title = self.parent.str_val.strings_values_idx(
            "ru_settings_main_title", 2
        )
        text_for_main_list = self.parent.str_val.strings_values_idx(
            "ru_settings_main_list", 2, 4
        )
        text_for_main_dash = self.parent.str_val.strings_values_idx(
            "ru_settings_main_dash", 1
        )
        text_for_title_punctuations = self.parent.str_val.string_values(
            "ru_settings_main_title_punctuations"
        )
        text_for_hint_punctuations = self.parent.str_val.string_values(
            "ru_settings_main_hint_punctuations"
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
            (text_for_main_list[0][0], "settings_checkboxes_find"),
            (text_for_main_list[2], "settings_checkboxes_two_part"),
            (text_for_main_list[0][1], "settings_checkboxes_find")
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

    @Slot()
    def save_settings(self) -> None:
        """
        Saving NEW DATA to 1 SETTINGS FILE
        """

        # STRINGS
        text_for_success_msg_save_title = self.parent.str_val.string_values(
            "ru_success_msg_save_settings_title"
        )
        text_for_success_msg_save_text = self.parent.str_val.string_values(
            "ru_success_msg_save_settings_text"
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

        new_data = {
            "title": main_title.isChecked(),
            "list": main_list.isChecked(),
            "dash": main_dash.isChecked(),
            "block": main_textbox_set_list
        }

        filesystem = FileSystem(self.parent.parent.basedir)
        filesystem.write_file_settings(new_data)
        self.parent.parent.data_settings_file = new_data
        self.punctuations.setText(" ".join(main_textbox_set_list))

        MessageBox(  # SUCCESS
            "app/icons/success.svg",
            text_for_success_msg_save_title,
            text_for_success_msg_save_text,
            self
        )

# --------------------------------------
