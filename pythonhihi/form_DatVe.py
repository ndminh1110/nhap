import tkinter as tk
from tkinter import ttk

# === TẠO FORM CHÍNH ===
root = tk.Tk()
root.title("Quản Lý Đặt Vé")
root.geometry("1000x650")
root.config(bg="#fff8dc")  # Màu nền vàng nhạt

# === NÚT VỀ TRANG CHỦ ===
btn_home = tk.Button(root, text="Về Trang Chủ", bg="#f0f0f0", font=("Arial", 12, "bold"), width=12, height=2)
btn_home.place(x=50, y=40)

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

# === CÁC NÚT CHỨC NĂNG (bên phải) ===
btn_them = tk.Button(root, text="Thêm", bg="#87cefa", font=("Arial", 12, "bold"), width=10)
btn_them.place(x=850, y=150)

btn_xoa = tk.Button(root, text="Xóa", bg="#87cefa", font=("Arial", 12, "bold"), width=10)
btn_xoa.place(x=850, y=200)

btn_sua = tk.Button(root, text="Sửa", bg="#87cefa", font=("Arial", 12, "bold"), width=10)
btn_sua.place(x=850, y=250)

btn_huy = tk.Button(root, text="Hủy", bg="#87cefa", font=("Arial", 12, "bold"), width=10)
btn_huy.place(x=850, y=300)

btn_luu = tk.Button(root, text="Lưu", bg="#87cefa", font=("Arial", 12, "bold"), width=10)
btn_luu.place(x=850, y=350)

btn_thoat = tk.Button(root, text="Thoát", bg="#87cefa", font=("Arial", 12, "bold"), width=10)
btn_thoat.place(x=850, y=400)

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
