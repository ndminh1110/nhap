import tkinter as tk
from tkinter import ttk

# ===========================
# TẠO CỬA SỔ CHÍNH
# ===========================
root = tk.Tk()
root.title("Form3 - Quản Lý Nhân Viên")
root.geometry("1000x650")
root.configure(bg="#FFFACD")  # màu nền vàng nhạt

# ===========================
# NÚT VỀ TRANG CHỦ
# ===========================
btn_home = tk.Button(root, text="Về Trang Chủ", font=("Times New Roman", 12, "bold"),
                     bg="white", relief="raised", width=15)
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
# Mã nhân viên
tk.Label(root, text="Mã Nhân Viên", bg="#FFFACD", font=("Times New Roman", 12)).place(x=150, y=120)
entry_ma = tk.Entry(root, width=35)
entry_ma.place(x=280, y=120)

# Giới tính
tk.Label(root, text="Giới Tính", bg="#FFFACD", font=("Times New Roman", 12)).place(x=580, y=120)
gender = tk.StringVar()
tk.Radiobutton(root, text="Nam", variable=gender, value="Nam", bg="#FFFACD", font=("Times New Roman", 12)).place(x=660, y=120)
tk.Radiobutton(root, text="Nữ", variable=gender, value="Nữ", bg="#FFFACD", font=("Times New Roman", 12)).place(x=730, y=120)

# Tên nhân viên
tk.Label(root, text="Tên Nhân Viên", bg="#FFFACD", font=("Times New Roman", 12)).place(x=150, y=160)
entry_ten = tk.Entry(root, width=35)
entry_ten.place(x=280, y=160)

# Ngày sinh
tk.Label(root, text="Ngày Sinh", bg="#FFFACD", font=("Times New Roman", 12)).place(x=580, y=160)
entry_ngaysinh = tk.Entry(root, width=35)
entry_ngaysinh.place(x=660, y=160)

# Chức vụ
tk.Label(root, text="Chức Vụ", bg="#FFFACD", font=("Times New Roman", 12)).place(x=150, y=200)
entry_chucvu = tk.Entry(root, width=35)
entry_chucvu.place(x=280, y=200)

# Địa chỉ
tk.Label(root, text="Địa Chỉ", bg="#FFFACD", font=("Times New Roman", 12)).place(x=580, y=200)
entry_diachi = tk.Entry(root, width=35)
entry_diachi.place(x=660, y=200)

# Số điện thoại
tk.Label(root, text="Số Điện Thoại", bg="#FFFACD", font=("Times New Roman", 12)).place(x=150, y=240)
entry_sdt = tk.Entry(root, width=35)
entry_sdt.place(x=280, y=240)

# Lương
tk.Label(root, text="Lương", bg="#FFFACD", font=("Times New Roman", 12)).place(x=580, y=240)
entry_luong = tk.Entry(root, width=35)
entry_luong.place(x=660, y=240)

# ===========================
# KHUNG THÔNG TIN NHÂN VIÊN
# ===========================
frame_info = tk.LabelFrame(root, text="Thông tin nhân viên",
                           font=("Times New Roman", 12, "bold"), bg="#FFFACD")
frame_info.place(x=90, y=320, width=820, height=250)

text_info = tk.Text(frame_info, width=100, height=10)
text_info.pack(padx=10, pady=10)

# ===========================
# NÚT CHỨC NĂNG (bên phải)
# ===========================
btn_color = "skyblue"
btn_font = ("Times New Roman", 12, "bold")

btn_them = tk.Button(root, text="Thêm", font=btn_font, bg=btn_color, width=10)
btn_them.place(x=860, y=120)

btn_xoa = tk.Button(root, text="Xóa", font=btn_font, bg=btn_color, width=10)
btn_xoa.place(x=860, y=170)

btn_sua = tk.Button(root, text="Sửa", font=btn_font, bg=btn_color, width=10)
btn_sua.place(x=860, y=220)

btn_huy = tk.Button(root, text="Hủy", font=btn_font, bg=btn_color, width=10)
btn_huy.place(x=860, y=270)

btn_luu = tk.Button(root, text="Lưu", font=btn_font, bg=btn_color, width=10)
btn_luu.place(x=860, y=320)

btn_thoat = tk.Button(root, text="Thoát", font=btn_font, bg=btn_color, width=10)
btn_thoat.place(x=860, y=370)

# ===========================
root.mainloop()
