import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QDialog, QMessageBox, QDialog
from PyQt5.QtCore import QDate
from pyexpat.errors import messages
import resources_rc  # Import Icons
from Student_management import Ui_MainWindow  # File giao diện gốc (auto-generated)
from function_dialog import Ui_Dialog  # File giao diện cập nhật sinh viên
from config_ui import TableHelper  # File xử lí giao diện khó
from database import CsvData, Student # file lưu trữ data sinh viên, load csv

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.function_dialog = Ui_Dialog()

        self.database = CsvData()
        # Load dữ liệu ngay khi mở
        self.load_data_to_table()
        # Thêm dữ liệu
        self.ui.btn_add_student.clicked.connect(self.add_student_from_table)

    def load_data_to_table(self):
        table = self.ui.studentsTableWidget
        # --- TỐI ƯU HÓA TỐC ĐỘ ---
        table.setSortingEnabled(False)  # Tắt sắp xếp (quan trọng nhất)
        table.setRowCount(0)  # Xóa sạch bảng
        # -------------------------
        list_students = self.database.list_students
        for row_index, student in enumerate(list_students):
            table.insertRow(row_index)
            #Thêm thông tin sinh viên
            table.setItem(row_index, 0, QTableWidgetItem(student.ID))
            table.setItem(row_index, 1, QTableWidgetItem(student.full_name))
            table.setItem(row_index, 2, QTableWidgetItem(student.DateOfBirth))
            table.setItem(row_index, 3, QTableWidgetItem(student.Gender))
            table.setItem(row_index, 4, QTableWidgetItem(student.Class))
            table.setItem(row_index, 5, QTableWidgetItem(f"{student.GPA:.2f}"))
            #Thêm nút xóa, sửa
            TableHelper.add_button_to_tableWidget(self, self.ui.studentsTableWidget, row_index, 6,
                                                  student, self.edit_student_from_table, self.delete_student_from_table)
        table.setSortingEnabled(True) # Bật lại sắp xếp để user bấm vào tiêu đề cột

    def get_data_dialog(self):
        ID = self.function_dialog.lineEdit_ID.text().strip()
        full_name = self.function_dialog.lineEdit_fullName.text().strip()
        DateOfBirth = self.function_dialog.dateEdit_DateBirth.text().strip()
        Gender = self.function_dialog.comboBox_gender.currentText().strip()
        Class = self.function_dialog.lineEdit_class.text().strip()
        GPA = self.function_dialog.lineEdit_GPA.text().strip()
        return Student( ID, full_name, DateOfBirth, Gender, Class, GPA)

    def add_student_from_table(self):
        #load giao diện thêm, sửa sinh viên ( function_dialog )
        dialog_window = QDialog()
        self.function_dialog.setupUi(dialog_window)
        def check_data() :
            try :
                new_student = self.get_data_dialog()
                succes , message = self.database.check_data_dialog(new_student)
                if succes :
                    message = self.database.add_student(new_student)
                    QMessageBox.information(self, "Thông báo" , message)
                    dialog_window.accept()
                    self.load_data_to_table()
                else:
                    QMessageBox.critical(dialog_window, "Lỗi" , message)
            except Exception as e :
                QMessageBox.warning(dialog_window, "Dữ liệu không hợp lệ" , str(e))

        # Bấm nút hủy thoát khỏi giao diện
        self.function_dialog.btn_cancel.clicked.connect( dialog_window.reject )
        # Ngắt kết nối cũ tránh bấm 1 lần thành 2 lần
        try:
            self.function_dialog.btn_update_infor.clicked.disconnect()
        except:
            pass
        self.function_dialog.btn_update_infor.clicked.connect( check_data )
        #-----Hiên thị dialog_window---------
        dialog_window.exec_()

    def edit_student_from_table(self):
        # load dialog lên để chỉnh sửa thông tin
        dialog_window = QDialog()
        self.function_dialog.setupUi(dialog_window)

        sender_button = self.sender() # để biết mình ấn vào nút edit nào
        old_student = sender_button.inf_student # lấy thông tin student cần sửa
        # điền thông tin student cần sửa lên dialog
        dialog_window.lineEdit_ID.setText(old_student.ID)
        dialog_window.lineEdit_fullName.setText(old_student.full_name)
        dialog_window.lineEdit_GPA.setText(old_student.DateOfBirth)
        dialog_window.lineEdit_gender.setText(old_student.gender)
        dialog_window.lineEdit_class.setText(old_student.Class)
        dialog_window.lineEdit_ID.setText(old_student.GPA)

        try :
            new_student = self.get_data_dialog()
            succes , message = self.database.check_data_dialog(new_student)
            if succes :
                message = self.database.edit_student(new_student, old_student)
                QMessageBox.information(self, "Thông báo" , message)
                dialog_window.accept()
                self.load_data_to_table()
            else:
                QMessageBox.critical(self, "Lỗi" , message)
        except Exception as e:
            QMessageBox.warning(dialog_window, "Dữ liệu không hợp lệ", str(e))

        dialog_window.exec_()

    def delete_student_from_table(self):
        pass

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())