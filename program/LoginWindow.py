from PyQt6.QtWidgets import QDialog, QLineEdit, QVBoxLayout, QPushButton, QLabel
import sys
import requests as rq
import GlobalVariableAccess as gva

class Login(QDialog):
    def __init__(self):
        super().__init__()
        # window attributes
        self.setWindowTitle("Agent Info")
        self.resize(300, 150)

        self.layout = QVBoxLayout()
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Agent: ")
        self.layout.addWidget(self.username_input)

        self.message = QLabel()
        self.layout.addWidget(self.message)

        self.login_btn = QPushButton("Enter")
        self.login_btn.clicked.connect(self.verify_code)
        self.layout.addWidget(self.login_btn)

        self.setLayout(self.layout)

    def verify_code(self):
        try:
            data = rq.get("https://api.spacetraders.io/v2/my/agent", headers = {"Authorization": "Bearer " + self.username_input.text()})
            if ("error" in data.json()):
                raise ValueError("No ID")
        except Exception as e:
            print("login failure, unable to find agent token")
            print(e)
            self.message.setText("❌ Invalid token")
        else:
            print("login successful")
            gva.current_auth_token = self.username_input.text()
            self.accept()