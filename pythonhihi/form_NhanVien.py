import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
from datetime import date
import pyodbc

# ------------------ KẾT NỐI SQL SERVER ------------------
conn = pyodbc.connect(
    'DRIVER={SQL Server};'
    'SERVER=localhost\\SQLEXPRESS01;'
    'DATABASE=QuanLyTuyenDuLich;'
    'Trusted_Connection=yes;'
)
cursor = conn.cursor()

root = tk.Tk()
root.title("Quản Lý Nhân Viên")
root.geometry("1000x650")
root.configure(bg="#FFFACD")

# ------------------ HÀM ------------------
def xem_luong():
    thang = combo_thang.get()
    nam = combo_nam.get()
    if not thang or not nam:
        messagebox.showwarning("Thiếu thông tin", "Vui lòng chọn tháng và năm!")
        return
    
    for row in tree.get_children():
        tree.delete(row)

    cursor.execute("""
        SELECT maNV, hoTen, sdt, phai, ngsinh, dchi, chucVu, luong 
        FROM NhanVien 
        WHERE MONTH(ngsinh)=? AND YEAR(ngsinh)=?
    """, (thang, nam))
    
    for r in cursor.fetchall():
        tree.insert("", "end", values=r)

    toggle_luong_visibility(True)

def toggle_luong_visibility(show=True):
    if show:
        tree["displaycolumns"] = ("maNV", "hoTen", "sdt", "phai", "ngsinh", "dchi", "chucVu", "luong")
    else:
        tree["displaycolumns"] = ("maNV", "hoTen", "sdt", "phai", "ngsinh", "dchi", "chucVu")

def auto_maNV():
    cursor.execute("SELECT maNV FROM NHANVIEN")
    existing_ids = [row[0].strip() for row in cursor.fetchall()]
    if not existing_ids:
        return "NV0001"
    nums = sorted([int(x[2:]) for x in existing_ids if x[2:].isdigit()])
    next_num = 1
    for n in nums:
        if n == next_num:
            next_num += 1
        else:
            break
    return f"NV{next_num:04d}"

def load_data():
    for i in tree.get_children():
        tree.delete(i)
    cursor.execute("SELECT maNV, hoTen, sdt, phai, ngsinh, dchi, chucVu, luong FROM NHANVIEN")
    for row in cursor.fetchall():
        tree.insert("", "end", values=row)
    toggle_luong_visibility(False)

def lam_moi_form():
    entry_maNV.config(state='normal')
    entry_maNV.delete(0, tk.END)
    entry_maNV.insert(0, auto_maNV())
    entry_maNV.config(state='readonly')

    entry_hoTen.delete(0, tk.END)
    entry_sdt.delete(0, tk.END)
    combo_phai.set("Chọn giới tính")
    date_ngsinh.set_date(date.today())
    entry_dchi.delete(0, tk.END)
    combo_chucvu.set("Chọn chức vụ")

def them():
    lam_moi_form()
    entry_hoTen.focus()

def xoa():
    selected = tree.selection()
    if not selected:
        messagebox.showwarning("Chưa chọn", "Vui lòng chọn nhân viên để xóa!")
        return
    confirm = messagebox.askyesno("Xác nhận", "Bạn có chắc muốn xóa?")
    if confirm:
        maNV = tree.item(selected[0])['values'][0]
        cursor.execute("DELETE FROM NHANVIEN WHERE maNV=?", (maNV,))
        conn.commit()
        load_data()
        lam_moi_form()

def sua():
    selected = tree.selection()
    if not selected:
        messagebox.showwarning("Chưa chọn", "Vui lòng chọn nhân viên để sửa!")
        return
    ma = tree.item(selected[0])['values'][0]
    ten = entry_hoTen.get().strip()
    chucvu = combo_chucvu.get().strip()
    sdt = entry_sdt.get().strip()
    gioi_tinh = combo_phai.get()
    ngsinh = date_ngsinh.get_date().strftime('%Y-%m-%d')
    dchi = entry_dchi.get().strip()

    if not ten or not sdt:
        messagebox.showwarning("Thiếu dữ liệu", "Vui lòng nhập đầy đủ thông tin!")
        return
    if not (sdt.isdigit() and len(sdt) == 10 and sdt.startswith("0")):
        messagebox.showerror("Lỗi", "SĐT phải bắt đầu bằng 0 và đủ 10 số!")
        return

    cursor.execute(
        "UPDATE NHANVIEN SET hoTen=?, chucVu=?, sdt=?, phai=?, ngsinh=?, dchi=? WHERE maNV=?",
        (ten, chucvu, sdt, gioi_tinh, ngsinh, dchi, ma)
    )
    conn.commit()
    messagebox.showinfo("Thành công", "Đã cập nhật thông tin!")
    load_data()
    lam_moi_form()

