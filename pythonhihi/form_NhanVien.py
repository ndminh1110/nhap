import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
from datetime import date
import pyodbc

# ------------------ KẾT NỐI SQL SERVER ------------------
conn = pyodbc.connect(
    'DRIVER={ODBC Driver 17 for SQL Server};'
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
def auto_maNV():
    """Tạo mã nhân viên mới tự động dạng NV0001, NV0002,..."""
    cursor.execute("SELECT MAX(maNV) FROM NHANVIEN")
    max_manv = cursor.fetchone()[0]

    tree_list = []
    for item in tree.get_children():
        val = tree.item(item, "values")[0]  # maNV
        if val.startswith("NV"):
            tree_list.append(int(val[2:]))
    max_tree = max(tree_list) if tree_list else 0

    max_val = max(int(max_manv[2:]) if max_manv else 0, max_tree)
    return f"NV{max_val + 1:04d}"

def load_data():
    """Load dữ liệu từ CSDL lên Treeview"""
    for i in tree.get_children():
        tree.delete(i)
    cursor.execute("SELECT maNV, hoTen, sdt, phai, ngsinh, dchi, chucVu FROM NHANVIEN")
    rows = cursor.fetchall()
    for row in rows:
        tree.insert("", "end", values=(row[0], row[1], row[2], row[3], row[4], row[5], row[6], 0, 0))

def load_nam():
    """Lấy danh sách năm từ bảng DATVE"""
    cursor.execute("SELECT DISTINCT YEAR(ngDat) FROM DATVE ORDER BY YEAR(ngDat)")
    nam_list = [str(r[0]) for r in cursor.fetchall()]
    combo_nam['values'] = nam_list
    if nam_list:
        combo_nam.set(nam_list[0])
    else:
        combo_nam.set(str(date.today().year))

def lam_moi_form():
    """Xóa dữ liệu form và tạo mã nhân viên mới"""
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

def toggle_luong_visibility(show=True):
    if show:
        tree["displaycolumns"] = ("maNV","hoTen","sdt","phai","ngsinh","dchi","chucVu","soChuyen","luong")
    else:
        tree["displaycolumns"] = ("maNV","hoTen","sdt","phai","ngsinh","dchi","chucVu","soChuyen")

# ------------------ XEM LƯƠNG ------------------
def xem_luong():
    thang_str = combo_thang.get()
    nam_str = combo_nam.get()

    if not thang_str or not nam_str:
        messagebox.showwarning("Thiếu thông tin", "Vui lòng chọn tháng và năm!")
        return

    thang = int(thang_str)
    nam = int(nam_str)

    # Xóa Treeview
    for row in tree.get_children():
        tree.delete(row)

    # Lấy danh sách nhân viên
    cursor.execute("SELECT maNV, hoTen, sdt, phai, ngsinh, dchi, chucVu FROM NHANVIEN")
    nhanviens = cursor.fetchall()

    # Lấy số chuyến của mỗi nhân viên theo tháng/năm
    cursor.execute("""
        SELECT maNV, COUNT(*) AS soChuyen
        FROM CHUYENDI
        WHERE MONTH(ngKh) = ? AND YEAR(ngKh) = ?
        GROUP BY maNV
    """, (thang, nam))
    chuyens = dict(cursor.fetchall())

    # Hiển thị
    for nv in nhanviens:
        maNV, hoTen, sdt, phai, ngsinh, dchi, chucVu = nv
        soChuyen = chuyens.get(maNV, 0)
        if chucVu == "Cơ Trưởng":
            luong_cb = 2000000
        elif chucVu == "Hướng Dẫn Viên":
            luong_cb = 1800000
        else:
            luong_cb = 1200000
        luong_thuc = luong_cb * soChuyen
        tree.insert("", "end", values=(maNV, hoTen, sdt, phai, ngsinh, dchi, chucVu, soChuyen, luong_thuc))

    toggle_luong_visibility(True)

# ------------------ CHỨC NĂNG TREEVIEW ------------------
def them():
    entry_hoTen.focus()
    ma = entry_maNV.get()
    hoTen = entry_hoTen.get()
    sdt = entry_sdt.get()
    phai = combo_phai.get()
    ngsinh = date_ngsinh.get_date().strftime('%d/%m/%Y')
    dchi = entry_dchi.get()
    chucvu = combo_chucvu.get()
    tree.insert("", "end", values=(ma, hoTen, sdt, phai, ngsinh, dchi, chucvu, 0, 0))
    lam_moi_form()

def sua():
    selected = tree.selection()
    if not selected:
        messagebox.showwarning("Chưa chọn", "Vui lòng chọn nhân viên để sửa!")
        return
    ma = tree.item(selected[0], "values")[0]
    ten = entry_hoTen.get().strip()
    sdt_val = entry_sdt.get().strip()
    phai_val = combo_phai.get()
    ngsinh_val = date_ngsinh.get_date().strftime('%Y-%m-%d')
    dchi_val = entry_dchi.get().strip()
    chucvu_val = combo_chucvu.get().strip()
    tree.item(selected[0], values=(ma, ten, sdt_val, phai_val, ngsinh_val, dchi_val, chucvu_val, 0, 0))
def xoa():
    selected = tree.selection()
    if not selected:
        messagebox.showwarning("Chưa chọn", "Vui lòng chọn nhân viên cần xóa!")
        return
    confirm = messagebox.askyesno("Xác nhận", "Bạn có chắc muốn xóa nhân viên này?")
    if not confirm:
        return
    for item in selected:
        maNV = tree.item(item, "values")[0]
        tree.delete(item)  # <-- xóa khỏi Treeview luôn

    conn.commit()
    messagebox.showinfo("Thành công!")
def luu():
    confirm = messagebox.askyesno("Xác nhận", "Bạn có chắc muốn lưu tất cả dữ liệu vào CSDL?")
    if not confirm:
        return

    # 👉 Xóa toàn bộ dữ liệu cũ trong bảng NHANVIEN
    cursor.execute("DELETE FROM NHANVIEN")
    conn.commit()

    # 👉 Duyệt tất cả các dòng trong Treeview và lưu lại
    for item in tree.get_children():
        maNV, hoTen, sdt, phai, ngsinh, dchi, chucvu, soChuyen, _ = tree.item(item, "values")

        # Kiểm tra SĐT hợp lệ
        if not (sdt.isdigit() and len(sdt) == 10 and sdt.startswith("0")):
            messagebox.showwarning("Bỏ qua", f"SĐT {sdt} của {hoTen} không hợp lệ, không lưu vào CSDL!")
            continue

        # Thêm vào CSDL
        cursor.execute(
            "INSERT INTO NHANVIEN(maNV, hoTen, sdt, phai, ngsinh, dchi, chucVu) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (maNV, hoTen, sdt, phai, ngsinh, dchi, chucvu)
        )

        conn.commit()
        messagebox.showinfo("Thành công", "Đã lưu toàn bộ dữ liệu Treeview vào CSDL!")
    load_data()
    lam_moi_form()


def hien_thi_chi_tiet(event):
    selected = tree.selection()
    if selected:
        ma, hoTen, sdt_val, phai_val, ngsinh_val, dchi_val, chucvu_val, soChuyen_val, luong_val = tree.item(selected[0], "values")
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
            date_ngsinh.set_date(date(d, m, y))
        except:
            date_ngsinh.set_date(date.today())

def huy():
    lam_moi_form()

def thoat():
    conn.close()
    root.destroy()

# ------------------ GIAO DIỆN ------------------
tk.Label(root, text="Quản Lý Nhân Viên", font=("Arial", 20, "bold"), bg="#FFFACD").place(x=330, y=20)

form_frame = tk.Frame(root, bg="#FFFACD")
form_frame.place(x=80, y=60)

# Form
tk.Label(form_frame, text="Mã NV:", font=("Arial", 11), bg="#FFFACD").grid(row=0, column=0, sticky="w", padx=10, pady=8)
entry_maNV = tk.Entry(form_frame, width=25)
entry_maNV.grid(row=0, column=1, padx=10, pady=8)

tk.Label(form_frame, text="Họ tên:", font=("Arial", 11), bg="#FFFACD").grid(row=0, column=2, sticky="w", padx=10, pady=8)
entry_hoTen = tk.Entry(form_frame, width=25)
entry_hoTen.grid(row=0, column=3, padx=10, pady=8)

tk.Label(form_frame, text="SĐT:", font=("Arial", 11), bg="#FFFACD").grid(row=1, column=0, sticky="w", padx=10, pady=8)
entry_sdt = tk.Entry(form_frame, width=25)
entry_sdt.grid(row=1, column=1, padx=10, pady=8)

tk.Label(form_frame, text="Phái:", font=("Arial", 11), bg="#FFFACD").grid(row=1, column=2, sticky="w", padx=10, pady=8)
combo_phai = ttk.Combobox(form_frame, width=22, state="readonly", values=["Nam","Nữ"])
combo_phai.set("Chọn giới tính")
combo_phai.grid(row=1, column=3, padx=10, pady=8)

tk.Label(form_frame, text="Ngày sinh:", font=("Arial", 11), bg="#FFFACD").grid(row=2, column=0, sticky="w", padx=10, pady=8)
date_ngsinh = DateEntry(form_frame, width=23, date_pattern='dd/mm/yyyy')
date_ngsinh.grid(row=2, column=1, padx=10, pady=8)

tk.Label(form_frame, text="Địa chỉ:", font=("Arial", 11), bg="#FFFACD").grid(row=2, column=2, sticky="w", padx=10, pady=8)
entry_dchi = tk.Entry(form_frame, width=25)
entry_dchi.grid(row=2, column=3, padx=10, pady=8)

tk.Label(form_frame, text="Chức vụ:", font=("Arial", 11), bg="#FFFACD").grid(row=3, column=0, sticky="w", padx=10, pady=8)
combo_chucvu = ttk.Combobox(form_frame, width=22, state="readonly", values=["Cơ Trưởng","Hướng Dẫn Viên","Nhân Viên"])
combo_chucvu.set("Chọn chức vụ")
combo_chucvu.grid(row=3, column=1, padx=10, pady=8)

# Tháng & Năm
tk.Label(form_frame, text="Tháng:", font=("Arial", 11), bg="#FFFACD").grid(row=3, column=2, sticky="w", padx=(0,0), pady=8)
combo_thang = ttk.Combobox(form_frame, width=5, values=[str(i) for i in range(1,13)], state="readonly")
combo_thang.set(str(date.today().month))
combo_thang.grid(row=3, column=2, padx=(60,0), sticky="w")

tk.Label(form_frame, text="Năm:", font=("Arial", 11), bg="#FFFACD").grid(row=3, column=3, sticky="w", padx=(0,0), pady=8)
combo_nam = ttk.Combobox(form_frame, width=7, state="readonly")
combo_nam.grid(row=3, column=3, padx=(45,0), sticky="w")

btn_xemluong = tk.Button(form_frame, text="👁 Xem lương", bg="#ADD8E6", font=("Arial",10,"bold"), command=xem_luong)
btn_xemluong.grid(row=3, column=4, padx=20, pady=8)

load_nam()

# ------------------ NÚT CHỨC NĂNG ------------------
btn_them = tk.Button(root, text="Thêm", bg="#87cefa", font=("Arial",12,"bold"), width=10, command=them)
btn_them.place(x=100, y=235)
btn_sua = tk.Button(root, text="Sửa", bg="#87cefa", font=("Arial",12,"bold"), width=10, command=sua)
btn_sua.place(x=240, y=235)
btn_xoa = tk.Button(root, text="Xóa", bg="#87cefa", font=("Arial",12,"bold"), width=10, command=xoa)
btn_xoa.place(x=380, y=235)
btn_huy = tk.Button(root, text="Hủy", bg="#87cefa", font=("Arial",12,"bold"), width=10, command=huy)
btn_huy.place(x=520, y=235)
btn_luu = tk.Button(root, text="Lưu", bg="#87cefa", font=("Arial",12,"bold"), width=10, command=luu)
btn_luu.place(x=660, y=235)
btn_thoat = tk.Button(root, text="Thoát", bg="#87cefa", font=("Arial",12,"bold"), width=10, command=thoat)
btn_thoat.place(x=800, y=235)

# ------------------ TREEVIEW ------------------
tree_frame = tk.LabelFrame(root, text="Danh sách nhân viên", font=("Times New Roman",12), bg="#fff8dc", width=900, height=400)
tree_frame.place(x=50, y=280)

columns = ("maNV","hoTen","sdt","phai","ngsinh","dchi","chucVu","soChuyen","luong")
tree = ttk.Treeview(tree_frame, columns=columns, show="headings", height=15)

for col, text, width in zip(columns,
    ["Mã NV","Họ Tên","SĐT","Phái","Ngày Sinh","Địa Chỉ","Chức Vụ","Số chuyến","Lương"],
    [100,150,100,60,100,200,120,100,100]):
    tree.heading(col, text=text)
    tree.column(col, width=width, anchor="center" if col in ["maNV","sdt","phai","ngsinh","chucVu","soChuyen","luong"] else "w")

scrollbar_v = ttk.Scrollbar(tree_frame, orient="vertical", command=tree.yview)
scrollbar_h = ttk.Scrollbar(tree_frame, orient="horizontal", command=tree.xview)
tree.configure(yscrollcommand=scrollbar_v.set, xscrollcommand=scrollbar_h.set)
tree.grid(row=0, column=0, sticky="nsew", padx=(5,0), pady=(5,0))
scrollbar_v.grid(row=0, column=1, sticky="ns", pady=(5,0))
scrollbar_h.grid(row=1, column=0, sticky="ew", padx=(5,0))
tree_frame.grid_rowconfigure(0, weight=1)
tree_frame.grid_columnconfigure(0, weight=1)

toggle_luong_visibility(False)
tree.bind("<<TreeviewSelect>>", hien_thi_chi_tiet)

# ------------------ KHỞI TẠO ------------------
load_data()
lam_moi_form()

root.mainloop()
