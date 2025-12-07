import sys
import math
import re  # Quan trọng: Import thư viện xử lý chuỗi
from datetime import datetime

# --- KHỐI IMPORT QUAN TRỌNG ---
try:
    from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QDialog, QMessageBox
    from PyQt5.QtCore import QDate, Qt
except ImportError as e:
    print(f"LỖI NGHIÊM TRỌNG: Không tìm thấy thư viện PyQt5. Hãy chạy 'pip install PyQt5'. Chi tiết: {e}")
    sys.exit(1)

# --- IMPORT CÁC FILE TRONG DỰ ÁN ---
try:
    # Nếu báo lỗi ở đây -> Chạy lệnh: pyrcc5 resources.qrc -o resources_rc.py
    import resources_rc
    from Student_management import Ui_MainWindow
    from function_dialog import Ui_Dialog
    from config_ui import TableHelper
    from database import CsvData, Student
except ImportError as e:
    print(f"LỖI IMPORT FILE DỰ ÁN: {e}")
    print("Gợi ý: Kiểm tra xem đã chạy lệnh 'pyrcc5' chưa hoặc file database.py có lỗi không.")
    sys.exit(1)


# --- CLASS 1: Xử lý sắp xếp cột ID (Số ra số, chữ ra chữ) ---
class IDWidgetItem(QTableWidgetItem):
    def __lt__(self, other):
        # Chốt chặn 1: Kiểm tra nếu ô kia bị rỗng (None)
        if (not other) or (not hasattr(other, 'text')):
            return False

        try:
            text1 = self.text()
            text2 = other.text()
            # Hàm tách chuỗi: "SV10" -> ['SV', 10]
            def natural_keys(text):
                if not text: return []
                # Tách phần số và phần chữ riêng biệt
                return [int(c) if c.isdigit() else c.lower() for c in re.split(r'(\d+)', text)]

            return natural_keys(text1) < natural_keys(text2)
        except Exception:
            # Chốt chặn 2: Nếu lỗi logic, dùng so sánh chuỗi mặc định để không bị crash app
            return self.text() < other.text()


# --- CLASS 2: Xử lý sắp xếp cột Ngày Sinh ---
class DateWidgetItem(QTableWidgetItem):
    def __lt__(self, other):
        if (not other) or (not hasattr(other, 'text')):
            return False

        try:
            date_str1 = self.text().strip()
            date_str2 = other.text().strip()
            # Chuyển chuỗi sang ngày tháng
            date1 = datetime.strptime(date_str1, '%d/%m/%Y')
            date2 = datetime.strptime(date_str2, '%d/%m/%Y')
            return date1 < date2
        except ValueError:
            return self.text() < other.text()