def hien_thi_chi_tiet(event):
    selected = tree.selection()
    if selected:
        ma, hoTen, sdt_val, phai_val, ngsinh_val, dchi_val, chucvu_val, luong_val = tree.item(selected[0], "values")
        entry_maNV.config(state='normal')
        entry_maNV.delete(0, tk.END)
        entry_maNV.insert(0, ma)
        entry_maNV.config(state='readonly')

        entry_hoTen.delete(0, tk.END)
        entry_hoTen.insert(0, hoTen)

        entry_sdt.delete(0, tk.END)
        entry_sdt.insert(0, sdt_val)

        combo_phai.set(phai_val)
        combo_chucvu.set(chucvu_val)
        entry_dchi.delete(0, tk.END)
        entry_dchi.insert(0, dchi_val)

        try:
            y, m, d = map(int, str(ngsinh_val).split('-'))
            date_ngsinh.set_date(date(y, m, d))
        except:
            date_ngsinh.set_date(date.today())

def huy():
    lam_moi_form()

def luu():
    ma = entry_maNV.get().strip()
    ten = entry_hoTen.get().strip()
    sdt = entry_sdt.get().strip()
    phai = combo_phai.get()
    ngsinh = date_ngsinh.get_date().strftime('%Y-%m-%d')
    dchi = entry_dchi.get().strip()
    chucvu = combo_chucvu.get().strip()
    if not ten or not sdt:
        messagebox.showwarning("Thiếu dữ liệu", "Vui lòng nhập đủ thông tin!")
        return
    if not (sdt.isdigit() and len(sdt) == 10 and sdt.startswith("0")):
        messagebox.showerror("Lỗi", "SĐT phải bắt đầu bằng 0 và đủ 10 số!")
        return
    cursor.execute(
        "INSERT INTO NHANVIEN(maNV, hoTen, sdt, phai, ngsinh, dchi, chucVu) VALUES (?, ?, ?, ?, ?, ?, ?)",
        (ma, ten, sdt, phai, ngsinh, dchi, chucvu)
    )
    conn.commit()
    messagebox.showinfo("Thành công", "Đã thêm nhân viên!")
    load_data()
    lam_moi_form()

def thoat():
    conn.close()
    root.destroy()
# ------------------ TIÊU ĐỀ ------------------
title_frame = tk.Frame(root, bg="#FFFACD")
title_frame.pack(pady=(10, 0))  # tạo khoảng cách trên

tk.Label(root, text="Quản Lý Nhân Viên", font=("Arial", 20, "bold"), bg="#FFFACD").place(x=330, y=20)
# ------------------ FORM ------------------
form_frame = tk.Frame(root, bg="#FFFACD")
form_frame.place(x=80, y=60)  

# Hàng 1
tk.Label(form_frame, text="Mã NV:", font=("Arial", 11), bg="#FFFACD").grid(row=0, column=0, sticky="w", padx=10, pady=8)
entry_maNV = tk.Entry(form_frame, width=25)
entry_maNV.grid(row=0, column=1, padx=10, pady=8)

tk.Label(form_frame, text="Họ tên:", font=("Arial", 11), bg="#FFFACD").grid(row=0, column=2, sticky="w", padx=10, pady=8)
entry_hoTen = tk.Entry(form_frame, width=25)
entry_hoTen.grid(row=0, column=3, padx=10, pady=8)

# Hàng 2
tk.Label(form_frame, text="SĐT:", font=("Arial", 11), bg="#FFFACD").grid(row=1, column=0, sticky="w", padx=10, pady=8)
entry_sdt = tk.Entry(form_frame, width=25)
entry_sdt.grid(row=1, column=1, padx=10, pady=8)

tk.Label(form_frame, text="Phái:", font=("Arial", 11), bg="#FFFACD").grid(row=1, column=2, sticky="w", padx=10, pady=8)
combo_phai = ttk.Combobox(form_frame, width=22, state="readonly", values=["Nam", "Nữ"])
combo_phai.set("Chọn giới tính")
combo_phai.grid(row=1, column=3, padx=10, pady=8)

# Hàng 3
tk.Label(form_frame, text="Ngày sinh:", font=("Arial", 11), bg="#FFFACD").grid(row=2, column=0, sticky="w", padx=10, pady=8)
date_ngsinh = DateEntry(form_frame, width=23, date_pattern='yyyy-mm-dd')
date_ngsinh.grid(row=2, column=1, padx=10, pady=8)

tk.Label(form_frame, text="Địa chỉ:", font=("Arial", 11), bg="#FFFACD").grid(row=2, column=2, sticky="w", padx=10, pady=8)
entry_dchi = tk.Entry(form_frame, width=25)
entry_dchi.grid(row=2, column=3, padx=10, pady=8)

# Hàng 4
tk.Label(form_frame, text="Chức vụ:", font=("Arial", 11), bg="#FFFACD").grid(row=3, column=0, sticky="w", padx=10, pady=8)
combo_chucvu = ttk.Combobox(form_frame, width=22, state="readonly", values=["Quản lý", "Nhân viên", "Kế toán"])
combo_chucvu.set("Chọn chức vụ")
combo_chucvu.grid(row=3, column=1, padx=10, pady=8)

