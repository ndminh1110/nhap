import tkinter as tk
from tkinter import ttk
from tkcalendar import DateEntry

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

# TẠO CỬA SỔ CHÍNH
# ===========================
root = tk.Tk()
root.title("Form3 - Quản Lý Nhân Viên")
root.geometry("1000x650")
root.configure(bg="#FFFACD")  # màu nền vàng nhạt

# ========== Nút Về Trang Chủ ==========
btn_home = tk.Button(root, text="Về Trang Chủ", font=("Times New Roman", 10, "bold"), bg="white", relief="groove", command=ve_trang_chu)
btn_home.place(x=50, y=40)

# ===========================
# TIÊU ĐỀ
# ===========================
lbl_title = tk.Label(root, text="Quản Lý Nhân Viên", font=("Times New Roman", 24, "bold"),
                     bg="#FFFACD")
lbl_title.place(x=380, y=35)

# ===========================
# NHÃN & Ô NHẬP LIỆU
# ===========================

# ========== Thông tin khách hàng ==========
frame_info = tk.Frame(root, bg="#FFFACD")
frame_info.place(x=100, y=100)

tk.Label(frame_info, text="Mã Nhân Viên", bg="#FFFACD", font=("Times New Roman", 12)).grid(row=0, column=0, sticky="w", pady=5)
entry_ma = tk.Entry(frame_info, width=30)
entry_ma.grid(row=0, column=1, padx=10, pady=5)

tk.Label(frame_info, text="Giới Tính", bg="#FFFACD", font=("Times New Roman", 12)).grid(row=0, column=2, padx=10, sticky="w")
gender = tk.StringVar(value="Nam")
tk.Radiobutton(frame_info, text="Nam", variable=gender, value="Nam", bg="#FFFACD").grid(row=0, column=3, sticky="w")
tk.Radiobutton(frame_info, text="Nữ", variable=gender, value="Nữ", bg="#FFFACD").grid(row=0, column=4, sticky="w")

tk.Label(frame_info, text="Tên Nhân Viên", bg="#FFFACD", font=("Times New Roman", 12)).grid(row=1, column=0, sticky="w", pady=5)
entry_ten = tk.Entry(frame_info, width=30)
entry_ten.grid(row=1, column=1, padx=10, pady=5)

tk.Label(frame_info, text="Ngày Sinh", bg="#FFFACD", font=("Times New Roman", 12)).grid(row=1, column=2, padx=10, sticky="w")
date_ngaysinh = DateEntry(frame_info, width=12, background='darkblue', foreground='white', borderwidth=2, date_pattern='d/m/yyyy')
date_ngaysinh.grid(row=1, column=3, padx=10, pady=5, columnspan=2)

tk.Label(frame_info, text="Chức vụ", bg="#FFFACD", font=("Times New Roman", 12)).grid(row=2, column=0, sticky="w", pady=5)
entry_chucvu = tk.Entry(frame_info, width=30)
entry_chucvu.grid(row=2, column=1, padx=10, pady=5)

tk.Label(frame_info, text="Địa Chỉ", bg="#FFFACD", font=("Times New Roman", 12)).grid(row=2, column=2, sticky="w", padx=10)
entry_diachi = tk.Entry(frame_info, width=30)
entry_diachi.grid(row=2, column=3, padx=10, pady=5, columnspan=2)

tk.Label(frame_info, text="Số Điện Thoại", bg="#FFFACD", font=("Times New Roman", 12)).grid(row=3, column=0, sticky="w", pady=5)
entry_sdt = tk.Entry(frame_info, width=30)
entry_sdt.grid(row=3, column=1, padx=10, pady=5)

tk.Label(frame_info, text="Lương", bg="#FFFACD", font=("Times New Roman", 12)).grid(row=3, column=2, sticky="w", padx=10)
entry_luong = tk.Entry(frame_info, width=30)
entry_luong.grid(row=3, column=3, padx=10, pady=5, columnspan=2)

# ===========================
# KHUNG THÔNG TIN NHÂN VIÊN
# ===========================
#frame_info = tk.LabelFrame(root, text="Thông tin nhân viên",font=("Times New Roman", 12, "bold"), bg="#FFFACD")
#text_info.pack(padx=10, pady=10)

# ========== Khung Thông tin khách hàng ==========
frame_info = tk.LabelFrame(root, text="Thông tin nhân viên", font=("Times New Roman", 12), bg="#fff8dc", width=750, height=350)
frame_info.place(x=50, y=250)

# Bảng dữ liệu (Treeview)
columns = ("maNV", "hoTen", "chucVu", "phai", "ngsinh","sdt", "dchi","luong")
tree = ttk.Treeview(frame_info, columns=columns, show="headings", height=10)       
tree.heading("maNV", text="Mã NV")
tree.heading("hoTen", text="Họ Tên")
tree.heading("chucVu", text="Chức Vụ")
tree.heading("phai", text="Giới")
tree.heading("ngsinh", text="Ngày Sinh")
tree.heading("sdt", text="Số Điện Thoại")
tree.heading("dchi", text="Địa Chỉ")
tree.heading("luong", text="Lương")

tree.column("maNV", width=50)
tree.column("hoTen", width=130)
tree.column("chucVu", width=80)
tree.column("phai", width=30)
tree.column("ngsinh", width=70)
tree.column("sdt", width=80)
tree.column("dchi", width=200)
tree.column("luong", width=100)

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

# ===========================
root.mainloop()
