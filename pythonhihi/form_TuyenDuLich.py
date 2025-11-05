import tkinter as tk
from tkinter import ttk, messagebox
import pyodbc
#moi nhatttttt

root = tk.Tk()
root.title("Quản Lý Tuyến Du Lịch")
root.geometry("1000x650")
root.configure(bg="#FFFACD")

# ------------------ KẾT NỐI SQL SERVER ------------------
conn = pyodbc.connect(
    'DRIVER={SQL Server};'
    'SERVER=localhost\\SQLEXPRESS01;'  
    'DATABASE=QuanLyTuyenDuLich;'
    'Trusted_Connection=yes;'
)
cursor = conn.cursor()

# ------------------ HÀM SINH MÃ TỰ ĐỘNG ------------------
def tao_ma_tuyen_tu_dong():
    cursor.execute("SELECT MAX(maTuyen) FROM TUYENDULICH")
    result = cursor.fetchone()[0]
    if result is None:
        return "T0001"
    so = int(result[1:]) + 1
    return f"T{so:04d}"

# ------------------ HÀM HIỂN THỊ DỮ LIỆU ------------------
def hien_thi_du_lieu():
    for row in tree.get_children():
        tree.delete(row)
    cursor.execute("SELECT * FROM TUYENDULICH")
    for row in cursor.fetchall():
        tree.insert("", "end", values=row)

# ------------------ HÀM LÀM MỚI FORM ------------------
def lam_moi_form():
    entry_ddDi.set("Chọn địa điểm đi")
    entry_ddDen.set("Chọn địa điểm đến")
    entry_matuyen.config(state='normal')
    entry_matuyen.delete(0, tk.END)
    entry_matuyen.insert(0, tao_ma_tuyen_tu_dong())
    entry_matuyen.config(state='readonly')

# ------------------ CÁC HÀM XỬ LÝ ------------------
trang_thai = None

def them_tuyen():
    global trang_thai
    trang_thai = "them"
    ma = entry_matuyen.get().strip()
    di = entry_ddDi.get()
    den = entry_ddDen.get()

    if not ma or di == "Chọn địa điểm đi" or den == "Chọn địa điểm đến":
        messagebox.showwarning("Thiếu thông tin", "Vui lòng nhập đủ dữ liệu!")
        return


    # ====== Thêm dữ liệu vào Treeview ======
    tree.insert("", "end", values=(ma, di, den))

    # Xóa dữ liệu trong ô nhập để tiện thêm mới
    entry_matuyen.delete(0, tk.END)
    entry_ddDi.set("Chọn địa điểm đi")
    entry_ddDen.set("Chọn địa điểm đến")

def sua_tuyen():
    global trang_thai
    trang_thai = "sua"
    messagebox.showinfo("Sửa", "Chế độ chỉnh sửa đã bật! Hãy nhập mã tuyến cần sửa.")

def xoa_tuyen():
    maTuyen = entry_matuyen.get()
    if not maTuyen:
        messagebox.showwarning("Thiếu dữ liệu", "Vui lòng nhập mã tuyến cần xóa!")
        return
    try:
        cursor.execute("DELETE FROM TUYENDULICH WHERE maTuyen=?", (maTuyen,))
        conn.commit()
        messagebox.showinfo("Thành công", f"Đã xóa tuyến {maTuyen}!")
        hien_thi_du_lieu()
        lam_moi_form()
    except Exception as e:
        messagebox.showerror("Lỗi", f"Không thể xóa tuyến!\n{e}")

def huy_thao_tac():
    global trang_thai
    trang_thai = None
    lam_moi_form()
    messagebox.showinfo("Hủy", "Đã hủy thao tác hiện tại.")

def luu_tuyen():
    global trang_thai
    maTuyen = entry_matuyen.get()
    ddDi = entry_ddDi.get()
    ddDen = entry_ddDen.get()

    if ddDi == "Chọn địa điểm đi" or ddDen == "Chọn địa điểm đến":
        messagebox.showwarning("Thiếu thông tin", "Vui lòng chọn đầy đủ địa điểm đi và đến!")
        return

    try:
        if trang_thai == "them":
            cursor.execute("INSERT INTO TUYENDULICH (maTuyen, ddDi, ddDen) VALUES (?, ?, ?)", (maTuyen, ddDi, ddDen))
            conn.commit()
            messagebox.showinfo("Thành công", f"Đã thêm tuyến {maTuyen}!")
        elif trang_thai == "sua":
            cursor.execute("UPDATE TUYENDULICH SET ddDi=?, ddDen=? WHERE maTuyen=?", (ddDi, ddDen, maTuyen))
            conn.commit()
            messagebox.showinfo("Thành công", f"Đã cập nhật tuyến {maTuyen}!")
        else:
            messagebox.showwarning("Chưa chọn thao tác", "Hãy chọn Thêm hoặc Sửa trước khi lưu!")
            return
        hien_thi_du_lieu()
        lam_moi_form()
        trang_thai = None
    except Exception as e:
        messagebox.showerror("Lỗi", f"Không thể lưu!\n{e}")

def thoat():
    root.destroy()
def home():
    root.destroy()


