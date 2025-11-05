import tkinter as tk
from tkinter import ttk

def them():
    print("Thêm khách hàng")

def xoa():
    pass

def sua():
    pass

def huy():
    pass

def luu():
    pass

def thoat():
    root.quit()

# === TẠO FORM CHÍNH ===
root = tk.Tk()
root.title("Quản Lý Đặt Vé")
root.geometry("1000x650")
root.config(bg="#fff8dc")  # Màu nền vàng nhạt

# ========== Nút Về Trang Chủ ==========
btn_home = tk.Button(root, text="Về Trang Chủ", font=("Times New Roman", 10, "bold"), bg="white", relief="groove", command=quit)
btn_home.place(x=50, y=30)

# === TIÊU ĐỀ CHÍNH ===
title_label = tk.Label(root, text="Quản Lý Đặt Vé", font=("Arial", 20, "bold"), bg="#fff8dc")
title_label.place(x=400, y=45)

# === NHÃN & Ô NHẬP LIỆU ===
tk.Label(root, text="Mã Vé", font=("Arial", 12), bg="#fff8dc").place(x=150, y=130)
entry_ma_ve = tk.Entry(root, width=25)
entry_ma_ve.place(x=230, y=130)

tk.Label(root, text="Số Lượng", font=("Arial", 12), bg="#fff8dc").place(x=550, y=130)
spin_so_luong = tk.Spinbox(root, from_=1, to=100, width=10)
spin_so_luong.place(x=640, y=130)

tk.Label(root, text="Mã Chuyến Đi", font=("Arial", 12), bg="#fff8dc").place(x=150, y=180)
entry_ma_cd = tk.Entry(root, width=25)
entry_ma_cd.place(x=280, y=180)

tk.Label(root, text="Giá Vé", font=("Arial", 12), bg="#fff8dc").place(x=550, y=180)
entry_gia_ve = tk.Entry(root, width=25)
entry_gia_ve.place(x=640, y=180)

tk.Label(root, text="Mã Khách Hàng", font=("Arial", 12), bg="#fff8dc").place(x=150, y=230)
entry_ma_kh = tk.Entry(root, width=25)
entry_ma_kh.place(x=280, y=230)

tk.Label(root, text="Trạng Thái", font=("Arial", 12), bg="#fff8dc").place(x=550, y=230)
entry_trang_thai = tk.Entry(root, width=25)
entry_trang_thai.place(x=640, y=230)

tk.Label(root, text="Ngày Đặt", font=("Arial", 12), bg="#fff8dc").place(x=150, y=280)
entry_ngay_dat = tk.Entry(root, width=25)
entry_ngay_dat.place(x=280, y=280)

tk.Label(root, text="Thành Tiền", font=("Arial", 12), bg="#fff8dc").place(x=550, y=280)
entry_thanh_tien = tk.Entry(root, width=25)
entry_thanh_tien.place(x=640, y=280)

# ========== Các nút chức năng bên phải ==========
button_style = {"font": ("Times New Roman", 13, "bold"), "bg": "#B0E0E6", "width": 8, "height": 1}

btn_them = tk.Button(root, text="Thêm", **button_style, command=them)
btn_them.place(x=820, y=120)

btn_xoa = tk.Button(root, text="Xóa", **button_style, command=xoa)
btn_xoa.place(x=820, y=200)

btn_sua = tk.Button(root, text="Sửa", **button_style, command=sua)
btn_sua.place(x=820, y=280)

btn_huy = tk.Button(root, text="Hủy", **button_style, command=huy)
btn_huy.place(x=820, y=360)

btn_luu = tk.Button(root, text="Lưu", **button_style, command=luu)
btn_luu.place(x=820, y=440)

btn_thoat = tk.Button(root, text="Thoát", **button_style, command=thoat)
btn_thoat.place(x=820, y=520)

# === KHUNG THÔNG TIN ĐẶT VÉ ===
frame_info = tk.LabelFrame(root, text="Thông Tin Đặt Vé", font=("Arial", 12, "bold"), bg="#fff8dc", width=750, height=220)
frame_info.place(x=50, y=370)

# Bảng dữ liệu (Treeview)
columns = ("ma_ve", "ma_cd", "ma_kh", "ngay_dat", "so_luong", "gia_ve", "trang_thai", "thanh_tien")
tree = ttk.Treeview(frame_info, columns=columns, show="headings", height=10)
tree.heading("ma_ve", text="Mã Vé")
tree.heading("ma_cd", text="Mã Chuyến Đi")
tree.heading("ma_kh", text="Mã Khách Hàng")
tree.heading("ngay_dat", text="Ngày Đặt")
tree.heading("so_luong", text="Số Lượng")
tree.heading("gia_ve", text="Giá Vé")
tree.heading("trang_thai", text="Trạng Thái")
tree.heading("thanh_tien", text="Thành Tiền")
tree.place(x=10, y=10, width=700, height=180)

# === CHẠY FORM ===
root.mainloop()
