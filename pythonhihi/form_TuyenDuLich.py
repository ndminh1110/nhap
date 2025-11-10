import tkinter as tk
from tkinter import ttk, messagebox
import pyodbc

conn = pyodbc.connect(
    'DRIVER={SQL Server};'
    'SERVER=localhost\\SQLEXPRESS01;'  
    'DATABASE=QuanLyTuyenDuLich;'
    'Trusted_Connection=yes;'
)
cursor = conn.cursor()
# ------------------ TẠO BẢNG NẾU CHƯA CÓ ------------------
cursor.execute("""
IF OBJECT_ID('TUYENDULICH', 'U') IS NULL
BEGIN
    CREATE TABLE TUYENDULICH (
        maTuyen NVARCHAR(10) PRIMARY KEY,
        ddDi NVARCHAR(100),
        ddDen NVARCHAR(200)
    )
END
""")
conn.commit()

# ------------------ DANH SÁCH ĐỊA ĐIỂM ------------------
list_di = ["Hà Nội", "Đà Nẵng", "Hồ Chí Minh"]
mien_bac = ["Tràng An-Tam Cốc-Bái Đính-Hoa Lư", "Mộc Châu-Điện Biên-Sapa",
            "Hà Giang-Cao Bằng", "Ninh Bình-Hạ Long-Sapa", "Vịnh Hạ Long-Hạ Long Park-Bãi Cháy-Yên Tử"]
mien_trung = ["Quy Nhơn-Phú Yên", "Pleiku-Kontum- Măng Đen",
              "Hội An-Bà Nà Hills-Núi Thần Tài", "Phan Thiết-Mũi Né", "Quảng Bình-Suối Moọc- Động Thiên Đường"]
mien_nam = ["Tiền Giang-Bến Tre- An Giang-Cần Thơ", "Vũng Tàu", "Phú Quốc", "Tây Ninh"]

# ------------------ KHỞI TẠO GIAO DIỆN ------------------
root = tk.Tk()
root.title("Quản Lý Tuyến Du Lịch")
root.geometry("1000x600")
root.configure(bg="#FFFACD")

tk.Label(root, text="Quản Lý Tuyến Du Lịch", font=("Arial", 20, "bold"), bg="#FFFACD").place(x=330, y=40)

# Treeview
frame = tk.LabelFrame(root, text="Danh sách tuyến du lịch", font=("Arial", 12, "bold"), bg="#FFFACD", width=850, height=280)
frame.place(x=70, y=270)

columns = ("maTuyen", "ddDi", "ddDen")
tree = ttk.Treeview(frame, columns=columns, show="headings", height=12)
tree.heading("maTuyen", text="Mã Tuyến")
tree.heading("ddDi", text="Địa Điểm Đi")
tree.heading("ddDen", text="Địa Điểm Đến")
tree.column("maTuyen", width=150, anchor="center")
tree.column("ddDi", width=150, anchor="center")
tree.column("ddDen", width=400, anchor="center")

scrollbar = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
tree.configure(yscrollcommand=scrollbar.set)
tree.pack(side="left", fill="both", expand=True, padx=10, pady=10)
scrollbar.pack(side="right", fill="y")

# ------------------ HÀM SINH MÃ TUYẾN ------------------

def tao_ma_tuyen_moi():
    """Tự động sinh mã tuyến mới dựa vào cả Treeview và CSDL, lấp khoảng trống."""
    # --- Lấy mã từ Treeview ---
    ma_tree = [tree.item(item)['values'][0].strip() for item in tree.get_children() if tree.item(item)['values']]
    so_tree = [int(ma[2:]) for ma in ma_tree if ma.startswith("TD") and ma[2:].isdigit()]

    # --- Lấy mã từ CSDL ---
    cursor.execute("SELECT maTuyen FROM TUYENDULICH")
    ma_sql = [row[0].strip() for row in cursor.fetchall() if row[0]]
    so_sql = [int(ma[2:]) for ma in ma_sql if ma.startswith("TD") and ma[2:].isdigit()]

    # --- Gộp tất cả và sắp xếp ---
    so_all = sorted(set(so_tree + so_sql))

    # --- Tìm khoảng trống đầu tiên ---
    next_num = 1
    for num in so_all:
        if num == next_num:
            next_num += 1
        elif num > next_num:
            break

    return f"TD{next_num:04d}"


