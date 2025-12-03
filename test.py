import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QFrame, QScrollArea, QProgressBar, QSizePolicy
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QColor, QPainter
# Import PyQtChart cho phần biểu đồ
from PyQt5.QtChart import QChart, QChartView, QBarSet, QBarSeries, QBarCategoryAxis, QValueAxis


# ===========================
# 1. CUSTOM WIDGETS
# ===========================

class TaskCard(QFrame):
    """Widget tùy chỉnh đại diện cho một thẻ nhiệm vụ."""

    def __init__(self, title, desc="", progress=None, color_accent="#ff4081"):
        super().__init__()
        self.setObjectName("TaskCard")
        layout = QVBoxLayout(self)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(10)

        # --- Header Card (Tiêu đề & Nút menu 3 chấm) ---
        header_layout = QHBoxLayout()
        lbl_title = QLabel(title)
        lbl_title.setStyleSheet("color: white; font-weight: bold; font-size: 14px;")
        btn_menu = QPushButton("⋮")
        btn_menu.setFixedSize(20, 20)
        btn_menu.setStyleSheet(
            "color: #a0a0a0; border: none; font-weight: bold; font-size: 16px; background: transparent;")
        btn_menu.setCursor(Qt.PointingHandCursor)
        header_layout.addWidget(lbl_title)
        header_layout.addStretch()
        header_layout.addWidget(btn_menu)
        layout.addLayout(header_layout)

        # --- Description with accent color bar (Mô tả có nền màu nhấn) ---
        if desc:
            desc_container = QFrame()
            desc_container.setStyleSheet(f"background-color: {color_accent}; border-radius: 5px;")
            desc_layout = QHBoxLayout(desc_container)
            desc_layout.setContentsMargins(10, 8, 10, 8)
            lbl_desc = QLabel(desc)
            lbl_desc.setStyleSheet("color: white; font-size: 12px;")
            desc_layout.addWidget(lbl_desc)
            layout.addWidget(desc_container)

        # --- Progress Bar (Thanh tiến độ - Tùy chọn) ---
        if progress is not None:
            progress_layout = QHBoxLayout()
            lbl_prog = QLabel(f"Progress")
            lbl_prog.setStyleSheet("color: #a0a0a0; font-size: 10px;")

            pbar = QProgressBar()
            pbar.setValue(progress)
            pbar.setTextVisible(False)
            pbar.setFixedHeight(6)
            # QSS tùy chỉnh cho thanh progress bar nhỏ và đẹp
            pbar.setStyleSheet(f"""
                QProgressBar {{ background-color: #3a3a55; border-radius: 3px; }}
                QProgressBar::chunk {{ background-color: {color_accent}; border-radius: 3px; }}
            """)
            lbl_val = QLabel(f"{progress}%")
            lbl_val.setStyleSheet("color: white; font-size: 10px; font-weight: bold;")

            progress_layout.addWidget(lbl_prog)
            progress_layout.addWidget(pbar)
            progress_layout.addWidget(lbl_val)
            layout.addLayout(progress_layout)

        # --- Footer Info (Fake icons & stats) ---
        footer_layout = QHBoxLayout()
        lbl_stats = QLabel("💬 3   📎 2")
        lbl_stats.setStyleSheet("color: #707090; font-size: 11px;")
        lbl_star = QLabel("★")
        lbl_star.setStyleSheet("color: #ffea00; font-size: 14px;")
        footer_layout.addWidget(lbl_stats)
        footer_layout.addStretch()
        footer_layout.addWidget(lbl_star)
        layout.addLayout(footer_layout)


class KanbanColumn(QFrame):
    """Widget tùy chỉnh đại diện cho một cột trong Kanban board."""

    def __init__(self, title, header_color="#ff4081"):
        super().__init__()
        self.setObjectName("KanbanColumn")
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # --- Column Header (Tiêu đề cột) ---
        header = QLabel(title)
        header.setAlignment(Qt.AlignCenter)
        header.setStyleSheet(f"""
            background-color: transparent; color: {header_color}; font-weight: bold;
            font-size: 12px; padding: 15px 0; text-transform: uppercase; letter-spacing: 1px;
        """)
        layout.addWidget(header)

        # --- Scroll Area (Vùng cuộn chứa các task) ---
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("background: transparent; border: none;")

        self.task_container = QWidget()
        self.task_layout = QVBoxLayout(self.task_container)
        self.task_layout.setContentsMargins(10, 0, 10, 10)
        self.task_layout.setSpacing(15)
        self.task_layout.addStretch()  # Đẩy các task lên trên cùng

        scroll.setWidget(self.task_container)
        layout.addWidget(scroll)

    def add_task(self, task_card):
        """Hàm trợ giúp để thêm một TaskCard vào cột."""
        self.task_layout.insertWidget(self.task_layout.count() - 1, task_card)


