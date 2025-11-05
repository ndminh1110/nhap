import tkinter as tk
from tkinter import ttk

# === FORM CHÍNH ===
root = tk.Tk()
root.title("Quản Lý Tuyến Du Lịch")
root.geometry("1000x650")
root.config(bg="#fff8dc")  # Màu nền vàng nhạt

# === NÚT VỀ TRANG CHỦ ===
btn_home = tk.Button(root, text="Về Trang Chủ", bg="#f0f0f0", font=("Arial", 12, "bold"), width=12, height=2)
btn_home.place(x=50, y=40)

# === TIÊU ĐỀ CHÍNH ===
title_label = tk.Label(root, text="Quản Lý Tuyến Du Lịch", font=("Arial", 20, "bold"), bg="#fff8dc")
title_label.place(x=370, y=45)

# === NHÃN & Ô NHẬP LIỆU ===
tk.Label(root, text="Địa Điểm Khởi Hành", font=("Arial", 12), bg="#fff8dc").place(x=200, y=150)
entry_khoihanh = tk.Entry(root, width=50)
entry_khoihanh.place(x=380, y=150)

tk.Label(root, text="Địa Điểm Đến", font=("Arial", 12), bg="#fff8dc").place(x=200, y=190)
entry_den = tk.Entry(root, width=50)
entry_den.place(x=380, y=190)

tk.Label(root, text="Mã Tuyến", font=("Arial", 12), bg="#fff8dc").place(x=200, y=230)
entry_matuyen = tk.Entry(root, width=50)
entry_matuyen.place(x=380, y=230)

# === KHUNG THÔNG TIN NHÂN VIÊN ===
frame_info = tk.LabelFrame(root, text="Thông tin nhân viên", font=("Arial", 12, "bold"), bg="#fff8dc", width=750, height=280)
frame_info.place(x=50, y=270)

# Bảng dữ liệu (Treeview)
columns = ("ma_tuyen", "khoi_hanh", "den")
tree = ttk.Treeview(frame_info, columns=columns, show="headings", height=10)
tree.heading("ma_tuyen", text="Mã Tuyến")
tree.heading("khoi_hanh", text="Địa Điểm Khởi Hành")
tree.heading("den", text="Địa Điểm Đến")
tree.place(x=10, y=10, width=725, height=240)

# === CÁC NÚT CHỨC NĂNG (bên phải) ===
btn_them = tk.Button(root, text="Thêm", bg="#87cefa", font=("Arial", 12, "bold"), width=10)
btn_them.place(x=850, y=120)

btn_xoa = tk.Button(root, text="Xóa", bg="#87cefa", font=("Arial", 12, "bold"), width=10)
btn_xoa.place(x=850, y=200)

btn_sua = tk.Button(root, text="Sửa", bg="#87cefa", font=("Arial", 12, "bold"), width=10)
btn_sua.place(x=850, y=280)

btn_huy = tk.Button(root, text="Hủy", bg="#87cefa", font=("Arial", 12, "bold"), width=10)
btn_huy.place(x=850, y=360)

btn_luu = tk.Button(root, text="Lưu", bg="#87cefa", font=("Arial", 12, "bold"), width=10)
btn_luu.place(x=850, y=420)

btn_thoat = tk.Button(root, text="Thoát", bg="#87cefa", font=("Arial", 12, "bold"), width=10)
btn_thoat.place(x=850, y=500)

# === CHẠY FORM ===
root.mainloop()