# ------------------ Entry & Combobox ------------------
tk.Label(root, text="Mã Tuyến:", font=("Arial", 12), bg="#FFFACD").place(x=200, y=130)
entry_matuyen = tk.Entry(root, width=50)
entry_matuyen.place(x=350, y=130)
entry_matuyen.insert(0, tao_ma_tuyen_moi())
entry_matuyen.config(state="readonly")

tk.Label(root, text="Địa Điểm Đi:", font=("Arial", 12), bg="#FFFACD").place(x=200, y=170)
entry_ddDi = ttk.Combobox(root, width=48, values=list_di, state="normal")
entry_ddDi.place(x=350, y=170)
entry_ddDi.set("")

tk.Label(root, text="Địa Điểm Đến:", font=("Arial", 12), bg="#FFFACD").place(x=200, y=210)
entry_ddDen = ttk.Combobox(root, width=48, values=[], state="normal")
entry_ddDen.place(x=350, y=210)
entry_ddDen.set("")

# ------------------ Hàm cập nhật gợi ý loại trừ ------------------
def cap_nhat_ddDen(event=None):
    di = entry_ddDi.get()
    if di == "Hà Nội":
        den_list = mien_bac.copy()
    elif di == "Đà Nẵng":
        den_list = mien_trung.copy()
    elif di == "Hồ Chí Minh":
        den_list = mien_nam.copy()
    else:
        den_list = []

    # Loại bỏ tuyến đã có trong CSDL
    cursor.execute("SELECT ddDen FROM TUYENDULICH WHERE ddDi=?", (di,))
    csdl_den = [row[0] for row in cursor.fetchall()]

    # Loại bỏ tuyến đã có trong Treeview
    tree_den = [tree.item(item, "values")[2] for item in tree.get_children() if tree.item(item, "values")[1] == di]

    # Loại bỏ các tuyến trùng
    den_list = [d for d in den_list if d not in csdl_den and d not in tree_den]

    entry_ddDen['values'] = den_list
    entry_ddDen.set("")

entry_ddDi.bind("<<ComboboxSelected>>", cap_nhat_ddDen)

def load_data():
    # Xóa dữ liệu cũ
    for item in tree.get_children():
        tree.delete(item)

    # Lấy dữ liệu từ SQL
    cursor.execute("SELECT maTuyen, ddDi, ddDen FROM TUYENDULICH")
    rows = cursor.fetchall()

    # Chèn từng dòng (lưu ý: không dùng str(row))
    for row in rows:
        # row là tuple ('TD0001', 'Hà Nội', 'Đà Nẵng')
        tree.insert("", "end", values=(row[0].strip(), row[1].strip(), row[2].strip()))

# ------------------ HÀM CHỨC NĂNG ------------------
trang_thai = None

def lam_moi_form():
    entry_ddDi.set("")
    entry_ddDen.set("")
    entry_matuyen.config(state='normal')
    entry_matuyen.delete(0, tk.END)
    entry_matuyen.insert(0, tao_ma_tuyen_moi())
    entry_matuyen.config(state='readonly')



def them_tuyen():
    global trang_thai
    trang_thai = "them"
    ma = tao_ma_tuyen_moi()
    di = entry_ddDi.get()
    den = entry_ddDen.get()
    if not di or not den:
        messagebox.showwarning("Thiếu thông tin", "Vui lòng chọn địa điểm đi và đến")
        return
    tree.insert("", "end", values=(ma, di, den))
    lam_moi_form()

def sua_tuyen():
    global trang_thai
    selected = tree.selection()
    if not selected:
        messagebox.showwarning("Lỗi", "Chưa chọn tuyến để sửa")
        return
    trang_thai = "sua"
    item = selected[0]
    ma, di, den = tree.item(item, "values")
    entry_matuyen.config(state='normal')
    entry_matuyen.delete(0, tk.END)
    entry_matuyen.insert(0, ma)
    entry_matuyen.config(state='readonly')
    entry_ddDi.set(di)
    entry_ddDen.set(den)

