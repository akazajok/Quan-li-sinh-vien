import sys
import re

from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QDialog, QMessageBox, QDialog
from PyQt5.QtCore import QDate
from datetime import datetime
from pyexpat.errors import messages
import resources_rc  # Import Icons
from Student_management import Ui_MainWindow  # File giao diện gốc (auto-generated)
from function_dialog import Ui_Dialog  # File giao diện cập nhật sinh viên
from config_ui import TableHelper  # File xử lí giao diện khó
from database import CsvData, Student # file lưu trữ data sinh viên, load csv

class IDWidgetItem(QTableWidgetItem):
    def __lt__(self, other):
        try:
            # Hàm tách chuỗi thành các phần nhỏ: số ra số, chữ ra chữ
            # Ví dụ: "D21CNTT02" -> ['D', 21, 'CNTT', 2]
            def natural_keys(text):
                return [ int(c) if c.isdigit() else c.lower() for c in re.split(r'(\d+)', text) ]
            return natural_keys(self.text()) < natural_keys(other.text())
        except ValueError:
            # Nếu lỗi (ví dụ ô trống hoặc sai định dạng), dùng cách so sánh mặc định
            return super().__lt__(other)

class DateWidgetItem(QTableWidgetItem):
    def __lt__(self, other):
        try:
            # Lấy text của 2 ô đang so sánh
            date_str1 = self.text().strip()
            date_str2 = other.text().strip()
            # Chuyển đổi từ chuỗi "dd/MM/yyyy" sang đối tượng ngày tháng để so sánh
            # Nếu định dạng file csv của bạn khác, hãy sửa '%d/%m/%Y' tương ứng
            date1 = datetime.strptime(date_str1, '%d/%m/%Y')
            date2 = datetime.strptime(date_str2, '%d/%m/%Y')

            return date1 < date2
        except ValueError:
            # Nếu lỗi (ví dụ ô trống hoặc sai định dạng), dùng cách so sánh mặc định
            return super().__lt__(other)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.function_dialog = Ui_Dialog()

        self.database = CsvData()
        # Load dữ liệu ngay khi mở
        self.load_data_to_table()
        # Thêm dữ liệu sinh viên
        self.ui.btn_add_student.clicked.connect(self.add_student_from_table)
        # Tìm kiếm sinh viên
        self.ui.lineEdit_search_student.textChanged.connect(self.search_student)

    def load_data_to_table(self, data_list=None):
        table = self.ui.studentsTableWidget
        # --- TỐI ƯU HÓA TỐC ĐỘ ---
        table.setSortingEnabled(False)  # Tắt sắp xếp (quan trọng nhất)
        table.setRowCount(0)  # Xóa sạch bảng
        # -------------------------
        # Nếu không truyền dữ liệu vào (data_list là None) -> Lấy tất cả sinh viên
        if data_list is None:
            list_students = self.database.list_students
        else : # Nếu có truyền vào (kết quả tìm kiếm) -> Chỉ hiển thị danh sách đó
            list_students = data_list

        for row_index, student in enumerate(list_students):
            table.insertRow(row_index)
            #Thêm thông tin sinh viên
            table.setItem(row_index, 0, IDWidgetItem(student.ID))
            table.setItem(row_index, 1, QTableWidgetItem(student.full_name))
            table.setItem(row_index, 2, DateWidgetItem(student.DateOfBirth))
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
        def save_student() :
            try :
                new_student = self.get_data_dialog()
                succes , message = self.database.add_student(new_student)
                if succes :
                    QMessageBox.information(self, "Thông báo" , message)
                    self.load_data_to_table()
                    dialog_window.accept()
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
        self.function_dialog.btn_update_infor.clicked.connect( save_student )
        #-----Hiên thị dialog_window---------
        dialog_window.exec_()

    def edit_student_from_table(self):
        # load dialog lên để chỉnh sửa thông tin
        dialog_window = QDialog()
        self.function_dialog.setupUi(dialog_window)

        sender_button = self.sender() # để biết mình ấn vào nút edit nào
        old_student = sender_button.property("inf_student") # lấy thông tin student cần sửa
        # điền thông tin student cần sửa lên dialog
        self.function_dialog.lineEdit_ID.setText(old_student.ID)
        self.function_dialog.lineEdit_fullName.setText(old_student.full_name)
        try:
            # Chuyển chuỗi ngày (ví dụ "20/11/2005") thành đối tượng QDate
            # Lưu ý: "dd/MM/yyyy" phải khớp với định dạng ngày bạn lưu trong file CSV
            qdate = QDate.fromString(old_student.DateOfBirth, "dd/MM/yyyy")
            # Gán vào widget QDateEdit bằng lệnh setDate
            self.function_dialog.dateEdit_DateBirth.setDate(qdate)
        except Exception as e:
            print(f"Lỗi ngày tháng: {e}")
        self.function_dialog.comboBox_gender.setCurrentText(old_student.Gender)
        self.function_dialog.lineEdit_class.setText(old_student.Class)
        self.function_dialog.lineEdit_GPA.setText(f"{old_student.GPA:.2f}")
        def save_student() :
            try :
                new_student = self.get_data_dialog()
                succes , message = self.database.edit_student(new_student, old_student)
                if succes :
                    QMessageBox.information(self, "Thông báo" , message)
                    self.load_data_to_table()
                    dialog_window.accept()
                else:
                    QMessageBox.critical(self, "Lỗi" , message)
            except Exception as e:
                QMessageBox.warning(dialog_window, "Dữ liệu không hợp lệ", str(e))
        # btn_cancel đóng bảng dialog
        self.function_dialog.btn_cancel.clicked.connect( dialog_window.reject )
        # Ngắt kết nối cũ tránh bấm 1 lần thành 2 lần
        try :
            self.function_dialog.btn_update_infor.clicked.disconnect()
        except:
            pass
        self.function_dialog.btn_update_infor.clicked.connect( save_student )
        dialog_window.exec_()

    def delete_student_from_table(self):
        # 1. Lấy đối tượng sinh viên từ nút bấm (Sender)
        sender_button = self.sender()
        student = sender_button.property("inf_student")
        # 2. Hiển thị hộp thoại xác nhận (Quan trọng!)
        # QMessageBox.question(cha, tiêu_đề, nội_dung, nút_bấm)
        reply = QMessageBox.question(
            self,
            "Xác nhận xóa",
            f"Bạn có chắc chắn muốn xóa sinh viên:\n{student.full_name} (MSV: {student.ID})?\n\nHành động này không thể hoàn tác!",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No  # Mặc định chọn No để an toàn
        )
        # 3. Nêu muốn xóa thật
        if reply == QMessageBox.Yes:
            success, message = self.database.delete_student(student)
            if success:
                QMessageBox.information(self, "Thành công", message)
                self.load_data_to_table()
            else :
                QMessageBox.warning(self, "Lỗi", message)

    def search_student(self):
        # Từ khóa muốn tìm kiếm
        keyword = self.ui.lineEdit_search_student.text().strip().lower()
        results = [] # Tất cả student có liên quan
        for student in self.database.list_students:
            if keyword in student.ID.lower() or keyword in student.full_name.lower() or keyword in student.Class.lower():
                results.append(student)
        self.load_data_to_table(results)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())