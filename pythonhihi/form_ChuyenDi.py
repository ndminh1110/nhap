import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
import pyodbc
from datetime import date
import datetime

# ------------------ ROOT ------------------
root = tk.Tk()
root.title("Quản Lý Chuyến Đi")
root.geometry("1000x650")
root.config(bg="#fff8dc")

# ------------------ KẾT NỐI SQL ------------------
conn = pyodbc.connect(
    'DRIVER={SQL Server};'
    'SERVER=localhost\\SQLEXPRESS01;'
    'DATABASE=QuanLyTuyenDuLich;'
    'Trusted_Connection=yes;'
)
cursor = conn.cursor()

# ------------------ HÀM TIỆN ÍCH ------------------
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
    cursor.execute("SELECT maTuyen FROM TUYENDULICH WHERE trangThai = N'Hoạt động'")
    return [row[0] for row in cursor.fetchall()]


# ------------------ HÀM LOAD DỮ LIỆU ------------------
def load_data():
    # Xoá dữ liệu cũ
    for item in tree.get_children():
        tree.delete(item)

    # Lấy tất cả chuyến đi
    cursor.execute("""
    SELECT maCD, maTuyen, ngKh, tgKh, trangThai
    FROM CHUYENDI
    WHERE trangThai = N'Hoạt động'
    ORDER BY maCD
    """)

    chuyen_list = cursor.fetchall()

    for chuyen in chuyen_list:
        maCD, maTuyen, ngKh, tgKh, trangThai = chuyen

        # --- Lấy danh sách nhân viên phụ trách chuyến (chỉ maNV) ---
        cursor.execute("SELECT maNV FROM CHUYENDI_NHANVIEN WHERE maCD=?", (maCD,))
        nv_list = [row[0].strip() for row in cursor.fetchall()]
        nv_str = ", ".join(nv_list)  # nối tất cả NV của chuyến bằng dấu phẩy

        # --- Chuẩn bị dữ liệu hiển thị Treeview ---
        tgKh_display = tgKh[:5] if tgKh else ""
        ngKh_display = ngKh.strftime("%d/%m/%Y") if isinstance(ngKh, datetime.date) else str(ngKh)

        # Chèn vào Treeview
        tree.insert("", "end", values=(maCD, maTuyen, tgKh_display, ngKh_display, nv_str))

def load_nhanvien_ranh_ghep(nv_cua_chuyen=None, ngKh_value=None, current_maCD=None):
    lb_nv.delete(0, tk.END)
    if ngKh_value is None:
        ngKh_value = date_ngKh.get_date()
    ngKh_str = ngKh_value.strftime("%Y-%m-%d")
    if nv_cua_chuyen is None:
        nv_cua_chuyen = []

    # Gom NV bận từ Treeview
    busy_nv = set()
    for item in tree.get_children():
        row = tree.item(item)["values"]
        if len(row) < 5:
            continue
        maCD_row, ngKh_row, nhanVien_row = row[0], row[3], row[4]
        if ngKh_row == ngKh_str and maCD_row != (current_maCD or ""):
            if nhanVien_row:
                busy_nv.update([nv.strip().upper() for nv in nhanVien_row.split(",")])

    # NV đang phân công DB cho chuyến đang sửa
    selected_nv = []
    if current_maCD:
        cursor.execute("SELECT maNV FROM CHUYENDI_NHANVIEN WHERE maCD=?", (current_maCD,))
        selected_nv = [row[0].strip().upper() for row in cursor.fetchall()]

    # Load toàn bộ NV
    cursor.execute("SELECT maNV, hoTen, chucVu FROM NHANVIEN ORDER BY maNV")
    for maNV, hoTen, chucVu in cursor.fetchall():
        maNV_clean = maNV.strip().upper()
        if maNV_clean not in busy_nv or maNV_clean in nv_cua_chuyen or maNV_clean in selected_nv:
            display = f"{maNV_clean} - {hoTen} - {chucVu}"
            lb_nv.insert(tk.END, display)
            if maNV_clean in nv_cua_chuyen or maNV_clean in selected_nv:
                lb_nv.selection_set(tk.END)

# ------------------ HÀM FORM ------------------
def lam_moi_form():
    txt_ma_cd.config(state="normal")
    txt_ma_cd.delete(0, tk.END)
    txt_ma_cd.insert(0, tao_ma_chuyen_di())
    txt_ma_cd.config(state="readonly")
    cb_ma_tuyen.set("Chọn mã tuyến")
    txt_tgkh.delete(0, tk.END)
    date_ngKh.set_date(date.today())
    load_nhanvien_ranh_ghep()

