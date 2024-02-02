# Developer && Owner: МогучийДД (MoguchiyDD)
# LICENSE: MIT License which is located in the text file LICENSE
#
# Goal: Contain All The DIFFERENT ANIMATIONS of The SOFTWARE
# Result: Finished WORKING ANIMATIONS
#
# Past Modification: Renaming «AnimationText» to «AnimationTextEdit»
# Last Modification: Editing The «AnimationTextEdit» CLASS (DOCS)
# Modification Date: 2024.02.02, 05:23 PM
#
# Create Date: 2024.01.31, 12:31 AM


from PySide6.QtCore import (
    Slot,
    QTimer,
    QPropertyAnimation,
    QSequentialAnimationGroup
)
from PySide6.QtGui import QTextCursor
from PySide6.QtWidgets import QWidget, QTextEdit


# ------------ ANIMATION 2ND TEXTBOX ------------

class AnimationTextEdit(QWidget):
    """
    Responsible for The ANIMATION of TEXT in 1 TEXTBOX

    ---
    PARAMETERS:
    - textbox: QTextEdit -> The TEXTBOX
    ---
    FUNCTIONS:
    - animation() -> None : RUNS to an ANIMATION
    """

    def __init__(self, textbox: QTextEdit) -> None:
        super(AnimationTextEdit, self).__init__()
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
        self.animation()

        # DURATION : START && END
        durations = self.s_duration_anim_text + self.e_duration_anim_text

        self.timer_text = QTimer()
        self.timer_text.setInterval(durations)
        self.timer_text.timeout.connect(self.animation)

    def __start_animation(self) -> None:
        """
        An ANIMATION that goes from TEXT POSITION 0 to The LAST POSITION
        """

        self.s_duration_anim_text = self.doc_textbox.blockCount() * 1000 / 2

        self.s_anim_text.stop()
        self.s_anim_text.setStartValue(0)
        self.s_anim_text.setEndValue(self.doc_textbox.blockCount())
        self.s_anim_text.setDuration(self.s_duration_anim_text)

        return self.s_anim_text

    def __end_animation(self) -> None:
        """
        An ANIMATION that goes from TEXT POSITION The LAST POSITION to 0
        """

        self.e_duration_anim_text = self.doc_textbox.blockCount() * 10 / 2

        self.e_anim_text.stop()
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
