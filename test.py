import csv
import os


class CsvStorage:
    def __init__(self, filename='database.csv'):
        self.filename = filename
        self.headers = ['Mã SV', 'Họ tên', 'Ngày sinh', 'Giới tính', 'Lớp', 'GPA']
        if not os.path.exists(self.filename):
            with open(self.filename, mode='w', encoding='utf-8-sig', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(self.headers)

    def load_all(self):
        """Đọc dữ liệu từ CSV trả về list các list"""
        data = []
        if not os.path.exists(self.filename):
            return data
        try:
            with open(self.filename, mode='r', encoding='utf-8-sig') as f:
                reader = csv.reader(f)
                next(reader, None)  # Bỏ qua header an toàn hơn
                for row in reader:
                    if row:
                        data.append(row)
        except Exception as e:
            print(f"Lỗi đọc file: {e}")
        return data

    def add_student(self, student_data):
        """Thêm sinh viên mới (student_data là list: [Mã, Tên, ...])"""
        try:
            with open(self.filename, mode='a', encoding='utf-8-sig', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(student_data)
            return True
        except Exception as e:
            print(f"Lỗi thêm mới: {e}")
            return False

    def delete_student(self, msv):
        """Xóa sinh viên theo Mã SV"""
        data = self.load_all()
        new_data = [row for row in data if row[0] != msv]  # Giữ lại các dòng KHÔNG trùng mã

        if len(data) == len(new_data):  # Không có gì thay đổi
            return False

        return self.save_all(new_data)

    def update_student(self, msv, new_info):
        """Cập nhật thông tin sinh viên theo Mã SV"""
        data = self.load_all()
        updated = False
        for i in range(len(data)):
            if data[i][0] == msv:
                data[i] = new_info  # Ghi đè thông tin mới
                updated = True
                break

        if updated:
            return self.save_all(data)
        return False

    def save_all(self, data):
        """Ghi đè lại toàn bộ file (Dùng cho Xóa và Sửa)"""
        try:
            with open(self.filename, mode='w', encoding='utf-8-sig', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(self.headers)
                writer.writerows(data)
            return True
        except Exception as e:
            print(f"Lỗi lưu file: {e}")
            return False