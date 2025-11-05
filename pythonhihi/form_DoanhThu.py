import tkinter as tk
from tkinter import ttk

# ===========================
# TẠO CỬA SỔ CHÍNH
# ===========================
root = tk.Tk()
root.title("Form6 - Doanh Thu")
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
lbl_title = tk.Label(root, text="Doanh Thu", font=("Times New Roman", 24, "bold"),
                     bg="#FFFACD")
lbl_title.place(x=440, y=35)

# ===========================
# PHẦN CHỌN QUÝ
# ===========================
tk.Label(root, text="Quý", font=("Times New Roman", 12), bg="#FFFACD").place(x=180, y=120)
quarter = tk.IntVar(value=1)

tk.Radiobutton(root, text="1", variable=quarter, value=1, bg="#FFFACD", font=("Times New Roman", 12)).place(x=220, y=120)
tk.Radiobutton(root, text="2", variable=quarter, value=2, bg="#FFFACD", font=("Times New Roman", 12)).place(x=270, y=120)
tk.Radiobutton(root, text="3", variable=quarter, value=3, bg="#FFFACD", font=("Times New Roman", 12)).place(x=320, y=120)
tk.Radiobutton(root, text="4", variable=quarter, value=4, bg="#FFFACD", font=("Times New Roman", 12)).place(x=370, y=120)

tk.Label(root, text="hoặc", font=("Times New Roman", 12), bg="#FFFACD").place(x=430, y=120)

# ===========================
# PHẦN CHỌN THÁNG
# ===========================
tk.Label(root, text="Tháng", font=("Times New Roman", 12), bg="#FFFACD").place(x=160, y=170)
month = tk.IntVar(value=1)

# dòng 1
tk.Radiobutton(root, text="1", variable=month, value=1, bg="#FFFACD", font=("Times New Roman", 12)).place(x=220, y=170)
tk.Radiobutton(root, text="2", variable=month, value=2, bg="#FFFACD", font=("Times New Roman", 12)).place(x=270, y=170)
tk.Radiobutton(root, text="3", variable=month, value=3, bg="#FFFACD", font=("Times New Roman", 12)).place(x=320, y=170)
tk.Radiobutton(root, text="4", variable=month, value=4, bg="#FFFACD", font=("Times New Roman", 12)).place(x=370, y=170)

# dòng 2
tk.Radiobutton(root, text="5", variable=month, value=5, bg="#FFFACD", font=("Times New Roman", 12)).place(x=220, y=200)
tk.Radiobutton(root, text="6", variable=month, value=6, bg="#FFFACD", font=("Times New Roman", 12)).place(x=270, y=200)
tk.Radiobutton(root, text="7", variable=month, value=7, bg="#FFFACD", font=("Times New Roman", 12)).place(x=320, y=200)
tk.Radiobutton(root, text="8", variable=month, value=8, bg="#FFFACD", font=("Times New Roman", 12)).place(x=370, y=200)

# dòng 3
tk.Radiobutton(root, text="9", variable=month, value=9, bg="#FFFACD", font=("Times New Roman", 12)).place(x=220, y=230)
tk.Radiobutton(root, text="10", variable=month, value=10, bg="#FFFACD", font=("Times New Roman", 12)).place(x=270, y=230)
tk.Radiobutton(root, text="11", variable=month, value=11, bg="#FFFACD", font=("Times New Roman", 12)).place(x=320, y=230)
tk.Radiobutton(root, text="12", variable=month, value=12, bg="#FFFACD", font=("Times New Roman", 12)).place(x=370, y=230)

tk.Label(root, text="hoặc", font=("Times New Roman", 12), bg="#FFFACD").place(x=430, y=210)

# ===========================
# NĂM
# ===========================
tk.Label(root, text="Năm", font=("Times New Roman", 12), bg="#FFFACD").place(x=160, y=280)
entry_year = tk.Entry(root, width=30)
entry_year.place(x=220, y=280)

# ===========================
# NÚT XEM
# ===========================
btn_xem = tk.Button(root, text="Xem", font=("Times New Roman", 14, "bold"),
                    bg="skyblue", width=10)
btn_xem.place(x=650, y=180)

# ===========================
# KHUNG THÔNG TIN
# ===========================
frame_info = tk.LabelFrame(root, text="Thông tin nhân viên", font=("Times New Roman", 12, "bold"),
                           bg="#FFFACD")
frame_info.place(x=90, y=350, width=820, height=230)

text_info = tk.Text(frame_info, width=100, height=10)
text_info.pack(padx=10, pady=10)

# ===========================
root.mainloop()