def chon_chuyen_di(event=None):
    sel = tree.selection()
    if not sel: return
    maCD, maTuyen, tgKh, ngKh, nhanVien = tree.item(sel[0])["values"]
    txt_ma_cd.config(state="normal")
    txt_ma_cd.delete(0, tk.END)
    txt_ma_cd.insert(0, maCD)
    txt_ma_cd.config(state="readonly")
    cb_ma_tuyen.set(maTuyen)
    txt_tgkh.delete(0, tk.END)
    txt_tgkh.insert(0, tgKh)
    try:
        date_ngKh.set_date(datetime.datetime.strptime(ngKh, "%Y-%m-%d").date())
    except:
        try:
            date_ngKh.set_date(datetime.datetime.strptime(ngKh, "%d/%m/%Y").date())
        except:
            date_ngKh.set_date(date.today())
    nv_cua_chuyen = [nv.strip() for nv in nhanVien.split(",")] if nhanVien else []
    load_nhanvien_ranh_ghep(nv_cua_chuyen=nv_cua_chuyen, ngKh_value=date_ngKh.get_date(), current_maCD=maCD)

# ------------------ HÀM THÊM/SỬA/XÓA ------------------
def them_chuyen_di():
    maCD = txt_ma_cd.get()
    maTuyen = cb_ma_tuyen.get()
    tgKh_value = txt_tgkh.get()
    ngKh_value = date_ngKh.get_date()
    selected_nv = [lb_nv.get(i).split(" - ")[0].strip() for i in lb_nv.curselection()]

    if maTuyen=="Chọn mã tuyến" or not selected_nv or not tgKh_value:
        messagebox.showwarning("Thiếu dữ liệu", "Vui lòng nhập đầy đủ dữ liệu")
        return

    try:
        tgKh_str = datetime.datetime.strptime(tgKh_value, "%H:%M").strftime("%H:%M")
    except:
        messagebox.showerror("Lỗi", "Thời gian phải HH:MM")
        return

    cursor.execute("SELECT 1 FROM CHUYENDI WHERE maCD=?", (maCD,))
    if cursor.fetchone():
        messagebox.showerror("Lỗi", "Mã chuyến đi đã tồn tại")
        return

    ngKh_str = ngKh_value.strftime("%Y-%m-%d")
    cursor.execute("INSERT INTO CHUYENDI(maCD, maTuyen, ngKh, tgKh, trangThai) VALUES (?, ?, ?, ?, N'Hoạt động')",
                   (maCD, maTuyen, ngKh_str, tgKh_str))
    for maNV in selected_nv:
        cursor.execute("INSERT INTO CHUYENDI_NHANVIEN(maCD, maNV) VALUES (?, ?)", (maCD, maNV))
    conn.commit()
    messagebox.showinfo("Thành công", "Thêm chuyến đi thành công")
    load_data()
    lam_moi_form()

def sua_chuyen_di():
    maCD = txt_ma_cd.get()
    maTuyen = cb_ma_tuyen.get()
    tgKh_value = txt_tgkh.get()
    ngKh_value = date_ngKh.get_date()
    selected_nv = [lb_nv.get(i).split(" - ")[0].strip() for i in lb_nv.curselection()]

    if not maCD or maTuyen=="Chọn mã tuyến" or not tgKh_value:
        messagebox.showwarning("Thiếu dữ liệu", "Vui lòng nhập đầy đủ dữ liệu")
        return

    try:
        tgKh_str = datetime.datetime.strptime(tgKh_value, "%H:%M").strftime("%H:%M")
    except:
        messagebox.showerror("Lỗi", "Thời gian phải HH:MM")
        return

    ngKh_str = ngKh_value.strftime("%Y-%m-%d")
    cursor.execute("UPDATE CHUYENDI SET maTuyen=?, ngKh=?, tgKh=?, trangThai=N'Hoạt động' WHERE maCD=?",
                   (maTuyen, ngKh_str, tgKh_str, maCD))
    cursor.execute("DELETE FROM CHUYENDI_NHANVIEN WHERE maCD=?", (maCD,))
    for maNV in selected_nv:
        cursor.execute("INSERT INTO CHUYENDI_NHANVIEN(maCD, maNV) VALUES (?, ?)", (maCD, maNV))
    conn.commit()
    messagebox.showinfo("Thành công", "Cập nhật chuyến đi thành công")
    load_data()
    lam_moi_form()

