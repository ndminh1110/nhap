import tkinter as tk
from tkinter import ttk, messagebox

root = tk.Tk()
root.title("Quản Lý Tuyến Du Lịch")
root.geometry("1000x650")
root.configure(bg="#FFFACD")

# ------------------ DANH SÁCH MẶC ĐỊNH ------------------
list_di = ["Hồ Chí Minh", "Hà Nội", "Đà Nẵng"]

mien_bac = ["Tràng An-Tam Cốc-Bái Đính-Hoa Lư", "Mộc Châu-Điện Biên-Sapa", "Hà Giang-Cao Bằng", "Ninh Bình-Hạ Long-Sapa", "Vịnh Hạ Long-Hạ Long Park-Bãi Cháy-Yên Tử"]
mien_trung = ["Quy Nhơn-Phú Yên", "Pleiku-Kontum- Măng Đen", "Hội An-Bà Nà Hills-Núi Thần Tài", "Phan Thiết-Mũi Né", "Quảng Bình-Suối Moọc- Động Thiên Đường"]
mien_nam = ["Tiền Giang-Bến Tre- An GIang-Cần Thơ", "Vũng Tàu", "Phú Quốc", "Tây Ninh"]

list_tuyen = []  # danh sách tuyến du lịch
trang_thai = None

# ------------------ HÀM ------------------
def tao_ma_tuyen():
    return f"TD{len(list_tuyen)+1:04d}"

def cap_nhat_dia_diem_den(event):
    di = entry_ddDi.get()


# Thứ tự ưu tiên hiển thị
thu_tu_di = {"Hà Nội": 0, "Đà Nẵng": 1, "Hồ Chí Minh": 2}

def hien_thi_du_lieu():
    # Sắp xếp trước khi hiển thị theo di, maTuyen
    list_tuyen.sort(key=lambda x: (thu_tu_di.get(x["di"], 99), x["maTuyen"]))
    for row in tree.get_children():
        tree.delete(row)
    for tuy in list_tuyen:
        tree.insert("", "end", values=(tuy["maTuyen"], tuy["di"], tuy["den"]))

def lam_moi_form():
    entry_ddDi.set("")             
    entry_ddDen.delete(0, tk.END) 
    entry_matuyen.config(state='normal')
    entry_matuyen.delete(0, tk.END)
    entry_matuyen.insert(0, tao_ma_tuyen())
    entry_matuyen.config(state='readonly')

def them_tuyen():
    global trang_thai
    trang_thai = "them"
    lam_moi_form()

def xoa_tuyen():
    selected = tree.selection()
    if not selected:
        messagebox.showwarning("Lỗi", "Chưa chọn tuyến để xóa!")
        return
    index = tree.index(selected[0])
    confirm = messagebox.askyesno("Xác nhận", f"Bạn có chắc muốn xóa tuyến {list_tuyen[index]['maTuyen']}?")
    if confirm:
        list_tuyen.pop(index)
        hien_thi_du_lieu()
        lam_moi_form()

def sua_tuyen():
    global trang_thai
    selected = tree.selection()
    if not selected:
        messagebox.showwarning("Lỗi", "Chưa chọn tuyến để sửa!")
        return
    trang_thai = "sua"
    index = tree.index(selected[0])
    tuy = list_tuyen[index]
    entry_matuyen.config(state='normal')
    entry_matuyen.delete(0, tk.END)
    entry_matuyen.insert(0, tuy["maTuyen"])
    entry_matuyen.config(state='readonly')
    entry_ddDi.set(tuy["di"])
    #entry_ddDen.set(tuy["den"])

def huy_thao_tac():
    global trang_thai
    trang_thai = None
    lam_moi_form()

def luu_tuyen():
    global trang_thai
    maTuyen = entry_matuyen.get()
    di = entry_ddDi.get().strip()
    den = entry_ddDen.get().strip()
    if not di or not den:
        messagebox.showwarning("Thiếu thông tin", "Vui lòng nhập đầy đủ địa điểm đi và đến!")
        return
    if trang_thai == "them":
        list_tuyen.append({"maTuyen": maTuyen, "di": di, "den": den})
        messagebox.showinfo("Thành công", f"Đã thêm tuyến {maTuyen}")
    elif trang_thai == "sua":
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("Lỗi", "Chọn tuyến cần lưu!")
            return
        index = tree.index(selected[0])
        list_tuyen[index]["di"] = di
        list_tuyen[index]["den"] = den
        messagebox.showinfo("Thành công", f"Đã cập nhật tuyến {maTuyen}")
    else:
        messagebox.showwarning("Chưa chọn thao tác", "Hãy chọn Thêm hoặc Sửa trước khi lưu!")
        return
    trang_thai = None
    hien_thi_du_lieu()
    lam_moi_form()

