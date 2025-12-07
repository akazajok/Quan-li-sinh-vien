import csv
import random
from datetime import datetime, timedelta

# --- CẤU HÌNH ---
SO_LUONG_SINH_VIEN = 3000  # Số lượng sinh viên muốn tạo (Bạn có thể tăng lên 10000 nếu thích)
FILE_NAME = "database.csv"

# --- DỮ LIỆU MẪU VIỆT NAM ---
HO = ["Nguyễn", "Trần", "Lê", "Phạm", "Hoàng", "Huỳnh", "Phan", "Vũ", "Võ", "Đặng", "Bùi", "Đỗ", "Hồ", "Ngô", "Dương",
      "Lý"]
LOT_NAM = ["Văn", "Hữu", "Đức", "Thành", "Công", "Minh", "Quốc", "Gia", "Xuân", "Ngọc", "Thanh", "Bảo", "Tuấn", "Hoàng"]
LOT_NU = ["Thị", "Thu", "Phương", "Thanh", "Mỹ", "Ngọc", "Hồng", "Kim", "Khánh", "Diệu", "Thảo", "Bích", "Uyên",
          "Hương"]
TEN_NAM = ["Hùng", "Cường", "Dũng", "Nam", "Hải", "Hiếu", "Minh", "Tùng", "Sơn", "Phúc", "Vinh", "Quân", "Nghĩa",
           "Long"]
TEN_NU = ["Hoa", "Lan", "Hương", "Trang", "Mai", "Ly", "Hà", "Linh", "Huyền", "Tâm", "Thư", "Anh", "Nga", "Châu", "Vân"]

# Mã ngành và Lớp tương ứng
# Cấu trúc: "Mã Prefix trong MSV": ("Mã Lớp", "Ngành")
MA_NGANH = {
    "DCCN": ("CNTT", "D24CNTT"),
    "DCAT": ("ATTT", "D24ATTT"),
    "DCVT": ("DTVT", "D24DTVT"),
    "DCTM": ("TMDT", "D24TMDT"),
    "DCMK": ("MKT", "D24MKT"),
    "DCTN": ("AI", "D24AI"),
    "DCKT": ("KT", "D24KT"),
    "DCQK": ("QTKD", "D24QTKD"),
    "DCLG": ("LOG", "D24LOG")
}


def tao_ten_va_gioi_tinh():
    """Random tên và giới tính phù hợp"""
    ho = random.choice(HO)
    if random.choice([True, False]):  # 50% là Nam
        gioi_tinh = "Nam"
        lot = random.choice(LOT_NAM)
        ten = random.choice(TEN_NAM)
    else:  # 50% là Nữ
        gioi_tinh = "Nữ"
        lot = random.choice(LOT_NU)
        ten = random.choice(TEN_NU)
    full_name = f"{ho} {lot} {ten}"
    return full_name, gioi_tinh


def tao_ngay_sinh():
    """Random ngày sinh cho sinh viên năm nhất (khoảng 2006)"""
    start_date = datetime(2006, 1, 1)
    end_date = datetime(2006, 12, 31)
    random_days = random.randint(0, (end_date - start_date).days)
    birth_date = start_date + timedelta(days=random_days)
    return birth_date.strftime("%d/%m/%Y")


def tao_gpa():
    """
    Tạo GPA theo yêu cầu:
    - 10% cơ hội được >= 3.6 (Xuất sắc)
    - 90% cơ hội từ 1.5 đến 3.59 (Trung bình - Khá - Giỏi)
    """
    if random.random() < 0.1:  # 10% tỉ lệ rơi vào đây
        # Random từ 3.60 đến 4.00
        gpa = random.uniform(3.6, 4.0)
    else:
        # Random từ 1.5 đến 3.59 (Điểm thực tế ít khi thấp hơn 1.5)
        gpa = random.uniform(1.5, 3.59)

    return round(gpa, 2)  # Làm tròn 2 chữ số thập phân


def main():
    print(f"Đang tạo {SO_LUONG_SINH_VIEN} dữ liệu mẫu...")

    danh_sach_sv = []

    # Tạo danh sách các key của ngành để random
    keys_nganh = list(MA_NGANH.keys())

    # Biến đếm số thứ tự cho từng ngành để mã SV không trùng
    # Ví dụ: {'DCCN': 1, 'DCAT': 1...}
    counter_nganh = {k: 1 for k in keys_nganh}

    for _ in range(SO_LUONG_SINH_VIEN):
        # 1. Chọn ngành ngẫu nhiên
        key_ma = random.choice(keys_nganh)
        lop_prefix, lop_root = MA_NGANH[key_ma]

        # 2. Tạo Mã Sinh Viên (Ví dụ: B24DCCN001)
        stt = counter_nganh[key_ma]
        msv = f"B24{key_ma}{stt:03d}"  # :03d nghĩa là số 1 thành 001, 10 thành 010
        counter_nganh[key_ma] += 1

        # 3. Tạo Tên, Giới tính, Ngày sinh
        ho_ten, gioi_tinh = tao_ten_va_gioi_tinh()
        ngay_sinh = tao_ngay_sinh()

        # 4. Tạo Lớp (Chia thành nhiều lớp nhỏ 01, 02, 03 cho phong phú)
        # Ví dụ: D24CNTT01, D24CNTT02...
        so_lop = random.randint(1, 4)
        lop = f"{lop_root}0{so_lop}"

        # 5. Tạo GPA (Logic 10%)
        gpa = tao_gpa()

        # Thêm vào danh sách
        # Cấu trúc file csv của bạn: ID, Name, DoB, Gender, Class, GPA
        danh_sach_sv.append([msv, ho_ten, ngay_sinh, gioi_tinh, lop, gpa])

    # --- GHI VÀO FILE CSV ---
    try:
        # Dùng mode 'w' để ghi đè (xóa dữ liệu cũ), nếu muốn ghi nối thêm thì dùng 'a'
        # encoding='utf-8-sig' để Excel hiển thị đúng tiếng Việt
        with open(FILE_NAME, mode='w', encoding='utf-8-sig', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(danh_sach_sv)

        print(f"Thành công! Đã tạo file '{FILE_NAME}' với {SO_LUONG_SINH_VIEN} sinh viên.")
        print("Bạn có thể chạy main.py để kiểm tra tốc độ.")

    except Exception as e:
        print(f"Có lỗi xảy ra khi ghi file: {e}")


if __name__ == "__main__":
    main()