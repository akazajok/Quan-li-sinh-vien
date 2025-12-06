import csv
import random
import calendar

# ================= CẤU HÌNH DỮ LIỆU MẪU =================
HO = ["Nguyễn", "Trần", "Lê", "Phạm", "Hoàng", "Huỳnh", "Phan", "Vũ", "Võ", "Đặng",
      "Bùi", "Đỗ", "Hồ", "Ngô", "Dương", "Lý", "Phí", "Đinh", "Trương", "Lương", "Trịnh"]

DEM_NAM = ["Văn", "Đức", "Thành", "Minh", "Quốc", "Gia", "Bảo", "Ngọc", "Tuấn", "Hoàng", "Hữu", "Công", "Xuân", "Thanh"]
DEM_NU = ["Thị", "Mỹ", "Thu", "Hồng", "Thanh", "Ngọc", "Khánh", "Phương", "Thảo", "Uyên", "Bích", "Kim", "Diệu"]

TEN_NAM = ["Hùng", "Dũng", "Cường", "Vinh", "Nam", "Sơn", "Tùng", "Phúc", "Minh", "Quân", "Hiếu", "Nghĩa", "Long",
           "Hải", "Khánh"]
TEN_NU = ["Lan", "Hương", "Trang", "Linh", "Mai", "Hoa", "Vân", "Anh", "Nga", "Huyền", "Ly", "Thư", "Tâm", "Hà", "Châu"]

# Cấu trúc: (Khóa, Năm sinh, Các mã ngành)
KHOA_HOC_INFO = [
    ("D21", 2003, ["CNTT", "ATTT", "DTVT", "KT", "MKT"]),
    ("D22", 2004, ["CNTT", "ATTT", "DTVT", "KT", "QTKD"]),
    ("D23", 2005, ["CNTT", "ATTT", "DTVT", "KT", "TMDT"]),
    ("D24", 2006, ["CNTT", "ATTT", "DTVT", "KT", "AI"]),
    ("D25", 2007, ["CNTT", "ATTT", "DTVT", "KT", "LOG"])
]


def tao_ten_va_gioi_tinh():
    """Tạo tên và giới tính khớp nhau"""
    is_nam = random.choice([True, False])
    ho = random.choice(HO)

    if is_nam:
        dem = random.choice(DEM_NAM)
        ten = random.choice(TEN_NAM)
        gioi_tinh = "Nam"
    else:
        dem = random.choice(DEM_NU)
        ten = random.choice(TEN_NU)
        gioi_tinh = "Nữ"

    full_name = f"{ho} {dem} {ten}"
    return full_name, gioi_tinh


def tao_ngay_sinh_chuan(year):
    """Tạo ngày sinh hợp lệ (xử lý cả năm nhuận)"""
    month = random.randint(1, 12)
    _, max_day = calendar.monthrange(year, month)
    day = random.randint(1, max_day)
    return f"{day:02d}/{month:02d}/{year}"


def tao_gpa_thuc_te():
    """
    Tạo GPA theo phân phối có trọng số để có cả người giỏi và người trượt.
    """
    # Định nghĩa các khoảng điểm và tỷ lệ xuất hiện (Trọng số)
    ranges = [
        ((0.0, 1.99), 10),  # 10% Sinh viên Yếu/Kém (Trượt)
        ((2.0, 2.49), 20),  # 20% Sinh viên Trung bình
        ((2.5, 3.19), 40),  # 40% Sinh viên Khá (Số đông)
        ((3.2, 3.59), 20),  # 20% Sinh viên Giỏi
        ((3.6, 4.0), 10)  # 10% Sinh viên Xuất sắc
    ]

    # Chọn ngẫu nhiên một khoảng dựa trên trọng số
    selected_range = random.choices(
        [r[0] for r in ranges],
        weights=[r[1] for r in ranges]
    )[0]

    # Random con số cụ thể trong khoảng đó
    gpa = random.uniform(selected_range[0], selected_range[1])
    return round(gpa, 2)


def tao_ma_sv(khoa, nganh, danh_sach_da_co):
    """Tạo mã SV không trùng lặp"""
    ma_nganh_code = {
        "CNTT": "DCCN", "ATTT": "DCAT", "DTVT": "DCVT",
        "KT": "DCKT", "MKT": "DCMK", "QTKD": "DCQK",
        "TMDT": "DCTM", "AI": "DCAI", "LOG": "DCLG"
    }.get(nganh, "DCXX")

    while True:
        stt = random.randint(1, 9999)  # Tăng lên 4 chữ số để chứa được nhiều SV hơn
        msv = f"B{khoa[1:]}{ma_nganh_code}{stt:04d}"  # VD: B23DCCN0123
        if msv not in danh_sach_da_co:
            danh_sach_da_co.add(msv)
            return msv


def generate_data(filename='ramdom_data.csv', so_luong=1000):

    data = []
    existed_msv = set()

    print(f"🔄 Đang khởi tạo dữ liệu cho {so_luong} sinh viên...")

    for i in range(so_luong):
        # 1. Chọn khóa học
        khoa_code, nam_sinh, list_nganh = random.choice(KHOA_HOC_INFO)
        nganh = random.choice(list_nganh)

        # 2. Tạo thông tin
        msv = tao_ma_sv(khoa_code, nganh, existed_msv)
        ho_ten, gioi_tinh = tao_ten_va_gioi_tinh()
        ngay_sinh = tao_ngay_sinh_chuan(nam_sinh)

        # 3. Tạo Lớp (VD: D21CNTT01 - 05)
        lop = f"{khoa_code}{nganh}{random.randint(1, 5):02d}"

        # 4. Tạo GPA theo logic mới (Có cả điểm trượt)
        gpa = tao_gpa_thuc_te()

        data.append([msv, ho_ten, ngay_sinh, gioi_tinh, lop, gpa])

        # In tiến trình mỗi khi xong 10% (để biết tool đang chạy)
        if (i + 1) % (so_luong // 10) == 0:
            print(f"   ...Đã tạo {i + 1}/{so_luong} sinh viên")

    # Sắp xếp danh sách
    data.sort(key=lambda x: (x[4], x[0]))

    # Ghi file
    try:
        with open(filename, mode='w', encoding='utf-8-sig', newline='') as f:
            writer = csv.writer(f)
            writer.writerows(data)
        print(f"✅ HOÀN TẤT! Đã tạo file '{filename}' với {so_luong} dòng.")
        print(f"   (Bao gồm cả sinh viên điểm thấp < 2.0 để test)")
    except Exception as e:
        print(f"❌ Lỗi ghi file: {e}")


if __name__ == "__main__":
    # Tạo 1000 sinh viên để test thoải mái
    generate_data('ramdom_data.csv', 1000)