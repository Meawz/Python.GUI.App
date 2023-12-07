import os
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QFileDialog, QMessageBox
from PyQt5.QtGui import QFont
import PyPDF2



class MyWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Python GUI Test")
        self.setGeometry(150, 150, 315, 250)

        self.setStyleSheet("QWidget { background-color: black; }"
                           "QPushButton { background-color: #8F00FF; color: white; border: none; padding: 10px; font-size: 14px; border-radius: 5px; }"
                           "QPushButton:hover { background-color: #6F2DA8; }") 

        self.init_ui()
    
    def init_ui(self):
        merge_button = QPushButton("Merge PDFs", self)
        merge_button.clicked.connect(self.show_file_dialog)
        merge_button.setGeometry(30, 70, 120, 50)

        exit_button = QPushButton("Exit", self)
        exit_button.clicked.connect(self.close)
        exit_button.setGeometry(160, 70, 120, 50)

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

if __name__ == "__main__":
    app = QApplication([])
    window = MyWindow()
    window.show()
    app.exec_()