# --- CLASS CHÍNH: MAIN WINDOW ---
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.function_dialog = Ui_Dialog()
        self.database = CsvData()  # Load CSV
        self.table_helper = TableHelper()  # Class hỗ trợ thêm nút

        # Biến quản lý phân trang và tìm kiếm
        self.list_search = None  # Mặc định là None (không tìm gì)
        self.current_page = 1
        self.limit = 20
        self.total_pages = 1

        # Gán sự kiện cho các nút
        self.ui.btn_prev.clicked.connect(self.prev_page)
        self.ui.btn_next.clicked.connect(self.next_page)
        self.ui.btn_add_student.clicked.connect(self.add_student_from_table)
        self.ui.lineEdit_search_student.textChanged.connect(self.search_student)

        # Load dữ liệu lần đầu
        self.load_data_to_table()

    def load_data_to_table(self, data_list=None):
        """Hàm hiển thị dữ liệu lên bảng (Có phân trang)"""
        # 1. Xác định danh sách cần hiển thị
        if data_list is None:
            list_students = self.database.list_students
        else:
            list_students = data_list

        # 2. Tính toán phân trang
        total_items = len(list_students)
        self.total_pages = math.ceil(total_items / self.limit)
        if self.total_pages == 0: self.total_pages = 1

        # Đảm bảo trang hiện tại hợp lệ
        if self.current_page > self.total_pages: self.current_page = self.total_pages
        if self.current_page < 1: self.current_page = 1

        # 3. Lấy dữ liệu của trang hiện tại
        start_index = (self.current_page - 1) * self.limit
        end_index = start_index + self.limit
        page_student = list_students[start_index:end_index]

        # 4. Hiển thị lên bảng
        table = self.ui.studentsTableWidget
        table.setSortingEnabled(False)  # Tắt sort để tránh lỗi khi đang insert
        table.setRowCount(0)  # Xóa bảng cũ

        for row_index, student in enumerate(page_student):
            table.insertRow(row_index)
            # Cột 0: ID (Dùng IDWidgetItem để sort đúng)
            table.setItem(row_index, 0, IDWidgetItem(student.ID))
            # Cột 1: Tên
            table.setItem(row_index, 1, QTableWidgetItem(student.full_name))
            # Cột 2: Ngày sinh (Dùng DateWidgetItem)
            table.setItem(row_index, 2, DateWidgetItem(student.DateOfBirth))
            # Cột 3, 4, 5
            table.setItem(row_index, 3, QTableWidgetItem(student.Gender))
            table.setItem(row_index, 4, QTableWidgetItem(student.Class))
            try:
                gpa_val = float(student.GPA)
            except:
                gpa_val = 0.0
            table.setItem(row_index, 5, QTableWidgetItem(f"{gpa_val:.2f}"))

            # Cột 6: Các nút chức năng
            self.table_helper.add_button_to_tableWidget(table, row_index, 6,
                                                        student, self.edit_student_from_table,
                                                        self.delete_student_from_table)

        table.setSortingEnabled(True)  # Bật lại sort

        # 5. Cập nhật UI phân trang
        self.ui.lbl_page_info.setText(f"Trang {self.current_page} / {self.total_pages}")
        self.ui.btn_prev.setEnabled(self.current_page > 1)
        self.ui.btn_next.setEnabled(self.current_page < self.total_pages)

    def prev_page(self):
        if self.current_page > 1:
            self.current_page -= 1
            self.load_data_to_table(self.list_search)

    def next_page(self):
        if self.current_page < self.total_pages:
            self.current_page += 1
            self.load_data_to_table(self.list_search)

    def get_data_dialog(self):
        # Lấy dữ liệu từ Form nhập liệu
        ID = self.function_dialog.lineEdit_ID.text().strip()
        full_name = self.function_dialog.lineEdit_fullName.text().strip()
        # Sửa lỗi lấy ngày tháng: Dùng text() thay vì date() để lấy chuỗi hiển thị
        DateOfBirth = self.function_dialog.dateEdit_DateBirth.text().strip()
        Gender = self.function_dialog.comboBox_gender.currentText().strip()
        Class = self.function_dialog.lineEdit_class.text().strip()
        GPA = self.function_dialog.lineEdit_GPA.text().strip()
        return Student(ID, full_name, DateOfBirth, Gender, Class, GPA)

    def add_student_from_table(self):
        dialog_window = QDialog()
        self.function_dialog.setupUi(dialog_window)

        # Reset form
        self.function_dialog.lineEdit_ID.setText("")
        self.function_dialog.lineEdit_fullName.setText("")
        self.function_dialog.lineEdit_class.setText("")
        self.function_dialog.lineEdit_GPA.setText("")
        self.function_dialog.dateEdit_DateBirth.setDate(QDate.currentDate())

        def save_student():
            try:
                new_student = self.get_data_dialog()
                succes, message = self.database.add_student(new_student)
                if succes:
                    QMessageBox.information(self, "Thông báo", message)
                    # Nếu đang không tìm kiếm thì reset về trang cuối để thấy SV mới
                    if self.list_search is None:
                        self.current_page = self.total_pages
                    self.load_data_to_table(self.list_search)
                    dialog_window.accept()
                else:
                    QMessageBox.critical(dialog_window, "Lỗi", message)
            except Exception as e:
                QMessageBox.warning(dialog_window, "Dữ liệu không hợp lệ", str(e))

        self.function_dialog.btn_cancel.clicked.connect(dialog_window.reject)
        self.function_dialog.btn_update_infor.clicked.connect(save_student)
        dialog_window.exec_()

    def edit_student_from_table(self):
        dialog_window = QDialog()
        self.function_dialog.setupUi(dialog_window)

        sender_button = self.sender()
        if not sender_button: return
        old_student = sender_button.property("inf_student")

        # Điền dữ liệu cũ lên form
        self.function_dialog.lineEdit_ID.setText(old_student.ID)
        self.function_dialog.lineEdit_fullName.setText(old_student.full_name)
        try:
            qdate = QDate.fromString(old_student.DateOfBirth, "dd/MM/yyyy")
            self.function_dialog.dateEdit_DateBirth.setDate(qdate)
        except:
            pass
        self.function_dialog.comboBox_gender.setCurrentText(old_student.Gender)
        self.function_dialog.lineEdit_class.setText(old_student.Class)
        self.function_dialog.lineEdit_GPA.setText(f"{float(old_student.GPA):.2f}")

        def save_student():
            try:
                new_student = self.get_data_dialog()
                succes, message = self.database.edit_student(new_student, old_student)
                if succes:
                    QMessageBox.information(self, "Thông báo", message)
                    self.load_data_to_table(self.list_search)
                    dialog_window.accept()
                else:
                    QMessageBox.critical(dialog_window, "Lỗi", message)
            except Exception as e:
                QMessageBox.warning(dialog_window, "Dữ liệu không hợp lệ", str(e))

        self.function_dialog.btn_cancel.clicked.connect(dialog_window.reject)
        self.function_dialog.btn_update_infor.clicked.connect(save_student)
        dialog_window.exec_()

    def delete_student_from_table(self):
        sender_button = self.sender()
        if not sender_button: return
        student = sender_button.property("inf_student")

        reply = QMessageBox.question(
            self, "Xác nhận xóa",
            f"Bạn có chắc chắn muốn xóa: {student.full_name}?",
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )
        if reply == QMessageBox.Yes:
            success, message = self.database.delete_student(student)
            if success:
                QMessageBox.information(self, "Thành công", message)
                # Nếu trang hiện tại trống sau khi xóa thì lùi lại 1 trang
                self.load_data_to_table(self.list_search)
            else:
                QMessageBox.warning(self, "Lỗi", message)

    def search_student(self):
        keyword = self.ui.lineEdit_search_student.text().strip().lower()

        if keyword == "":
            self.list_search = None
        else:
            self.list_search = []
            for student in self.database.list_students:
                if (keyword in student.ID.lower() or
                        keyword in student.full_name.lower() or
                        keyword in student.Class.lower()):
                    self.list_search.append(student)

        self.current_page = 1  # Reset về trang 1 khi tìm kiếm
        self.load_data_to_table(self.list_search)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())