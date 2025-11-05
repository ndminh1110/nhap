import tkinter as tk
from tkinter import ttk

# === TẠO FORM CHÍNH ===
root = tk.Tk()
root.title("Quản Lý Chuyến Đi")
root.geometry("1000x650")
root.config(bg="#fff8dc")  # Màu nền vàng nhạt

# === TIÊU ĐỀ ===
title_label = tk.Label(root, text="Quản Lý Chuyến Đi", font=("Arial", 20, "bold"), bg="#fff8dc")
title_label.place(x=400, y=30)

# === NÚT VỀ TRANG CHỦ ===
btn_home = tk.Button(root, text="Về Trang Chủ", bg="#b0e0e6", font=("Arial", 12, "bold"), width=12, height=2)
btn_home.place(x=50, y=40)

# === NHÃN VÀ Ô NHẬP LIỆU ===
tk.Label(root, text="Mã Tuyến", font=("Arial", 12), bg="#fff8dc").place(x=150, y=120)
txt_ma_tuyen = tk.Entry(root, width=25)
txt_ma_tuyen.place(x=250, y=120)

tk.Label(root, text="Mã Chuyến Đi", font=("Arial", 12), bg="#fff8dc").place(x=550, y=120)
txt_ma_cd = tk.Entry(root, width=25)
txt_ma_cd.place(x=700, y=120)

tk.Label(root, text="Mã Nhân Viên", font=("Arial", 12), bg="#fff8dc").place(x=150, y=170)
txt_ma_nv = tk.Entry(root, width=25)
txt_ma_nv.place(x=250, y=170)

tk.Label(root, text="Số Lượng Hành Khách", font=("Arial", 12), bg="#fff8dc").place(x=550, y=170)
txt_sl = tk.Entry(root, width=25)
txt_sl.place(x=750, y=170)

tk.Label(root, text="Thời Gian Khởi Hành", font=("Arial", 12), bg="#fff8dc").place(x=550, y=220)
txt_tg = tk.Entry(root, width=25)
txt_tg.place(x=750, y=220)

# === CÁC NÚT CHỨC NĂNG ===
btn_them = tk.Button(root, text="Thêm", bg="#87cefa", font=("Arial", 12, "bold"), width=10)
btn_them.place(x=200, y=270)

btn_xoa = tk.Button(root, text="Xóa", bg="#87cefa", font=("Arial", 12, "bold"), width=10)
btn_xoa.place(x=320, y=270)

btn_sua = tk.Button(root, text="Sửa", bg="#87cefa", font=("Arial", 12, "bold"), width=10)
btn_sua.place(x=440, y=270)

btn_huy = tk.Button(root, text="Hủy", bg="#87cefa", font=("Arial", 12, "bold"), width=10)
btn_huy.place(x=560, y=270)

btn_luu = tk.Button(root, text="Lưu", bg="#87cefa", font=("Arial", 12, "bold"), width=10)
btn_luu.place(x=680, y=270)

btn_thoat = tk.Button(root, text="Thoát", bg="#87cefa", font=("Arial", 12, "bold"), width=10)
btn_thoat.place(x=800, y=270)

# === KHUNG THÔNG TIN CHUYẾN ĐI ===
frame_info = tk.LabelFrame(root, text="Thông Tin Chuyến Đi", font=("Arial", 12, "bold"), bg="#fff8dc", width=900, height=250)
frame_info.place(x=50, y=350)

# Bảng hiển thị thông tin (Treeview)
columns = ("ma_tuyen", "ma_cd", "ma_nv", "so_luong", "thoi_gian")
tree = ttk.Treeview(frame_info, columns=columns, show="headings", height=10)
tree.heading("ma_tuyen", text="Mã Tuyến")
tree.heading("ma_cd", text="Mã Chuyến Đi")
tree.heading("ma_nv", text="Mã Nhân Viên")
tree.heading("so_luong", text="Số Lượng HK")
tree.heading("thoi_gian", text="Thời Gian KH")
tree.place(x=10, y=10, width=870, height=210)

# === CHẠY FORM ===
root.mainloop()
