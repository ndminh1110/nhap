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

# ------------------ HÀM LỌC DOANH THU ------------------
def chon_quy():
    month.set(0)

def chon_thang():
    quarter.set(0)

def xem_doanh_thu():
    for row in tree.get_children():
        tree.delete(row)

    try:
        nam = int(entry_year.get())
    except:
        messagebox.showwarning("Lỗi", "Vui lòng nhập năm hợp lệ!")
        return

    thang_chon = month.get()
    quy_chon = quarter.get()
    tong_tien = 0

    # Truy vấn dữ liệu dựa trên ngày khởi hành ngKh
    query = """
        SELECT D.maCD, D.giaVe, D.soLuong, D.tongTien, C.ngKh
        FROM DOANHTHU D
        JOIN CHUYENDI C ON D.maCD = C.maCD
        WHERE YEAR(C.ngKh) = ?
    """
    params = [nam]

    if quy_chon != 0:
        query += " AND DATEPART(QUARTER, C.ngKh) = ?"
        params.append(quy_chon)
    elif thang_chon != 0:
        query += " AND MONTH(C.ngKh) = ?"
        params.append(thang_chon)

    cursor.execute(query, params)
    rows = cursor.fetchall()

    for row in rows:
        maCD, giaVe, soLuong, tongTienCD, ngKh = row
        tree.insert("", "end", values=(maCD, f"{giaVe:,.0f}", soLuong, f"{tongTienCD:,.0f}", ngKh.strftime("%d/%m/%Y")))
        tong_tien += tongTienCD or 0

    lbl_tong.config(text=f"Tổng doanh thu: {tong_tien:,.0f} VND")

# ------------------ GIAO DIỆN ------------------
root = tk.Tk()
root.title("Quản Lý Doanh Thu")
root.geometry("1000x650")
root.configure(bg="#FFFACD")

def ve_trang_chu():
    root.destroy()

# Nút về trang chủ
btn_home = tk.Button(root, text="Về Trang Chủ", font=("Times New Roman", 10, "bold"),
                     bg="white", relief="groove", command=ve_trang_chu)
btn_home.place(x=50, y=40)

# Tiêu đề
tk.Label(root, text="Quản Lý Doanh Thu", font=("Times New Roman", 24, "bold"), bg="#FFFACD").place(x=440, y=35)

# Quý
tk.Label(root, text="Quý", font=("Times New Roman", 12), bg="#FFFACD").place(x=160, y=120)
quarter = tk.IntVar(value=0)
for i in range(1, 5):
    tk.Radiobutton(root, text=str(i), variable=quarter, value=i, bg="#FFFACD",
                   font=("Times New Roman", 12), command=chon_quy).place(x=220+(i-1)*150, y=120)

# Tháng
tk.Label(root, text="Tháng", font=("Times New Roman", 12), bg="#FFFACD").place(x=160, y=170)
month = tk.IntVar(value=0)
for i in range(12):
    tk.Radiobutton(root, text=str(i+1), variable=month, value=i+1, bg="#FFFACD",
                   font=("Times New Roman", 12), command=chon_thang).place(x=220+(i%4)*150, y=170+(i//4)*30)

# Năm
tk.Label(root, text="Năm", font=("Times New Roman", 12), bg="#FFFACD").place(x=160, y=280)
entry_year = tk.Entry(root, width=30)
entry_year.place(x=220, y=280)

# Nút xem
tk.Button(root, text="Xem", font=("Times New Roman", 14, "bold"),
          bg="skyblue", width=10, command=xem_doanh_thu).place(x=780, y=170)

# Treeview
frame_info = tk.LabelFrame(root, text="Thông tin doanh thu", font=("Times New Roman", 12, "bold"), bg="#FFFACD")
frame_info.place(x=50, y=350, width=900, height=250)

columns = ("maCD", "giaVe", "soLuong", "tongTien", "ngKh")
tree = ttk.Treeview(frame_info, columns=columns, show="headings", height=10)
# ngày lập = ngày khởi hành ( của chuyến đi nho )
for col, txt in zip(columns, ["Mã Chuyến", "Giá Vé", "Số Lượng", "Tổng Tiền", "Ngày Lập"]):
    tree.heading(col, text=txt)
    tree.column(col, anchor="center", width=150)
tree.pack(fill="both", expand=True)

scrollbar = ttk.Scrollbar(frame_info, orient="vertical", command=tree.yview)
tree.configure(yscroll=scrollbar.set)
scrollbar.pack(side="right", fill="y")

# Tổng doanh thu
lbl_tong = tk.Label(root, text="Tổng doanh thu: 0 VND", font=("Times New Roman", 12, "bold"),
                    bg="#FFFACD", fg="red")
lbl_tong.place(x=50, y=610)

root.mainloop()