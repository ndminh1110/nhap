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

# ------------------ HÀM ------------------
def load_data():
    for i in tree.get_children():
        tree.delete(i)
    cursor.execute("SELECT maNV, hoTen, chucVu, sdt, phai, ngsinh, dchi, luong FROM NHANVIEN")
    rows = cursor.fetchall()
    for row in rows:
        tree.insert("", "end", values=(
            row[0].strip(), row[1].strip(), row[2] if row[2] else "", row[3], row[4],
            row[5], row[6] if row[6] else "", row[7] if row[7] else 0
        ))

def auto_maNV():
    ma_list = [tree.item(item)['values'][0].strip() for item in tree.get_children()]
    if not ma_list:
        return "NV0001"
    so_list = sorted([int(ma[2:]) for ma in ma_list if ma[2:].isdigit()])
    next_num = 1
    for num in so_list:
        if num == next_num:
            next_num += 1
        elif num > next_num:
            break
    return f"NV{next_num:04d}"

def lam_moi_form():
    entry_maNV.config(state='normal')
    entry_maNV.delete(0, tk.END)
    entry_maNV.insert(0, auto_maNV())
    entry_maNV.config(state='readonly')

    entry_ten.delete(0, tk.END)
    entry_chucvu.delete(0, tk.END)
    entry_sdt.delete(0, tk.END)
    entry_diachi.delete(0, tk.END)
    entry_luong.delete(0, tk.END)

    gender.set("Nam")
    date_ngaysinh.set_date(date.today())

def them():
    lam_moi_form()
    entry_ten.focus()

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
    ten = entry_ten.get().strip()
    chucvu = entry_chucvu.get().strip()
    sdt = entry_sdt.get().strip()
    gioi_tinh = gender.get()
    ngsinh = date_ngaysinh.get_date().strftime('%Y-%m-%d')
    dchi = entry_diachi.get().strip()
    try:
        luong_val = float(entry_luong.get())
        if luong_val < 0:
            raise ValueError
    except:
        messagebox.showerror("Lỗi", "Lương phải là số dương hợp lệ!")
        return

    if not ten or not sdt:
        messagebox.showwarning("Thiếu dữ liệu", "Vui lòng nhập đầy đủ thông tin!")
        return
    if not (sdt.isdigit() and len(sdt) == 10 and sdt.startswith("0")):
        messagebox.showerror("Lỗi", "Số điện thoại phải bắt đầu bằng 0 và đủ 10 số!")
        return

    cursor.execute(
        "UPDATE NHANVIEN SET hoTen=?, chucVu=?, sdt=?, phai=?, ngsinh=?, dchi=?, luong=? WHERE maNV=?",
        (ten, chucvu, sdt, gioi_tinh, ngsinh, dchi, luong_val, ma)
    )
    conn.commit()
    messagebox.showinfo("Thành công", "Đã cập nhật thông tin nhân viên!")
    load_data()
    lam_moi_form()

def hien_thi_chi_tiet(event):
    selected = tree.selection()
    if selected:
        ma, ten, chucvu, sdt_val, phai_val, ngsinh_val, dchi_val, luong_val = tree.item(selected[0], "values")
        entry_maNV.config(state='normal')
        entry_maNV.delete(0, tk.END)
        entry_maNV.insert(0, ma)
        entry_maNV.config(state='readonly')

        entry_ten.delete(0, tk.END)
        entry_ten.insert(0, ten)

        entry_chucvu.delete(0, tk.END)
        entry_chucvu.insert(0, chucvu)

        entry_sdt.delete(0, tk.END)
        entry_sdt.insert(0, sdt_val)

        gender.set(phai_val)

        if isinstance(ngsinh_val, str) and ngsinh_val:
            year, month, day = map(int, ngsinh_val.split('-'))
            date_ngaysinh.set_date(date(year, month, day))
        else:
            date_ngaysinh.set_date(date.today())

        entry_diachi.delete(0, tk.END)
        entry_diachi.insert(0, dchi_val)

        entry_luong.delete(0, tk.END)
        entry_luong.insert(0, luong_val)

def huy():
    lam_moi_form()

def luu():
    for item in tree.get_children():
        maNV, hoTen, chucvu, sdt_val, phai_val, ngsinh_val, dchi_val, luong_val = tree.item(item, "values")
        # Kiểm tra dữ liệu hợp lệ
        if not (sdt_val.isdigit() and len(sdt_val) == 10 and sdt_val.startswith("0")):
            messagebox.showwarning("Bỏ qua", f"SĐT {sdt_val} của {hoTen} không hợp lệ, không lưu vào CSDL!")
            continue
        try:
            luong_val = float(luong_val)
            if luong_val < 0:
                raise ValueError
        except:
            messagebox.showwarning("Bỏ qua", f"Lương của {hoTen} không hợp lệ, không lưu!")
            continue
        cursor.execute("SELECT 1 FROM NHANVIEN WHERE maNV=?", (maNV,))
        if not cursor.fetchone():
            cursor.execute(
                "INSERT INTO NHANVIEN (maNV, hoTen, chucVu, sdt, phai, ngsinh, dchi, luong) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                (maNV, hoTen, chucvu, sdt_val, phai_val, ngsinh_val, dchi_val, luong_val)
            )
    conn.commit()
    messagebox.showinfo("Thành công", "Đã lưu dữ liệu vào CSDL!")
    load_data()
    lam_moi_form()

