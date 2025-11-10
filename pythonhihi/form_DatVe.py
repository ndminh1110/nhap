import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
import pyodbc
from datetime import date

# ------------------ KẾT NỐI SQL SERVER ------------------
conn = pyodbc.connect(
    'DRIVER={SQL Server};'
    'SERVER=localhost\\SQLEXPRESS01;'
    'DATABASE=QuanLyTuyenDuLich;'
    'Trusted_Connection=yes;'
)
cursor = conn.cursor()

def load_data():
    """Load dữ liệu từ CSDL lên Treeview"""
    for i in tree.get_children():
        tree.delete(i)
    cursor.execute("SELECT maVe, maKH, maCD, ngDat, trangThai, giaVe, soluong, thanhTien FROM DATVE")
    rows = cursor.fetchall()
    for row in rows:
        tree.insert("", "end", values=(row[0].strip(), row[1].strip(), row[2].strip(), row[3].strip(), row[4].strip(), row[5], row[6],row[7]) )

def auto_maVe():
    cursor.execute("SELECT maVe FROM DATVE")
    ma_list = [row[0] for row in cursor.fetchall()]
    if not ma_list:
        return "VE00000001"
    so_list = sorted([int(ma[2:]) for ma in ma_list if ma[2:].isdigit()])
    next_num = 1
    for num in so_list:
        if num == next_num:
            next_num += 1
        elif num > next_num:
            break
    return f"VE{next_num:08d}"

def lay_danh_sach_ma_khach_hang():
    cursor.execute("SELECT maKh FROM KHACHHANG")
    data = cursor.fetchall()
    ds_ma = [row[0] for row in data]  # lấy cột maKh
    return ds_ma

def lay_danh_sach_ma_chuyen_di():
    cursor.execute("SELECT maCD FROM CHUYENDI")
    data = cursor.fetchall()
    ds_cd = [row[0] for row in data]  # lấy cột maKh
    return ds_cd

def lam_moi_form():
    entry_maVe.config(state='normal')
    entry_maVe.delete(0, tk.END)
    entry_maVe.insert(0, auto_maVe())
    entry_maVe.config(state='readonly')

    entry_maKH.set("")
    entry_maCD.set("")
    date_ngDat.set_date(date.today())
    entry_trangThai.delete(0, tk.END)
    entry_giaVe.delete(0, tk.END)
    spin_soLuong.delete(0, tk.END)

def them():
    maVe = auto_maVe()
    maKH = entry_maKH.get().strip()
    maCD = entry_maCD.get().strip()
    ngDat = date_ngDat.get_date().strftime('%Y-%m-%d')
    trangThai = entry_trangThai.get().strip()
    giaVe = float(entry_giaVe.get().strip())
    soluong = int(spin_soLuong.get().strip())
    thanhTien = giaVe * soluong

    if not trangThai or not giaVe or not soluong:
        messagebox.showwarning("Thiếu dữ liệu", "Vui lòng nhập đầy đủ thông tin!")
        return

    tree.insert("", "end", values=(maVe, maKH, maCD, ngDat, trangThai, giaVe, soluong, thanhTien))
    lam_moi_form()

def xoa():
    selected = tree.selection()
    if not selected:
        messagebox.showwarning("Chưa chọn", "Vui lòng chọn vé để xóa!")
        return
    confirm = messagebox.askyesno("Xác nhận", "Bạn có chắc muốn xóa?")
    if confirm:
        tree.delete(selected[0])
        lam_moi_form()

def sua():
    selected = tree.selection()
    if not selected:
        messagebox.showwarning("Chưa chọn", "Vui lòng chọn vé để sửa!")
        return

    maVe = tree.item(selected[0])['values'][0].strip()
    maKH = entry_maKH.get().strip()
    maCD = entry_maCD.get().strip()
    ngDat = date_ngDat.get().strip().strftime('%d/%m/%Y')
    trangThai = entry_trangThai.get().strip()
    giaVe = float(entry_giaVe.get().strip())
    soluong = int(spin_soLuong.get().strip())

    if not trangThai or not giaVe or not soluong:
        messagebox.showwarning("Thiếu dữ liệu", "Vui lòng nhập đầy đủ thông tin!")
        return
    tree.item(selected[0], values=(maVe, maKH, maCD, ngDat, trangThai, giaVe, soluong))
    messagebox.showinfo("Thành công", "Đã cập nhật thông tin khách hàng!")
    lam_moi_form()