# ------------------ GIAO DIỆN ------------------
tk.Label(root, text="Quản Lý Tuyến Du Lịch", font=("Arial", 20, "bold"), bg="#fff8dc").place(x=370, y=45)
# === KHUNG DANH SÁCH TUYẾN DU LỊCH ===
frame_info = tk.LabelFrame(root, text="Danh sách tuyến du lịch", font=("Arial", 12, "bold"), bg="#fff8dc", width=750, height=280)
frame_info.place(x=120, y=300)
# Định nghĩa các cột
columns = ("maTuyen", "ddDi", "ddDen")
tree = ttk.Treeview(frame_info, columns=columns, show="headings", height=10)
# Cấu hình tiêu đề cột
tree.heading("maTuyen", text="Mã Tuyến", anchor = 'center')
tree.heading("ddDi", text="Địa Điểm Đi",anchor = 'center')
tree.heading("ddDen", text="Địa Điểm Đến", anchor = 'center')
# Cấu hình độ rộng và căn giữa từng cột
tree.column("maTuyen", width=120, anchor="center")
tree.column("ddDi", width=250, anchor="center")
tree.column("ddDen", width=250, anchor="center")
# Thêm thanh cuộn dọc
scrollbar = ttk.Scrollbar(frame_info, orient="vertical", command=tree.yview)
tree.configure(yscroll=scrollbar.set)
scrollbar.pack(side="right", fill="y")
# Hiển thị bảng
tree.pack(fill="both", expand=True)
tree.place(relx=0.5, rely=0.5, anchor="center", width=720, height=240)



# combo box
mien_bac = ["Tràng An-Tam Cốc-Bái Đính-Hoa Lư", "Mộc Châu-Điện Biên-Sapa", "Hà Giang-Cao Bằng", "Ninh Bình-Hạ Long-Sapa", "Vịnh Hạ Long-Hạ Long Park-Bãi Cháy-Yên Tử"]
mien_trung = ["Quy Nhơn-Phú Yên", "Pleiku-Kontum- Măng Đen", "Hội An-Bà Nà Hills-Núi Thần Tài", "Phan Thiết-Mũi Né", "Quảng Bình-Suối Moọc- Động Thiên Đường"]
mien_nam = ["Tiền Giang-Bến Tre- An GIang-Cần Thơ", "Vũng Tàu", "Phú Quốc", "Tây Ninh"]
# Cập nhật địa điểm:
def cap_nhat_dia_diem_den(event):
    di = entry_ddDi.get()
    if di == "Hồ Chí Minh":
        entry_ddDen["values"] = mien_nam
    elif di == "Hà Nội":
        entry_ddDen["values"] = mien_bac
    elif di == "Đà Nẵng":
        entry_ddDen["values"] = mien_trung
    else:
        entry_ddDen["values"] = []
    entry_ddDen.set("Chọn địa điểm đến")
# Địa điểm đi
tk.Label(root, text="Địa Điểm Đi", font=("Arial", 12), bg="#fff8dc").place(x=200, y=150)
list_di = ["Hồ Chí Minh", "Hà Nội", "Đà Nẵng"]
entry_ddDi = ttk.Combobox(root, width=50, state="readonly", values=list_di)
entry_ddDi.place(x=380, y=150)
entry_ddDi.set("Chọn địa điểm đi")
entry_ddDi.bind("<<ComboboxSelected>>", cap_nhat_dia_diem_den)

# Địa điểm đến
tk.Label(root, text="Địa Điểm Đến", font=("Arial", 12), bg="#fff8dc").place(x=200, y=190)
entry_ddDen = ttk.Combobox(root, width=37, state="readonly")
entry_ddDen.place(x=380, y=190)
entry_ddDen.set("Chọn địa điểm đến")

# Mã tuyến
tk.Label(root, text="Mã Tuyến", font=("Arial", 12), bg="#fff8dc").place(x=200, y=230)
entry_matuyen = tk.Entry(root, width=50)
entry_matuyen.place(x=380, y=230)
entry_matuyen.insert(0, tao_ma_tuyen_tu_dong())
entry_matuyen.config(state='readonly')

# Khung thông tin
frame_info = tk.LabelFrame(root, text="Danh sách tuyến du lịch", font=("Arial", 12, "bold"), bg="#fff8dc", width=750, height=280)
frame_info.place(x=50, y=270)

columns = ("maTuyen", "ddDi", "ddDen")
tree = ttk.Treeview(frame_info, columns=columns, show="headings", height=10)
tree.heading("maTuyen", text="Mã Tuyến")
tree.heading("ddDi", text="Địa Điểm Đi")
tree.heading("ddDen", text="Địa Điểm Đến")
tree.place(x=10, y=10, width=725, height=240)

# Nút chức năng
btn_them = tk.Button(root, text="Thêm", bg="#87cefa", font=("Arial", 12, "bold"), width=10, command=them_tuyen)
btn_them.place(x=850, y=120)

btn_xoa = tk.Button(root, text="Xóa", bg="#87cefa", font=("Arial", 12, "bold"), width=10, command=xoa_tuyen)
btn_xoa.place(x=850, y=200)

btn_sua = tk.Button(root, text="Sửa", bg="#87cefa", font=("Arial", 12, "bold"), width=10, command=sua_tuyen)
btn_sua.place(x=850, y=280)

btn_huy = tk.Button(root, text="Hủy", bg="#87cefa", font=("Arial", 12, "bold"), width=10, command=huy_thao_tac)
btn_huy.place(x=850, y=360)

btn_luu = tk.Button(root, text="Lưu", bg="#87cefa", font=("Arial", 12, "bold"), width=10, command=luu_tuyen)
btn_luu.place(x=850, y=420)

btn_thoat = tk.Button(root, text="Thoát", bg="#87cefa", font=("Arial", 12, "bold"), width=10, command=thoat)
btn_thoat.place(x=850, y=500)

btn_home = tk.Button(root, text="Về Trang Chủ", font=("Arial", 10, "bold"), bg="white", relief="groove", command=home)
btn_home.place(x=50, y=30)

# Hiển thị dữ liệu khi mở form
hien_thi_du_lieu()

root.mainloop()