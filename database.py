import csv
import os

class Student:
    def __init__(self, ID, full_name, DateOfBirth, Gender, Class, GPA):
        self.ID = ID
        self.full_name = full_name
        self.DateOfBirth = DateOfBirth
        self.Gender = Gender
        self.Class = Class
        self.GPA = GPA

class CsvData:
    def __init__(self, filename = "database.csv"):
        self.csv_file = filename

    def get_data_Csv(self):
        list_student = []
        with open(self.csv_file, 'r', encoding="utf-8-sig", newline='') as csvfile:
            for line in csvfile:
                try:
                    ID, full_name, DateOfBirth, Gender, Class, GPA = line.strip().split(',')
                    GPA = float(GPA)
                    list_student.append(Student(ID, full_name, DateOfBirth, Gender, Class, GPA))
                except:
                    pass
        return list_student

    def update_data_Csv(self, list_student):
        with open(self.csv_file, 'w', encoding="utf-8-sig", newline='') as csvfile:
            for student in list_student:
                csvfile.write(
                    f"{student.ID},{student.full_name},{student.DateOfBirth},{student.Gender},{student.Class},{student.GPA}\n")