# ===========================
# 2. MAIN APPLICATION WINDOW
# ===========================

class ModernDashboardApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Task Management Dashboard - Dark Pro")
        self.resize(1280, 800)  # Kích thước cửa sổ lớn

        # --- Setup Main Layout (Chia 3 cột ngang) ---
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QHBoxLayout(main_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # --------------------------
        # PART 1: LEFT SIDEBAR
        # --------------------------
        sidebar = QFrame()
        sidebar.setObjectName("LeftSidebar")
        sidebar.setFixedWidth(70)
        sidebar_layout = QVBoxLayout(sidebar)
        sidebar_layout.setContentsMargins(0, 20, 0, 20)
        sidebar_layout.setSpacing(15)

        # Fake Menu Icons (Dùng ký tự thay cho icon ảnh để đơn giản hóa demo)
        menu_icons = ["☰", "⊞", "✉", "✓", "📅", "🌐", "📊"]
        for icon_text in menu_icons:
            btn = QPushButton(icon_text)
            btn.setObjectName("SidebarBtn")
            btn.setFixedHeight(50)
            btn.setCursor(Qt.PointingHandCursor)
            sidebar_layout.addWidget(btn)
        sidebar_layout.addStretch()

        btn_user = QPushButton("👤")
        btn_user.setObjectName("SidebarBtn")
        btn_user.setFixedHeight(50)
        sidebar_layout.addWidget(btn_user)

        main_layout.addWidget(sidebar)

        # --------------------------
        # PART 2: MAIN KANBAN AREA
        # --------------------------
        kanban_area = QWidget()
        kanban_layout = QVBoxLayout(kanban_area)
        kanban_layout.setContentsMargins(30, 30, 30, 0)  # Căn lề rộng rãi

        # --- Header Section ---
        header = QHBoxLayout()
        lbl_breadcrumb = QLabel("Tasks > Today")
        lbl_breadcrumb.setStyleSheet("color: #a0a0a0; font-size: 12px;")
        lbl_header_title = QLabel("Task Management")
        lbl_header_title.setStyleSheet("color: white; font-size: 28px; font-weight: bold; margin-top: 5px;")

        header_right = QHBoxLayout()
        btn_pricing = QPushButton("Pricing")
        btn_pricing.setObjectName("HeaderBtnHighlight")
        header_right.addWidget(btn_pricing)
        for text in ["About", "Language", "Conditions"]:
            btn = QPushButton(text)
            btn.setObjectName("HeaderBtn")
            btn.setCursor(Qt.PointingHandCursor)
            header_right.addWidget(btn)
        header_right.addStretch()

        kanban_layout.addLayout(header)
        kanban_layout.addWidget(lbl_breadcrumb)
        kanban_layout.addWidget(lbl_header_title)

        # --- Kanban Columns Grid ---
        kanban_grid = QHBoxLayout()
        kanban_grid.setSpacing(25)  # Khoảng cách giữa các cột

        # Tạo 4 cột và thêm các task mẫu
        # Cột 1: DRAFT
        col_draft = KanbanColumn("DRAFT", "#a0a0a0")
        col_draft.add_task(TaskCard("Main Task", "Incididunt ut labore et dolore", color_accent="#40c4ff"))
        col_draft.add_task(TaskCard("Secondary Task", "Ad minim veniam, quis nostrud", color_accent="#b388ff"))
        kanban_grid.addWidget(col_draft)

        # Cột 2: IN PROGRESS
        col_progress = KanbanColumn("IN PROGRESS", "#40c4ff")
        col_progress.add_task(
            TaskCard("Main Task", "Incididunt ut labore et dolore", progress=75, color_accent="#ff4081"))
        col_progress.add_task(TaskCard("Secondary Task", "Magna aliqua enim", progress=50, color_accent="#00e676"))
        kanban_grid.addWidget(col_progress)

        # Cột 3: EDITING
        col_editing = KanbanColumn("EDITING", "#b388ff")
        col_editing.add_task(TaskCard("Main Task", "Adipiscing elit sed do eiusmod", color_accent="#40c4ff"))
        col_editing.add_task(TaskCard("Secondary Task", "Adipiscing elit sed do eiusmod", color_accent="#00e676"))
        kanban_grid.addWidget(col_editing)

        # Cột 4: DONE
        col_done = KanbanColumn("DONE", "#00e676")
        col_done.add_task(TaskCard("Main Task", "Incididunt ut labore et...", color_accent="#40c4ff"))
        col_done.add_task(TaskCard("Secondary Task", "Magna aliqua enim...", color_accent="#ff4081"))
        kanban_grid.addWidget(col_done)

        kanban_layout.addLayout(kanban_grid)
        main_layout.addWidget(kanban_area, 1)  # Tỷ lệ co giãn chính

        # --------------------------
        # PART 3: RIGHT STATS SIDEBAR
        # --------------------------
        stats_sidebar = QFrame()
        stats_sidebar.setObjectName("StatsSidebar")
        stats_sidebar.setFixedWidth(320)
        stats_layout = QVBoxLayout(stats_sidebar)
        stats_layout.setContentsMargins(25, 35, 25, 25)
        stats_layout.setSpacing(25)

        # --- User Profile ---
        user_layout = QHBoxLayout()
        lbl_user_name = QLabel("Name\nSurname")
        lbl_user_name.setStyleSheet("color: white; font-weight: bold; font-size: 18px;")
        lbl_user_desc = QLabel("Quản trị viên hệ thống")
        lbl_user_desc.setStyleSheet("color: #a0a0a0; font-size: 11px;")

        user_info = QVBoxLayout()
        user_info.addWidget(lbl_user_name)
        user_info.addWidget(lbl_user_desc)

        # Placeholder Avatar (Nút tròn)
        btn_avatar = QPushButton("")
        btn_avatar.setFixedSize(55, 55)
        btn_avatar.setStyleSheet("background-color: #40c4ff; border-radius: 27px; border: 3px solid #2d2d44;")

        user_layout.addLayout(user_info)
        user_layout.addWidget(btn_avatar)
        stats_layout.addLayout(user_layout)

        # --- Chart Area (Biểu đồ cột mẫu) ---
        stats_layout.addWidget(self.create_bar_chart())

        # --- Efficiency Section (Chỉ số hiệu quả) ---
        lbl_eff = QLabel("EFFICIENCY")
        lbl_eff.setStyleSheet(
            "color: white; font-weight: bold; font-size: 11px; margin-top: 10px; letter-spacing: 1px;")
        stats_layout.addWidget(lbl_eff)

        eff_layout = QHBoxLayout()
        # Tạo các vòng tròn chỉ số giả lập
        for val, color in [("75", "#40c4ff"), ("44", "#ff4081"), ("68", "#b388ff"), ("55", "#ffea00")]:
            btn_eff = QPushButton(val)
            btn_eff.setFixedSize(45, 45)
            btn_eff.setStyleSheet(f"""
                background-color: transparent; color: white; font-weight: bold; font-size: 14px;
                border: 3px solid {color}; border-radius: 22px;
             """)
            eff_layout.addWidget(btn_eff)
        stats_layout.addLayout(eff_layout)

        # --- Plan Section (Lịch trình) ---
        lbl_plan = QLabel("PLAN")
        lbl_plan.setStyleSheet(
            "color: white; font-weight: bold; font-size: 11px; margin-top: 20px; letter-spacing: 1px;")
        stats_layout.addWidget(lbl_plan)

        plan_data = [("09:00 - 10:30", "Họp giao ban đầu tuần", "#40c4ff"),
                     ("13:00 - 14:00", "Review code dự án QLSV", "#ff4081"),
                     ("15:00 - 16:00", "Báo cáo tiến độ", "#ffea00")]
        for time, desc, color in plan_data:
            plan_item = QFrame()
            # Tạo hiệu ứng đường viền màu bên trái
            plan_item.setStyleSheet(f"background-color: #3a3a55; border-left: 4px solid {color}; border-radius: 4px;")
            plan_item_layout = QVBoxLayout(plan_item)
            plan_item_layout.setContentsMargins(15, 10, 10, 10)
            lbl_time = QLabel(time)
            lbl_time.setStyleSheet("color: #a0a0a0; font-size: 11px;")
            lbl_plan_desc = QLabel(desc)
            lbl_plan_desc.setStyleSheet("color: white; font-size: 13px; font-weight: 500;")
            plan_item_layout.addWidget(lbl_time)
            plan_item_layout.addWidget(lbl_plan_desc)
            stats_layout.addWidget(plan_item)

        stats_layout.addStretch()
        main_layout.addWidget(stats_sidebar)

        # ===========================
        # 3. APPLY GLOBAL STYLESHEET (QSS)
        # ===========================
        self.apply_stylesheet()

    def create_bar_chart(self):
        """Hàm tạo biểu đồ cột mẫu."""
        set0 = QBarSet("Tasks");
        set0.append([210, 110, 176, 145]);
        set0.setColor(QColor("#40c4ff"))
        series = QBarSeries();
        series.append(set0);
        series.setBarWidth(0.3)

        chart = QChart();
        chart.addSeries(series)
        chart.setTitle("COMPLETED TASKS")
        chart.setTitleFont(QFont("Segoe UI", 10, QFont.Bold))
        chart.setTitleBrush(QColor("white"))
        chart.setBackgroundBrush(QColor("transparent"))
        chart.legend().setVisible(False)
        chart.layout().setContentsMargins(0, 0, 0, 0)

        axisX = QBarCategoryAxis();
        axisX.append(["A", "B", "C", "D"])
        axisX.setLabelsColor(QColor("#a0a0a0"));
        axisX.setGridLineVisible(False)
        chart.addAxis(axisX, Qt.AlignBottom);
        series.attachAxis(axisX)

        axisY = QValueAxis();
        axisY.setLabelsColor(QColor("#a0a0a0"))
        axisY.setGridLineColor(QColor("#3a3a55"));
        chart.addAxis(axisY, Qt.AlignLeft);
        series.attachAxis(axisY)

        chart_view = QChartView(chart)
        chart_view.setRenderHint(QPainter.Antialiasing)
        chart_view.setStyleSheet("background: transparent;")
        chart_view.setFixedHeight(180)
        return chart_view

    def apply_stylesheet(self):
        """Áp dụng QSS toàn cục để định kiểu cho giao diện."""
        style = """
        QMainWindow { background-color: #1e1e2d; }
        QWidget { font-family: 'Segoe UI', sans-serif; }

        /* --- SIDEBARS --- */
        QFrame#LeftSidebar, QFrame#StatsSidebar { background-color: #2d2d44; border: none; }

        /* --- SIDEBAR BUTTONS --- */
        QPushButton#SidebarBtn {
            background-color: transparent; color: #707090; border: none; font-size: 22px;
        }
        QPushButton#SidebarBtn:hover { color: #ffffff; background-color: #3a3a55; border-radius: 5px; }

        /* --- HEADER BUTTONS --- */
        QPushButton#HeaderBtn { background-color: transparent; color: #a0a0a0; border: none; padding: 8px 15px; font-weight: 500; }
        QPushButton#HeaderBtn:hover { color: white; }
        QPushButton#HeaderBtnHighlight { 
            background-color: #3a3a55; color: #40c4ff; border: none; 
            padding: 8px 20px; border-radius: 18px; font-weight: bold;
        }

        /* --- KANBAN COMPONENTS --- */
        QFrame#KanbanColumn { background-color: #25253a; border-radius: 12px; }
        QFrame#TaskCard { background-color: #2d2d44; border-radius: 10px; }
        QFrame#TaskCard:hover { background-color: #32324a; /* Hiệu ứng sáng lên khi di chuột vào thẻ */ }

        /* --- TÙY BIẾN THANH CUỘN (SCROLLBAR) CHO ĐẸP --- */
        QScrollBar:vertical {
            border: none; background: #25253a; width: 8px; margin: 0px; border-radius: 4px;
        }
        QScrollBar::handle:vertical {
            background: #3a3a55; min-height: 30px; border-radius: 4px;
        }
        QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical { height: 0px; }
        """
        self.setStyleSheet(style)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    # Thiết lập font mặc định cho toàn bộ ứng dụng
    font = QFont("Segoe UI", 10)
    app.setFont(font)

    window = ModernDashboardApp()
    window.show()
    sys.exit(app.exec_())