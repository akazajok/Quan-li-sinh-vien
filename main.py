import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem

from Student_management import Ui_MainWindow  # File giao diện gốc (auto-generated)
from config_ui import TableHelper  # File trợ lý bạn vừa tạo
from database import CsvData

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.database = CsvData()
        self.list_student = self.database.get_data_Csv()
        # Load dữ liệu ngay khi mở
        self.load_data_to_table()

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
            table.setItem(row_index, 5, QTableWidgetItem(str(student.GPA)))
            #Thêm nút xóa, sửa
            TableHelper.add_button_to_tableWidget(self, self.ui.studentsTableWidget, row_index, 6)
        table.setSortingEnabled(True) # Bật lại sắp xếp để user bấm vào tiêu đề cột

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())