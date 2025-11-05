import tkinter as tk
from tkinter import ttk
from tkcalendar import DateEntry

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

'''tk.Label(root, text="Số Lượng", font=("Arial", 12), bg="#fff8dc").place(x=550, y=130)
spin_so_luong = tk.Spinbox(root, from_=1, to=100, width=10)
spin_so_luong.place(x=640, y=130)'''

# ========== Thông tin khách hàng ==========
frame_info = tk.Frame(root, bg="#FFFACD")
frame_info.place(x=100, y=100)

tk.Label(frame_info, text="Mã Vé", bg="#FFFACD", font=("Times New Roman", 12)).grid(row=0, column=0, sticky="w", pady=5)
entry_maVe = tk.Entry(frame_info, width=30)
entry_maVe.grid(row=0, column=1, padx=10, pady=5)

tk.Label(frame_info, text="Số Lượng", font=("Times New Roman", 12), bg="#fff8dc").grid(row=0, column=2, sticky="w", padx=10, pady=5)
spin_soLuong = tk.Spinbox(frame_info, from_=1, to=100, width=10)
spin_soLuong.grid(row=0, column=3, padx=10, pady=5, columnspan=2)

tk.Label(frame_info, text="Mã Chuyến Đi", bg="#FFFACD", font=("Times New Roman", 12)).grid(row=2, column=0, sticky="w", pady=5)
entry_maCD = tk.Entry(frame_info, width=30)
entry_maCD.grid(row=1, column=1, padx=10, pady=5)

tk.Label(frame_info, text="Giá Vé", bg="#FFFACD", font=("Times New Roman", 12)).grid(row=1, column=2, sticky="w", padx=10)
entry_giaVe = tk.Entry(frame_info, width=30)
entry_giaVe.grid(row=1, column=3, padx=10, pady=5, columnspan=2)

tk.Label(frame_info, text="Mã Khách Hàng", bg="#FFFACD", font=("Times New Roman", 12)).grid(row=1, column=0, sticky="w", pady=5)
entry_maKH = tk.Entry(frame_info, width=30)
entry_maKH.grid(row=2, column=1, padx=10, pady=5)

tk.Label(frame_info, text="Trạng Thái", bg="#FFFACD", font=("Times New Roman", 12)).grid(row=2, column=2, sticky="w", padx=10)
entry_trangThai = tk.Entry(frame_info, width=30)
entry_trangThai.grid(row=2, column=3, padx=10, pady=5, columnspan=2)

tk.Label(frame_info, text="Ngày Đặt", bg="#FFFACD", font=("Times New Roman", 12)).grid(row=3, column=0, sticky="w", padx=5)
date_ngDat = DateEntry(frame_info, width=12, background='darkblue', foreground='white', borderwidth=2, date_pattern='d/m/yyyy')
date_ngDat.grid(row=3, column=1, padx=10, pady=5)

tk.Label(frame_info, text="Thành Tiền", bg="#FFFACD", font=("Times New Roman", 12)).grid(row=3, column=2, sticky="w", padx=10)
entry_thanhTien = tk.Entry(frame_info, width=30)
entry_thanhTien.grid(row=3, column=3, padx=10, pady=5, columnspan=2)


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
frame_info = tk.LabelFrame(root, text="Thông Tin Đặt Vé", font=("Arial", 12, "bold"), bg="#fff8dc", width=750, height=320)
frame_info.place(x=50, y=250)

# Bảng dữ liệu (Treeview)
columns = ("maVe", "maCD", "maKH", "ngDat", "soLuong", "giaVe", "trangThai", "thanhTien")
tree = ttk.Treeview(frame_info, columns=columns, show="headings", height=10)
tree.heading("maVe", text="Mã Vé")
tree.heading("maCD", text="Mã Chuyến Đi")
tree.heading("maKH", text="Mã Khách Hàng")
tree.heading("ngDat", text="Ngày Đặt")
tree.heading("soLuong", text="Số Lượng")
tree.heading("giaVe", text="Giá Vé")
tree.heading("trangThai", text="Trạng Thái")
tree.heading("thanhTien", text="Thành Tiền")

tree.column("maVe", width=65)
tree.column("maCD", width=90)
tree.column("maKH", width=95)
tree.column("ngDat", width=80)
tree.column("soLuong", width=70)
tree.column("giaVe", width=90)
tree.column("trangThai", width=100)
tree.column("thanhTien", width=120)

tree.place(x=10, y=10, width=720, height=280)

# === CHẠY FORM ===
root.mainloop()
