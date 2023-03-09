print("thanks for trusting data-finder")
import sys
from PyQt5.QtCore import QStandardPaths
from PyQt5.QtWidgets import QApplication, QLabel, QWidget, QPushButton, QLineEdit, QMessageBox
passwords = []
file_path = QStandardPaths.writableLocation(QStandardPaths.DocumentsLocation) + '/passwords.txt'
class PasswordManager(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # create a label to display the title
        title = QLabel('Password Manager, by data-finder', self)
        title.move(50, 50)
        title.resize(200, 30)

        # create a label for the username
        user_label = QLabel('Username:', self)
        user_label.move(50, 100)
        user_label.resize(80, 20)

        # create a text input for the username
        self.user_input = QLineEdit(self)
        self.user_input.move(130, 100)
        self.user_input.resize(150, 20)

        # create a label for the password
        password_label = QLabel('Password:', self)
        password_label.move(50, 150)
        password_label.resize(80, 20)

        # create a text input for the password
        self.password_input = QLineEdit(self)
        self.password_input.move(130, 150)
        self.password_input.resize(150, 20)
        self.password_input.setEchoMode(QLineEdit.Password)

        # create a button to save the password
        save_button = QPushButton('Save', self)
        save_button.move(50, 200)
        save_button.resize(80, 30)
        save_button.clicked.connect(self.savepass)

        # create a button to open the saved passwords window
        saved_passwords_button = QPushButton('Saved Passwords', self)
        saved_passwords_button.move(100, 250)
        saved_passwords_button.resize(150, 30)
        saved_passwords_button.clicked.connect(self.show_saved_passwords)

        # set the window title and size
        self.setWindowTitle('Password Manager')
        self.setGeometry(100, 100, 350, 300)
        self.show()

    def savepass(self):
        username = self.user_input.text()
        password = self.password_input.text()
        

        # check if the password is already saved under the same username
        file_path = QStandardPaths.writableLocation(QStandardPaths.DocumentsLocation) + '/passwords.txt'
        try:
            with open(file_path, 'r') as f:
                saved_passwords = f.read()
            for saved_password in saved_passwords.splitlines():
                saved_username, saved_password = saved_password.split(':')
                if saved_username == username and saved_password == password:
                    QMessageBox.warning(self, 'Warning', 'Same password found under the same username.')
                    return

        except FileNotFoundError:
            pass

        # save passwords to file
        with open(file_path, 'a') as f:
            f.write(f"{username}:{password}\n")
        
        passwords.append({'username': username, 'password': password})
        self.saved_passwords = Passwords()
        self.saved_passwords.show()

    def show_saved_passwords(self):
        self.saved_passwords = Passwords()
        self.saved_passwords.show()
class Passwords(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # create a label to display the title
        title = QLabel('Saved Passwords', self)
        title.move(50, 50)
        title.resize(200, 30)

        # create a label for the saved passwords
        self.passwords_label = QLabel(self)
        self.passwords_label.move(50, 100)
        self.passwords_label.resize(250, 200)
        # read passwords from file and update the label text
        self.update_passwords_label()

        delete_button = QPushButton('Delete Password', self)
        delete_button.move(50, 250)
        delete_button.resize(150, 30)
        delete_button.clicked.connect(self.delete_password)

    def update_passwords_label(self):
        try:
            with open(file_path, 'r') as f:
                self.passwords_label.setText(f.read())
        except FileNotFoundError:
            self.passwords_label.setText('No passwords saved yet.')

    def delete_password(self):
        passwords.clear()
        with open(file_path, "w") as f:
            f.write('')
        # update the passwords list widget
        self.passwords_label.setText("")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = PasswordManager()
    sys.exit(app.exec_())
