import tkinter as tk
from tkinter import ttk, messagebox
import pyodbc

# ------------------ KẾT NỐI SQL SERVER ------------------
conn = pyodbc.connect(
    'DRIVER={SQL Server};'
    'SERVER=localhost\\SQLEXPRESS01;'  
    'DATABASE=QuanLyTuyenDuLich;'
    'Trusted_Connection=yes;'
)
cursor = conn.cursor()

# ------------------ TẠO BẢNG CHUYENDI NẾU CHƯA CÓ ------------------
cursor.execute("""
IF OBJECT_ID('CHUYENDI', 'U') IS NULL
BEGIN
    CREATE TABLE CHUYENDI (
        maCD NVARCHAR(10) PRIMARY KEY,
        maTuyen NVARCHAR(10),
        tgKhoiHanh NVARCHAR(50),
        soLuong INT,
        giaVe DECIMAL(18,2),
        FOREIGN KEY (maTuyen) REFERENCES TUYENDULICH(maTuyen)
    )
END
""")
conn.commit()

# ------------------ HÀM TẠO MÃ CHUYẾN ĐI ------------------
def tao_ma_chuyen_di():
    cursor.execute("SELECT MAX(maCD) FROM CHUYENDI")
    max_ma = cursor.fetchone()[0]
    if max_ma:
        return f"CD{int(max_ma[2:]) + 1:04d}"
    return "CD0001"

# ------------------ LẤY DANH SÁCH MÃ TUYẾN ------------------
def lay_ds_ma_tuyen():
    cursor.execute("SELECT maTuyen FROM TUYENDULICH")
    return [row[0] for row in cursor.fetchall()]

# ------------------ LOAD DỮ LIỆU VÀO TREEVIEW ------------------
def load_data():
    for item in tree.get_children():
        tree.delete(item)
    cursor.execute("SELECT maCD, maTuyen, tgKhoiHanh, soLuong, giaVe FROM CHUYENDI")
    rows = cursor.fetchall()
    for row in rows:
        tree.insert("", "end", values=(row[0].strip(), row[1].strip(), row[2].strip(), row[3], float(row[4])))

# ------------------ KHỞI TẠO GIAO DIỆN ------------------
root = tk.Tk()
root.title("Quản Lý Chuyến Đi")
root.geometry("1000x650")
root.config(bg="#fff8dc")

tk.Label(root, text="Quản Lý Chuyến Đi", font=("Arial", 20, "bold"), bg="#fff8dc").place(x=380, y=30)

# ------------------ NHÃN VÀ Ô NHẬP ------------------
tk.Label(root, text="Mã Chuyến Đi", font=("Arial", 12), bg="#fff8dc").place(x=50, y=100)
txt_ma_cd = tk.Entry(root, width=20)
txt_ma_cd.place(x=180, y=100)
txt_ma_cd.insert(0, tao_ma_chuyen_di())
txt_ma_cd.config(state="readonly")

tk.Label(root, text="Mã Tuyến", font=("Arial", 12), bg="#fff8dc").place(x=400, y=100)
cb_ma_tuyen = ttk.Combobox(root, width=20, state="readonly", values=lay_ds_ma_tuyen())
cb_ma_tuyen.place(x=500, y=100)
cb_ma_tuyen.set("Chọn mã tuyến")

tk.Label(root, text="Thời Gian Khởi Hành", font=("Arial", 12), bg="#fff8dc").place(x=50, y=150)
txt_tgkh = tk.Entry(root, width=25)
txt_tgkh.place(x=180, y=150)

tk.Label(root, text="Số Lượng Hành Khách", font=("Arial", 12), bg="#fff8dc").place(x=400, y=150)
txt_sl = tk.Entry(root, width=25)
txt_sl.place(x=550, y=150)

tk.Label(root, text="Giá Vé (VNĐ)", font=("Arial", 12), bg="#fff8dc").place(x=50, y=200)
txt_gia = tk.Entry(root, width=25)
txt_gia.place(x=180, y=200)

# ------------------ TREEVIEW ------------------
frame_info = tk.LabelFrame(root, text="Danh Sách Chuyến Đi", font=("Arial", 12, "bold"), bg="#fff8dc", width=900, height=300)
frame_info.place(x=50, y=260)

columns = ("maCD", "maTuyen", "tgKhoiHanh", "soLuong", "giaVe")
tree = ttk.Treeview(frame_info, columns=columns, show="headings", height=12)
for col, text in zip(columns, ["Mã CD", "Mã Tuyến", "Thời Gian KH", "SL Hành Khách", "Giá Vé (VNĐ)"]):
    tree.heading(col, text=text)
    tree.column(col, width=160, anchor="center")

