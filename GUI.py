import os
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QFileDialog, QMessageBox, QLineEdit, QVBoxLayout
from PyQt5.QtGui import QFont
import PyPDF2

class NewWindow(QWidget):
    def __init__(self, parent):
        super().__init__()

        self.parent = parent

        self.setWindowTitle("New Window")
        self.setGeometry(300, 300, 315, 250)

        self.setStyleSheet("QWidget { background-color: black; border: 2px solid black; border-radius: 8px; }"
                           "QPushButton { background-color: #8F00FF; color: white; border: 2px solid #6F2DA8; padding: 10px; font-size: 14px; border-radius: 5px; }"
                           "QPushButton:hover { background-color: #6F2DA8; }")

        self.name_input = QLineEdit(self)
        self.name_input.setPlaceholderText("Enter your name")
        self.name_input.setStyleSheet("background-color: #FFFFCC; border: 2px solid #FF9900; padding: 5px;")

        self.email_input = QLineEdit(self)
        self.email_input.setPlaceholderText("Enter your email")
        self.email_input.setStyleSheet("background-color: #FFFFCC; border: 2px solid #FF9900; padding: 5px;")

        back_button = QPushButton("Back", self)
        back_button.clicked.connect(self.go_back)
        back_button.setGeometry(30, 70, 120, 50)

        exit_button = QPushButton("Exit", self)
        exit_button.clicked.connect(self.close)
        exit_button.setGeometry(160, 70, 120, 50)

        layout = QVBoxLayout(self)
        layout.addWidget(self.name_input)
        layout.addWidget(self.email_input)
        layout.addWidget(back_button)
        layout.addWidget(exit_button)

        self.setLayout(layout)
        

    def go_back(self):
        self.close()
        self.parent.show()

class MyWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.new_window = None

        self.setWindowTitle("Python GUI Test")
        self.setGeometry(150, 150, 315, 250)


        self.setStyleSheet("QWidget { background-color: black; border: 2px solid black; border-radius: 8px; }"
                           "QPushButton { background-color: #8F00FF; color: white; border: 2px solid #6F2DA8; padding: 10px; font-size: 14px; border-radius: 5px; }"
                           "QPushButton:hover { background-color: #6F2DA8; }") 

        self.init_ui()
    
    def init_ui(self):
        merge_button = QPushButton("Merge PDFs", self)
        merge_button.clicked.connect(self.show_file_dialog)
        merge_button.setGeometry(30, 70, 120, 50)

        exit_button = QPushButton("Exit", self)
        exit_button.clicked.connect(self.close)
        exit_button.setGeometry(160, 70, 120, 50)

        new_window_button = QPushButton("Open New Window", self)
        new_window_button.clicked.connect(self.open_new_window)
        new_window_button.setGeometry(30, 130, 250, 50)

        font = QFont()
        font.setPointSize(12)
        merge_button.setFont(font)
        exit_button.setFont(font)

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
    
    def open_new_window(self):
        self.new_window = NewWindow(self)
        self.new_window.show()
        self.close()

if __name__ == "__main__":
    app = QApplication([])
    window = MyWindow()
    window.show()
    app.exec_()