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
    cursor.execute("SELECT COUNT(*) FROM CHUYENDI")
    count = cursor.fetchone()[0] + 1
    return f"CD{count:04d}"

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

tk.Label(root, text="Ngày Khởi Hành", font=("Arial", 12), bg="#fff8dc").place(x=120, y=200)
date_ngKh = DateEntry(root, width=20, background='darkblue', foreground='white', borderwidth=2, date_pattern='dd/mm/yyyy')
date_ngKh.place(x=300, y=200)
date_ngKh.set_date(date.today())

tk.Label(root, text="Thời Gian Khởi Hành", font=("Arial", 12), bg="#fff8dc").place(x=550, y=150)
txt_tgkh = tk.Entry(root, width=25)
txt_tgkh.place(x=700, y=150)

tk.Label(root, text="Số Lượng Hành Khách", font=("Arial", 12), bg="#fff8dc").place(x=120, y=250)
txt_sl = tk.Entry(root, width=25)
txt_sl.place(x=300, y=250)

tk.Label(root, text="Giá Vé (VNĐ)", font=("Arial", 12), bg="#fff8dc").place(x=550, y=200)
txt_gia = tk.Entry(root, width=25)
txt_gia.place(x=700, y=200)

# ------------------ KHUNG BẢNG HIỂN THỊ ------------------
frame_info = tk.LabelFrame(root, text="Danh Sách Chuyến Đi", font=("Arial", 12, "bold"), bg="#fff8dc", width=900, height=300)
frame_info.place(x=50, y=320)

columns = ("maCD", "maTuyen", "maNV", "ngKh", "tgKh", "soLuong", "giaVe")
tree = ttk.Treeview(frame_info, columns=columns, show="headings", height=10)

for col, text in zip(columns, ["Mã CD", "Mã Tuyến", "Mã NV", "Ngày Khởi Hành", "Giờ Khởi Hành", "Số Lượng", "Giá Vé"]):
    tree.heading(col, text=text)
    tree.column(col, width=120, anchor="center")

tree.pack(fill="both", expand=True, padx=10, pady=10)

# ------------------ HÀM CHỨC NĂNG ------------------
def lam_moi_form():
    txt_ma_cd.config(state="normal")
    txt_ma_cd.delete(0, tk.END)
    txt_ma_cd.insert(0, tao_ma_chuyen_di())
    txt_ma_cd.config(state="readonly")
    cb_ma_tuyen.set("Chọn mã tuyến")
    cb_ma_nv.set("Chọn nhân viên")
    date_ngKh.set_date(date.today())
    txt_tgkh.delete(0, tk.END)
    txt_sl.delete(0, tk.END)
    txt_gia.delete(0, tk.END)

def them_chuyen_di():
    maCD = txt_ma_cd.get()
    maTuyen = cb_ma_tuyen.get()
    maNV = cb_ma_nv.get()
    ngKh_value = date_ngKh.get_date()
    tgKh_value = txt_tgkh.get()
    soLuong_value = txt_sl.get() or 0
    giaVe_value = txt_gia.get() or 0

    if maTuyen == "Chọn mã tuyến" or maNV == "Chọn nhân viên" or not tgKh_value:
        messagebox.showwarning("Thiếu thông tin", "Vui lòng nhập đủ dữ liệu")
        return

    tree.insert("", "end", values=(maCD, maTuyen, maNV, ngKh_value, tgKh_value, soLuong_value, giaVe_value))
    lam_moi_form()

def xoa_chuyen_di():
    selected = tree.selection()
    if not selected:
        messagebox.showwarning("Lỗi", "Chưa chọn chuyến đi để xóa")
        return
    for item in selected:
        tree.delete(item)

def luu_chuyen_di():
    for item in tree.get_children():
        maCD, maTuyen, maNV, ngKh_value, tgKh_value, soLuong_value, giaVe_value = tree.item(item, "values")
        soLuong_value = int(soLuong_value or 0)
        giaVe_value = float(giaVe_value or 0)
        
        # Thêm chuyến đi nếu chưa có
        cursor.execute("""
            IF NOT EXISTS (SELECT 1 FROM CHUYENDI WHERE maCD=?)
            INSERT INTO CHUYENDI (maCD, ngKh, tgKh, maNV, maTuyen, giaVe)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (maCD, maCD, ngKh_value, tgKh_value, maNV, maTuyen, giaVe_value))
        
        # Cập nhật doanh thu ban đầu nếu chưa có
        cursor.execute("""
            IF NOT EXISTS (SELECT 1 FROM DOANHTHU WHERE maCD=?)
            INSERT INTO DOANHTHU (maCD, giaVe, soLuong, tongTien)
            VALUES (?, ?, ?, ?)
        """, (maCD, maCD, giaVe_value, soLuong_value, giaVe_value*soLuong_value))
    conn.commit()
    messagebox.showinfo("Thành công", "Đã lưu tất cả chuyến đi vào CSDL")

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
    txt_sl.delete(0, tk.END)
    txt_sl.insert(0, soLuong_value)
    txt_gia.delete(0, tk.END)
    txt_gia.insert(0, giaVe_value)

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


root.mainloop()