def thoat():
    conn.close()
    root.destroy()

# ------------------ GIAO DIỆN ------------------
root = tk.Tk()
root.title("Quản Lý Nhân Viên")
root.geometry("1100x650")
root.configure(bg="#FFFACD")

# Tiêu đề
tk.Label(root, text="Quản Lý Nhân Viên", bg="#FFFACD", fg="black", font=("Times New Roman", 22, "bold")).place(x=380, y=20)

# Form nhập liệu
frame_input = tk.Frame(root, bg="#FFFACD", width=1050, height=150)
frame_input.place(x=25, y=70)

tk.Label(frame_input, text="Mã NV", bg="#FFFACD").place(x=10, y=10)
entry_maNV = tk.Entry(frame_input, width=10)
entry_maNV.place(x=100, y=10)
entry_maNV.config(state='readonly')

tk.Label(frame_input, text="Họ Tên", bg="#FFFACD").place(x=200, y=10)
entry_ten = tk.Entry(frame_input, width=30)
entry_ten.place(x=280, y=10)

tk.Label(frame_input, text="Chức Vụ", bg="#FFFACD").place(x=520, y=10)
entry_chucvu = tk.Entry(frame_input, width=20)
entry_chucvu.place(x=600, y=10)

tk.Label(frame_input, text="Giới Tính", bg="#FFFACD").place(x=10, y=50)
gender = tk.StringVar(value="Nam")
tk.Radiobutton(frame_input, text="Nam", variable=gender, value="Nam", bg="#FFFACD").place(x=70, y=48)
tk.Radiobutton(frame_input, text="Nữ", variable=gender, value="Nữ", bg="#FFFACD").place(x=130, y=48)

tk.Label(frame_input, text="Ngày Sinh", bg="#FFFACD").place(x=200, y=50)
date_ngaysinh = DateEntry(frame_input, width=12, background='darkblue', foreground='white', borderwidth=2, date_pattern='dd/mm/yyyy')
date_ngaysinh.place(x=280, y=50)

tk.Label(frame_input, text="SĐT", bg="#FFFACD").place(x=400, y=50)
entry_sdt = tk.Entry(frame_input, width=20)
entry_sdt.place(x=450, y=50)

tk.Label(frame_input, text="Địa Chỉ", bg="#FFFACD").place(x=10, y=90)
entry_diachi = tk.Entry(frame_input, width=50)
entry_diachi.place(x=100, y=90)

tk.Label(frame_input, text="Lương", bg="#FFFACD").place(x=520, y=90)
entry_luong = tk.Entry(frame_input, width=20)
entry_luong.place(x=600, y=90)

# Treeview + Scrollbar
frame_tree = tk.LabelFrame(root, text="Danh sách nhân viên", font=("Times New Roman", 12), bg="#fff8dc", width=1050, height=400)
frame_tree.place(x=25, y=230)

columns = ("maNV", "hoTen", "chucVu", "sdt", "phai", "ngsinh", "dchi", "luong")
tree = ttk.Treeview(frame_tree, columns=columns, show="headings")
for col in columns:
    tree.heading(col, text=col)
tree.column("maNV", width=80, anchor="center")
tree.column("hoTen", width=150)
tree.column("chucVu", width=100)
tree.column("sdt", width=120, anchor="center")
tree.column("phai", width=80, anchor="center")
tree.column("ngsinh", width=100, anchor="center")
tree.column("dchi", width=200)
tree.column("luong", width=100, anchor="center")

scrollbar_v = ttk.Scrollbar(frame_tree, orient="vertical", command=tree.yview)
scrollbar_h = ttk.Scrollbar(frame_tree, orient="horizontal", command=tree.xview)
tree.configure(yscrollcommand=scrollbar_v.set, xscrollcommand=scrollbar_h.set)
tree.place(x=10, y=10, width=1020, height=340)
scrollbar_v.place(x=1030, y=10, width=20, height=340)
scrollbar_h.place(x=10, y=350, width=1020, height=20)

# Bind chọn dòng Treeview
tree.bind("<<TreeviewSelect>>", hien_thi_chi_tiet)

# Nút chức năng
button_style = {"font": ("Times New Roman", 13, "bold"), "bg": "#B0E0E6", "width": 8, "height": 1}
tk.Button(root, text="Thêm", **button_style, command=them).place(x=870, y=120)
tk.Button(root, text="Xóa", **button_style, command=xoa).place(x=870, y=200)
tk.Button(root, text="Sửa", **button_style, command=sua).place(x=870, y=280)
tk.Button(root, text="Hủy", **button_style, command=huy).place(x=870, y=360)
tk.Button(root, text="Lưu", **button_style, command=luu).place(x=870, y=440)
tk.Button(root, text="Thoát", **button_style, command=thoat).place(x=870, y=520)

# Load dữ liệu và thiết lập form lúc đầu
load_data()
lam_moi_form()

root.mainloop()