def xoa_chuyen_di():
    sel = tree.selection()
    if not sel:
        messagebox.showwarning("Lỗi", "Chưa chọn chuyến đi")
        return
    for item in sel:
        maCD = tree.item(item)["values"][0]
        cursor.execute("UPDATE CHUYENDI SET trangThai=N'Ngưng hoạt động' WHERE maCD=?", (maCD,))
    conn.commit()
    messagebox.showinfo("Thành công", "Xóa chuyến đi thành công")
    load_data()
    lam_moi_form()


def luu_chuyen_di():
    confirm = messagebox.askyesno("Xác nhận", "Bạn có chắc muốn lưu dữ liệu Treeview vào CSDL?")
    if not confirm:
        return

    # --- 1) Lấy danh sách tất cả mã chuyến từ Treeview ---
    ds_tree = []
    chuyen_di_nv = {}  # dict lưu maCD -> list maNV
    for item in tree.get_children():
        values = tree.item(item, "values")
        if len(values) < 5:  # đảm bảo đủ dữ liệu
            continue
        maCD, maTuyen, tgKh_value, ngKh_value, nhanVien_str = values[:5]

        ds_tree.append(maCD)

        # --- Lấy danh sách NV phụ trách chuyến này ---
        # Giả sử nhanVien_str dạng "NV01 - Mai, NV02 - Phuong"
        nv_list = []
        if nhanVien_str:
            for nv in nhanVien_str.split(","):
                nv_list.append(nv.strip().split(" - ")[0])
        chuyen_di_nv[maCD] = nv_list

    # --- 2) Cập nhật trạng thái chuyến KHÔNG có trong Treeview ---
    if ds_tree:
        placeholders = ",".join("?" for _ in ds_tree)
        sql_update_off = f"""
            UPDATE CHUYENDI
            SET trangThai = N'Ngưng hoạt động'
            WHERE maCD NOT IN ({placeholders})
        """
        cursor.execute(sql_update_off, ds_tree)
    else:
        # Nếu Treeview rỗng → tất cả chuyến đi ngưng hoạt động
        cursor.execute("UPDATE CHUYENDI SET trangThai = N'Ngưng hoạt động'")

    # --- 3) Cập nhật hoặc thêm mới từng chuyến ---
    for item in tree.get_children():
        maCD, maTuyen, tgKh_value, ngKh_value, _ = tree.item(item, "values")[:5]

        # Chuyển ngày
        try:
            ngKh_date = datetime.datetime.strptime(str(ngKh_value), "%Y-%m-%d").date()
        except:
            ngKh_date = datetime.datetime.strptime(str(ngKh_value), "%d/%m/%Y").date()
        ngKh_str = ngKh_date.strftime("%Y-%m-%d")

        # Giờ KH dạng HH:MM
        tgKh_str = tgKh_value[:5] if tgKh_value else ""

        # --- Kiểm tra chuyến đi đã tồn tại chưa ---
        cursor.execute("SELECT COUNT(*) FROM CHUYENDI WHERE maCD=?", (maCD,))
        exists = cursor.fetchone()[0]

        if exists:
            # --- Cập nhật chuyến đi ---
            cursor.execute("""
                UPDATE CHUYENDI
                SET maTuyen=?, ngKh=?, tgKh=?, trangThai=N'Hoạt động'
                WHERE maCD=?
            """, (maTuyen, ngKh_str, tgKh_str, maCD))

            # Xoá NV cũ để thêm lại
            cursor.execute("DELETE FROM CHUYENDI_NHANVIEN WHERE maCD=?", (maCD,))
        else:
            # --- Thêm mới ---
            cursor.execute("""
                INSERT INTO CHUYENDI(maCD, maTuyen, ngKh, tgKh, trangThai)
                VALUES (?, ?, ?, ?, N'Hoạt động')
            """, (maCD, maTuyen, ngKh_str, tgKh_str))

        # --- Thêm nhân viên phụ trách ---
        for maNV in chuyen_di_nv.get(maCD, []):
            cursor.execute(
                "INSERT INTO CHUYENDI_NHANVIEN(maCD, maNV) VALUES (?, ?)",
                (maCD, maNV)
            )

    conn.commit()
    messagebox.showinfo("Thành công", "Đã lưu dữ liệu!")


