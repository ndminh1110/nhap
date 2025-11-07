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

# ------------------ HÀM TẠO MÃ TỰ ĐỘNG ------------------
def tao_ma_chuyen_di():
    cursor.execute("SELECT COUNT(*) FROM CHUYENDI")
    count = cursor.fetchone()[0] + 1
    return f"CD{count:04d}"

# ------------------ HÀM LẤY DỮ LIỆU COMBOBOX ------------------
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

# === TIÊU ĐỀ ===
tk.Label(root, text="Quản Lý Chuyến Đi", font=("Arial", 20, "bold"), bg="#fff8dc").place(x=380, y=30)

# ========== Nút Về Trang Chủ ==========
btn_home = tk.Button(root, text="Trang Chủ", font=("Arial", 10, "bold"), bg="white", relief="groove", command=root.quit)
btn_home.place(x=50, y=30)

# ------------------ NHÃN VÀ Ô NHẬP ------------------
tk.Label(root, text="Mã Chuyến Đi", font=("Arial", 12), bg="#fff8dc").place(x=140, y=100)
txt_ma_cd = tk.Entry(root, width=20)
txt_ma_cd.place(x=300, y=100)
txt_ma_cd.insert(0, tao_ma_chuyen_di())
txt_ma_cd.config(state="readonly")

tk.Label(root, text="Mã Tuyến", font=("Arial", 12), bg="#fff8dc").place(x=550, y=100)
cb_ma_tuyen = ttk.Combobox(root, width=20, state="readonly", values=lay_ds_ma_tuyen())
cb_ma_tuyen.place(x=700, y=100)
cb_ma_tuyen.set("Chọn mã tuyến")

tk.Label(root, text="Mã Nhân Viên", font=("Arial", 12), bg="#fff8dc").place(x=140, y=150)
cb_ma_nv = ttk.Combobox(root, width=20, state="readonly", values=lay_ds_ma_nv())
cb_ma_nv.place(x=300, y=150)
cb_ma_nv.set("Chọn nhân viên")

tk.Label(root, text="Thời Gian Khởi Hành", font=("Arial", 12), bg="#fff8dc").place(x=550, y=150)
txt_tgkh = tk.Entry(root, width=25)
txt_tgkh.place(x=700, y=150)

tk.Label(root, text="Số Lượng Hành Khách", font=("Arial", 12), bg="#fff8dc").place(x=140, y=200)
txt_sl = tk.Entry(root, width=25)
txt_sl.place(x=300, y=200)

tk.Label(root, text="Giá Vé (VNĐ)", font=("Arial", 12), bg="#fff8dc").place(x=550, y=200)
txt_gia = tk.Entry(root, width=25)
txt_gia.place(x=700, y=200)

# ------------------ KHUNG BẢNG HIỂN THỊ ------------------
frame_info = tk.LabelFrame(root, text="Danh Sách Chuyến Đi", font=("Arial", 12, "bold"), bg="#fff8dc", width=900, height=300)
frame_info.place(x=50, y=260)

columns = ("maCD", "maTuyen", "maNV", "tgKhoiHanh", "soLuong", "giaVe")
tree = ttk.Treeview(frame_info, columns=columns, show="headings", height=10)

for col, text in zip(columns, ["Mã Chuyến Đi", "Mã Tuyến", "Mã Nhân Viên", "Thời Gian Khởi Hành", "Số Lượng", "Giá Vé (VNĐ)"]):
    tree.heading(col, text=text)
    tree.column(col, width=140, anchor="center")

tree.pack(fill="both", expand=True, padx=10, pady=10)

# ------------------ NÚT CHỨC NĂNG ------------------
btn_them = tk.Button(root, text="Thêm", bg="#87cefa", font=("Arial", 12, "bold"), width=10)
btn_them.place(x=100, y=580)

btn_xoa = tk.Button(root, text="Xóa", bg="#87cefa", font=("Arial", 12, "bold"), width=10)
btn_xoa.place(x=240, y=580)

btn_sua = tk.Button(root, text="Sửa", bg="#87cefa", font=("Arial", 12, "bold"), width=10)
btn_sua.place(x=380, y=580)

btn_huy = tk.Button(root, text="Hủy", bg="#87cefa", font=("Arial", 12, "bold"), width=10)
btn_huy.place(x=520, y=580)

btn_luu = tk.Button(root, text="Lưu", bg="#87cefa", font=("Arial", 12, "bold"), width=10)
btn_luu.place(x=660, y=580)

btn_thoat = tk.Button(root, text="Thoát", bg="#87cefa", font=("Arial", 12, "bold"), width=10, command=root.quit)
btn_thoat.place(x=800, y=580)

root.mainloop()
