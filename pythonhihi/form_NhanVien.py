import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
import pyodbc
from datetime import date

# ---------------- KẾT NỐI SQL SERVER ----------------
conn = pyodbc.connect(
    'DRIVER={SQL Server};'
    'SERVER=localhost\\SQLEXPRESS01;'
    'DATABASE=QuanLyTuyenDuLich;'
    'Trusted_Connection=yes;'
)
cursor = conn.cursor()

# ---------------- HÀM HỖ TRỢ ----------------
def auto_maNV():
    tree_items = tree.get_children()
    if not tree_items:
        return "NV001"
    else:
        ma_list = [tree.item(item)['values'][0] for item in tree_items]
        last_ma = sorted(ma_list)[-1]
        num = int(last_ma[2:]) + 1
        return f"NV{num:03d}"

def lam_moi_form():
    entry_maNV.config(state='normal')
    entry_maNV.delete(0, tk.END)
    entry_maNV.insert(0, auto_maNV())
    entry_maNV.config(state='readonly')
    
    entry_hoTen.delete(0, tk.END)
    entry_sdt.delete(0, tk.END)
    combo_phai.set("Chọn giới tính")
    combo_chucvu.set("Chọn chức vụ")
    entry_ngsinh.set_date(date.today())
    entry_dchi.delete(0, tk.END)
    entry_luong.config(state='normal')
    entry_luong.delete(0, tk.END)
    entry_luong.config(state='readonly')

def load_data(month=None, year=None):
    """Load dữ liệu từ CSDL lên Treeview"""
    for item in tree.get_children():
        tree.delete(item)
    cursor.execute("SELECT maNV, hoTen, sdt, phai, ngsinh, dchi, chucVu, luong FROM NHANVIEN")
    for row in cursor.fetchall():
        maNV, hoTen, sdt, phai, ngsinh, dchi, chucVu, luong = row
        tree.insert("", tk.END, values=(maNV, hoTen, sdt, phai, ngsinh, dchi, chucVu, luong))

def hien_thi_chi_tiet(event):
    selected = tree.focus()
    if selected:
        values = tree.item(selected)['values']
        entry_maNV.config(state='normal')
        entry_maNV.delete(0, tk.END)
        entry_maNV.insert(0, values[0])
        entry_maNV.config(state='readonly')

        entry_hoTen.delete(0, tk.END)
        entry_hoTen.insert(0, values[1])

        entry_sdt.delete(0, tk.END)
        entry_sdt.insert(0, values[2])

        combo_phai.set(values[3])
        entry_ngsinh.set_date(values[4] if values[4] else date.today())
        entry_dchi.delete(0, tk.END)
        entry_dchi.insert(0, values[5] if values[5] else "")
        combo_chucvu.set(values[6] if values[6] else "")
        entry_luong.config(state='normal')
        entry_luong.delete(0, tk.END)
        entry_luong.insert(0, values[7] if values[7] else "")
        entry_luong.config(state='readonly')

# ---------------- HÀM CHỨC NĂNG ----------------
def them():
    lam_moi_form()
    entry_hoTen.focus()

def sua():
    selected = tree.focus()
    if not selected:
        messagebox.showwarning("Chưa chọn", "Vui lòng chọn nhân viên để sửa")
        return
    hien_thi_chi_tiet(None)
    entry_hoTen.focus()

def huy():
    lam_moi_form()
    tree.selection_remove(tree.selection())

def thoat():
    conn.close()
    root.destroy()

# ---------------- HÀM TÍNH LƯƠNG ----------------
def tinh_luong(chucvu, so_chuyen, luong_cb):
    """Tính lương: cơ trưởng và HDV x1.5"""
    if chucvu in ("Cơ trưởng", "Hướng dẫn viên"):
        return luong_cb * so_chuyen * 1.5
    else:
        return luong_cb * so_chuyen

def luu():
    maNV = entry_maNV.get().strip()
    hoTen = entry_hoTen.get().strip()
    sdt = entry_sdt.get().strip()
    phai = combo_phai.get()
    ngsinh = entry_ngsinh.get_date()
    dchi = entry_dchi.get().strip()
    chucvu = combo_chucvu.get()
    luong_cb = 10000000  # lương cơ bản 10 triệu VND
    so_chuyen = int(combo_thang.get())  # ví dụ số chuyến = tháng đang chọn
    luong = tinh_luong(chucvu, so_chuyen, luong_cb)

    if not hoTen or not sdt or phai=="Chọn giới tính" or chucvu=="Chọn chức vụ":
        messagebox.showwarning("Thiếu dữ liệu", "Vui lòng nhập đầy đủ thông tin!")
        return
    if not (sdt.isdigit() and len(sdt)==10 and sdt.startswith("0")):
        messagebox.showwarning("SĐT không hợp lệ", "SĐT phải 10 số và bắt đầu bằng 0!")
        return

    selected = tree.focus()
    try:
        if selected:  # cập nhật
            cursor.execute(
                "UPDATE NHANVIEN SET hoTen=?, sdt=?, phai=?, ngsinh=?, dchi=?, chucVu=?, luong=? WHERE maNV=?",
                (hoTen, sdt, phai, ngsinh, dchi, chucvu, luong, maNV)
            )
            messagebox.showinfo("Thành công", f"Đã cập nhật nhân viên {hoTen}")
        else:  # thêm mới
            cursor.execute(
                "INSERT INTO NHANVIEN (maNV, hoTen, sdt, phai, ngsinh, dchi, chucVu, luong) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                (maNV, hoTen, sdt, phai, ngsinh, dchi, chucvu, luong)
            )
            messagebox.showinfo("Thành công", f"Đã thêm nhân viên {hoTen}")
        conn.commit()
        lam_moi_form()
        load_data()
    except pyodbc.IntegrityError as e:
        messagebox.showerror("Lỗi SQL", str(e))

