import csv
import random

# Cấu hình dữ liệu
HO = ["Nguyễn", "Trần", "Lê", "Phạm", "Hoàng", "Huỳnh", "Phan", "Vũ", "Võ", "Đặng", "Bùi", "Đỗ", "Hồ", "Ngô", "Dương",
      "Lý"]
DEM = ["Văn", "Thị", "Đức", "Thành", "Minh", "Mỹ", "Quốc", "Gia", "Bảo", "Ngọc", "Khánh", "Thu", "Hồng", "Tuấn",
       "Thanh"]
TEN = ["An", "Bình", "Cường", "Dũng", "Giang", "Hương", "Hùng", "Lan", "Linh", "Minh", "Nam", "Nga", "Oanh", "Phúc",
       "Quân", "Quang", "Sơn", "Tâm", "Thảo", "Trang", "Tuấn", "Uyên", "Vân", "Việt", "Vinh", "Yến"]

# Cấu trúc: (Khóa, Năm sinh, Mã đầu ngành)
KHOA_HOC = [
    ("D21", 2003, ["CNTT", "ATTT", "DTVT", "KT", "MKT"]),
    ("D22", 2004, ["CNTT", "ATTT", "DTVT", "KT", "QTKD"]),
    ("D23", 2005, ["CNTT", "ATTT", "DTVT", "KT", "TMDT"]),
    ("D24", 2006, ["CNTT", "ATTT", "DTVT", "KT", "AI"]),
    ("D25", 2007, ["CNTT", "ATTT", "DTVT", "KT", "LOG"])
]


def tao_ten_ngau_nhien():
    ho = random.choice(HO)
    dem = random.choice(DEM)
    ten = random.choice(TEN)
    # Xác định giới tính dựa trên tên đệm (tương đối)
    nu_indicator = ["Thị", "Mỹ", "Thu", "Hương", "Lan", "Nga", "Oanh", "Thảo", "Trang", "Uyên", "Vân", "Yến"]
    gioi_tinh = "Nữ" if dem in nu_indicator or ten in nu_indicator else random.choice(["Nam", "Nam", "Nam", "Nữ"])
    return f"{ho} {dem} {ten}", gioi_tinh


def tao_ngay_sinh(nam_sinh):
    day = random.randint(1, 28)
    month = random.randint(1, 12)
    return f"{day:02d}/{month:02d}/{nam_sinh}"


def main(so_luong=50):
    headers = ['Mã SV', 'Họ tên', 'Ngày sinh', 'Giới tính', 'Lớp', 'GPA']
    data = []

    da_co_msv = set()

    for _ in range(so_luong):
        # 1. Chọn ngẫu nhiên 1 khóa (D21 -> D25)
        khoa, nam_sinh, nganh_list = random.choice(KHOA_HOC)
        nganh = random.choice(nganh_list)

        # 2. Tạo Mã SV: Ví dụ B23 + DCCN + 001
        # Mã ngành viết tắt cho MSV
        ma_nganh_code = "DCCN" if nganh == "CNTT" else "DCAT" if nganh == "ATTT" else "DCVT" if nganh == "DTVT" else "DCKT"

        # Random số thứ tự 001 -> 999
        while True:
            stt = random.randint(1, 999)
            msv = f"B{khoa[1:]}{ma_nganh_code}{stt:03d}"  # VD: B23DCCN123
            if msv not in da_co_msv:
                da_co_msv.add(msv)
                break

        # 3. Tạo thông tin khác
        ho_ten, gioi_tinh = tao_ten_ngau_nhien()
        ngay_sinh = tao_ngay_sinh(nam_sinh)

        # Lớp: VD D23CNTT01
        lop = f"{khoa}{nganh}{random.randint(1, 5):02d}"

        # GPA: Random có trọng số (nhiều người điểm khá giỏi hơn điểm kém)
        # uniform(2.0, 4.0) nhưng xu hướng nghiêng về 2.8 - 3.5
        gpa = round(random.triangular(2.0, 4.0, 3.2), 2)

        data.append([msv, ho_ten, ngay_sinh, gioi_tinh, lop, gpa])

    # Sắp xếp theo Mã SV cho đẹp trước khi lưu
    data.sort(key=lambda x: x[0])

    # Ghi file
    try:
        with open('ramdom_data.csv', mode='w', encoding='utf-8-sig', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(headers)
            writer.writerows(data)
        print(f"✅ Đã tạo thành công {so_luong} sinh viên đa dạng (D21-D25) vào file ramdom_data.csv")
    except Exception as e:
        print(f"❌ Lỗi: {e}")


if __name__ == "__main__":
    # Bạn muốn bao nhiêu sinh viên thì sửa số ở đây
    main(100)