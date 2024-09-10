import sys
import sqlite3
import bcrypt
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLineEdit, QVBoxLayout, QLabel, QHBoxLayout, QFormLayout

def init_db():
    conn = sqlite3.connect('passwords.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS accounts (
            id INTEGER PRIMARY KEY,
            website TEXT NOT NULL,
            username TEXT NOT NULL,
            password TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

class PasswordHasher(QWidget):
    def __init__(self):
        super().__init__()
        init_db()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        # Form layout for user inputs
        form_layout = QFormLayout()
        self.website_input = QLineEdit()
        self.username_input = QLineEdit()
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        form_layout.addRow('Website:', self.website_input)
        form_layout.addRow('Username:', self.username_input)
        form_layout.addRow('Password:', self.password_input)
        layout.addLayout(form_layout)

        # Hash button
        self.hash_button = QPushButton('Hash and Save Password')
        self.hash_button.clicked.connect(self.save_password)
        layout.addWidget(self.hash_button)

        # Display hashed password
        self.hashed_password_label = QLabel("Hashed password will appear here")
        layout.addWidget(self.hashed_password_label)

        self.setLayout(layout)
        self.setWindowTitle('Password Hasher App')

    def save_password(self):
        website = self.website_input.text()
        username = self.username_input.text()
        password = self.password_input.text().encode('utf-8')
        hashed = bcrypt.hashpw(password, bcrypt.gensalt())

        # Display the hashed password
        self.hashed_password_label.setText(hashed.decode('utf-8'))

        # Save the data to the database
        conn = sqlite3.connect('passwords.db')
        c = conn.cursor()
        c.execute('INSERT INTO accounts (website, username, password) VALUES (?, ?, ?)', (website, username, password.decode('utf-8')))
        conn.commit()
        conn.close()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = PasswordHasher()
    ex.show()
    sys.exit(app.exec_())
