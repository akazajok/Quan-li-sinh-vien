from PyQt5.QtWidgets import (QPushButton, QWidget, QHBoxLayout, QVBoxLayout,
                             QLabel, QGridLayout, QFrame)
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import QSize, Qt


class TableHelper:
    """Class hỗ trợ tạo nút bấm trong bảng"""

    def add_button_to_tableWidget(self, table_widget, row_index, col_index, object_studnet, func_edit, func_delete):
        container = QWidget()
        layout = QHBoxLayout()
        # Quan trọng: setMargins(0,0,0,0) để nút sát lề, không bị đệm thừa
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(10)  # Khoảng cách giữa 2 nút Sửa - Xóa

        # --- NÚT SỬA ---
        btn_edit = QPushButton("")
        # Icon to 24x24 cho rõ
        btn_edit.setIcon(QIcon(":/icons/icons/edit.png"))
        btn_edit.setIconSize(QSize(24, 24))
        btn_edit.setToolTip("Sửa thông tin")
        btn_edit.setProperty("inf_student", object_studnet)
        btn_edit.clicked.connect(func_edit)
        btn_edit.setObjectName("btn_table_edit")  # ID để CSS

        # --- NÚT XÓA ---
        btn_delete = QPushButton("")
        btn_delete.setIcon(QIcon(":/icons/icons/delete.png"))
        btn_delete.setIconSize(QSize(24, 24))
        btn_delete.setToolTip("Xóa sinh viên")
        btn_delete.setProperty("inf_student", object_studnet)
        btn_delete.clicked.connect(func_delete)
        btn_delete.setObjectName("btn_table_delete")  # ID để CSS

        layout.addWidget(btn_edit)
        layout.addWidget(btn_delete)
        layout.setAlignment(Qt.AlignCenter)  # Căn giữa ô
        container.setLayout(layout)
        table_widget.setCellWidget(row_index, col_index, container)


