import sys
import time
import psutil
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QMessageBox, QVBoxLayout

class Window(QWidget):
    def __init__(self):
        super().__init__()

        self.is_suspended = False  # Flag to track suspension state
        self.initUI()

    def initUI(self):
        self.setWindowTitle("GTA V Lobby Clearer")

        self.button = QPushButton("Empty the Lobby! (Suspend GTA for 10 seconds)", self)
        self.button.clicked.connect(self.suspend_clicked)

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.button)
        self.setLayout(self.layout)

        self.show()

    def suspend_clicked(self):
        if self.is_suspended:
            self.show_message("Error", "GTA V is already suspended, please wait.")
        else:
            # Find the GTA5.exe process
            for proc in psutil.process_iter():
                if proc.name() == "GTA5.exe":
                    try:
                        # Suspend the process
                        proc.suspend()
                        self.is_suspended = True
                        self.button.setEnabled(False)
                        self.show_message("GTA V Suspended", "GTA V has been suspended for 10 seconds, please wait for the \"unsuspended\" message box before entering the game.")
                        # Wait for 10 seconds
                        time.sleep(10)
                        # Resume the process
                        proc.resume()
                        self.is_suspended = False
                        self.button.setEnabled(True)
                        self.show_message("GTA V Unsuspended", "GTA V has been unsuspended, the lobby should now be empty! :)")
                        return
                    except psutil.AccessDenied:
                        self.show_message("Error", "Unable to suspend GTA V.")
            self.show_message("Error", "GTA V process not found.")

    def show_message(self, title, text):
        msg = QMessageBox()
        msg.setWindowTitle(title)
        msg.setText(text)
        msg.exec_()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Window()
    window.resize(400, 200)  # Set initial size
    sys.exit(app.exec_())