def huy():
    lam_moi_form()
def hien_thi_chi_tiet():
    selected = tree.selection()
    if selected:
        maVe, maKh, maCD, ngDat, trangThai, giaVe,soluong, thanhTien = tree.item(selected[0], "values")
        entry_maVe.config(state='normal')
        entry_maVe.delete(0, tk.END)
        entry_maVe.insert(0, maVe)
        entry_maVe.config(state='readonly')

        entry_maKH.delete(0, tk.END)
        entry_maKH.insert(0, maKh)

        entry_maCD.delete(0, tk.END)
        entry_maCD.insert(0, maCD)

        date_ngDat.delete(0, tk.END)
        date_ngDat.set_date(ngDat)

        entry_trangThai.delete(0, tk.END)
        entry_trangThai.insert(0, trangThai)

        entry_giaVe.delete(0, tk.END)
        entry_giaVe.insert(0, giaVe)

        spin_soLuong.delete(0, tk.END)
        spin_soLuong.insert(0, soluong)

        

def luu():
    for item in tree.get_children():
        maVe, maKH, maCD, ngDat, trangThai, giaVe, soluong, thanhTien = tree.item(item, "values")
        cursor.execute("SELECT 1 FROM DATVE WHERE maVe=?", (maVe,))
        if not cursor.fetchone():
            cursor.execute(
                "INSERT INTO DATVE (maVe, maKH, maCD, trangThai, ngDat, giaVe, soluong, thanhTien) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                maVe, maKH, maCD, trangThai, ngDat, giaVe, soluong, thanhTien
            )
    conn.commit()
    messagebox.showinfo("Thành công", "Đã lưu dữ liệu vào CSDL!")
    load_data()
    lam_moi_form()

def thoat():
    root.quit()

# === TẠO FORM CHÍNH ===
root = tk.Tk()
root.title("Quản Lý Đặt Vé")
root.geometry("1000x650")
root.config(bg="#fff8dc")  # Màu nền vàng nhạt

# ========== Nút Về Trang Chủ ==========
btn_home = tk.Button(root, text="Về Trang Chủ", font=("Times New Roman", 10, "bold"), bg="white", relief="groove", command=quit)
btn_home.place(x=50, y=30)

# === TIÊU ĐỀ CHÍNH ===
title_label = tk.Label(root, text="Quản Lý Đặt Vé", font=("Arial", 20, "bold"), bg="#fff8dc")
title_label.place(x=400, y=45)

# ========== Thông tin khách hàng ==========
frame_info = tk.Frame(root, bg="#FFFACD")
frame_info.place(x=100, y=100)

tk.Label(frame_info, text="Mã Vé", bg="#FFFACD", font=("Times New Roman", 12)).grid(row=0, column=0, sticky="w", pady=5)
entry_maVe = tk.Entry(frame_info, width=30)
entry_maVe.grid(row=0, column=1, padx=10, pady=5)
entry_maVe.config(state='readonly')

tk.Label(frame_info, text="Số Lượng", font=("Times New Roman", 12), bg="#fff8dc").grid(row=0, column=2, sticky="w", padx=10, pady=5)
spin_soLuong = tk.Spinbox(frame_info, from_=1, to=100, width=10)
spin_soLuong.grid(row=0, column=3, padx=10, pady=5, columnspan=2)

tk.Label(frame_info, text="Mã Chuyến Đi", bg="#FFFACD", font=("Times New Roman", 12)).grid(row=2, column=0, sticky="w", pady=5)
entry_maCD = ttk.Combobox(frame_info, width=30, values=lay_danh_sach_ma_chuyen_di(),state="readonly")
entry_maCD.grid(row=2, column=1, padx=10, pady=5)
entry_maCD.set("")

tk.Label(frame_info, text="Giá Vé", bg="#FFFACD", font=("Times New Roman", 12)).grid(row=1, column=2, sticky="w", padx=10)
entry_giaVe = tk.Entry(frame_info, width=30)
entry_giaVe.grid(row=1, column=3, padx=10, pady=5, columnspan=2)

