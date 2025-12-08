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
    from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QDialog, QMessageBox, QHeaderView
    from PyQt5 import QtCore
    from PyQt5.QtCore import QDate, Qt, QPropertyAnimation, QEasingCurve
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
        # figsize=(5, 4): Kích thước mặc định (ngang 5 inch, cao 4 inch)
        # dpi=100: Độ phân giải (dots per inch)
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
        # Lệnh này ép bảng chia đều chiều rộng cho 7 cột
        self.ui.studentsTableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        self.list_search = None # tạo danh sách cần tìm kiếm

        self.current_page = 1  # Trang hiện tại
        self.limit = 20  # Số dòng mỗi trang
        self.total_pages = 1  # Tổng số trang
        self.ui.btn_prev.clicked.connect(self.prev_page)
        self.ui.btn_next.clicked.connect(self.next_page)
        self.ui.txt_page.returnPressed.connect(self.show_page)

        # Định nghĩa chiều rộng của sidebar
        self.sidebar_expanded = True  # Mặc định là đang mở to
        # --- Cấu hình cho Sidebar Menu (QUAN TRỌNG: Cần khai báo biến này) ---
        self.width_standard = 250  # Độ rộng khi mở to (khớp với Qt Designer)
        self.width_collapsed = 60  # Độ rộng khi thu nhỏ
        # Load dữ liệu ngay khi mở
        self.load_data_to_table()
        self.update_dashboard()
        # Thêm dữ liệu sinh viên
        self.ui.btn_add_student.clicked.connect(self.add_student_from_table)
        # Tìm kiếm sinh viên
        self.ui.lineEdit_search_student.textChanged.connect(self.search_student)
        # Kết nối nút Menu với hàm xử lý
        self.ui.btn_menu.clicked.connect(self.toggle_menu)
        self.ui.sidebar.setMaximumWidth(250)
        self.ui.sidebar.setMinimumWidth(250)
        new_icon_size = QtCore.QSize(50, 50)  # Kích thước mới (40x40)
        self.ui.btn_menu.setIconSize(new_icon_size)
        self.ui.btn_Dashboard.setIconSize(new_icon_size)
        self.ui.btn_sinh_vien.setIconSize(new_icon_size)
        self.ui.btn_dashboard.setIconSize(new_icon_size)
        # Nút Trang chủ -> Hiện màn hình HomePage
        self.ui.btn_Dashboard.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.HomePage))
        # Nút Sinh viên -> Hiện màn hình quản lý sinh viên
        self.ui.btn_sinh_vien.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.studentsPage))
        # Nút Thống kê -> Hiện màn hình biểu đồ
        self.ui.btn_dashboard.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.page_dashboard))
        # Mặc định khi mở lên sẽ vào trang "Trang chủ"
        self.ui.stackedWidget.setCurrentWidget(self.ui.HomePage)
        # ---------------------------------------------------------

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

    def update_dashboard(self):
        # Lấy danh sách sinh viên trực tiếp từ database.py
        students = self.database.list_students
        # 1. Tổng số sinh viên
        total_sv = len(students)
        # 2. Điểm trung bình (GPA)
        if total_sv > 0:
            # s.GPA đã được convert sang float trong class Student
            avg_gpa = sum(s.GPA for s in students) / total_sv
            # 3. Tổng số lớp (Dùng set để lọc các lớp trùng nhau)
            total_classes = len(set(s.Class for s in students))
            # 4. Sinh viên cảnh báo (GPA < 2.0)
            warning_count = sum(1 for s in students if s.GPA < 2.0)
            # --- Hiển thị lên giao diện ---
            try:
                self.ui.lbl_total_students.setText(str(total_sv))
                self.ui.lbl_avg_gpa.setText(f"{avg_gpa:.2f}")
                self.ui.lbl_total_classes.setText(str(total_classes))
                self.ui.lbl_warning_students.setText(str(warning_count))
                # Đổi màu đỏ nếu có cảnh báo
                if warning_count > 0:
                    self.ui.lbl_warning_students.setStyleSheet("color: red; font-weight: bold;")
                else:
                    self.ui.lbl_warning_students.setStyleSheet("color: green;")
            except AttributeError:
                pass  # Bỏ qua nếu chưa thiết kế xong giao diện các label này
            # Vẽ biểu đồ
            self.draw_charts(students)

    def draw_charts(self, students):
        # --- 1. Chuẩn bị dữ liệu ---
        gender_counts = {"Nam": 0, "Nữ": 0}
        gpa_counts = {"Yếu": 0, "TB": 0, "Khá": 0, "Giỏi": 0, "Xuất sắc": 0}
        for s in students:
            gender = s.Gender.strip()
            if gender in gender_counts:
                gender_counts[gender] += 1
            # Phân loại GPA
            gpa = s.GPA
            if gpa < 2.0: gpa_counts["Yếu"] += 1
            elif 2.0 <= gpa < 2.5: gpa_counts["TB"] += 1
            elif 2.5 <= gpa < 3.2: gpa_counts["Khá"] += 1
            elif 3.2 <= gpa < 3.6: gpa_counts["Giỏi"] += 1
            else: gpa_counts["Xuất sắc"] += 1
        # --- 2. Vẽ Biểu đồ tròn (Giới tính) ---
        # Xóa biểu đồ cũ để vẽ lại
        if hasattr(self, 'canvas_gender'):
            self.ui.verticalLayout_gender.removeWidget(self.canvas_gender)
            self.canvas_gender.deleteLater()

        self.canvas_gender = ChartCanvas(self)
        # Lọc bỏ các mục có giá trị 0 để biểu đồ đẹp hơn
        labels = [k for k, v in gender_counts.items() if v > 0]
        sizes = [v for v in gender_counts.values() if v > 0]
        colors = ['#66b3ff', '#ff9999']  # Xanh, Hồng
        # Hàm hiển thị: Số lượng + (Phần trăm)
        # pct là phần trăm tự động tính, allvals là tổng số
        def func_pct(pct, allvals):
            absolute = int(round(pct / 100. * sum(allvals)))
            return f"{absolute}\n({pct:.1f}%)"
            #return f"{absolute}" #chỉ nhận số lượng &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&7
        if sizes:
            # Vẽ biểu đồ tròn
            # autopct='%1.1f%%': Hiển thị số phần trăm trên biểu đồ (ví dụ: 50.5%).
            # startangle=90: Xoay biểu đồ bắt đầu từ góc 12 giờ (thay vì 3 giờ mặc định).
            # Nếu chỉ cần % autopct='%1.1f%%' ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^&&&&&&&&&&&&&&&&&&&&&
            self.canvas_gender.ax.pie(sizes, labels=labels, colors=colors, autopct=lambda pct: func_pct(pct, sizes), startangle=90)
            # axis('equal') giúp biểu đồ tròn vo, không bị méo thành hình bầu dục
            self.canvas_gender.ax.axis('equal')
            self.canvas_gender.ax.set_title("Tỷ lệ Giới tính")
        else:
            self.canvas_gender.ax.text(0.5, 0.5, "Chưa có dữ liệu", ha='center')
        # Thêm vào Widget trên UI (Cần đảm bảo widget_chart_gender đã có layout)
        if self.ui.widget_chart_gender.layout() is None:
            self.ui.verticalLayout_gender = QVBoxLayout(self.ui.widget_chart_gender)
        self.ui.verticalLayout_gender.addWidget(self.canvas_gender)

        # --- 3. Vẽ Biểu đồ cột (GPA) ---
        if hasattr(self, 'canvas_gpa'):
            self.ui.verticalLayout_gpa.removeWidget(self.canvas_gpa)
            self.canvas_gpa.deleteLater()

        self.canvas_gpa = ChartCanvas(self)
        categories = list(gpa_counts.keys())
        values = list(gpa_counts.values())
        # Vẽ biểu đồ cột
        # color='#4CAF50': Màu xanh lá cây
        # width=0.5: Độ rộng của cột
        bars = self.canvas_gpa.ax.bar(categories, values, color='#4CAF50', width=0.5)
        # Đặt tiêu đề và nhãn trục
        self.canvas_gpa.ax.set_title("Phân bố điểm GPA")
        self.canvas_gpa.ax.set_ylabel("Số lượng")
        # --- FIX LỖI BỊ ĐÈ: Tăng giới hạn trần trục Y ---
        if values:
            max_val = max(values)
            # Tăng trần lên 1.2 lần (thêm 20% khoảng trống phía trên)
            self.canvas_gpa.ax.set_ylim(0, max_val * 1.25)
        # --- TẠO NHÃN: SỐ LƯỢNG + % ---
        total_sv = sum(values)
        combined_labels = []
        for v in values:
            if total_sv > 0:
                pct = (v / total_sv) * 100
                # Format: Số lượng (xuống dòng) (Phần trăm)
                combined_labels.append(f"{v}\n({pct:.1f}%)")
                #combined_labels.append(f"{pct:.2f}%") #chỉ lấy %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
            else:
                combined_labels.append(f"{v}\n(0%)")
                #combined_labels.append("0%") # chỉ lấy %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        # Hiển thị số lên biểu đồ
        # Gắn nhãn với cỡ chữ nhỏ (fontsize=8)
        #self.canvas_gpa.ax.bar_label(bars, labels=combined_labels)
        self.canvas_gpa.ax.bar_label(bars) # chỉ lấy số ssssssssssssssssssssssssssssssssssssssssssssssssssssss
        # Chỉ cần % :

        if self.ui.widget_chart_gpa.layout() is None:
            self.ui.verticalLayout_gpa = QVBoxLayout(self.ui.widget_chart_gpa)
        self.ui.verticalLayout_gpa.addWidget(self.canvas_gpa)

    def toggle_menu(self):
        # Lấy độ rộng hiện tại
        width = self.ui.sidebar.width()

        # --- ĐIỀU CHỈNH ĐỘ RỘNG Ở ĐÂY ---
        collapsed_width = 100  # Độ rộng khi thu nhỏ (Tăng từ 70 -> 100)
        expanded_width = 250  # Độ rộng khi mở to

        if width == collapsed_width:
            new_width = expanded_width
            # Hiện lại chữ
            self.ui.appTitle.setVisible(True)
            self.ui.appSubitle.setVisible(True)
            self.ui.profileName.setVisible(True)
            self.ui.profileEmail.setVisible(True)
            self.ui.LogoPtit.setVisible(True)

            # Khôi phục chữ cho các nút
            self.ui.btn_Dashboard.setText("  Trang chủ")
            self.ui.btn_sinh_vien.setText("  Sinh Viên")
            self.ui.btn_dashboard.setText("  Thống kê")
            self.ui.btn_menu.setText("  MENU")
        else:
            new_width = collapsed_width
            # Ẩn chữ
            self.ui.appTitle.setVisible(False)
            self.ui.appSubitle.setVisible(False)
            self.ui.profileName.setVisible(False)
            self.ui.profileEmail.setVisible(False)
            self.ui.LogoPtit.setVisible(False)

            # Xóa chữ trên các nút, chỉ để lại Icon
            self.ui.btn_Dashboard.setText("")
            self.ui.btn_sinh_vien.setText("")
            self.ui.btn_dashboard.setText("")
            self.ui.btn_menu.setText("")

        # Chạy Animation
        self.animation = QPropertyAnimation(self.ui.sidebar, b"minimumWidth")
        self.animation.setDuration(300)
        self.animation.setStartValue(width)
        self.animation.setEndValue(new_width)
        self.animation.setEasingCurve(QEasingCurve.InOutQuart)
        self.animation.start()

        # Cập nhật maximumWidth để giữ cố định kích thước mới
        self.ui.sidebar.setMaximumWidth(new_width)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())