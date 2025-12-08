Quan-li-sinh-vien/
├── main.py                 # File chạy chính (Controller)
├── database.py             # Xử lý dữ liệu CSV (Model)
├── database.csv            # File lưu trữ dữ liệu sinh viên
├── Student_management.py   # Giao diện chính (View - convert từ .ui)
├── function_dialog.py      # Giao diện hộp thoại Thêm/Sửa (View)
├── config_ui.py            # Cấu hình giao diện bổ sung (Helper)
├── resources_rc.py         # File tài nguyên hình ảnh (đã đóng gói)
├── resources.qrc           # Nguồn tài nguyên gốc
└── icons/                  # Thư mục chứa icon & logo

# 🎓 Phần Mềm Quản Lý Sinh Viên (Student Management System)

> Dự án kết thúc môn học / Bài tập lớn - Học viện Công nghệ Bưu chính Viễn thông (PTIT)
> Được xây dựng bằng **Python** và thư viện **PyQt5**.

## 📖 Giới thiệu
Đây là ứng dụng Desktop giúp quản lý hồ sơ sinh viên, được thiết kế với giao diện hiện đại, thân thiện. Ứng dụng sử dụng cơ sở dữ liệu dạng file CSV giúp dễ dàng sao chép và di chuyển mà không cần cài đặt SQL phức tạp.

## 🚀 Tính năng chính

* **📊 Dashboard Thống kê:**
    * Hiển thị tổng quan số lượng sinh viên, điểm trung bình, số lớp.
    * Biểu đồ tròn (Pie Chart): Tỷ lệ Nam/Nữ.
    * Biểu đồ cột (Bar Chart): Phân bố điểm GPA (Yếu, Trung bình, Khá, Giỏi, Xuất sắc).
* **📝 Quản lý hồ sơ (CRUD):**
    * **Thêm mới:** Nhập thông tin sinh viên và lưu vào hệ thống.
    * **Sửa:** Cập nhật thông tin sinh viên trực tiếp.
    * **Xóa:** Xóa sinh viên với hộp thoại cảnh báo an toàn.
* **🔎 Tìm kiếm & Lọc:**
    * Tìm kiếm sinh viên theo Mã SV, Họ tên hoặc Lớp học.
* **📄 Phân trang thông minh:**
    * Hệ thống tự động phân trang (20 sinh viên/trang) giúp ứng dụng chạy mượt mà ngay cả khi có hàng nghìn dòng dữ liệu.
* **🎨 Giao diện:**
    * Sidebar Menu có hiệu ứng đóng/mở (Animation).
    * Icon và màu sắc trực quan.

## 🛠️ Cài đặt & Hướng dẫn chạy

### 1. Yêu cầu hệ thống
* Python 3.x trở lên.

### 2. Cài đặt thư viện
Mở terminal (CMD/PowerShell/VSCode Terminal) tại thư mục dự án và chạy lệnh:

```bash
pip install PyQt5 matplotlib

