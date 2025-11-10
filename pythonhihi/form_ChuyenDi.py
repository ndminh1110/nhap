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

# ------------------ HÀM TẠO MÃ TỰ ĐỘNG ------------------
def tao_ma_chuyen_di():
    cursor.execute("SELECT maCD FROM CHUYENDI")
    ma_list = [row[0] for row in cursor.fetchall()]
    if not ma_list:
        return "CD0001"
    so_list = sorted([int(ma[2:]) for ma in ma_list if ma[2:].isdigit()])
    next_num = 1
    for num in so_list:
        if num == next_num:
            next_num += 1
        elif num > next_num:
            break
    return f"CD{next_num:04d}"

def lay_ds_ma_tuyen():
    cursor.execute("SELECT maTuyen FROM TUYENDULICH")
    return [row[0] for row in cursor.fetchall()]

def lay_ds_ma_nv():
    cursor.execute("SELECT maNV FROM NHANVIEN")
    return [row[0] for row in cursor.fetchall()]

# ------------------ GIAO DIỆN CHÍNH ------------------
root = tk.Tk()
root.title("Quản Lý Chuyến Đi")
root.geometry("1000x650")
root.config(bg="#fff8dc")

tk.Label(root, text="Quản Lý Chuyến Đi", font=("Arial", 20, "bold"), bg="#fff8dc").place(x=380, y=30)

btn_home = tk.Button(root, text="Về Trang Chủ", font=("Arial", 10, "bold"), bg="white", relief="groove", command=root.quit)
btn_home.place(x=50, y=30)

# ------------------ NHÃN VÀ Ô NHẬP ------------------
tk.Label(root, text="Mã Chuyến Đi", font=("Arial", 12), bg="#fff8dc").place(x=120, y=100)
txt_ma_cd = tk.Entry(root, width=20)
txt_ma_cd.place(x=300, y=100)
txt_ma_cd.insert(0, tao_ma_chuyen_di())
txt_ma_cd.config(state="readonly")

tk.Label(root, text="Mã Tuyến", font=("Arial", 12), bg="#fff8dc").place(x=550, y=100)
cb_ma_tuyen = ttk.Combobox(root, width=20, state="readonly", values=lay_ds_ma_tuyen())
cb_ma_tuyen.place(x=700, y=100)
cb_ma_tuyen.set("Chọn mã tuyến")

tk.Label(root, text="Mã Nhân Viên", font=("Arial", 12), bg="#fff8dc").place(x=120, y=150)
cb_ma_nv = ttk.Combobox(root, width=20, state="readonly", values=lay_ds_ma_nv())
cb_ma_nv.place(x=300, y=150)
cb_ma_nv.set("Chọn nhân viên")

tk.Label(root, text="Ngày Khởi Hành", font=("Ariqal", 12), bg="#fff8dc").place(x=120, y=200)
date_ngKh = DateEntry(root, width=20, background='darkblue', foreground='white', borderwidth=2, date_pattern='dd/mm/yyyy')
date_ngKh.place(x=300, y=200)
date_ngKh.set_date(date.today())

tk.Label(root, text="Thời Gian Khởi Hành", font=("Arial", 12), bg="#fff8dc").place(x=550, y=150)
txt_tgkh = tk.Entry(root, width=25)
txt_tgkh.place(x=700, y=150)


# ------------------ KHUNG BẢNG HIỂN THỊ ------------------
frame_info = tk.LabelFrame(root, text="Danh Sách Chuyến Đi", font=("Arial", 12, "bold"), bg="#fff8dc", width=900, height=300)
frame_info.place(x=50, y=320)

columns = ("maCD", "maTuyen", "maNV", "ngKh", "tgKh")
tree = ttk.Treeview(frame_info, columns=columns, show="headings", height=10)

for col, text in zip(columns, ["Mã CD", "Mã Tuyến", "Mã NV", "Ngày Khởi Hành", "Giờ Khởi Hành"]):
    tree.heading(col, text=text)
    tree.column(col, width=120, anchor="center")

tree.pack(fill="both", expand=True, padx=10, pady=10)

# ------------------ HÀM CHỨC NĂNG ------------------
def load_data():
    """Load dữ liệu từ CSDL lên Treeview"""
    for i in tree.get_children():
        tree.delete(i)
    cursor.execute("SELECT maCD, maNV,maTuyen, tgKH, ngKH FROM CHUYENDI")
    rows = cursor.fetchall()
    for row in rows:
        tree.insert("", "end", values=(row[0].strip(), row[1].strip(), row[2].strip(), row[3].strip(), row[4].strip()))

