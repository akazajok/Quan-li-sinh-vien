# Hệ Thống Quản Lý Sinh Viên - PyQt5 UI Files

## Các file UI đã tạo:

### 1. student_management.ui
File UI chính cho ứng dụng quản lý sinh viên, bao gồm:
- **Sidebar**: Menu điều hướng với Dashboard và Sinh Viên
- **Dashboard Page**: Trang tổng quan với thống kê và danh sách sinh viên mới
- **Students Page**: Trang quản lý sinh viên với bảng dữ liệu và tìm kiếm

### 2. add_student_dialog.ui
Dialog để thêm sinh viên mới với các trường:
- Mã Sinh Viên
- Họ và Tên
- Khóa Học (ComboBox)
- Email

## Cách sử dụng:

### 1. Load file UI trong Python:

```python
from PyQt5 import QtWidgets, uic

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        uic.loadUi('student_management.ui', self)

        # Kết nối signals
        self.dashboardButton.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(0))
        self.studentsButton.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(1))
        self.addStudentButton.clicked.connect(self.show_add_dialog)

    def show_add_dialog(self):
        dialog = AddStudentDialog(self)
        if dialog.exec_():
            # Xử lý thêm sinh viên
            pass

class AddStudentDialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(AddStudentDialog, self).__init__(parent)
        uic.loadUi('add_student_dialog.ui', self)

if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
```

### 2. Hoặc convert sang Python code:

```bash
pyuic5 student_management.ui -o student_management_ui.py
pyuic5 add_student_dialog.ui -o add_student_dialog_ui.py
```

## Tính năng UI:

✅ Giao diện hiện đại với màu xanh chủ đạo (#3b5bdb)
✅ Sidebar cố định với navigation
✅ 2 trang: Dashboard và Quản lý sinh viên
✅ Thẻ thống kê (cards) hiển thị số liệu
✅ Bảng dữ liệu sinh viên với 5 cột
✅ Tìm kiếm sinh viên
✅ Dialog thêm sinh viên mới
✅ Responsive và dễ tùy chỉnh

## Lưu ý:

- File UI đã bao gồm đầy đủ styling CSS trong thuộc tính styleSheet
- Các button đã được thiết lập checkable cho navigation
- Table widget đã có dữ liệu mẫu
- Dialog có validation cơ bản thông qua accept/reject slots
