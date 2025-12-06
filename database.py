import csv
import os

from numpy.f2py.crackfortran import expectbegin
from function_dialog import Ui_Dialog

class Student:
    def __init__(self, ID, full_name, DateOfBirth, Gender, Class, GPA):
        self.ID = ID
        self.full_name = full_name
        self.DateOfBirth = DateOfBirth
        self.Gender = Gender
        self.Class = Class
        self.GPA = float(GPA)

class CsvData:
    def __init__(self, filename = "database.csv"):
        self.csv_file = filename
        self.function_dialog = Ui_Dialog()

    def get_data_Csv(self):
        list_student = []
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
                            list_student.append(Student(ID, full_name, DateOfBirth, Gender, Class, GPA))
                        except:
                            pass
        except Exception as e:
            print(f"Lỗi khi đọc file: {e}")

        return list_student

    def update_data_Csv(self, list_student):
        try:
            with open(self.csv_file, 'w', encoding="utf-8-sig", newline='') as csvfile:
                writer = csv.writer(csvfile)
                for student in list_student:
                    writer.writerow([
                        student.ID,  student.full_name,  student.DateOfBirth,
                        student.Gender, student.Class, student.GPA
                    ])
        except Exception as e:
            print(f"Lỗi khi đọc file: {e}")

    def add_student_to_csv(self):
        ID = self.function_dialog.lineEdit_ID.text().strip()
        full_name = self.function_dialog.lineEdit_fullName.text().strip()
        DateOfBirth = self.function_dialog.dateEdit_DateBirth.text().strip()
        Gender = self.function_dialog.comboBox_gender.text().strip()
        Class = self.function_dialog.lineEdit_class.text().strip()
        GPA = self.function_dialog.lineEdit_GPA.text().strip()
        student = Student(ID, full_name, DateOfBirth, Gender, Class, GPA)
        try:
            with open(self.csv_file, 'a', encoding="utf-8-sig", newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow([ ID, full_name, DateOfBirth, Gender, Class, GPA])
        except Exception as e:
            print(f"Lỗi khi đọc file: {e}")
        return student
            
