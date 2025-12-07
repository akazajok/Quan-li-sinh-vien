import csv
import random
import calendar

# ================= CẤU HÌNH DỮ LIỆU =================

HO = ["Nguyễn", "Trần", "Lê", "Phạm", "Hoàng", "Huỳnh", "Phan", "Vũ", "Võ", "Đặng",
      "Bùi", "Đỗ", "Hồ", "Ngô", "Dương", "Lý", "Phí", "Đinh", "Trương", "Lương", "Trịnh"]

DEM_NAM = ["Văn", "Đức", "Thành", "Minh", "Quốc", "Gia", "Bảo", "Ngọc", "Tuấn", "Hoàng", "Hữu", "Công", "Xuân", "Thanh"]
DEM_NU = ["Thị", "Mỹ", "Thu", "Hồng", "Thanh", "Ngọc", "Khánh", "Phương", "Thảo", "Uyên", "Bích", "Kim", "Diệu"]

TEN_NAM = ["Hùng", "Dũng", "Cường", "Vinh", "Nam", "Sơn", "Tùng", "Phúc", "Minh", "Quân", "Hiếu", "Nghĩa", "Long",
           "Hải", "Khánh"]
TEN_NU = ["Lan", "Hương", "Trang", "Linh", "Mai", "Hoa", "Vân", "Anh", "Nga", "Huyền", "Ly", "Thư", "Tâm", "Hà", "Châu"]

# Cập nhật mã ngành AI -> DCTN
MAP_NGANH = {
    "CNTT": "DCCN",
    "ATTT": "DCAT",
    "DTVT": "DCVT",
    "KT": "DCKT",
    "MKT": "DCMK",
    "QTKD": "DCQK",
    "TMDT": "DCTM",
    "AI": "DCTN",  # Đã đổi theo yêu cầu
    "LOG": "DCLG"
}

# Thêm khóa D25
KHOA_HOC = {
    "D21": 2003,
    "D22": 2004,
    "D23": 2005,
    "D24": 2006,
    "D25": 2007  # Đã thêm
}


# ================= HÀM HỖ TRỢ =================

def tao_ten_va_gioi_tinh():
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
    return f"{ho} {dem} {ten}", gioi_tinh


def tao_ngay_sinh(year):
    month = random.randint(1, 12)
    _, max_day = calendar.monthrange(year, month)
    day = random.randint(1, max_day)
    return f"{day:02d}/{month:02d}/{year}"


def tao_gpa():
    # Tỉ lệ điểm: 5% Liệt | 15% TB | 50% Khá | 20% Giỏi | 10% Xuất sắc
    weights = [0.05, 0.15, 0.50, 0.20, 0.10]
    ranges = [(0.0, 1.9), (2.0, 2.4), (2.5, 3.19), (3.2, 3.59), (3.6, 4.0)]
    selected_range = random.choices(ranges, weights=weights, k=1)[0]
    return round(random.uniform(selected_range[0], selected_range[1]), 2)


# ================= HÀM CHÍNH =================

def generate_database(filename="database.csv"):
    data = []
    total_sv = 0

    print("🚀 Đang tạo dữ liệu (D21 - D25)...")

    for khoa, nam_sinh in KHOA_HOC.items():
        year_suffix = khoa[1:]  # Lấy chuỗi "21", "25"...

        for ten_nganh, ma_sv_code in MAP_NGANH.items():
            stt_sv = 1

            # GIẢM SỐ LỚP: Chỉ tạo 1 lớp cho mỗi ngành để giảm tổng số SV
            for i in range(1, 2):
                ma_lop = f"{khoa}{ten_nganh}{i:02d}"

                # GIẢM SĨ SỐ: 10 - 15 sinh viên/lớp
                si_so_lop = random.randint(10, 15)

                for _ in range(si_so_lop):
                    # Mã SV 3 số: :03d
                    msv = f"B{year_suffix}{ma_sv_code}{stt_sv:03d}"

                    ho_ten, gioi_tinh = tao_ten_va_gioi_tinh()
                    ngay_sinh = tao_ngay_sinh(nam_sinh)
                    gpa = tao_gpa()

                    # Thêm vào list (không có header như yêu cầu)
                    data.append([msv, ho_ten, ngay_sinh, gioi_tinh, ma_lop, gpa])

                    stt_sv += 1
                    total_sv += 1

    # Sắp xếp lại theo Lớp rồi đến Mã SV cho đẹp
    data.sort(key=lambda x: (x[4], x[0]))

    try:
        with open(filename, mode='w', encoding='utf-8-sig', newline='') as f:
            writer = csv.writer(f)
            writer.writerows(data)

        print(f"✅ XONG! File '{filename}' đã được tạo.")
        print(f"📊 Tổng số sinh viên: {total_sv}")
        print("ℹ️  Thay đổi: Mã ngành AI -> DCTN, MSV 3 số, có khóa D25.")

    except Exception as e:
        print(f"❌ Lỗi: {e}")


if __name__ == "__main__":
    generate_database()