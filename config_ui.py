from PyQt5.QtWidgets import QPushButton, QWidget, QHBoxLayout, QToolButton
from PyQt5.QtGui import QIcon, QColor
from PyQt5.QtCore import QSize

class TableHelper:
    """Class này chuyên giúp xử lý các việc phức tạp trên TableWidget"""
    def add_button_to_tableWidget(self, table_widget, row_index, col_index, object_studnet, func_edit, func_delete):
        """
            Hàm tạo 2 nút Sửa/Xóa và nhét vào ô của bảng.
            :param table_widget: Cái bảng cần thêm nút
            :param row_index: Dòng hiện tại
            :param col_index: Cột tính năng (Cột 6)
        """
        # 1. Tạo widget chứa
        container = QWidget()
        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(5)
        # 2. Tạo button edit
        btn_edit = QPushButton("")
        btn_edit.setIcon(QIcon(":/icons/icons/edit.png"))
        btn_edit.setIconSize(QSize(20, 20))
        btn_edit.setToolTip("Sửa thông tin") # Khi di chuột vào sẽ hiển thị
        btn_edit.setProperty("inf_student", object_studnet) # btn_edit cất vào nhãn "student_id" một id ( key - value )
        btn_edit.clicked.connect( func_edit )
        # 2. Tạo button delete
        btn_delete = QPushButton("")
        btn_delete.setIcon(QIcon(":/icons/icons/delete.png"))
        btn_delete.setIconSize(QSize(20, 20))
        btn_delete.setToolTip("Xóa sinh viên") ## Khi di chuột vào sẽ hiển thị
        btn_delete.setProperty("inf_student", object_studnet) # btn_delete cất vào nhãn "student_id" một id ( key - value )
        btn_delete.clicked.connect( func_delete )

        # 3. Gom vào layout
        layout.addWidget(btn_delete)
        layout.addWidget(btn_edit)
        layout.setContentsMargins(2, 2, 2, 2) # Căn lề nhỏ lại cho gọn
        container.setLayout(layout)
        # 4. Gắn vào bảng tableWidget
        table_widget.setCellWidget(row_index, col_index, container)