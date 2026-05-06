CREATE DATABASE WebsiteTrangSuc;
GO

USE WebsiteTrangSuc;
GO

-- 1. Bảng vai trò
CREATE TABLE VaiTro (
    MaVaiTro INT IDENTITY(1,1) PRIMARY KEY,
    TenVaiTro NVARCHAR(50) NOT NULL UNIQUE
);
GO

-- 2. Bảng admin
CREATE TABLE Admin (
    MaAdmin INT IDENTITY(1,1) PRIMARY KEY,
    HoTen NVARCHAR(150) NOT NULL,
    SoDienThoai VARCHAR(15) NULL,
    Email VARCHAR(100) NOT NULL UNIQUE,
    TenDangNhap VARCHAR(50) NOT NULL UNIQUE,
    MatKhau VARCHAR(100) NOT NULL,
    MaVaiTro INT NOT NULL,
    TrangThai NVARCHAR(50) DEFAULT N'Hoạt động',

    CONSTRAINT FK_Admin_VaiTro
        FOREIGN KEY (MaVaiTro) REFERENCES VaiTro(MaVaiTro)
);
GO

-- 3. Bảng khách hàng
CREATE TABLE KhachHang (
    MaKhachHang INT IDENTITY(1,1) PRIMARY KEY,
    HoTen NVARCHAR(150) NOT NULL,
    SoDienThoai VARCHAR(15) NOT NULL,
    Email VARCHAR(100) UNIQUE NULL,
    DiaChi NVARCHAR(255) NULL,
    TenDangNhap VARCHAR(50) UNIQUE NOT NULL,
    MatKhau VARCHAR(100) NOT NULL,
    MaVaiTro INT NOT NULL,
    TrangThai NVARCHAR(50) DEFAULT N'Hoạt động',

    CONSTRAINT FK_KhachHang_VaiTro
        FOREIGN KEY (MaVaiTro) REFERENCES VaiTro(MaVaiTro)
);
GO

-- 4. Bảng danh mục
CREATE TABLE DanhMuc (
    MaDanhMuc INT IDENTITY(1,1) PRIMARY KEY,
    TenDanhMuc NVARCHAR(100) NOT NULL,
    MoTa NVARCHAR(255) NULL
);
GO

-- 5. Bảng sản phẩm
CREATE TABLE SanPham (
    MaSanPham INT IDENTITY(1,1) PRIMARY KEY,
    TenSanPham NVARCHAR(200) NOT NULL,
    ChatLieu NVARCHAR(100) NULL,
    TrongLuong DECIMAL(10,2) NULL,
    Gia DECIMAL(18,2) NOT NULL,
    SoLuongTon INT NOT NULL DEFAULT 0,
    HinhAnh NVARCHAR(255) NULL,
    MoTa NVARCHAR(MAX) NULL,
    MaDanhMuc INT NOT NULL,
    TrangThai NVARCHAR(50) DEFAULT N'Còn hàng',

    CONSTRAINT FK_SanPham_DanhMuc
        FOREIGN KEY (MaDanhMuc) REFERENCES DanhMuc(MaDanhMuc)
);
GO

-- 6. Bảng giỏ hàng
CREATE TABLE GioHang (
    MaGioHang INT IDENTITY(1,1) PRIMARY KEY,
    MaKhachHang INT NOT NULL,
    MaSanPham INT NOT NULL,
    SoLuong INT NOT NULL CHECK (SoLuong > 0),
    NgayThem DATETIME DEFAULT GETDATE(),

    CONSTRAINT FK_GioHang_KhachHang
        FOREIGN KEY (MaKhachHang) REFERENCES KhachHang(MaKhachHang),

    CONSTRAINT FK_GioHang_SanPham
        FOREIGN KEY (MaSanPham) REFERENCES SanPham(MaSanPham)
);
GO

-- 7. Bảng đơn hàng
CREATE TABLE DonHang (
    MaDonHang INT IDENTITY(1,1) PRIMARY KEY,
    MaKhachHang INT NOT NULL,
    NgayDat DATETIME DEFAULT GETDATE(),
    TongTien DECIMAL(18,2) NOT NULL,
    TrangThai NVARCHAR(50) DEFAULT N'Chờ xác nhận',
    DiaChiGiaoHang NVARCHAR(255) NOT NULL,

    CONSTRAINT FK_DonHang_KhachHang
        FOREIGN KEY (MaKhachHang) REFERENCES KhachHang(MaKhachHang)
);
GO

-- 8. Bảng chi tiết đơn hàng
CREATE TABLE ChiTietDonHang (
    MaChiTiet INT IDENTITY(1,1) PRIMARY KEY,
    MaDonHang INT NOT NULL,
    MaSanPham INT NOT NULL,
    SoLuong INT NOT NULL CHECK (SoLuong > 0),
    DonGia DECIMAL(18,2) NOT NULL,
    ThanhTien AS (SoLuong * DonGia),

    CONSTRAINT FK_ChiTietDonHang_DonHang
        FOREIGN KEY (MaDonHang) REFERENCES DonHang(MaDonHang),

    CONSTRAINT FK_ChiTietDonHang_SanPham
        FOREIGN KEY (MaSanPham) REFERENCES SanPham(MaSanPham)
);
GO



INSERT INTO VaiTro (TenVaiTro)
VALUES 
(N'Admin'),
(N'KhachHang');
GO

-- Admin
INSERT INTO Admin (HoTen, SoDienThoai, Email, TenDangNhap, MatKhau, MaVaiTro, TrangThai)
VALUES
(N'Nguyễn Ngọc Hiến', '0336076551', 'adminhien@gmail.com', 'adminnnhien', '123456', 1, N'Hoạt động');
GO

-- Khách hàng
INSERT INTO KhachHang (HoTen, SoDienThoai, Email, DiaChi, TenDangNhap, MatKhau, MaVaiTro, TrangThai)
VALUES
(N'Trần Minh Anh', '0987654321', 'minhanh@gmail.com', N'Hà Nội', 'minhanh', '123456', 2, N'Hoạt động'),
(N'Lê Thu Trang', '0912345678', 'thutrang@gmail.com', N'Hải Phòng', 'thutrang', '123456', 2, N'Hoạt động');
GO

INSERT INTO DanhMuc (TenDanhMuc, MoTa)
VALUES
(N'Nhẫn', N'Các loại nhẫn vàng bạc'),
(N'Dây chuyền', N'Các loại dây chuyền trang sức'),
(N'Bông tai', N'Các loại bông tai cao cấp');
GO

INSERT INTO SanPham (TenSanPham, ChatLieu, TrongLuong, Gia, SoLuongTon, HinhAnh, MoTa, MaDanhMuc, TrangThai)
VALUES
(N'Nhẫn vàng 18K đính đá', N'Vàng 18K', 3.5, 5500000, 10, 'nhanvang18k.jpg', N'Nhẫn vàng sang trọng', 1, N'Còn hàng'),
(N'Dây chuyền bạc 925', N'Bạc 925', 5.0, 1200000, 15, 'daychuyenbac925.jpg', N'Dây chuyền đẹp cho nữ', 2, N'Còn hàng'),
(N'Bông tai vàng 24K', N'Vàng 24K', 2.0, 3200000, 8, 'bongtaivang24k.jpg', N'Bông tai vàng nguyên chất', 3, N'Còn hàng');
GO

select * from KhachHang;