# Tháng & Năm
tk.Label(form_frame, text="Tháng:", font=("Arial", 11), bg="#FFFACD").grid(row=3, column=2, sticky="w", padx=10, pady=8)
combo_thang = ttk.Combobox(form_frame, width=5, values=[str(i) for i in range(1, 13)], state="readonly")
combo_thang.set("11")
combo_thang.grid(row=3, column=2, padx=(70, 0), sticky="w")

tk.Label(form_frame, text="Năm:", font=("Arial", 11), bg="#FFFACD").grid(row=3, column=3, sticky="w", padx=(0, 0), pady=8)
combo_nam = ttk.Combobox(form_frame, width=7, values=["2024", "2025", "2026"], state="readonly")
combo_nam.set("2025")
combo_nam.grid(row=3, column=3, padx=(45, 0), pady=8, sticky="w")

# Nút xem lương
btn_xemluong = tk.Button(form_frame, text="👁 Xem lương", bg="#ADD8E6", font=("Arial", 10, "bold"), command=xem_luong)
btn_xemluong.grid(row=3, column=4, padx=20, pady=8)


# ------------------ NÚT CHỨC NĂNG ------------------
btn_them = tk.Button(root, text="Thêm", bg="#87cefa", font=("Arial", 12, "bold"), width=10, command=them)
btn_them.place(x=100, y=235)

btn_sua = tk.Button(root, text="Sửa", bg="#87cefa", font=("Arial", 12, "bold"), width=10, command=sua)
btn_sua.place(x=240, y=235)

btn_xoa = tk.Button(root, text="Xóa", bg="#87cefa", font=("Arial", 12, "bold"), width=10, command=xoa)
btn_xoa.place(x=380, y=235)

btn_huy = tk.Button(root, text="Hủy", bg="#87cefa", font=("Arial", 12, "bold"), width=10, command=huy)
btn_huy.place(x=520, y=235)

btn_luu = tk.Button(root, text="Lưu", bg="#87cefa", font=("Arial", 12, "bold"), width=10, command=luu)
btn_luu.place(x=660, y=235)

btn_thoat = tk.Button(root, text="Thoát", bg="#87cefa", font=("Arial", 12, "bold"), width=10, command=root.quit)
btn_thoat.place(x=800, y=235)

# ------------------ TREEVIEW ------------------
tree_frame = tk.LabelFrame(root, text="Danh sách nhân viên", font=("Times New Roman", 12),
                           bg="#fff8dc", width=900, height=400)
tree_frame.place(x=50, y=280)

columns = ("maNV", "hoTen", "sdt", "phai", "ngsinh", "dchi", "chucVu", "luong")
tree = ttk.Treeview(tree_frame, columns=columns, show="headings", height=15)

# Cấu hình tiêu đề
tree.heading("maNV", text="Mã NV")
tree.heading("hoTen", text="Họ Tên")
tree.heading("sdt", text="SĐT")
tree.heading("phai", text="Phái")
tree.heading("ngsinh", text="Ngày Sinh")
tree.heading("dchi", text="Địa Chỉ")
tree.heading("chucVu", text="Chức Vụ")
tree.heading("luong", text="Lương")

# Cấu hình độ rộng cột
tree.column("maNV", width=100, anchor="center")
tree.column("hoTen", width=150)
tree.column("sdt", width=100, anchor="center")
tree.column("phai", width=60, anchor="center")
tree.column("ngsinh", width=100, anchor="center")
tree.column("dchi", width=200)
tree.column("chucVu", width=120, anchor="center")
tree.column("luong", width=100, anchor="center")

# Tạo scrollbar
scrollbar_v = ttk.Scrollbar(tree_frame, orient="vertical", command=tree.yview)
scrollbar_h = ttk.Scrollbar(tree_frame, orient="horizontal", command=tree.xview)
tree.configure(yscrollcommand=scrollbar_v.set, xscrollcommand=scrollbar_h.set)

# Đặt TreeView và Scrollbar gọn trong khung
tree.grid(row=0, column=0, sticky="nsew", padx=(5, 0), pady=(5, 0))
scrollbar_v.grid(row=0, column=1, sticky="ns", pady=(5, 0))
scrollbar_h.grid(row=1, column=0, sticky="ew", padx=(5, 0))

# Cho khung tree_frame tự co giãn hợp lý
tree_frame.grid_rowconfigure(0, weight=1)
tree_frame.grid_columnconfigure(0, weight=1)

# Ẩn lương mặc định nếu cần
toggle_luong_visibility(False)

# Sự kiện khi chọn dòng
tree.bind("<<TreeviewSelect>>", hien_thi_chi_tiet)

load_data()
root.mainloop()
