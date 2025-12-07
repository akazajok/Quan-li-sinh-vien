import os
import sys
import math
import re  # Quan trọng: Import thư viện xử lý chuỗi
from datetime import datetime
# --- BẮT BUỘC PHẢI CÓ KHI DÙNG MINICONDA ĐỂ CHẠY DEBUG ---
if os.name == 'nt':
    # Thay vì tìm biến môi trường, ta dùng sys.prefix để lấy đường dẫn gốc của Python hiện tại
    # Cách này hoạt động ổn định cả khi Run và Debug
    base_path = sys.prefix

    # Đường dẫn plugin chuẩn của Conda trên Windows
    plugin_path = os.path.join(base_path, 'Library', 'plugins', 'platforms')

    # Nếu không tìm thấy (ví dụ dùng Python thường không phải Conda), thử đường dẫn khác
    if not os.path.exists(plugin_path):
        plugin_path = os.path.join(base_path, 'Lib', 'site-packages', 'PyQt5', 'Qt5', 'plugins', 'platforms')

    if os.path.exists(plugin_path):
        os.environ['QT_QPA_PLATFORM_PLUGIN_PATH'] = plugin_path
# ---------------------------------------------------------
# --- KHỐI IMPORT QUAN TRỌNG ---
try:
    from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QDialog, QMessageBox
    from PyQt5.QtCore import QDate, Qt
    from PyQt5.QtWidgets import QVBoxLayout  # Cần thêm cái này để bố trí biểu đồ
    # --- Import thư viện vẽ biểu đồ ---
    from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
    import matplotlib.pyplot as plt
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

# Class dùng để tạo khung vẽ biểu đồ
class ChartCanvas(FigureCanvas):
    def __init__(self, parent=None):
        # Tạo đối tượng Figure của Matplotlib
        # figsize=(width, height), dpi=độ phân giải
        self.fig, self.ax = plt.subplots(figsize=(5, 4), dpi=100)
        super().__init__(self.fig)
        self.setParent(parent)

class IDWidgetItem(QTableWidgetItem):
    def __lt__(self, other):
        if (not other) or (not hasattr(other, 'text')):
            return False
        try:
            def natural_keys(text):
                if not text :
                    return []
                # Hàm tách chuỗi thành các phần nhỏ: số ra số, chữ ra chữ
                # Ví dụ: "D21CNTT02" -> ['D', 21, 'CNTT', 2]
                return [int(c) if c.isdigit() else c.lower() for c in re.split(r'(\d+)', text)]

            return natural_keys(self.text()) < natural_keys(other.text())
        except Exception:
            # Nếu lỗi (ví dụ ô trống hoặc sai định dạng), dùng cách so sánh mặc định
            return super().__lt__(other)

