🎓 Phần Mềm Quản Lý Sinh Viên (Student Management System)
Dự án kết thúc môn học / Bài tập lớn - Học viện Công nghệ Bưu chính Viễn thông (PTIT)

Được xây dựng và phát triển bằng ngôn ngữ Python kết hợp với thư viện giao diện PyQt5.

📖 Giới thiệu
Đây là ứng dụng Desktop giúp quản lý hồ sơ sinh viên một cách hiệu quả, trực quan. Hệ thống được thiết kế theo mô hình MVC (Model-View-Controller) đơn giản hóa, sử dụng CSV làm cơ sở dữ liệu giúp dễ dàng sao chép, di chuyển mà không cần cài đặt SQL server phức tạp.

Điểm đặc biệt của dự án là khả năng xử lý dữ liệu lớn (lên tới hàng chục nghìn sinh viên) mượt mà nhờ thuật toán phân trang và tối ưu hóa giao diện.

📂 Cấu trúc Dự án
Plaintext

Quan-li-sinh-vien/
├── main.py                 # 🚀 File chạy chính (Controller & Main Logic)
├── database.py             # 💾 Xử lý dữ liệu CSV và Excel (Model)
├── database.csv            # 📄 File lưu trữ dữ liệu sinh viên (Cơ sở dữ liệu)
├── ramdom_data.py          # 🎲 Script tạo dữ liệu giả lập (20,000+ sinh viên)
├── Student_management.py   # 🖼️ Giao diện chính (View - convert từ .ui)
├── function_dialog.py      # 🖼️ Giao diện hộp thoại Thêm/Sửa (View)
├── config_ui.py            # ⚙️ Cấu hình giao diện bổ sung, helper (QSS, Table setup)
├── resources_rc.py         # 📦 File tài nguyên hình ảnh (đã đóng gói)
├── resources.qrc           # 🛠️ Nguồn tài nguyên gốc (dùng cho Qt Designer)
└── icons/                  # 🎨 Thư mục chứa icon & logo gốc
🚀 Tính năng nổi bật
1. 📊 Dashboard Thống kê trực quan
Tổng quan: Hiển thị thời gian thực tổng số sinh viên, điểm GPA trung bình, tổng số lớp quản lý và số lượng sinh viên bị cảnh báo học vụ.

Biểu đồ (Matplotlib):

Biểu đồ tròn: Tỷ lệ giới tính (Nam/Nữ/Khác).

Biểu đồ cột: Phân bố học lực (Yếu, Trung bình, Khá, Giỏi, Xuất sắc).

2. 📝 Quản lý hồ sơ (CRUD)
Thêm mới: Hỗ trợ nhập liệu đầy đủ thông tin: Mã SV, Họ tên, Ngày sinh, Giới tính, Lớp, GPA.

Sửa: Cập nhật thông tin nhanh chóng qua hộp thoại dialog.

Xóa: Xóa sinh viên an toàn với hộp thoại xác nhận (Confirm Dialog).

3. 🔍 Tìm kiếm & Sắp xếp nâng cao
Tìm kiếm Real-time: Kết quả hiển thị ngay khi gõ phím. Hỗ trợ tìm theo Mã SV, Họ tên hoặc Lớp.

Sắp xếp thông minh: * Click vào tiêu đề cột để sắp xếp tăng/giảm dần.

Thuật toán sắp xếp tự nhiên (Natural Sort): Phân biệt được số trong chuỗi (ví dụ: B1, B2, B10 sẽ sắp xếp đúng thay vì B1, B10, B2).

Sắp xếp ngày tháng chính xác theo định dạng VN (dd/mm/yyyy).

4. 📄 Tiện ích mở rộng
Phân trang: Chia dữ liệu thành các trang (20 sinh viên/trang), giúp ứng dụng chạy mượt mà ngay cả với dữ liệu 20.000 dòng.

Xuất Excel (Pandas): * Xuất toàn bộ danh sách hiện tại.

Xuất danh sách lọc theo học lực (Xuất sắc, Giỏi, Khá, TB, Yếu) chỉ với 1 cú click.

5. 🎨 Giao diện UI/UX
Sidebar Menu có hiệu ứng trượt (Animation) đóng/mở chuyên nghiệp.

Thiết kế hiện đại, icon trực quan, bố cục rõ ràng.

🛠️ Cài đặt & Hướng dẫn chạy
1. Yêu cầu hệ thống
Python 3.x trở lên.

Các thư viện phụ thuộc liệt kê bên dưới.

2. Cài đặt thư viện
Mở terminal (CMD/PowerShell/Terminal) tại thư mục dự án và chạy lệnh sau để cài đặt các thư viện cần thiết:

Bash

pip install PyQt5 matplotlib pandas
(Lưu ý: Dự án cần pandas để xử lý xuất file Excel và matplotlib để vẽ biểu đồ)

3. Cách chạy chương trình
Tại terminal, chạy lệnh:

Bash

python main.py
4. (Tùy chọn) Tạo dữ liệu mẫu
Nếu bạn muốn test khả năng chịu tải của ứng dụng, bạn có thể chạy file ramdom_data.py để tạo tự động 20.000 sinh viên ảo vào file database.csv:

Bash

python ramdom_data.py
Lưu ý: File này sẽ ghi đè lên dữ liệu cũ trong database.csv.

🐛 Khắc phục lỗi thường gặp
Lỗi ModuleNotFoundError: No module named 'resources_rc':

Đây là do file tài nguyên chưa được biên dịch. Hãy chạy lệnh sau:

