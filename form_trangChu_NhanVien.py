import tkinter as tk
import subprocess

def open_form_KhachHang():
    #root.destroy()  # Đóng form 1
    subprocess.Popen(["python", "form_KhachHang.py"])  # Mở form 2

def thoat():
    root.destroy()

root = tk.Tk()
root.title("Trang Chủ - Nhân Viên")
root.geometry("1000x650")
root.configure(bg="#FFFACD")

frame = tk.Frame(root, bg="#FFFACD", padx=40, pady=40, relief="groove", bd=2)
frame.place(relx=0.5, rely=0.5, anchor="center")

tk.Label(frame, text="Trang Chủ", font=("Arial", 26, "bold"), bg="#FFFACD").grid(row=0, column=0, columnspan=2, pady=20)

# Hàng 1
tk.Button(frame, text="Quản Lý Khách Hàng", bg="#ADD8E6", font=("Arial", 14), width=20, height=2, command=open_form_KhachHang).grid(row=1, column=0, padx=30, pady=20)
tk.Button(frame, text="Quản Lý Chuyến Đi", bg="#ADD8E6", font=("Arial", 14), width=20, height=2).grid(row=1, column=1, padx=30, pady=20)

# Hàng 2
KH=tk.Button(frame, text="Quản Lý Đặt Vé", bg="#ADD8E6", font=("Arial", 14), width=20, height=2).grid(row=2, column=0, padx=30, pady=20)
tk.Button(frame, text="Quản Lý Tuyến Du Lịch", bg="#ADD8E6", font=("Arial", 14), width=20, height=2).grid(row=2, column=1, padx=30, pady=20)

# Nút thoát
tk.Button(root, text="Thoát", font=("Arial", 12), command=thoat).place(x=920, y=600)

root.mainloop()