class DateWidgetItem(QTableWidgetItem):
    def __lt__(self, other):
        if (not other) or (not hasattr(other, 'text')):
            return False
        try:
            # Lấy text của 2 ô đang so sánh
            date_str1 = self.text().strip()
            date_str2 = other.text().strip()
            # Chuyển đổi từ chuỗi "dd/MM/yyyy" sang đối tượng ngày tháng để so sánh
            # Nếu định dạng file csv của bạn khác, hãy sửa '%d/%m/%Y' tương ứng
            date1 = datetime.strptime(date_str1, '%d/%m/%Y')
            date2 = datetime.strptime(date_str2, '%d/%m/%Y')

            return date1 < date2
        except Exception:
            # Nếu lỗi (ví dụ ô trống hoặc sai định dạng), dùng cách so sánh mặc định
            return super().__lt__(other)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.function_dialog = Ui_Dialog()
        self.database = CsvData()

        self.list_search = None # tạo danh sách cần tìm kiếm

        self.current_page = 1  # Trang hiện tại
        self.limit = 20  # Số dòng mỗi trang
        self.total_pages = 1  # Tổng số trang
        self.ui.btn_prev.clicked.connect(self.prev_page)
        self.ui.btn_next.clicked.connect(self.next_page)
        self.ui.txt_page.returnPressed.connect(self.show_page)
        # Load dữ liệu ngay khi mở
        self.load_data_to_table()
        self.update_dashboard()
        # Thêm dữ liệu sinh viên
        self.ui.btn_add_student.clicked.connect(self.add_student_from_table)
        # Tìm kiếm sinh viên
        self.ui.lineEdit_search_student.textChanged.connect(self.search_student)

    def load_data_to_table(self, data_list=None):
        # Nếu không truyền dữ liệu vào (data_list là None) -> Lấy tất cả sinh viên
        if data_list is None:
            list_students = self.database.list_students
        else : # Nếu có truyền vào (kết quả tìm kiếm) -> Chỉ hiển thị danh sách đó
            list_students = data_list

        # Xem có bao nhiêu sinh viên
        total_items = len(list_students)
        # Cần bao nhiêu trang ( làm tròn lên )
        self.total_pages = math.ceil(total_items / self.limit)
        if self.total_pages == 0: self.total_pages = 1
        # Đảm bảo trang hiện tại không vượt quá giới hạn ( từ 1 -> total_pages )
        if self.current_page > self.total_pages :
            self.current_page = self.total_pages
        if self.current_page < 1:
            self.current_page = 1
        # Tính vị trí bắt đầu và kết thúc
        start_index = (self.current_page - 1) * self.limit
        end_index = start_index + self.limit
        # Cắt lấy danh sách con (chỉ lấy 20 bạn cần hiển thị)
        page_student = list_students[start_index:end_index]
        # 3. Hiển thị lên bảng
        table = self.ui.studentsTableWidget
        # --- TỐI ƯU HÓA TỐC ĐỘ ---
        table.setSortingEnabled(False)  # Tắt sắp xếp (quan trọng nhất)
        table.setRowCount(0)  # Xóa sạch bảng
        # -------------------------

        for row_index, student in enumerate(page_student):
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
        # Cập nhật thông tin số trang
        self.ui.txt_page.setText(str(self.current_page))
        self.ui.lbl_total_page.setText(f" / {self.total_pages}")
        # Ẩn/Hiện nút bấm
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

    def show_page(self):
        try :
            input_txt = int(self.ui.txt_page.text().strip())
            if 1 <= input_txt <= self.total_pages:
                self.current_page = input_txt
                self.load_data_to_table(self.list_search)
            else : # Nếu số trang không hợp lệ
                self.ui.txt_page.setText(str(self.current_page))
                QMessageBox.warning(self, "Lỗi", f"Số trang phải từ 1 đến {self.total_pages}")
        except ValueError:
            self.ui.lbl_total_page.setText(str(self.current_page))
            QMessageBox.warning(self, "Lỗi", "Vui lòng nhập số trang hợp lệ")

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
                    # Nếu đang không tìm kiếm thì reset về trang cuối để thấy SV mới
                    if self.list_search is None:
                        self.current_page = math.ceil(len(self.database.list_students) / self.limit)
                    self.load_data_to_table()
                    self.update_dashboard()
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
                    self.update_dashboard()
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
                self.update_dashboard()
            else :
                QMessageBox.warning(self, "Lỗi", message)

    def search_student(self):
        # Từ khóa muốn tìm kiếm
        keyword = self.ui.lineEdit_search_student.text().strip().lower()
        if keyword == "" :
            self.list_search = None
        else :
            self.list_search = [] # Tất cả student có liên quan
            for student in self.database.list_students:
                if keyword in student.ID.lower() or keyword in student.full_name.lower() or keyword in student.Class.lower():
                    self.list_search.append(student)
        self.current_page = 1
        self.load_data_to_table(self.list_search)

    # ... các hàm cũ như __init__, load_data_to_table ...

    # --- HÀM MỚI 1: Cập nhật số liệu Dashboard ---
    def update_dashboard(self):
        """Tính toán số liệu và hiển thị lên các thẻ (Card)"""
        students = self.database.list_students

        # 1. Tổng sinh viên
        total_sv = len(students)

        # 2. Điểm trung bình (GPA)
        if total_sv > 0:
            avg_gpa = sum(s.GPA for s in students) / total_sv
        else:
            avg_gpa = 0.0

        # 3. Tổng số lớp (Dùng set để lọc trùng)
        total_classes = len(set(s.Class for s in students))

        # 4. Sinh viên cảnh báo (Ví dụ: GPA < 2.0)
        warning_count = sum(1 for s in students if s.GPA < 2.0)

        # --- Hiển thị lên giao diện (UI) ---
        # Lưu ý: Các tên lbl_... phải khớp với tên bạn đặt trong Qt Designer
        try:
            self.ui.lbl_total_students.setText(str(total_sv))
            self.ui.lbl_avg_gpa.setText(f"{avg_gpa:.2f}")
            self.ui.lbl_total_classes.setText(str(total_classes))
            self.ui.lbl_warning_students.setText(str(warning_count))

            # Cảnh báo đỏ nếu có sinh viên yếu
            if warning_count > 0:
                self.ui.lbl_warning_students.setStyleSheet("color: red; font-weight: bold;")
            else:
                self.ui.lbl_warning_students.setStyleSheet("color: green;")

        except AttributeError:
            print("Chưa đặt đúng tên biến (objectName) trong Qt Designer!")

        # Sau khi tính toán xong thì vẽ lại biểu đồ
        self.draw_charts(students)

    # --- HÀM MỚI 2: Vẽ biểu đồ ---
    def draw_charts(self, students):
        """Vẽ biểu đồ tròn và cột"""

        # --- 1. Xử lý dữ liệu cho biểu đồ ---
        # Đếm giới tính
        gender_counts = {"Nam": 0, "Nữ": 0}
        for s in students:
            g = s.Gender.strip()  # Xóa khoảng trắng thừa
            if g in gender_counts:
                gender_counts[g] += 1
            # Xử lý trường hợp ghi khác (ví dụ 'nam', 'Nu') nếu cần

        # Phân loại GPA
        gpa_counts = {"Yếu": 0, "TB": 0, "Khá": 0, "Giỏi": 0, "Xuất sắc": 0}
        for s in students:
            gpa = s.GPA
            if gpa < 2.0:
                gpa_counts["Yếu"] += 1
            elif 2.0 <= gpa < 2.5:
                gpa_counts["TB"] += 1
            elif 2.5 <= gpa < 3.2:
                gpa_counts["Khá"] += 1
            elif 3.2 <= gpa < 3.6:
                gpa_counts["Giỏi"] += 1
            else:
                gpa_counts["Xuất sắc"] += 1

        # --- 2. Vẽ Biểu đồ tròn (Giới tính) ---
        # Xóa biểu đồ cũ nếu có (để tránh vẽ chồng lên nhau)
        if hasattr(self, 'canvas_gender'):
            self.ui.verticalLayout_gender.removeWidget(self.canvas_gender)
            self.canvas_gender.deleteLater()

        # Tạo vùng vẽ mới
        self.canvas_gender = ChartCanvas(self)
        ax = self.canvas_gender.ax

        # Vẽ
        labels = [k for k, v in gender_counts.items() if v > 0]  # Chỉ lấy nhãn có số liệu > 0
        sizes = [v for v in gender_counts.values() if v > 0]
        colors = ['#66b3ff', '#ff9999']  # Xanh, Hồng

        if sizes:  # Chỉ vẽ nếu có dữ liệu
            ax.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)
            ax.axis('equal')
            ax.set_title("Tỷ lệ Nam/Nữ", fontsize=10)
        else:
            ax.text(0.5, 0.5, "Chưa có dữ liệu", ha='center')

        # Thêm vào Widget trong UI
        # Bạn cần đảm bảo widget_chart_gender trong UI đã được set Layout (ví dụ Vertical Layout)
        # Nếu chưa set Layout trong Designer, ta làm code:
        if not self.ui.widget_chart_gender.layout():
            self.ui.verticalLayout_gender = QVBoxLayout(self.ui.widget_chart_gender)
        self.ui.verticalLayout_gender.addWidget(self.canvas_gender)

        # --- 3. Vẽ Biểu đồ cột (Phổ điểm) ---
        if hasattr(self, 'canvas_gpa'):
            self.ui.verticalLayout_gpa.removeWidget(self.canvas_gpa)
            self.canvas_gpa.deleteLater()

        self.canvas_gpa = ChartCanvas(self)
        ax2 = self.canvas_gpa.ax

        categories = list(gpa_counts.keys())
        values = list(gpa_counts.values())

        # Vẽ cột
        bars = ax2.bar(categories, values, color='#4CAF50', width=0.5)
        ax2.set_title("Phân bố điểm GPA", fontsize=10)
        ax2.set_ylabel("Số lượng SV")
        # Hiển thị số trên đầu cột
        ax2.bar_label(bars)

        # Thêm vào Widget
        if not self.ui.widget_chart_gpa.layout():
            self.ui.verticalLayout_gpa = QVBoxLayout(self.ui.widget_chart_gpa)
        self.ui.verticalLayout_gpa.addWidget(self.canvas_gpa)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())