class HomeUiSetup:
    """Class tự động vẽ giao diện Trang chủ"""

    @staticmethod
    def setup_home_ui(ui):
        parent_widget = ui.scrollAreaWidgetContents_2

        # Xóa layout cũ nếu có để tránh lỗi chồng đè khi reload
        if parent_widget.layout() is not None:
            # Lưu ý: Cách xóa layout an toàn trong PyQt hơi phức tạp,
            # nhưng ở đây ta kiểm tra nếu chưa có mới tạo cho đơn giản.
            main_layout = parent_widget.layout()
        else:
            main_layout = QVBoxLayout(parent_widget)
            main_layout.setSpacing(30)
            main_layout.setContentsMargins(40, 40, 40, 40)

            # --- 1. BANNER HEADER ---
            hero_frame = QFrame()
            hero_frame.setObjectName("hero_frame")
            hero_layout = QVBoxLayout(hero_frame)
            hero_layout.setSpacing(10)

            lbl_welcome = QLabel("HỆ THỐNG QUẢN LÝ\nSINH VIÊN PTIT")
            lbl_welcome.setObjectName("lbl_welcome")
            lbl_welcome.setAlignment(Qt.AlignCenter)

            lbl_desc = QLabel("Cổng thông tin đào tạo và quản lý hồ sơ trực tuyến")
            lbl_desc.setObjectName("lbl_desc")
            lbl_desc.setAlignment(Qt.AlignCenter)

            hero_layout.addWidget(lbl_welcome)
            hero_layout.addWidget(lbl_desc)
            main_layout.addWidget(hero_frame)

            # --- 2. GRID CARDS ---
            grid_layout = QGridLayout()
            grid_layout.setSpacing(30)

            # Tạo 4 thẻ chức năng
            cards_data = [
                ("HỒ SƠ SINH VIÊN", "Quản lý thông tin, điểm số", ":/icons/icons/student.png", 0, 0),
                ("THỐNG KÊ BÁO CÁO", "Biểu đồ trực quan dữ liệu", ":/icons/icons/dashboard.png", 0, 1),
                ("QUẢN TRỊ HỆ THỐNG", "Bảo mật và phân quyền", ":/icons/icons/admin-panel.png", 1, 0),
                ("THÔNG TIN SINH VIÊN", "MSV: B25DCTN065 - Lớp 02-TTNT 2025", ":/icons/icons/Logo_PTIT_University.png", 1, 1)
            ]

            for title, sub, icon, r, c in cards_data:
                card = HomeUiSetup.create_card(title, sub, icon)
                grid_layout.addWidget(card, r, c)

            main_layout.addLayout(grid_layout)
            main_layout.addStretch()

    @staticmethod
    def create_card(title, sub, icon_path):
        frame = QFrame()
        frame.setObjectName("info_card")
        layout = QVBoxLayout(frame)
        layout.setSpacing(15)

        lbl_icon = QLabel()
        lbl_icon.setPixmap(QPixmap(icon_path).scaled(64, 64, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        lbl_icon.setAlignment(Qt.AlignCenter)

        lbl_title = QLabel(title)
        lbl_title.setObjectName("card_title")
        lbl_title.setAlignment(Qt.AlignCenter)

        lbl_sub = QLabel(sub)
        lbl_sub.setObjectName("card_sub")
        lbl_sub.setAlignment(Qt.AlignCenter)
        lbl_sub.setWordWrap(True)

        layout.addWidget(lbl_icon)
        layout.addWidget(lbl_title)
        layout.addWidget(lbl_sub)
        return frame


def get_app_stylesheet():
    """CSS làm đẹp - Icon trong suốt, Chữ to"""
    return """
    /* --- CẤU HÌNH CHUNG --- */
    QMainWindow { background-color: #f4f7f6; }
    QLabel { font-family: 'Segoe UI', Arial, sans-serif; }

    /* --- SIDEBAR --- */
    QWidget#sidebar { background-color: #2c3e50; }
    QWidget#logoWidget { background-color: #1a252f; }
    QLabel#appTitle { color: white; font-size: 20px; font-weight: 900; }
    QLabel#appSubitle { color: #bdc3c7; font-size: 13px; font-style: italic; }

    /* Nút Menu */
    QPushButton#btn_menu, QPushButton#btn_Dashboard, QPushButton#btn_sinh_vien, QPushButton#btn_dashboard {
        color: #ecf0f1;
        text-align: left;
        padding: 15px; /* Giãn cách nút menu */
        border: none;
        font-size: 16px;
        border-left: 5px solid transparent;
        background-color: transparent;
    }
    QPushButton#btn_menu:hover, QPushButton#btn_Dashboard:hover, 
    QPushButton#btn_sinh_vien:hover, QPushButton#btn_dashboard:hover {
        background-color: #34495e;
        border-left: 5px solid #e74c3c; /* Vệt đỏ bên trái */
        color: white;
        font-weight: bold;
    }

    /* --- TIÊU ĐỀ TRANG (Header) --- */
    QLabel#headerTitle, QLabel#studentsHeaderTitle, QLabel#label_tittle {
        font-size: 32px; /* RẤT TO */
        font-weight: 900;
        color: #2c3e50;
        border-bottom: 3px solid #3498db; /* Gạch chân xanh */
        padding-bottom: 10px;
    }
    QLabel#headerSubTitle, QLabel#studentsHeaderSubTitle {
        font-size: 16px; color: #7f8c8d; margin-top: 5px;
    }

    /* --- TRANG CHỦ (Banner) --- */
    QFrame#hero_frame {
        background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, stop:0 #ff7675, stop:1 #d63031);
        border-radius: 15px;
        padding: 30px;
    }
    QLabel#lbl_welcome {
        font-size: 42px; /* CỰC ĐẠI */
        font-weight: 900;
        color: white;
    }
    QLabel#lbl_desc { font-size: 18px; color: #dfe6e9; }

    /* --- THẺ CARD --- */
    QFrame#info_card {
        background-color: white; border-radius: 12px; border: 1px solid #dfe6e9;
    }
    QFrame#info_card:hover {
        border: 2px solid #e74c3c; transform: scale(1.02);
    }
    QLabel#card_title { font-size: 18px; font-weight: bold; color: #2d3436; }
    QLabel#card_sub { font-size: 14px; color: #636e72; }

    /* --- BẢNG DỮ LIỆU --- */
    QTableWidget {
        font-size: 15px; /* Chữ bảng to */
        selection-background-color: #3498db;
        border: 1px solid #b2bec3;
    }
    QHeaderView::section {
        background-color: #dfe6e9;
        padding: 12px;
        font-size: 15px;
        font-weight: bold;
        color: #2d3436;
        border: none;
    }

    /* --- NÚT TÍNH NĂNG (Sửa/Xóa) --- */
    /* Quan trọng: Background transparent để hiện Icon gốc */
    QPushButton#btn_table_edit, QPushButton#btn_table_delete {
        background-color: transparent; 
        border: none;
        padding: 4px;
    }
    QPushButton#btn_table_edit:hover { background-color: rgba(241, 196, 15, 0.3); border-radius: 5px; }
    QPushButton#btn_table_delete:hover { background-color: rgba(231, 76, 60, 0.3); border-radius: 5px; }

    QPushButton#btn_add_student {
        background-color: #00b894; color: white;
        border-radius: 6px; padding: 10px 20px;
        font-weight: bold; font-size: 15px;
    }
    QPushButton#btn_add_student:hover { background-color: #00a885; }

    /* --- THỐNG KÊ --- */
    QLabel#lbl_total_students, QLabel#lbl_avg_gpa, QLabel#lbl_total_classes, QLabel#lbl_warning_students {
        font-size: 28px; font-weight: bold; color: #2c3e50;
    }
    """