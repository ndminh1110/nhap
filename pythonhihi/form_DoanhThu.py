import tkinter as tk
from tkinter import ttk

def ve_trang_chu():
    root.destroy()
# ===========================
# TẠO CỬA SỔ CHÍNH
# ===========================
root = tk.Tk()
root.title("Form6 - Doanh Thu")
root.geometry("1000x650")
root.configure(bg="#FFFACD")  # màu nền vàng nhạt


# NÚT VỀ TRANG CHỦ
btn_home = tk.Button(root, text="Về Trang Chủ", font=("Times New Roman", 10, "bold"), bg="white", relief="groove", command=ve_trang_chu)
btn_home.place(x=50, y=40)

# ===========================
# TIÊU ĐỀ
# ===========================
lbl_title = tk.Label(root, text="Doanh Thu", font=("Times New Roman", 24, "bold"),
                     bg="#FFFACD")
lbl_title.place(x=440, y=35)

# ===========================
# PHẦN CHỌN QUÝ
# ===========================
tk.Label(root, text="Quý", font=("Times New Roman", 12), bg="#FFFACD").place(x=160, y=120)
quarter = tk.IntVar(value=1)

tk.Radiobutton(root, text="1", variable=quarter, value=1, bg="#FFFACD", font=("Times New Roman", 12)).place(x=250, y=120,)
tk.Radiobutton(root, text="2", variable=quarter, value=2, bg="#FFFACD", font=("Times New Roman", 12)).place(x=400, y=120)
tk.Radiobutton(root, text="3", variable=quarter, value=3, bg="#FFFACD", font=("Times New Roman", 12)).place(x=550, y=120)
tk.Radiobutton(root, text="4", variable=quarter, value=4, bg="#FFFACD", font=("Times New Roman", 12)).place(x=700, y=120)

tk.Label(root, text="hoặc", font=("Times New Roman", 12), bg="#FFFACD").place(x=485, y=140)

# ===========================
# PHẦN CHỌN THÁNG
# ===========================
tk.Label(root, text="Tháng", font=("Times New Roman", 12), bg="#FFFACD").place(x=160, y=170)
month = tk.IntVar(value=1)

# dòng 1
tk.Radiobutton(root, text="1", variable=month, value=1, bg="#FFFACD", font=("Times New Roman", 12)).place(x=250, y=170)
tk.Radiobutton(root, text="2", variable=month, value=2, bg="#FFFACD", font=("Times New Roman", 12)).place(x=400, y=170)
tk.Radiobutton(root, text="3", variable=month, value=3, bg="#FFFACD", font=("Times New Roman", 12)).place(x=550, y=170)
tk.Radiobutton(root, text="4", variable=month, value=4, bg="#FFFACD", font=("Times New Roman", 12)).place(x=700, y=170)

# dòng 2
tk.Radiobutton(root, text="5", variable=month, value=5, bg="#FFFACD", font=("Times New Roman", 12)).place(x=250, y=200)
tk.Radiobutton(root, text="6", variable=month, value=6, bg="#FFFACD", font=("Times New Roman", 12)).place(x=400, y=200)
tk.Radiobutton(root, text="7", variable=month, value=7, bg="#FFFACD", font=("Times New Roman", 12)).place(x=550, y=200)
tk.Radiobutton(root, text="8", variable=month, value=8, bg="#FFFACD", font=("Times New Roman", 12)).place(x=700, y=200)

# dòng 3
tk.Radiobutton(root, text="9", variable=month, value=9, bg="#FFFACD", font=("Times New Roman", 12)).place(x=250, y=230)
tk.Radiobutton(root, text="10", variable=month, value=10, bg="#FFFACD", font=("Times New Roman", 12)).place(x=400, y=230)
tk.Radiobutton(root, text="11", variable=month, value=11, bg="#FFFACD", font=("Times New Roman", 12)).place(x=550, y=230)
tk.Radiobutton(root, text="12", variable=month, value=12, bg="#FFFACD", font=("Times New Roman", 12)).place(x=700, y=230)

tk.Label(root, text="hoặc", font=("Times New Roman", 12), bg="#FFFACD").place(x=485, y=250)

# ===========================
# NĂM
# ===========================
tk.Label(root, text="Năm", font=("Times New Roman", 12), bg="#FFFACD").place(x=160, y=280)
entry_year = tk.Entry(root, width=30)
entry_year.place(x=250, y=280)

# ===========================
# NÚT XEM
# ===========================
btn_xem = tk.Button(root, text="Xem", font=("Times New Roman", 14, "bold"),
                    bg="skyblue", width=10)
btn_xem.place(x=780, y=170)

# === KHUNG THÔNG TIN DOANH THU ===
frame_info = tk.LabelFrame(root, text="Thông Tin Doanh Thu", font=("Arial", 12, "bold"), bg="#fff8dc", width=800, height=280)
frame_info.place(x=100, y=320)

# Bảng dữ liệu (Treeview)
columns = ("maCD", "giaVe", "soLuongKhach", "tongTien")
tree = ttk.Treeview(frame_info, columns=columns, show="headings", height=10)
tree.heading("maCD", text="Mã Chuyến Đi")
tree.heading("giaVe", text="Giá Vé")
tree.heading("soLuongKhach", text="Số Lượng Khách")
tree.heading("tongTien", text="Tổng Tiền")

tree.column("maCD", width=150)
tree.column("giaVe", width=150)
tree.column("soLuongKhach", width=150)
tree.column("tongTien", width=200)

tree.place(x=30, y=10, width=740, height=230)

# ===========================
root.mainloop()
