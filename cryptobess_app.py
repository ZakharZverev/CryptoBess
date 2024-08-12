import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QLineEdit, QMessageBox, QRadioButton, QTextEdit

def caesar_cipher_coder(message, filename):
    with open("{0}.txt".format(filename), 'w') as f:
        for j in range(len(message)):
            f.write(str(1+ord(message[j]))+'\n')

def zverev_cipher_coder(codeword, message, filename):
    with open("{0}.txt".format(filename), 'w') as f:
        for j in range(len(message)):
            i=j%len(codeword)
            f.write(str(ord(codeword[i])+ord(message[j]))+'\n')

def caesar_cipher_decoder(filename):
    message=''
    with open("{0}.txt".format(filename), 'r') as f:
        for line_number, line in enumerate(f, 0):
            message+=chr(int(line)-1)
    return message


def zverev_cipher_decoder(codeword, filename):
    message=''
    with open("{0}.txt".format(filename), 'r') as f:
        for line_number, line in enumerate(f, 0):
            i=line_number%len(codeword)
            message+=chr(int(line)-ord(codeword[i]))
    return message

class CipherWindow(QWidget):
    def __init__(self, cipher_type):
        super().__init__()
        self.setWindowTitle(f"{cipher_type.upper()} Window")
        self.setGeometry(100, 100, 400, 350)

        layout = QVBoxLayout()

        self.cipher_type_label = QLabel("Choose Cipher Type:")
        self.caesar_radio = QRadioButton("Caesar (no codeword needed)")
        self.zverev_radio = QRadioButton("Zverev")

        self.codeword_label = QLabel("Codeword:")
        self.codeword_input = QLineEdit()

        if cipher_type == "cipher":
            self.message_label = QLabel("Message:")
            self.message_input = QLineEdit()

            self.filename_label = QLabel("Filename:")
            self.filename_input = QLineEdit()

            self.cipher_button = QPushButton("CIPHER")
            self.cipher_button.clicked.connect(self.cipher_action)

            layout.addWidget(self.cipher_type_label)
            layout.addWidget(self.caesar_radio)
            layout.addWidget(self.zverev_radio)
            layout.addWidget(self.codeword_label)
            layout.addWidget(self.codeword_input)
            layout.addWidget(self.message_label)
            layout.addWidget(self.message_input)
            layout.addWidget(self.filename_label)
            layout.addWidget(self.filename_input)
            layout.addWidget(self.cipher_button)

        elif cipher_type == "decipher":
            self.filename_label = QLabel("Filename:")
            self.filename_input = QLineEdit()

            self.decipher_button = QPushButton("DECIPHER")
            self.decipher_button.clicked.connect(self.decipher_action)

            self.output_label = QLabel("Deciphered Output:")
            self.output_text = QTextEdit()
            self.output_text.setReadOnly(True)

            layout.addWidget(self.cipher_type_label)
            layout.addWidget(self.caesar_radio)
            layout.addWidget(self.zverev_radio)
            layout.addWidget(self.codeword_label)
            layout.addWidget(self.codeword_input)
            layout.addWidget(self.filename_label)
            layout.addWidget(self.filename_input)
            layout.addWidget(self.decipher_button)
            layout.addWidget(self.output_label)
            layout.addWidget(self.output_text)

        self.setLayout(layout)

    def cipher_action(self):
        message = self.message_input.text()
        filename = self.filename_input.text()

        if not message or not filename:
            QMessageBox.warning(self, "Error", "Please fill in all the fields.")
            return

        if self.caesar_radio.isChecked():
            caesar_cipher_coder(message, filename)
        elif self.zverev_radio.isChecked():
            codeword = self.codeword_input.text()
            if not codeword:
                QMessageBox.warning(self, "Error", "Please fill in the codeword field.")
                return
            zverev_cipher_coder(codeword, message, filename)
        else:

            QMessageBox.warning(self, "Error", "Please select a cipher type.")
            return

    def decipher_action(self):
        filename = self.filename_input.text()

        if not filename:
            QMessageBox.warning(self, "Error", "Please fill in the filename field.")
            return

        if self.caesar_radio.isChecked():
            deciphered_text = caesar_cipher_decoder(filename)
        elif self.zverev_radio.isChecked():
            codeword = self.codeword_input.text()
            if not codeword:
                QMessageBox.warning(self, "Error", "Please fill in the codeword field.")
                return
            deciphered_text = zverev_cipher_decoder(codeword, filename)
        else:
            QMessageBox.warning(self, "Error", "Please select a cipher type.")
            return

        self.output_text.setText(deciphered_text)

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Cipher/Decipher Program")
        self.setGeometry(100, 100, 300, 200)

        layout = QVBoxLayout()

        self.cipher_button = QPushButton("CIPHER")
        self.cipher_button.clicked.connect(lambda: self.open_cipher_window("cipher"))

        self.decipher_button = QPushButton("DECIPHER")
        self.decipher_button.clicked.connect(lambda: self.open_cipher_window("decipher"))

        layout.addWidget(self.cipher_button)
        layout.addWidget(self.decipher_button)

        self.setLayout(layout)

    def open_cipher_window(self, cipher_type):
        self.cipher_window = CipherWindow(cipher_type)
        self.cipher_window.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())