scrollbar = ttk.Scrollbar(frame_info, orient="vertical", command=tree.yview)
tree.configure(yscrollcommand=scrollbar.set)
tree.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")

# ------------------ HÀM CHỨC NĂNG ------------------
def lam_moi_form():
    txt_ma_cd.config(state="normal")
    txt_ma_cd.delete(0, tk.END)
    txt_ma_cd.insert(0, tao_ma_chuyen_di())
    txt_ma_cd.config(state="readonly")
    cb_ma_tuyen.set("Chọn mã tuyến")
    txt_tgkh.delete(0, tk.END)
    txt_sl.delete(0, tk.END)
    txt_gia.delete(0, tk.END)

def them_chuyen_di():
    maCD = tao_ma_chuyen_di()
    maTuyen = cb_ma_tuyen.get()
    tgkh = txt_tgkh.get()
    soLuong = txt_sl.get()
    giaVe = txt_gia.get()
    if not maTuyen or not tgkh or not soLuong or not giaVe:
        messagebox.showwarning("Thiếu thông tin", "Vui lòng nhập đầy đủ thông tin")
        return
    tree.insert("", "end", values=(maCD, maTuyen, tgkh, int(soLuong), float(giaVe)))
    lam_moi_form()

def xoa_chuyen_di():
    selected = tree.selection()
    if not selected:
        messagebox.showwarning("Lỗi", "Chưa chọn chuyến đi để xóa")
        return
    confirm = messagebox.askyesno("Xác nhận", "Bạn có chắc muốn xóa chuyến đi này?")
    if confirm:
        for item in selected:
            maCD = tree.item(item, "values")[0]
            cursor.execute("DELETE FROM CHUYENDI WHERE maCD=?", (maCD,))
            conn.commit()
            tree.delete(item)

def sua_chuyen_di():
    selected = tree.selection()
    if not selected:
        messagebox.showwarning("Lỗi", "Chưa chọn chuyến đi để sửa")
        return
    item = selected[0]
    values = tree.item(item, "values")
    txt_ma_cd.config(state="normal")
    txt_ma_cd.delete(0, tk.END)
    txt_ma_cd.insert(0, values[0])
    txt_ma_cd.config(state="readonly")
    cb_ma_tuyen.set(values[1])
    txt_tgkh.delete(0, tk.END)
    txt_tgkh.insert(0, values[2])
    txt_sl.delete(0, tk.END)
    txt_sl.insert(0, values[3])
    txt_gia.delete(0, tk.END)
    txt_gia.insert(0, values[4])

def luu_chuyen_di():
    for item in tree.get_children():
        maCD, maTuyen, tgkh, soLuong, giaVe = tree.item(item, "values")
        cursor.execute("""
            IF EXISTS (SELECT 1 FROM CHUYENDI WHERE maCD=?)
                UPDATE CHUYENDI SET maTuyen=?, tgKhoiHanh=?, soLuong=?, giaVe=? WHERE maCD=?
            ELSE
                INSERT INTO CHUYENDI(maCD, maTuyen, tgKhoiHanh, soLuong, giaVe)
                VALUES (?, ?, ?, ?, ?)
        """, (maCD, maTuyen, tgkh, soLuong, giaVe, maCD, maCD, maTuyen, tgkh, soLuong, giaVe))
    conn.commit()
    messagebox.showinfo("Thành công", "Đã lưu tất cả chuyến đi vào CSDL")
    load_data()

def huy():
    lam_moi_form()

# ------------------ NÚT CHỨC NĂNG ------------------
btn_them = tk.Button(root, text="Thêm", bg="#87cefa", font=("Arial", 12, "bold"), width=10, command=them_chuyen_di)
btn_them.place(x=100, y=580)

btn_sua = tk.Button(root, text="Sửa", bg="#87cefa", font=("Arial", 12, "bold"), width=10, command=sua_chuyen_di)
btn_sua.place(x=240, y=580)

btn_xoa = tk.Button(root, text="Xóa", bg="#87cefa", font=("Arial", 12, "bold"), width=10, command=xoa_chuyen_di)
btn_xoa.place(x=380, y=580)

btn_huy = tk.Button(root, text="Hủy", bg="#87cefa", font=("Arial", 12, "bold"), width=10, command=huy)
btn_huy.place(x=520, y=580)

btn_luu = tk.Button(root, text="Lưu", bg="#87cefa", font=("Arial", 12, "bold"), width=10, command=luu_chuyen_di)
btn_luu.place(x=660, y=580)

btn_thoat = tk.Button(root, text="Thoát", bg="#87cefa", font=("Arial", 12, "bold"), width=10, command=root.quit)
btn_thoat.place(x=800, y=580)

# ------------------ LOAD DỮ LIỆU LẦN ĐẦU ------------------
load_data()
root.mainloop()