def lam_moi_form():
    txt_ma_cd.config(state="normal")
    txt_ma_cd.delete(0, tk.END)
    txt_ma_cd.insert(0, tao_ma_chuyen_di())
    txt_ma_cd.config(state="readonly")
    cb_ma_tuyen.set("Chọn mã tuyến")
    cb_ma_nv.set("Chọn nhân viên")
    date_ngKh.set_date(date.today())
    txt_tgkh.delete(0, tk.END)

def them_chuyen_di():
    maCD = txt_ma_cd.get()
    maTuyen = cb_ma_tuyen.get()
    maNV = cb_ma_nv.get()
    ngKh_value = date_ngKh.get_date()
    tgKh_value = txt_tgkh.get()

    if maTuyen == "Chọn mã tuyến" or maNV == "Chọn nhân viên" or not tgKh_value:
        messagebox.showwarning("Thiếu thông tin", "Vui lòng nhập đủ dữ liệu")
        return
    tree.insert("", "end", values=(maCD, maTuyen, maNV, ngKh_value, tgKh_value))
    lam_moi_form()

def xoa_chuyen_di():
    selected = tree.selection()
    if not selected:
        messagebox.showwarning("Lỗi", "Chưa chọn chuyến đi để xóa")
        return
    for item in selected:
        tree.delete(item)
def hien_thi_chi_tiet():
    selected = tree.selection()
    if selected:
        maCD, maTuyen, maNV, tgKH, ngKH = tree.item(selected[0], "values")
        txt_ma_cd.config(state='normal')
        txt_ma_cd.delete(0, tk.END)
        txt_ma_cd.insert(0, maCD)
        txt_ma_cd.config(state='readonly')

        cb_ma_tuyen.delete(0, tk.END)
        cb_ma_tuyen.insert(0, maTuyen)

        cb_ma_nv.delete(0, tk.END)
        cb_ma_nv.insert(0, maNV)

        date_ngKh.delete(0, tk.END)
        date_ngKh.set_date(ngKH)

        txt_tgkh.delete(0, tk.END)
        txt_tgkh.insert(0, tgKH)

def luu_chuyen_di():
    for item in tree.get_children():
        maCD, maTuyen, maNV, ngKh_value, tgKh_value = tree.item(item, "values")
        cursor.execute("SELECT 1 FROM CHUYENDI WHERE maCD=?", (maCD,))
        if not cursor.fetchone():
            cursor.execute(
                " INSERT INTO CHUYENDI (maCD, maTuyen, maNV, ngKh, tgKh) VALUES (?, ?, ?, ?, ?)",
                (maCD, maTuyen, maNV, ngKh_value, tgKh_value)
            )
    conn.commit()
    messagebox.showinfo("Thành công", "Đã lưu dữ liệu vào CSDL!")
    load_data()
    lam_moi_form()

def sua_chuyen_di():
    selected = tree.selection()
    if not selected:
        messagebox.showwarning("Lỗi", "Chưa chọn chuyến đi để sửa")
        return
    item = selected[0]
    maCD, maTuyen, maNV, ngKh_value, tgKh_value, soLuong_value, giaVe_value = tree.item(item, "values")
    txt_ma_cd.config(state="normal")
    txt_ma_cd.delete(0, tk.END)
    txt_ma_cd.insert(0, maCD)
    txt_ma_cd.config(state="readonly")
    cb_ma_tuyen.set(maTuyen)
    cb_ma_nv.set(maNV)
    date_ngKh.set_date(ngKh_value)
    txt_tgkh.delete(0, tk.END)
    txt_tgkh.insert(0, tgKh_value)


def huy():
    lam_moi_form()

# ------------------ NÚT CHỨC NĂNG ------------------
btn_them = tk.Button(root, text="Thêm", bg="#87cefa", font=("Arial", 12, "bold"), width=10, command=them_chuyen_di)
btn_them.place(x=100, y=280)

btn_sua = tk.Button(root, text="Sửa", bg="#87cefa", font=("Arial", 12, "bold"), width=10, command=sua_chuyen_di)
btn_sua.place(x=240, y=280)

btn_xoa = tk.Button(root, text="Xóa", bg="#87cefa", font=("Arial", 12, "bold"), width=10, command=xoa_chuyen_di)
btn_xoa.place(x=380, y=280)

btn_huy = tk.Button(root, text="Hủy", bg="#87cefa", font=("Arial", 12, "bold"), width=10, command=huy)
btn_huy.place(x=520, y=280)

btn_luu = tk.Button(root, text="Lưu", bg="#87cefa", font=("Arial", 12, "bold"), width=10, command=luu_chuyen_di)
btn_luu.place(x=660, y=280)

btn_thoat = tk.Button(root, text="Thoát", bg="#87cefa", font=("Arial", 12, "bold"), width=10, command=root.quit)
btn_thoat.place(x=800, y=280)

load_data()
lam_moi_form()
hien_thi_chi_tiet()
root.mainloop()
