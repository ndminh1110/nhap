import tkinter as tk
from tkinter import messagebox
import pyodbc
import subprocess
import sys,os

# ======= HÀM XỬ LÝ ========
def login():
    username = entry_user.get()
    password = entry_pass.get()

        # Kết nối tới SQL Server
    conn = pyodbc.connect(
            'DRIVER={SQL Server};'
            'SERVER=ADMIN-PC;'          # hoặc tên server thật, ví dụ: LAPTOP\\SQLEXPRESS
            'DATABASE=QuanLyTuyenDuLich;'
            'Trusted_Connection=yes;'    # Nếu bạn dùng Windows Authentication
        )
    cursor = conn.cursor()
    cursor.execute("SELECT VaiTro FROM TaiKhoan WHERE TenDangNhap=? AND MatKhau=?", (username, password))
    result = cursor.fetchone()
        
    if result:
            role = result[0]
            #root.destroy()  # Đóng form đăng nhập
            # Mở form tương ứng
            if role == "QuanLy":
                subprocess.Popen(["python", "form_trangChu_QuanLy.py"])
            elif role == "NhanVien":
                subprocess.Popen(["python", "form_trangChu_NhanVien.py"])  
    else:
            messagebox.showerror("Lỗi", "Sai tên đăng nhập hoặc mật khẩu!")
    conn.close()

def thoat():
    root.destroy()

# ======= TẠO CỬA SỔ CHÍNH ========
root = tk.Tk()
root.title("Login Form")
root.geometry("1000x650")  # kích thước form 1000x650
root.configure(bg="#FFFACD")  # màu nền vàng nhạt

# ======= FRAME LOGIN (khung giữa) ========
frame_login = tk.Frame(root, bg="#FFFACD", padx=40, pady=40, relief="groove", bd=2)
frame_login.place(relx=0.5, rely=0.5, anchor="center")

# ======= TIÊU ĐỀ ========
label_title = tk.Label(frame_login, text="Login", font=("Arial", 26, "bold"), bg="#FFFACD")
label_title.grid(row=0, column=0, columnspan=2, pady=20)

# ======= USERNAME ========
label_user = tk.Label(frame_login, text="User:", font=("Arial", 16), bg="#FFFACD")
label_user.grid(row=1, column=0, sticky="e", pady=10, padx=10)
entry_user = tk.Entry(frame_login, width=30, font=("Arial", 14))
entry_user.grid(row=1, column=1, pady=10, padx=10)

# ======= PASSWORD ========
label_pass = tk.Label(frame_login, text="Password:", font=("Arial", 16), bg="#FFFACD")
label_pass.grid(row=2, column=0, sticky="e", pady=10, padx=10)
entry_pass = tk.Entry(frame_login, width=30, show="*", font=("Arial", 14))
entry_pass.grid(row=2, column=1, pady=10, padx=10)

# ======= NÚT OK & CANCEL ========
button_ok = tk.Button(frame_login, text="OK", bg="#ADD8E6", width=12, height=1, font=("Arial", 14), command=login)
button_ok.grid(row=3, column=0, pady=25)

button_cancel = tk.Button(frame_login, text="Cancel", bg="#ADD8E6", width=12, height=1, font=("Arial", 14), command=thoat)
button_cancel.grid(row=3, column=1, pady=25)

root.mainloop()