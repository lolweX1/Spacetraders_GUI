import sys
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout,
    QLabel, QLineEdit, QPushButton, QCheckBox, QFrame
)
from PyQt6.QtCore import Qt, QSettings
from PyQt6.QtGui import QFont
import json
from Authorize import GET
 
def on_login(token: str, remember: bool):
    """
    Called when the Login button is clicked.
 
    Args:
        token:    The account token entered by the user.
        remember: True if the 'Remember account token' checkbox is checked.
    """
    data = GET("https://api.spacetraders.io/v2/my/account", token)
    if (data == None):
        print("Unable to get account data. The API may be down or your put in the wrong token")
    elif ("error" in data):
        print(data)
    else:
        if remember:
            with open("program/user_data.json", "r") as file:
                stored_data = json.load(file)
            stored_data["account-token"] = token
            with open("program/user_data.json", "w") as file:
                json.dump(stored_data, file, indent=4)
        # call the window creation function here here.
        print("Login Successful")
        print(data)

 
 
class LoginWindow(QWidget):
    SETTINGS_KEY = "account_token"
 
    def __init__(self):
        super().__init__()
        self.settings = QSettings("SpaceTraders", "Account Login Page")
        self.create_window()
        self._load_saved_token()
 
    #  UI construction                                                     #
    def create_window(self):
        self.setWindowTitle("Login")
        self.setFixedSize(420, 210)
        self._apply_theme()
 
        root = QVBoxLayout(self)
        root.setContentsMargins(40, 36, 40, 36)
        root.setSpacing(0)
 
        # — Token field label —
        lbl = QLabel("Account Token")
        lbl.setFont(QFont("Consolas", 8, QFont.Weight.Bold))
        lbl.setStyleSheet("color: #a09880; letter-spacing: 1px; margin-bottom: 5px;")
        root.addWidget(lbl)

        # check for initial login
        with open("program/user_data.json", "r") as file:
            login_info = json.load(file)["account-token"]
 
        # — Token input —
        self.token_input = QLineEdit()
        self.token_input.setPlaceholderText("Enter account token")
        self.token_input.setFont(QFont("Consolas", 10))
        self.token_input.setFixedHeight(40)
        self.token_input.setStyleSheet("""
            QLineEdit {
                background: #1a1814;
                border: 1px solid #3a352c;
                border-radius: 6px;
                color: #e8e0d4;
                padding: 0 12px;
            }
            QLineEdit:focus {
                border: 1px solid #c8a96e;
            }
        """)

        if (login_info != ""):
            self.token_input.setText(login_info)

        root.addWidget(self.token_input)
 
        root.addSpacing(12)
 
        # — Remember checkbox —
        self.remember_cb = QCheckBox("Remember token")
        self.remember_cb.setFont(QFont("Georgia", 9))
        self.remember_cb.setStyleSheet("""
            QCheckBox { color: #8a8070; spacing: 8px; }
            QCheckBox::indicator {
                width: 15px; height: 15px;
                border: 1px solid #3a352c;
                border-radius: 3px;
                background: #1a1814;
            }
            QCheckBox::indicator:checked {
                background: #c8a96e;
                border-color: #c8a96e;
            }
            QCheckBox:hover { color: #c8a96e; }
        """)
        root.addWidget(self.remember_cb)
 
        root.addSpacing(20)
 
        # — Login button —
        self.login_btn = QPushButton("Login")
        self.login_btn.setFixedHeight(42)
        self.login_btn.setFont(QFont("Georgia", 10, QFont.Weight.Bold))
        self.login_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.login_btn.setStyleSheet("""
            QPushButton {
                background: #c8a96e;
                color: #12100e;
                border: none;
                border-radius: 6px;
                letter-spacing: 1px;
            }
            QPushButton:hover  { background: #d4b87a; }
            QPushButton:pressed { background: #b8994e; }
        """)
        self.login_btn.clicked.connect(self._handle_login)
        root.addWidget(self.login_btn)
 
        # Allow Enter key to trigger login
        self.token_input.returnPressed.connect(self._handle_login)
 
    def _divider(self) -> QFrame:
        line = QFrame()
        line.setFrameShape(QFrame.Shape.HLine)
        line.setStyleSheet("color: #2a2520;")
        return line
 
    def _apply_theme(self):
        self.setStyleSheet("QWidget { background: #12100e; }")
 
    #  Logic                                                               #
    def _handle_login(self):
        token = self.token_input.text().strip()
        remember = self.remember_cb.isChecked()
 
        if remember:
            self.settings.setValue(self.SETTINGS_KEY, token)
        else:
            self.settings.remove(self.SETTINGS_KEY)
 
        on_login(token, remember)
 
    def _load_saved_token(self):
        saved = self.settings.value(self.SETTINGS_KEY, "")
        if saved:
            self.token_input.setText(saved)
            self.remember_cb.setChecked(True)