import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QDialog, QMessageBox
from PyQt5.QtCore import QDate

from Student_management import Ui_MainWindow  # File giao diện gốc (auto-generated)
from function_dialog import Ui_Dialog # file # File giao diện cập nhật sinh viên
from config_ui import TableHelper  # File trợ lý bạn vừa tạo
from database import CsvData

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

    def add_student_to_table(self):
        #load giao diện thêm, sửa sinh viên ( function_dialog )
        self.function_dialog.setupUi(QDialog())
        def check_data() :
            student = self.database.add_student_to_csv()
            if ( not student.ID and not student.full_name and not student.DateOfBirth
            and not student.Gender and not student.Class):
                QMessageBox.warning( QDialog(), "Cảnh báo" , "Vui lòng nhập ĐẦY ĐỦ thông tin sinh viên")
                return

            for inf in self.list_student:
                if student.ID == inf.ID :
                    QMessageBox.critical( QDialog(), "Lỗi" , f"Mã sinh viên {inf.ID} đã tồn tại!")
                    return

            self.list_student.append(student)
            self.load_data_to_table()
            QMessageBox.information(self, "Thông báo" , "Thêm sinh viên thành công")
            QDialog().accept() #Đóng dialog
        # Bấm nút hủy thoát khỏi giao diện
        self.function_dialog.btn_cancel.clicked.connect( QDialog().reject)
        # Cập nhật sinh viên
        self.function_dialog.btn_update_infor.clicked.connect( check_data )
        #-----Hiên thị Dialog---------
        QDialog().exec_()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())