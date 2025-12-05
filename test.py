import csv
import os


class CsvStorage:
    def __init__(self, filename='students.csv'):
        self.filename = filename
        # Tạo file header nếu file chưa tồn tại
        if not os.path.exists(self.filename):
            with open(self.filename, mode='w', encoding='utf-8-sig', newline='') as f:
                writer = csv.writer(f)
                # Header khớp với các cột trong TableWidget của bạn
                writer.writerow(['Mã SV', 'Họ tên', 'Ngày sinh', 'Giới tính', 'Lớp', 'GPA'])

    def save_all(self, students_list):
        """
        Lưu danh sách sinh viên vào file CSV (Ghi đè lại toàn bộ)
        :param students_list: List các tuple/list dữ liệu sinh viên
        """
        try:
            # Dùng 'utf-8-sig' để Excel mở lên không bị lỗi tiếng Việt
            with open(self.filename, mode='w', encoding='utf-8-sig', newline='') as f:
                writer = csv.writer(f)
                # Ghi header trước
                writer.writerow(['Mã SV', 'Họ tên', 'Ngày sinh', 'Giới tính', 'Lớp', 'GPA'])
                # Ghi dữ liệu
                writer.writerows(students_list)
            return True
        except Exception as e:
            print(f"Lỗi khi lưu file: {e}")
            return False

    def load_all(self):
        """Đọc dữ liệu từ CSV trả về list"""
        data = []
        if not os.path.exists(self.filename):
            return data

        try:
            with open(self.filename, mode='r', encoding='utf-8-sig') as f:
                reader = csv.reader(f)
                next(reader)  # Bỏ qua dòng Header
                for row in reader:
                    if row:  # Kiểm tra dòng không rỗng
                        data.append(row)
        except Exception as e:
            print(f"Lỗi khi đọc file: {e}")

        return data

    def add_student(self, student_data):
        """Thêm 1 sinh viên vào cuối file (Append mode)"""
        try:
            with open(self.filename, mode='a', encoding='utf-8-sig', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(student_data)
            return True
        except Exception as e:
            print(f"Lỗi thêm mới: {e}")
            return False