def xoa_tuyen():
    selected = tree.selection()
    if not selected:
        messagebox.showwarning("Lỗi", "Chưa chọn tuyến để xóa")
        return
    confirm = messagebox.askyesno("Xác nhận", "Bạn có chắc muốn xóa tuyến này?")
    if confirm:
        for item in selected:
            ma = tree.item(item, "values")[0]  # lấy mã tuyến
            tree.delete(item)
            lam_moi_form()
            # Xóa trong CSDL
         #  cursor.execute("DELETE FROM TUYENDULICH WHERE maTuyen=?", (ma,))
           # conn.commit()
def luu_tuyen():
    try:
        # 1️⃣ Lấy dữ liệu hiện có trong SQL
        cursor.execute("SELECT maTuyen, ddDi, ddDen FROM TUYENDULICH")
        data_sql = cursor.fetchall()
        dict_sql = {row[0]: (row[1], row[2]) for row in data_sql}  # {maTuyen: (ddDi, ddDen)}

        # 2️⃣ Lấy dữ liệu hiện có trên Treeview
        data_tree = {}
        for item in tree.get_children():
            values = tree.item(item, "values")
            if len(values) < 3:
                continue  # ⚠️ Bỏ qua dòng lỗi thiếu dữ liệu
            ma, di, den = values
            if ma and di and den and di != "Chọn địa điểm đi" and den != "Chọn địa điểm đến":
                data_tree[ma] = (di.strip(), den.strip())

        # 3️⃣ Xử lý thêm hoặc cập nhật
        for ma, (di, den) in data_tree.items():
            if ma not in dict_sql:
                # ✅ Tuyến mới → thêm vào SQL
                cursor.execute("""
                    INSERT INTO TUYENDULICH (maTuyen, ddDi, ddDen)
                    VALUES (?, ?, ?)
                """, (ma, di, den))
            else:
                # ✅ Nếu có thay đổi → cập nhật
                di_sql, den_sql = dict_sql[ma]
                if di != di_sql or den != den_sql:
                    cursor.execute("""
                        UPDATE TUYENDULICH
                        SET ddDi = ?, ddDen = ?
                        WHERE maTuyen = ?
                    """, (di, den, ma))

        # 4️⃣ Xử lý xóa (những tuyến không còn trong Treeview)
        for ma in list(dict_sql.keys()):
            if ma not in data_tree:
                cursor.execute("DELETE FROM TUYENDULICH WHERE maTuyen = ?", (ma,))

        # 5️⃣ Lưu thay đổi
        conn.commit()
        messagebox.showinfo("Thành công", "Đã lưu và đồng bộ dữ liệu với CSDL!")
        load_data()

    except Exception as e:
        messagebox.showerror("Lỗi", f"Lưu dữ liệu thất bại!\n{e}")

def huy():
    lam_moi_form()

def thoat():
    root.destroy()

# ------------------ NÚT CHỨC NĂNG ------------------
# ========== Các nút chức năng bên phải ==========
button_style = {"font": ("Times New Roman", 13, "bold"), "bg": "#B0E0E6", "width": 8, "height": 1}

btn_them = tk.Button(root, text="Thêm", **button_style, command=them_tuyen)
btn_them.place(x=870, y=120)

btn_xoa = tk.Button(root, text="Xóa", **button_style, command=xoa_tuyen)
btn_xoa.place(x=870, y=200)

btn_sua = tk.Button(root, text="Sửa", **button_style, command=sua_tuyen)
btn_sua.place(x=870, y=280)

btn_huy = tk.Button(root, text="Hủy", **button_style, command=huy)
btn_huy.place(x=870, y=360)

btn_luu = tk.Button(root, text="Lưu", **button_style, command=luu_tuyen)
btn_luu.place(x=870, y=440)

btn_thoat = tk.Button(root, text="Thoát", **button_style, command=thoat)
btn_thoat.place(x = 870, y=520)
# ------------------ KHỞI TẠO FORM ------------------
lam_moi_form()
load_data()
root.mainloop()
