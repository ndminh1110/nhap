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
root.title("Quản Lý Chuyến Đi")
root.geometry("1000x650")
root.config(bg="#fff8dc")  # Màu nền vàng nhạt

# === TIÊU ĐỀ ===
title_label = tk.Label(root, text="Quản Lý Chuyến Đi", font=("Arial", 20, "bold"), bg="#fff8dc")
title_label.place(x=400, y=30)

# ========== Nút Về Trang Chủ ==========
btn_home = tk.Button(root, text="Về Trang Chủ", font=("Times New Roman", 10, "bold"), bg="white", relief="groove", command=quit)
btn_home.place(x=50, y=30)

# === NHÃN VÀ Ô NHẬP LIỆU ===
tk.Label(root, text="Mã Tuyến", font=("Arial", 12), bg="#fff8dc").place(x=140, y=140)
txt_ma_tuyen = tk.Entry(root, width=30)
txt_ma_tuyen.place(x=250, y=140)

tk.Label(root, text="Mã Chuyến Đi", font=("Arial", 12), bg="#fff8dc").place(x=580, y=100)
txt_ma_cd = tk.Entry(root, width=15)
txt_ma_cd.place(x=730, y=100)

tk.Label(root, text="Mã Nhân Viên", font=("Arial", 12), bg="#fff8dc").place(x=140, y=190)
txt_ma_nv = tk.Entry(root, width=30)
txt_ma_nv.place(x=250, y=190)

tk.Label(root, text="Số Lượng Hành Khách", font=("Arial", 12), bg="#fff8dc").place(x=500, y=140)
txt_sl = tk.Entry(root, width=30)
txt_sl.place(x=700, y=140)

tk.Label(root, text="Thời Gian Khởi Hành", font=("Arial", 12), bg="#fff8dc").place(x=500, y=190)
txt_tg = tk.Entry(root, width=30)
txt_tg.place(x=700, y=190)

# === CÁC NÚT CHỨC NĂNG ===
btn_them = tk.Button(root, text="Thêm", bg="#87cefa", font=("Arial", 12, "bold"), width=10)
btn_them.place(x=90, y=250)

btn_xoa = tk.Button(root, text="Xóa", bg="#87cefa", font=("Arial", 12, "bold"), width=10)
btn_xoa.place(x=230, y=250)

btn_sua = tk.Button(root, text="Sửa", bg="#87cefa", font=("Arial", 12, "bold"), width=10)
btn_sua.place(x=370, y=250)

btn_huy = tk.Button(root, text="Hủy", bg="#87cefa", font=("Arial", 12, "bold"), width=10)
btn_huy.place(x=510, y=250)

btn_luu = tk.Button(root, text="Lưu", bg="#87cefa", font=("Arial", 12, "bold"), width=10)
btn_luu.place(x=650, y=250)

btn_thoat = tk.Button(root, text="Thoát", bg="#87cefa", font=("Arial", 12, "bold"), width=10)
btn_thoat.place(x=790, y=250)

# === KHUNG THÔNG TIN CHUYẾN ĐI ===
frame_info = tk.LabelFrame(root, text="Thông Tin Chuyến Đi", font=("Arial", 12, "bold"), bg="#fff8dc", width=900, height=250)
frame_info.place(x=50, y=300)

# Bảng hiển thị thông tin (Treeview)
columns = ("maTuyen", "maCD", "maNV", "tgKh", "ngKh")
tree = ttk.Treeview(frame_info, columns=columns, show="headings", height=10)
tree.heading("maTuyen", text="Mã Tuyến")
tree.heading("maCD", text="Mã Chuyến Đi")
tree.heading("maNV", text="Mã Nhân Viên")
tree.heading("tgKh", text="Thời Gian Khởi Hành")
tree.heading("ngKh", text="Ngay Khởi Hành")

tree.column("maTuyen", width=135)
tree.column("maCD", width=135)
tree.column("maNV", width=135)
tree.column("tgKh", width=200)
tree.column("ngKh", width=200)

tree.place(x=10, y=10, width=870, height=210)

# === CHẠY FORM ===
root.mainloop()