tk.Label(frame_info, text="Mã Khách Hàng", bg="#FFFACD", font=("Times New Roman", 12)).grid(row=1, column=0, sticky="w", pady=5)
entry_maKH = ttk.Combobox(frame_info, width=30, state='readonly', values=lay_danh_sach_ma_khach_hang())
entry_maKH.grid(row=1, column=1, padx=10, pady=5)
entry_maKH.set("")

tk.Label(frame_info, text="Trạng Thái", bg="#FFFACD", font=("Times New Roman", 12)).grid(row=2, column=2, sticky="w", padx=10)
entry_trangThai = ttk.Combobox(frame_info, width=30, values=["đã thanh toán","chưa thanh toán"], state='readonly')
entry_trangThai.grid(row=2, column=3, padx=10, pady=5, columnspan=2)
entry_trangThai.set("")

tk.Label(frame_info, text="Ngày Đặt", bg="#FFFACD", font=("Times New Roman", 12)).grid(row=3, column=0, sticky="w", padx=5)
date_ngDat = DateEntry(frame_info, width=12, background='darkblue', foreground='white', borderwidth=2, date_pattern='d/m/yyyy')
date_ngDat.grid(row=3, column=1, padx=10, pady=5)

# ========== Các nút chức năng bên phải ==========
button_style = {"font": ("Times New Roman", 13, "bold"), "bg": "#B0E0E6", "width": 8, "height": 1}

btn_them = tk.Button(root, text="Thêm", **button_style, command=them)
btn_them.place(x=820, y=120)

btn_xoa = tk.Button(root, text="Xóa", **button_style, command=xoa)
btn_xoa.place(x=820, y=200)

btn_sua = tk.Button(root, text="Sửa", **button_style) #command=sua)
btn_sua.place(x=820, y=280)

btn_huy = tk.Button(root, text="Hủy", **button_style, command=huy)
btn_huy.place(x=820, y=360)

btn_luu = tk.Button(root, text="Lưu", **button_style, command=luu)
btn_luu.place(x=820, y=440)

btn_thoat = tk.Button(root, text="Thoát", **button_style, command=thoat)
btn_thoat.place(x=820, y=520)

# === KHUNG THÔNG TIN ĐẶT VÉ ===
frame_info = tk.LabelFrame(root, text="Thông Tin Đặt Vé", font=("Arial", 12, "bold"), bg="#fff8dc", width=750, height=320)
frame_info.place(x=50, y=250)

# Bảng dữ liệu (Treeview)
columns = ("maVe", "maCD", "maKH", "ngDat", "soLuong", "giaVe", "trangThai", "thanhTien")
tree = ttk.Treeview(frame_info, columns=columns, show="headings", height=10)
tree.heading("maVe", text="Mã Vé")
tree.heading("maCD", text="Mã Chuyến Đi")
tree.heading("maKH", text="Mã Khách Hàng")
tree.heading("ngDat", text="Ngày Đặt")
tree.heading("soLuong", text="Số Lượng")
tree.heading("giaVe", text="Giá Vé")
tree.heading("trangThai", text="Trạng Thái")
tree.heading("thanhTien", text="Thành Tiền")

tree.column("maVe", width=90, anchor="center")
tree.column("maCD", width=90, anchor="center")
tree.column("maKH", width=95, anchor="center")
tree.column("ngDat", width=80, anchor="center")
tree.column("soLuong", width=70, anchor="center")
tree.column("giaVe", width=90, anchor="center")
tree.column("trangThai", width=100, anchor="center")
tree.column("thanhTien", width=120, anchor="center")

scrollbar_v = ttk.Scrollbar(frame_info, orient="vertical", command=tree.yview)
scrollbar_h = ttk.Scrollbar(frame_info, orient="horizontal", command=tree.xview)
tree.configure(yscrollcommand=scrollbar_v.set, xscrollcommand=scrollbar_h.set)
tree.place(x=10, y=10, width=720, height=300)
scrollbar_v.place(x=770, y=10, width=20, height=360)
scrollbar_h.place(x=10, y=350, width=750, height=20)

# === CHẠY FORM ===
lam_moi_form()
load_data()
hien_thi_chi_tiet()
root.mainloop()