from PyQt5.QtWidgets import QApplication, QWidget, QMessageBox, QPushButton, QFileDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QFormLayout
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
import PyPDF2

class NewContractWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("New Contract")
        self.setGeometry(0, 0, 500, 500)

        self.setStyleSheet("QWidget { background-color: black; border: 2px solid black; border-radius: 8px; }"
                           "QPushButton { background-color: #8F00FF; color: white; border: 2px solid #6F2DA8; padding: 10px; font-size: 14px; border-radius: 5px; }"
                           "QPushButton:hover { background-color: #6F2DA8; }"
                           "QLabel { color: white; }"
                           "QLineEdit { background-color: white; border: 2px solid #6F2DA8; padding: 10px; border-radius: 5px; }")

        label_nume = QLabel("Nume:")
        label_prenume = QLabel("Prenume:")
        label_cnp = QLabel("CNP:")

        self.lineedit_nume = QLineEdit(self)
        self.lineedit_prenume = QLineEdit(self)
        self.lineedit_cnp = QLineEdit(self)

        self.lineedit_nume.setMaximumWidth(150)
        self.lineedit_prenume.setMaximumWidth(150)
        self.lineedit_cnp.setMaximumWidth(150)

        confirm_button = QPushButton("Confirm", self)
        confirm_button.clicked.connect(self.show_confirmation_message)

        layout = QFormLayout(self)
        layout.addRow(label_nume, self.lineedit_nume)
        layout.addRow(label_prenume, self.lineedit_prenume)
        layout.addRow(label_cnp, self.lineedit_cnp)

        self.setLayout(layout)

    def show_confirmation_message(self):
        QMessageBox.information(self, "Confirmation", "You added a new contract!")

class MyWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Python GUI Test")
        self.setGeometry(0, 0, 500, 500)

        self.setStyleSheet("QWidget { background-color: black; border: 2px solid black; border-radius: 8px; }"
                           "QPushButton { background-color: #8F00FF; color: white; border: 2px solid #6F2DA8; padding: 10px; font-size: 14px; border-radius: 5px; }"
                           "QPushButton:hover { background-color: #6F2DA8; }")

        self.init_ui()

    def init_ui(self):
        merge_button = QPushButton("Merge PDFs", self)
        merge_button.clicked.connect(self.show_file_dialog)

        new_contract_button = QPushButton("New Contract", self)
        new_contract_button.clicked.connect(self.open_new_contract_window)

        exit_button = QPushButton("Exit", self)
        exit_button.clicked.connect(self.close)
        
        font = QFont()
        font.setPointSize(12)

        merge_button.setFont(font)
        new_contract_button.setFont(font)
        exit_button.setFont(font)
        
        button_layout = QHBoxLayout()
        button_layout.addWidget(merge_button)
        button_layout.addWidget(new_contract_button)
        button_layout.addWidget(exit_button)

        layout = QVBoxLayout(self)
        layout.addLayout(button_layout)
        self.setLayout(layout)

    def show_file_dialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        options |= QFileDialog.DontUseNativeDialog

        file_dialog = QFileDialog()
        file_dialog.setOptions(options)
        file_dialog.setNameFilter("PDF Files (*.pdf)")
        file_dialog.setFileMode(QFileDialog.ExistingFiles)

        if file_dialog.exec_():
            selected_files = file_dialog.selectedFiles()
            self.merge_pdfs(selected_files)

    def merge_pdfs(self, pdf_files):
        if pdf_files:
            merger = PyPDF2.PdfMerger()
            for file in pdf_files:
                merger.append(file)

            output_file = QFileDialog.getSaveFileName(self, "Save merged PDF", filter="PDF Files (*.pdf)")
            if output_file[0]:
                with open(output_file[0], "wb") as merged_pdf:
                    merger.write(merged_pdf)

                QMessageBox.information(self, "Success", "PDFs merged successfully!")
            else:
                QMessageBox.warning(self, "Error", "Invalid output file name.")
        else:
            QMessageBox.warning(self, "No PDFs", "No PDF files selected.")
    
    def open_new_contract_window(self):
        self.new_contract_window = NewContractWindow()
        self.new_contract_window.show()

if __name__ == "__main__":
    app = QApplication([])
    window = MyWindow()
    window.show()
    app.exec_()