import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem

from Student_management import Ui_MainWindow  # File giao diện gốc (auto-generated)
from config_ui import TableHelper  # File trợ lý bạn vừa tạo

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Load dữ liệu ngay khi mở
        self.load_data_to_table()

    def load_data_to_table(self):
        mock_data = [
            ('SV001', 'Nguyễn Văn A', '20/10/2005', 'Nam', 'CNTT1', '3.5'),
            ('SV002', 'Trần Thị B', '15/05/2005', 'Nữ', 'CNTT2', '3.8'),
        ]
        self.ui.studentsTableWidget.setRowCount(0)

        for row_index, row_data in enumerate(mock_data):
            self.ui.studentsTableWidget.insertRow(row_index)
            for col_index, col_data in enumerate(row_data):
                self.ui.studentsTableWidget.setItem(row_index, col_index, QTableWidgetItem(col_data))
            TableHelper.add_button_to_tableWidget(self, self.ui.studentsTableWidget, row_index, 6 , row_data[0])

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())