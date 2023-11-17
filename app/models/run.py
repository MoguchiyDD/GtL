
# Developer && Owner: МогучийДД (MoguchiyDD)
# LICENSE: MIT License which is located in the text file LICENSE
#
# Goal: Launching The SOFTWARE WINDOW
# Result: SOFTWARE WINDOW Open
#
# Past Modification: Checking CODE The PEP8
# Last Modification: Editing The «RUN» Block (REMOVING UNNECESSARY CODE)
# Modification Date: 2023.11.17, 11:37 AM
#
# Create Date: 2023.11.17, 12:18 AM


# ------------ RUN ------------

def run() -> None:
    """
    Launching The SOFTWARE WINDOW
    """

    from main import MainWindow  # Without ImportError

    window = MainWindow()
    window.show()

# -----------------------------