Bash

pyrcc5 resources.qrc -o resources_rc.py
Lỗi Plugin đường dẫn trên Windows (Conda):

Code trong main.py đã tích hợp sẵn đoạn fix lỗi đường dẫn plugin của Qt khi chạy trên môi trường Miniforge/Anaconda. Nếu vẫn lỗi, hãy đảm bảo biến môi trường QT_QPA_PLATFORM_PLUGIN_PATH trỏ đúng đến thư mục platforms của PyQt5.

Lỗi hiển thị tiếng Việt khi mở file CSV bằng Excel:

File CSV được lưu với encoding utf-8-sig để hiển thị tốt trên Excel. Nếu mở bằng phần mềm khác bị lỗi font, hãy chọn encoding là UTF-8.


📂 1. Cấu trúc tổng quan
Controller (Điều khiển): main.py - File chạy chính, kết nối giao diện với dữ liệu.

Model (Dữ liệu): database.py - Chứa logic đọc/ghi file CSV và Excel.

View (Giao diện): Student_management.py (Màn hình chính) và function_dialog.py (Cửa sổ nhập liệu).

Helper (Công cụ phụ): ramdom_data.py (Sinh dữ liệu giả) và config_ui.py.

📝 2. Giải thích chi tiết từng file
A. main.py - Trái tim của ứng dụng
Đây là file quan trọng nhất, nơi xử lý mọi sự kiện của người dùng.

Khởi tạo (__init__):

Thiết lập giao diện từ Ui_MainWindow.

Kết nối các nút bấm (Menu, Thêm, Sửa, Xóa, Export...) với các hàm xử lý tương ứng (Signals & Slots).

Cấu hình bảng (TableWidget), tắt tính năng sort mặc định của Qt để dùng custom sort.

Các hàm xử lý chính:

load_data_to_table(self, data_list): Hàm này nhận danh sách sinh viên và hiển thị lên bảng. Nó xử lý luôn cả logic Phân trang (Pagination), chỉ hiển thị 20 sinh viên mỗi trang để tối ưu hiệu năng.

update_dashboard(self): Tính toán tổng số sinh viên, GPA trung bình, số lượng cảnh báo học vụ và gọi hàm vẽ biểu đồ.

draw_charts(self, students): Sử dụng thư viện matplotlib để vẽ:

Biểu đồ tròn: Tính tỷ lệ Nam/Nữ/Khác và hiển thị phần trăm.

Biểu đồ cột: Phân loại GPA (Giỏi, Khá, TB...) và vẽ cột tương ứng.

search_student(self): Lọc danh sách sinh viên theo từ khóa nhập vào (Mã SV, Tên, Lớp) và load lại bảng.

sort_by_column(self, col_index): Hàm sắp xếp tùy chỉnh. Nó xử lý việc sắp xếp tự nhiên (Natural Sort) cho Mã SV (ví dụ: B2 đứng trước B10) và sắp xếp ngày tháng theo định dạng VN.

B. database.py - Quản lý dữ liệu
File này chịu trách nhiệm làm việc trực tiếp với file database.csv.

Class Student: Định nghĩa cấu trúc một sinh viên (ID, Tên, Ngày sinh, Giới tính, Lớp, GPA). Có kiểm tra tính hợp lệ của GPA (0-4.0).

Class CsvData:

load_data_Csv(): Đọc file CSV, chuyển từng dòng thành đối tượng Student và lưu vào list self.list_students.

add_student(), edit_student(), delete_student(): Các hàm thêm, sửa, xóa. Sau khi thay đổi list trong bộ nhớ, nó gọi update_data_Csv() để ghi đè lại file CSV.

export_to_excel(): Sử dụng thư viện Pandas để tạo DataFrame từ danh sách sinh viên và xuất ra file Excel (.xlsx). Có hỗ trợ sắp xếp theo GPA trước khi xuất.

C. ramdom_data.py - Tool sinh dữ liệu giả
Dùng để tạo nhanh database lớn nhằm test hiệu năng.

Sử dụng các mảng dữ liệu mẫu (Họ, Tên đệm, Tên) để ghép ngẫu nhiên thành tên người.

tao_gpa(): Sinh điểm GPA ngẫu nhiên nhưng có trọng số (tỷ lệ Xuất sắc/Giỏi ít hơn Trung bình/Khá để giống thực tế).

Tạo ra 20.000 dòng dữ liệu vào file database.csv chỉ trong vài giây.

D. Các file giao diện (.py convert từ .ui)
Student_management.py: Chứa code Python sinh ra giao diện chính (bảng, menu, sidebar). File này không nên sửa trực tiếp logic mà chỉ chứa định nghĩa widget.

function_dialog.py: Chứa giao diện của hộp thoại (Dialog) dùng khi bấm nút "Thêm sinh viên" hoặc "Sửa".

🔄 3. Luồng hoạt động (Workflow) ví dụ
Khi bạn bấm nút "Thêm sinh viên":

View: main.py mở Dialog nhập liệu (function_dialog.py).

Controller: Người dùng nhập thông tin -> bấm "Cập nhật". main.py lấy dữ liệu từ các ô input.

Model: main.py gọi database.add_student(new_student).

Database: Hàm này kiểm tra trùng mã SV -> Thêm vào list -> Ghi dòng mới vào file database.csv.

View: main.py nhận tín hiệu thành công -> Gọi load_data_to_table() để vẽ lại bảng và update_dashboard() để cập nhật lại số liệu thống kê.