def thoat():
    root.destroy()

def home():
    lam_moi_form()
    messagebox.showinfo("Trang chủ", "Bạn đã trở về trang chủ!")

# ------------------ GIAO DIỆN ------------------
tk.Label(root, text="Quản Lý Tuyến Du Lịch", font=("Arial", 20, "bold"), bg="#FFFACD").place(x=300, y=45)

# Combobox địa điểm đi/đến
tk.Label(root, text="Địa Điểm Đi", font=("Arial", 12), bg="#FFFACD").place(x=200, y=150)
entry_ddDi = ttk.Combobox(root, width=50, values=list_di, state="normal")

entry_ddDi.place(x=380, y=150)
entry_ddDi.bind("<<ComboboxSelected>>", cap_nhat_dia_diem_den)

tk.Label(root, text="Địa Điểm Đến", font=("Arial", 12), bg="#FFFACD").place(x=200, y=190)
entry_ddDen = tk.Entry(root, width=50)
entry_ddDen.place(x=380, y=190)

tk.Label(root, text="Mã Tuyến", font=("Arial", 12), bg="#FFFACD").place(x=200, y=230)
entry_matuyen = tk.Entry(root, width=50)
entry_matuyen.place(x=380, y=230)
entry_matuyen.insert(0, tao_ma_tuyen())
entry_matuyen.config(state='readonly')

# Frame Treeview full form
frame_info = tk.LabelFrame(root, text="Danh sách tuyến du lịch", font=("Arial", 12, "bold"), bg="#FFFACD", width=850, height=300)
frame_info.place(x=50, y=280)

columns = ("maTuyen", "ddDi", "ddDen")
tree = ttk.Treeview(frame_info, columns=columns, show="headings", height=12)
tree.heading("maTuyen", text="Mã Tuyến")
tree.heading("ddDi", text="Địa Điểm Đi")
tree.heading("ddDen", text="Địa Điểm Đến")
tree.column("maTuyen", width=150, anchor="center")
tree.column("ddDi", width=300, anchor="center")
tree.column("ddDen", width=300, anchor="center")

scrollbar = ttk.Scrollbar(frame_info, orient="vertical", command=tree.yview)
tree.configure(yscroll=scrollbar.set)
scrollbar.pack(side="right", fill="y")
tree.pack(fill="both", expand=True, padx=10, pady=10)

# Nút chức năng
btn_them = tk.Button(root, text="Thêm", bg="#87cefa", font=("Arial", 12, "bold"), width=10, command=them_tuyen)
btn_them.place(x=870, y=150)
btn_xoa = tk.Button(root, text="Xóa", bg="#87cefa", font=("Arial", 12, "bold"), width=10, command=xoa_tuyen)
btn_xoa.place(x=870, y=210)
btn_sua = tk.Button(root, text="Sửa", bg="#87cefa", font=("Arial", 12, "bold"), width=10, command=sua_tuyen)
btn_sua.place(x=870, y=270)
btn_huy = tk.Button(root, text="Hủy", bg="#87cefa", font=("Arial", 12, "bold"), width=10, command=huy_thao_tac)
btn_huy.place(x=870, y=330)
btn_luu = tk.Button(root, text="Lưu", bg="#87cefa", font=("Arial", 12, "bold"), width=10, command=luu_tuyen)
btn_luu.place(x=870, y=390)
btn_thoat = tk.Button(root, text="Thoát", bg="#87cefa", font=("Arial", 12, "bold"), width=10, command=thoat)
btn_thoat.place(x=870, y=450)
btn_home = tk.Button(root, text="Trang chủ", font=("Arial", 10, "bold"), bg="white", relief="groove", command=home)
btn_home.place(x=50, y=30)

# ------------------ KHỞI TẠO 12 TUYẾN MẶC ĐỊNH ------------------
for di_group in ["Hà Nội", "Đà Nẵng", "Hồ Chí Minh"]:
    if di_group == "Hà Nội":
        den_list = mien_bac
    elif di_group == "Đà Nẵng":
        den_list = mien_trung
    else:
        den_list = mien_nam
    for den in den_list[:4]:  # lấy 4 tuyến mỗi thành phố
        list_tuyen.append({"maTuyen": tao_ma_tuyen(), "di": di_group, "den": den})

hien_thi_du_lieu()
lam_moi_form()
root.mainloop()
