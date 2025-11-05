import tkinter as tk
from tkinter import ttk
from tkcalendar import DateEntry
import pyodbc

conn = pyodbc.connect(
            'DRIVER={SQL Server};'
            'SERVER=ADMIN-PC;'          # hoặc tên server thật, ví dụ: LAPTOP\\SQLEXPRESS
            'DATABASE=QuanLyTuyenDuLich;'
            'Trusted_Connection=yes;'    # Nếu bạn dùng Windows Authentication
        )

def ve_trang_chu():
    root.destroy()

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

root = tk.Tk()
root.title("Quản Lý Khách Hàng")
root.geometry("1000x650")
root.configure(bg="#FFFACD")

# ========== Nút Về Trang Chủ ==========
btn_home = tk.Button(root, text="Về Trang Chủ", font=("Times New Roman", 10, "bold"), bg="white", relief="groove", command=ve_trang_chu)
btn_home.place(x=50, y=30)

# ========== Tiêu đề ==========
lbl_title = tk.Label(root, text="Quản Lý Khách Hàng", bg="#FFFACD", fg="black", font=("Times New Roman", 22, "bold"))
lbl_title.place(x=330, y=20)

# ========== Thông tin khách hàng ==========
frame_info = tk.Frame(root, bg="#FFFACD")
frame_info.place(x=100, y=100)

tk.Label(frame_info, text="Mã Khách Hàng", bg="#FFFACD", font=("Times New Roman", 12)).grid(row=0, column=0, sticky="w", pady=5)
entry_ma = tk.Entry(frame_info, width=30)
entry_ma.grid(row=0, column=1, padx=10, pady=5)

tk.Label(frame_info, text="Giới Tính", bg="#FFFACD", font=("Times New Roman", 12)).grid(row=0, column=2, padx=10, sticky="w")
gender = tk.StringVar(value="Nam")
tk.Radiobutton(frame_info, text="Nam", variable=gender, value="Nam", bg="#FFFACD").grid(row=0, column=3, sticky="w")
tk.Radiobutton(frame_info, text="Nữ", variable=gender, value="Nữ", bg="#FFFACD").grid(row=0, column=4, sticky="w")

tk.Label(frame_info, text="Tên Khách Hàng", bg="#FFFACD", font=("Times New Roman", 12)).grid(row=1, column=0, sticky="w", pady=5)
entry_ten = tk.Entry(frame_info, width=30)
entry_ten.grid(row=1, column=1, padx=10, pady=5)

tk.Label(frame_info, text="Ngày Sinh", bg="#FFFACD", font=("Times New Roman", 12)).grid(row=1, column=2, padx=10, sticky="w")
date_ngaysinh = DateEntry(frame_info, width=12, background='darkblue', foreground='white', borderwidth=2, date_pattern='d/m/yyyy')
date_ngaysinh.grid(row=1, column=3, padx=10, pady=5, columnspan=2)

tk.Label(frame_info, text="Số Điện Thoại", bg="#FFFACD", font=("Times New Roman", 12)).grid(row=2, column=0, sticky="w", pady=5)
entry_sdt = tk.Entry(frame_info, width=30)
entry_sdt.grid(row=2, column=1, padx=10, pady=5)

tk.Label(frame_info, text="Địa Chỉ", bg="#FFFACD", font=("Times New Roman", 12)).grid(row=2, column=2, sticky="w", padx=10)
entry_diachi = tk.Entry(frame_info, width=30)
entry_diachi.grid(row=2, column=3, padx=10, pady=5, columnspan=2)

# ========== Khung Thông tin khách hàng ==========
frame_info = tk.LabelFrame(root, text="Thông tin khách hàng", font=("Times New Roman", 12), bg="#fff8dc", width=750, height=350)
frame_info.place(x=50, y=220)

# Bảng dữ liệu (Treeview)
columns = ("ma_khach", "ten_khach_hang", "so_dien_thoai", "gioi_tinh", "ngay_sinh", "dia_chi")
tree = ttk.Treeview(frame_info, columns=columns, show="headings", height=10)
tree.heading("ma_khach", text="Mã Khách Hàng")
tree.heading("ten_khach_hang", text="Tên Khách Hàng")
tree.heading("so_dien_thoai", text="Số Điện Thoại")
tree.heading("gioi_tinh", text="Giới Tính")
tree.heading("ngay_sinh", text="Ngày Sinh")
tree.heading("dia_chi", text="Địa Chỉ")

tree.column("ma_khach", width=95)
tree.column("ten_khach_hang", width=130)
tree.column("so_dien_thoai", width=130)
tree.column("gioi_tinh", width=60)
tree.column("ngay_sinh", width=130)
tree.column("dia_chi", width=250)

tree.place(x=10, y=10, width=725, height=310)

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

root.mainloop()
