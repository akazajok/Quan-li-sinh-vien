import csv
import random
from datetime import datetime, timedelta

# --- CẤU HÌNH ---
SO_LUONG_SINH_VIEN = 20000
FILE_NAME = "database.csv"

# --- DỮ LIỆU MẪU ---
HO = ["Nguyễn", "Trần", "Lê", "Phạm", "Hoàng", "Huỳnh", "Phan", "Vũ", "Võ", "Đặng", "Bùi", "Đỗ", "Hồ", "Ngô", "Dương",
      "Lý", "Vương", "Trịnh", "Đinh", "Lâm"]
LOT_NAM = ["Văn", "Hữu", "Đức", "Thành", "Công", "Minh", "Quốc", "Gia", "Xuân", "Ngọc", "Thanh", "Bảo", "Tuấn", "Hoàng",
           "Tiến", "Mạnh", "Quang", "Đăng"]
LOT_NU = ["Thị", "Thu", "Phương", "Thanh", "Mỹ", "Ngọc", "Hồng", "Kim", "Khánh", "Diệu", "Thảo", "Bích", "Uyên",
          "Hương", "Lan", "Quỳnh", "Ánh"]
TEN_NAM = ["Hùng", "Cường", "Dũng", "Nam", "Hải", "Hiếu", "Minh", "Tùng", "Sơn", "Phúc", "Vinh", "Quân", "Nghĩa",
           "Long", "Bách", "Khánh", "An", "Bình", "Thắng", "Đạt"]
TEN_NU = ["Hoa", "Lan", "Hương", "Trang", "Mai", "Ly", "Hà", "Linh", "Huyền", "Tâm", "Thư", "Anh", "Nga", "Châu", "Vân",
          "Ngân", "Yến", "Thảo", "Nhi", "Trâm"]

MA_NGANH = {
    "DCCN": ("CNTT", "D24CNTT"), "DCAT": ("ATTT", "D24ATTT"), "DCVT": ("DTVT", "D24DTVT"),
    "DCTM": ("TMDT", "D24TMDT"), "DCMK": ("MKT", "D24MKT"), "DCTN": ("AI", "D24AI"),
    "DCKT": ("KT", "D24KT"), "DCQK": ("QTKD", "D24QTKD"), "DCLG": ("LOG", "D24LOG")
}

# Tỉ lệ Nam dao động ngẫu nhiên từ 65% đến 80% (cho phần còn lại sau khi trừ đi giới tính Khác)
TI_LE_NAM = random.uniform(0.65, 0.80)
TI_LE_GIOI = random.uniform(0.15, 0.25)
TI_LE_KHAC = 0.03  # 3% cho giới tính Khác


def tao_ten_va_gioi_tinh():
    ho = random.choice(HO)

    rand_val = random.random()

    # 1. Xử lý giới tính KHÁC (3%)
    if rand_val < TI_LE_KHAC:
        gioi_tinh = "Khác"
        # Tên của giới tính Khác có thể là Nam hoặc Nữ ngẫu nhiên
        if random.random() < 0.5:
            lot = random.choice(LOT_NAM)
            ten = random.choice(TEN_NAM)
        else:
            lot = random.choice(LOT_NU)
            ten = random.choice(TEN_NU)

    # 2. Xử lý giới tính NAM
    elif rand_val < (TI_LE_KHAC + TI_LE_NAM):
        gioi_tinh = "Nam"
        lot = random.choice(LOT_NAM)
        ten = random.choice(TEN_NAM)

    # 3. Còn lại là NỮ
    else:
        gioi_tinh = "Nữ"
        lot = random.choice(LOT_NU)
        ten = random.choice(TEN_NU)

    return f"{ho} {lot} {ten}", gioi_tinh


def tao_ngay_sinh():
    start_date = datetime(2006, 1, 1)
    end_date = datetime(2006, 12, 31)
    days_between = (end_date - start_date).days
    return (start_date + timedelta(days=random.randint(0, days_between))).strftime("%d/%m/%Y")


def tao_gpa():
    rand = random.random()
    ti_le_xs = TI_LE_GIOI / 3
    limit_gioi = 1.0 - ti_le_xs - TI_LE_GIOI
    limit_kha = limit_gioi - 0.40
    limit_tb = limit_kha - 0.25

    if rand < limit_tb:
        gpa = random.uniform(1.0, 1.99)
    elif rand < limit_kha:
        gpa = random.uniform(2.0, 2.49)
    elif rand < limit_gioi:
        gpa = random.uniform(2.5, 3.19)
    elif rand < (1.0 - ti_le_xs):
        gpa = random.uniform(3.2, 3.59)
    else:
        gpa = random.uniform(3.6, 4.0)
    return round(gpa, 2)


def main():
    print(f"--- ĐANG TẠO DỮ LIỆU ---")
    print(f"   - Tỉ lệ 'Khác': {TI_LE_KHAC * 100}%")

    danh_sach_sv = []
    keys_nganh = list(MA_NGANH.keys())
    counter_nganh = {k: 1 for k in keys_nganh}

    for _ in range(SO_LUONG_SINH_VIEN):
        key_ma = random.choice(keys_nganh)
        lop_prefix, lop_root = MA_NGANH[key_ma]
        stt = counter_nganh[key_ma]
        msv = f"B24{key_ma}{stt:05d}"
        counter_nganh[key_ma] += 1

        ho_ten, gioi_tinh = tao_ten_va_gioi_tinh()
        ngay_sinh = tao_ngay_sinh()
        so_lop = random.randint(1, 10)
        lop = f"{lop_root}{so_lop:02d}"
        gpa = tao_gpa()

        danh_sach_sv.append([msv, ho_ten, ngay_sinh, gioi_tinh, lop, gpa])

    with open(FILE_NAME, mode='w', encoding='utf-8-sig', newline='') as file:
        csv.writer(file).writerows(danh_sach_sv)
    print("✅ XONG!")


if __name__ == "__main__":
    main()