# ------------------ GIAO DIỆN ------------------
tk.Label(root, text="Quản Lý Chuyến Đi", font=("Arial", 20, "bold"), bg="#fff8dc").place(x=380, y=30)

tk.Label(root, text="Mã Chuyến Đi", font=("Arial", 12), bg="#fff8dc").place(x=120, y=100)
txt_ma_cd = tk.Entry(root, width=20)
txt_ma_cd.place(x=300, y=100)
txt_ma_cd.insert(0, tao_ma_chuyen_di())
txt_ma_cd.config(state="readonly")

tk.Label(root, text="Mã Tuyến", font=("Arial", 12), bg="#fff8dc").place(x=120, y=130)
cb_ma_tuyen = ttk.Combobox(root, width=20, state="readonly", values=lay_ds_ma_tuyen())
cb_ma_tuyen.place(x=300, y=130)
cb_ma_tuyen.set("Chọn mã tuyến")

tk.Label(root, text="Ngày Khởi Hành", font=("Arial", 12), bg="#fff8dc").place(x=120, y=160)
date_ngKh = DateEntry(root, width=20, background='darkblue', foreground='white', borderwidth=2, date_pattern='dd/mm/yyyy')
date_ngKh.place(x=300, y=160)
date_ngKh.set_date(date.today())

tk.Label(root, text="Thời Gian Khởi Hành", font=("Arial", 12), bg="#fff8dc").place(x=120, y=190)
txt_tgkh = tk.Entry(root, width=20)
txt_tgkh.place(x=300, y=190)

tk.Label(root, text="Nhân Viên Phụ Trách", font=("Arial", 12), bg="#fff8dc").place(x=510, y=100)
lb_nv = tk.Listbox(root, selectmode="multiple", height=7)
lb_nv.place(x=680, y=100, width=300)
date_ngKh.bind("<<DateEntrySelected>>", lambda e: load_nhanvien_ranh_ghep(ngKh_value=date_ngKh.get_date()))

# Treeview
frame_tree = tk.LabelFrame(root, text="Danh Sách Chuyến Đi", font=("Arial", 12, "bold"), bg="#fff8dc", width=880, height=350)
frame_tree.place(x=60, y=300)
columns = ("maCD", "maTuyen", "tgKh", "ngKh", "nhanVien")
tree = ttk.Treeview(frame_tree, columns=columns, show="headings", height=10)
for col, txt, w in zip(columns, ["Mã Chuyến Đi","Mã Tuyến","Thời Gian KH","Ngày KH","Nhân Viên"], [90,90,110,120,300]):
    tree.heading(col, text=txt)
    tree.column(col, width=w, anchor=tk.W if col=="nhanVien" else tk.CENTER)
tree.place(x=10, y=10, width=840, height=300)
scrollbar_v = ttk.Scrollbar(frame_tree, orient="vertical", command=tree.yview)
tree.configure(yscrollcommand=scrollbar_v.set)
scrollbar_v.place(x=855, y=10, height=300)
tree.bind("<<TreeviewSelect>>", chon_chuyen_di)

# ------------------ NÚT CHỨC NĂNG ------------------
btn_them = tk.Button(root, text="Thêm", bg="#87cefa", font=("Arial", 12, "bold"), width=10, command=them_chuyen_di)
btn_them.place(x=100, y=250)
btn_sua = tk.Button(root, text="Sửa", bg="#87cefa", font=("Arial", 12, "bold"), width=10, command=sua_chuyen_di)
btn_sua.place(x=240, y=250)
btn_xoa = tk.Button(root, text="Xóa", bg="#87cefa", font=("Arial", 12, "bold"), width=10, command=xoa_chuyen_di)
btn_xoa.place(x=380, y=250)
btn_huy = tk.Button(root, text="Hủy", bg="#87cefa", font=("Arial", 12, "bold"), width=10, command=lam_moi_form)
btn_huy.place(x=520, y=250)
btn_luu = tk.Button(root, text="Lưu", bg="#87cefa", font=("Arial", 12, "bold"), width=10, command=luu_chuyen_di)
btn_luu.place(x=660, y=250)
btn_thoat = tk.Button(root, text="Thoát", bg="#87cefa", font=("Arial", 12, "bold"), width=10, command=root.destroy)
btn_thoat.place(x=800, y=250)

# ------------------ CHẠY ------------------
load_data()
root.mainloop()
