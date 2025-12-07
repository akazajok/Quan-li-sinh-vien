import csv

class Student:
    def __init__(self, ID, full_name, DateOfBirth, Gender, Class, GPA):
        self.ID = ID
        self.full_name = full_name
        self.DateOfBirth = DateOfBirth
        self.Gender = Gender
        self.Class = Class
        try :   
            self.GPA = float(GPA)
            if self.GPA < 0 or self.GPA > 4:
                raise ValueError(f"Điểm GPA không hợp lệ! Phải từ 0.0 đến 4.0")
        except ValueError:
            raise ValueError("Điểm GPA phải là 1 con số")


class CsvData:
    def __init__(self, filename = "database.csv"):
        self.csv_file = filename
        self.list_students = []
        self.load_data_Csv()

    def load_data_Csv(self):
        try :
            with open(self.csv_file, 'r', encoding="utf-8-sig", newline='') as csvfile:
                reader = csv.reader(csvfile)
                for line in reader:
                    if len(line) >=6 :
                        try:
                            ID = line[0]
                            full_name = line[1]
                            DateOfBirth = line[2]
                            Gender = line[3]
                            Class = line[4]
                            GPA = line[5]
                            self.list_students.append(Student(ID, full_name, DateOfBirth, Gender, Class, GPA))
                        except:
                            pass
        except Exception as e:
            print(f"Lỗi khi đọc file: {e}")

    def update_data_Csv(self):
        try:
            with open(self.csv_file, 'w', encoding="utf-8-sig", newline='') as csvfile:
                writer = csv.writer(csvfile)
                for student in self.list_students:
                    writer.writerow([
                        student.ID,  student.full_name,  student.DateOfBirth,
                        student.Gender, student.Class, student.GPA
                    ])
        except Exception as e:
            print(f"Lỗi khi đọc file: {e}")

    def add_student(self, new_student):
        if not new_student.ID or not new_student.full_name or not new_student.Class or not new_student.GPA:
            return False, f"Bạn phải nhập ĐẦY ĐỦ thông tin sinh viên"
        for student in self.list_students:
            if new_student.ID == student.ID:
                return False, f"Mã sinh viên {new_student.ID} đã tồn tại!"
        self.list_students.append(new_student)
        try:
            with open(self.csv_file, 'a', encoding="utf-8-sig", newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow([
                    new_student.ID, new_student.full_name, new_student.DateOfBirth,
                    new_student.Gender, new_student.Class, new_student.GPA
                ])
            return True, "Thêm sinh viên thành công"
        except Exception as e:
            return False, f"Lỗi đọc file {e}"

    def edit_student(self, new_student, old_student):
        if not new_student.ID or not new_student.full_name or not new_student.Class or not new_student.GPA:
            return False, f"Bạn phải nhập ĐẦY ĐỦ thông tin sinh viên"
        if new_student.ID != old_student.ID:
            for student in self.list_students:
                if new_student.ID == student.ID:
                    return False, f"Mã sinh viên {new_student.ID} đã tồn tại!"
        for index, student in enumerate(self.list_students):
            if old_student == student:
                self.list_students[index] = new_student
                self.update_data_Csv()
                return True, "Thay đổi thôn tin sinh viên thành công"
        return False, "Không tìm thấy sinh viên"

    def delete_student(self, student):
        for s in self.list_students:
            if s.ID == student.ID:
                self.list_students.remove(s)
                self.update_data_Csv()
                return True, "Xóa sinh viên thành công"
        return False, "Không tìm thấy sinh viên này trong hệ thống!"