def xoa():
    selected = tree.focus()
    if not selected:
        messagebox.showwarning("Chưa chọn", "Vui lòng chọn nhân viên để xóa")
        return
    values = tree.item(selected)['values']
    confirm = messagebox.askyesno("Xác nhận", f"Bạn có muốn xóa nhân viên {values[1]}?")
    if confirm:
        cursor.execute("DELETE FROM NHANVIEN WHERE maNV=?", (values[0],))
        conn.commit()
        load_data()
        lam_moi_form()

# ---------------- GIAO DIỆN ----------------
root = tk.Tk()
root.title("Quản Lý Nhân Viên")
root.geometry("1200x700")
root.configure(bg="#FFFACD")

# Labels + Entry
tk.Label(root, text="Mã NV", bg="#FFFACD").place(x=20, y=20)
entry_maNV = tk.Entry(root)
entry_maNV.place(x=120, y=20)

tk.Label(root, text="Họ tên", bg="#FFFACD").place(x=20, y=60)
entry_hoTen = tk.Entry(root)
entry_hoTen.place(x=120, y=60)

tk.Label(root, text="SĐT", bg="#FFFACD").place(x=20, y=100)
entry_sdt = tk.Entry(root)
entry_sdt.place(x=120, y=100)

tk.Label(root, text="Phái", bg="#FFFACD").place(x=20, y=140)
combo_phai = ttk.Combobox(root, width=17, state="readonly", values=["Nam","Nữ"])
combo_phai.place(x=120, y=140)
combo_phai.set("Chọn giới tính")

tk.Label(root, text="Ngày sinh", bg="#FFFACD").place(x=20, y=180)
entry_ngsinh = DateEntry(root, width=12, date_pattern='yyyy-mm-dd')
entry_ngsinh.place(x=120, y=180)

tk.Label(root, text="Địa chỉ", bg="#FFFACD").place(x=20, y=220)
entry_dchi = tk.Entry(root, width=50)
entry_dchi.place(x=120, y=220)

tk.Label(root, text="Chức vụ", bg="#FFFACD").place(x=20, y=260)
combo_chucvu = ttk.Combobox(root, width=20, state="readonly",
                             values=["Cơ trưởng","Hướng dẫn viên","Quản lý vé","Nhân viên hỗ trợ"])
combo_chucvu.place(x=120, y=260)
combo_chucvu.set("Chọn chức vụ")

tk.Label(root, text="Lương", bg="#FFFACD").place(x=20, y=300)
entry_luong = tk.Entry(root, state='readonly')
entry_luong.place(x=120, y=300)

# Chọn tháng/năm
tk.Label(root, text="Tháng", bg="#FFFACD").place(x=400, y=20)
combo_thang = ttk.Combobox(root, width=5, state="readonly", values=list(range(1,13)))
combo_thang.place(x=450, y=20)
combo_thang.set(date.today().month)

tk.Label(root, text="Năm", bg="#FFFACD").place(x=520, y=20)
combo_nam = ttk.Combobox(root, width=7, state="readonly", values=list(range(2020,2031)))
combo_nam.place(x=560, y=20)
combo_nam.set(date.today().year)

# Buttons
btn_them = tk.Button(root, text="Thêm", bg="#87cefa", width=10, command=them)
btn_them.place(x=20, y=350)
btn_sua = tk.Button(root, text="Sửa", bg="#87cefa", width=10, command=sua)
btn_sua.place(x=140, y=350)
btn_xoa = tk.Button(root, text="Xóa", bg="#87cefa", width=10, command=xoa)
btn_xoa.place(x=260, y=350)
btn_huy = tk.Button(root, text="Hủy", bg="#87cefa", width=10, command=huy)
btn_huy.place(x=380, y=350)
btn_luu = tk.Button(root, text="Lưu", bg="#87cefa", width=10, command=luu)
btn_luu.place(x=500, y=350)
btn_thoat = tk.Button(root, text="Thoát", bg="#87cefa", width=10, command=thoat)
btn_thoat.place(x=620, y=350)

# Treeview
columns = ("maNV","hoTen","sdt","phai","ngsinh","dchi","chucVu","luong")
tree = ttk.Treeview(root, columns=columns, show="headings")
for col in columns:
    tree.heading(col, text=col)
    tree.column(col, width=120)
tree.place(x=20, y=400, width=1150, height=280)
tree.bind("<<TreeviewSelect>>", hien_thi_chi_tiet)

# Load dữ liệu
load_data()
lam_moi_form()

root.mainloop()
