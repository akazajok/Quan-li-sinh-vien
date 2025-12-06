import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QDialog, QMessageBox, QDialog
from PyQt5.QtCore import QDate

from Student_management import Ui_MainWindow  # File giao diện gốc (auto-generated)
from function_dialog import Ui_Dialog # file # File giao diện cập nhật sinh viên
from config_ui import TableHelper  # File trợ lý bạn vừa tạo
from database import CsvData, Student

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.function_dialog = Ui_Dialog()

        self.database = CsvData()
        self.list_student = self.database.get_data_Csv()
        # Load dữ liệu ngay khi mở
        self.load_data_to_table()
        # Thêm dữ liệu
        self.ui.btn_add_student.clicked.connect(self.add_student_to_table)

    def load_data_to_table(self):
        table = self.ui.studentsTableWidget
        # --- TỐI ƯU HÓA TỐC ĐỘ ---
        table.setSortingEnabled(False)  # Tắt sắp xếp (quan trọng nhất)
        table.setRowCount(0)  # Xóa sạch bảng
        # -------------------------
        for row_index, student in enumerate(self.list_student):
            table.insertRow(row_index)
            #Thêm thông tin sinh viên
            table.setItem(row_index, 0, QTableWidgetItem(student.ID))
            table.setItem(row_index, 1, QTableWidgetItem(student.full_name))
            table.setItem(row_index, 2, QTableWidgetItem(student.DateOfBirth))
            table.setItem(row_index, 3, QTableWidgetItem(student.Gender))
            table.setItem(row_index, 4, QTableWidgetItem(student.Class))
            table.setItem(row_index, 5, QTableWidgetItem(f"{student.GPA:.2f}"))
            #Thêm nút xóa, sửa
            TableHelper.add_button_to_tableWidget(self, self.ui.studentsTableWidget, row_index, 6)
        table.setSortingEnabled(True) # Bật lại sắp xếp để user bấm vào tiêu đề cột

    def get_raw_data(self):
        ID = self.function_dialog.lineEdit_ID.text().strip()
        full_name = self.function_dialog.lineEdit_fullName.text().strip()
        DateOfBirth = self.function_dialog.dateEdit_DateBirth.text().strip()
        Gender = self.function_dialog.comboBox_gender.currentText().strip()
        Class = self.function_dialog.lineEdit_class.text().strip()
        GPA = self.function_dialog.lineEdit_GPA.text().strip()
        return ID, full_name, DateOfBirth, Gender, Class, GPA

    def add_student_to_table(self):
        #load giao diện thêm, sửa sinh viên ( function_dialog )
        dialog_window = QDialog()
        self.function_dialog.setupUi(dialog_window)
        def check_data() :
            id, full_name, dob, gender, Class, GPA = self.get_raw_data()
            if not id or not full_name or not Class or not GPA :
                QMessageBox.warning( dialog_window, "Cảnh báo" , "Vui lòng nhập ĐẦY ĐỦ thông tin sinh viên")
                return

            for inf in self.list_student:
                if id == inf.ID :
                    QMessageBox.critical( dialog_window, "Lỗi" , f"Mã sinh viên {inf.ID} đã tồn tại!")
                    return
            student = Student(id, full_name, dob, gender, Class, GPA)
            self.list_student.append(student)
            self.database.add_student_to_csv(student)
            self.load_data_to_table()
            QMessageBox.information(self, "Thông báo" , "Thêm sinh viên thành công")
            dialog_window.accept() #Đóng dialog

        # Bấm nút hủy thoát khỏi giao diện
        self.function_dialog.btn_cancel.clicked.connect( dialog_window.reject)
        # Cập nhật sinh viên
        try:
            self.function_dialog.btn_update_infor.clicked.disconnect()
        except:
            pass
        self.function_dialog.btn_update_infor.clicked.connect( check_data )
        #-----Hiên thị dialog_window---------
        dialog_window.exec_()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())