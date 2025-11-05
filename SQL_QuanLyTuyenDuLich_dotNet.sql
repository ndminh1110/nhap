CREATE DATABASE QuanLyTuyenDuLich

ON
(
	name = 'QuanLyTuyenDuLich_data',
	filename = 'D:\DoAn\QuanLyTuyenDuLich_data.mdf',
	size = 8MB,
	maxsize = 100MB,
	filegrowth = 2MB)
LOG ON
(
	name = 'QuanLyTuyenDuLich_log',
	filename = 'D:\DoAn\QuanLyTuyenDuLich_log.ldf',
	size = 8MB,
	maxsize = 100MB,
	filegrowth = 2MB);
GO

USE QuanLyTuyenDuLich;
GO

--TAO BANG--
CREATE TABLE KHACHHANG
(
	maKH VARCHAR(6) 
        CONSTRAINT chk_maKH CHECK (maKH LIKE 'KH[0-9][0-9][0-9][0-9]'),
	hoTen nvarchar(40) NOT NULL,
	phai NVARCHAR(3) CHECK (LOWER(phai) IN (N'nam', N'nữ')),
	ngsinh DATE,
	sdt VARCHAR(10) 
        CONSTRAINT chk_sdt CHECK (sdt LIKE '0[0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9]'),
	dchi nvarchar(50),
	CONSTRAINT pk_KHACHHANG PRIMARY KEY (maKH)
);

CREATE TABLE NHANVIEN
(
	maNV varchar(6)
		CONSTRAINT chk_maNV CHECK (maNV LIKE 'NV[0-9][0,9][0,9][0,9]'),
	hoTen nvarchar(40) NOT NULL,
	chucVu nvarchar(20),
	phai nvarchar(3) CHECK (LOWER(phai) IN (N'nam', N'nữ')),
	ngsinh DATE,
	sdt varchar(10) 
	CONSTRAINT chk_sdtNV check ( sdt like '[0][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9]'),
	dchi nvarchar(50),
	luong float,
	primary key (maNV)
);

CREATE TABLE TUYENDULICH
(
	ddDen nvarchar(50),
	ddDi nvarchar(50),
	 maTuyen VARCHAR(6) PRIMARY KEY 
        CHECK (maTuyen LIKE 'T[0-9][0-9][0-9][0-9]'),
);

CREATE TABLE CHUYENDI
(
	ngKh datetime,
	tgKh time,
	maTuyen varchar(6),
	maNV varchar(6),
	maCD VARCHAR(6) PRIMARY KEY 
        CHECK (maCD LIKE 'CD[0-9][0-9][0-9][0-9]'),
);
--chua co khoa chinh
CREATE TABLE DATVE
(
	maVe varchar(20),
	maKH varchar(6),
	maCD varchar(6),
	ngDat datetime,
	trangThai nvarchar(13),
	thanhTien float,
	giaVe float,
	soLuong int
);

CREATE TABLE DOANHTHU
(
	maCD varchar(6),
	giaVe float,
	tongTien float,
	ngayLap datetime
);

--LienKet SQL va Python
CREATE TABLE TaiKhoan 
(
    TenDangNhap NVARCHAR(50) PRIMARY KEY,
    MatKhau NVARCHAR(50) NOT NULL,
    VaiTro NVARCHAR(20) NOT NULL  -- 'QuanLy' hoặc 'NhanVien'
);
GO

INSERT INTO TaiKhoan (TenDangNhap, MatKhau, VaiTro)
VALUES 
('quanly', 'taolaquanly', 'QuanLy'),
('nhanvien', 'emchaosep', 'NhanVien');
GO

--DROP DATABASE QuanLyTuyenDuLich