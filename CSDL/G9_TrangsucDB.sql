CREATE DATABASE G9_TrangSucDB;
GO

USE G9_TrangSucDB;
GO

CREATE TABLE G9_VaiTro (
    G9_MaVaiTro INT IDENTITY PRIMARY KEY,
    G9_TenVaiTro NVARCHAR(50) UNIQUE NOT NULL
);

CREATE TABLE G9_NguoiDung (
    G9_MaNguoiDung INT IDENTITY PRIMARY KEY,
    G9_HoTen NVARCHAR(150) NOT NULL,
    G9_TenDangNhap VARCHAR(50) UNIQUE NOT NULL,
    G9_MatKhau VARCHAR(255) NOT NULL,
    G9_Email VARCHAR(100) UNIQUE,
    G9_SoDienThoai VARCHAR(15),
    G9_Avatar NVARCHAR(255),
    G9_MaVaiTro INT NOT NULL,
    G9_TrangThai NVARCHAR(30) DEFAULT N'Hoạt động',
    G9_NgayTao DATETIME DEFAULT GETDATE(),

    FOREIGN KEY (G9_MaVaiTro) REFERENCES G9_VaiTro(G9_MaVaiTro)
);

CREATE TABLE G9_DanhMuc (
    G9_MaDanhMuc INT IDENTITY PRIMARY KEY,
    G9_TenDanhMuc NVARCHAR(100) NOT NULL,
    G9_MoTa NVARCHAR(255) NULL,
    G9_MaDanhMucCha INT NULL,
    G9_TrangThai NVARCHAR(30) DEFAULT N'Hoạt động',

    CONSTRAINT FK_G9_DanhMuc_Cha
        FOREIGN KEY (G9_MaDanhMucCha)
        REFERENCES G9_DanhMuc(G9_MaDanhMuc)
);
--NULL → danh mục cha (cấp 1)
-- Có giá trị → danh mục con 

CREATE TABLE G9_SanPham (
    G9_MaSanPham INT IDENTITY PRIMARY KEY,
    G9_TenSanPham NVARCHAR(200) NOT NULL,
    G9_MaDanhMuc INT NOT NULL,
    G9_ChatLieu NVARCHAR(100),
    G9_Gia DECIMAL(18,2) NOT NULL,
    G9_SoLuongTon INT DEFAULT 0,
    G9_HinhAnhChinh NVARCHAR(255),
    G9_MoTa NVARCHAR(MAX),
    G9_TrangThai NVARCHAR(30) DEFAULT N'Còn hàng',
    G9_NgayTao DATETIME DEFAULT GETDATE(),

    FOREIGN KEY (G9_MaDanhMuc) REFERENCES G9_DanhMuc(G9_MaDanhMuc)
);

CREATE TABLE G9_HinhAnhSanPham (
    G9_MaHinh INT IDENTITY PRIMARY KEY,
    G9_MaSanPham INT NOT NULL,
    G9_DuongDan NVARCHAR(255),
    G9_LaAnhChinh BIT DEFAULT 0,

    FOREIGN KEY (G9_MaSanPham) REFERENCES G9_SanPham(G9_MaSanPham)
    ON DELETE CASCADE
);

CREATE TABLE G9_GioHang (
    G9_MaGioHang INT IDENTITY PRIMARY KEY,
    G9_MaNguoiDung INT NOT NULL,
    G9_NgayTao DATETIME DEFAULT GETDATE(),

    FOREIGN KEY (G9_MaNguoiDung) REFERENCES G9_NguoiDung(G9_MaNguoiDung)
);

CREATE TABLE G9_ChiTietGioHang (
    G9_MaChiTiet INT IDENTITY PRIMARY KEY,
    G9_MaGioHang INT NOT NULL,
    G9_MaSanPham INT NOT NULL,
    G9_SoLuong INT CHECK (G9_SoLuong > 0),
    G9_DonGia DECIMAL(18,2),

    FOREIGN KEY (G9_MaGioHang) REFERENCES G9_GioHang(G9_MaGioHang) ON DELETE CASCADE,
    FOREIGN KEY (G9_MaSanPham) REFERENCES G9_SanPham(G9_MaSanPham)
);

CREATE TABLE G9_DonHang (
    G9_MaDonHang INT IDENTITY PRIMARY KEY,
    G9_MaNguoiDung INT NOT NULL,
    G9_TenNguoiNhan NVARCHAR(150),
    G9_SDTNhan VARCHAR(15),
    G9_DiaChiGiao NVARCHAR(255),
    G9_TongTien DECIMAL(18,2),
    G9_TrangThai NVARCHAR(30) DEFAULT N'Chờ xác nhận',
    G9_NgayDat DATETIME DEFAULT GETDATE(),

    FOREIGN KEY (G9_MaNguoiDung) REFERENCES G9_NguoiDung(G9_MaNguoiDung)
);

CREATE TABLE G9_ChiTietDonHang (
    G9_MaChiTiet INT IDENTITY PRIMARY KEY,
    G9_MaDonHang INT NOT NULL,
    G9_MaSanPham INT NOT NULL,
    G9_SoLuong INT CHECK (G9_SoLuong > 0),
    G9_DonGia DECIMAL(18,2),
    G9_ThanhTien AS (G9_SoLuong * G9_DonGia),

    FOREIGN KEY (G9_MaDonHang) REFERENCES G9_DonHang(G9_MaDonHang) ON DELETE CASCADE,
    FOREIGN KEY (G9_MaSanPham) REFERENCES G9_SanPham(G9_MaSanPham)
);

CREATE TABLE G9_ThanhToan (
    G9_MaThanhToan INT IDENTITY PRIMARY KEY,
    G9_MaDonHang INT NOT NULL,
    G9_PhuongThuc NVARCHAR(50),
    G9_SoTien DECIMAL(18,2),
    G9_TrangThai NVARCHAR(30) DEFAULT N'Chưa thanh toán',
    G9_NgayThanhToan DATETIME DEFAULT GETDATE(),

    FOREIGN KEY (G9_MaDonHang) REFERENCES G9_DonHang(G9_MaDonHang)
);

CREATE TABLE G9_KhuyenMai (
    G9_MaKhuyenMai INT IDENTITY PRIMARY KEY,
    G9_MaCode VARCHAR(50) UNIQUE,
    G9_GiaTriGiam DECIMAL(18,2),
    G9_NgayBatDau DATETIME,
    G9_NgayKetThuc DATETIME,
    G9_TrangThai NVARCHAR(30) DEFAULT N'Hoạt động'
);

CREATE TABLE G9_SanPham_KhuyenMai (
    G9_ID INT IDENTITY PRIMARY KEY,
    G9_MaSanPham INT,
    G9_MaKhuyenMai INT,

    FOREIGN KEY (G9_MaSanPham) REFERENCES G9_SanPham(G9_MaSanPham) ON DELETE CASCADE,
    FOREIGN KEY (G9_MaKhuyenMai) REFERENCES G9_KhuyenMai(G9_MaKhuyenMai) ON DELETE CASCADE
);

CREATE TABLE G9_DanhGia (
    G9_MaDanhGia INT IDENTITY PRIMARY KEY,
    G9_MaSanPham INT,
    G9_MaNguoiDung INT,
    G9_SoSao INT CHECK (G9_SoSao BETWEEN 1 AND 5),
    G9_NoiDung NVARCHAR(500),
    G9_TrangThai NVARCHAR(30) DEFAULT N'Hiển thị',
    G9_NgayDanhGia DATETIME DEFAULT GETDATE(),

    FOREIGN KEY (G9_MaSanPham) REFERENCES G9_SanPham(G9_MaSanPham) ON DELETE CASCADE,
    FOREIGN KEY (G9_MaNguoiDung) REFERENCES G9_NguoiDung(G9_MaNguoiDung)
);

CREATE INDEX IX_G9_SanPham_Ten ON G9_SanPham(G9_TenSanPham);
CREATE INDEX IX_G9_DonHang_User ON G9_DonHang(G9_MaNguoiDung);
CREATE INDEX IX_G9_GioHang_User ON G9_GioHang(G9_MaNguoiDung);
CREATE INDEX IX_G9_DanhMuc_Cha 
ON G9_DanhMuc(G9_MaDanhMucCha);


/*Thêm dữ liệu cho các bảng */
INSERT INTO G9_VaiTro (G9_TenVaiTro)
VALUES 
(N'Admin'),
(N'Khách hàng');

INSERT INTO G9_NguoiDung 
(G9_HoTen, G9_TenDangNhap, G9_MatKhau, G9_Email, G9_SoDienThoai, G9_Avatar, G9_MaVaiTro)
VALUES
(N'Nguyễn Ngọc Hiến', 'nnhien', '123456', 'nnhien@gmail.com', '0900000001', NULL, 2),
(N'Vũ Mai Chi', 'vmchi', '123456', 'vmchi@gmail.com', '0900000002', NULL, 2),
(N'Phạm Tuấn Phong', 'ptphong', '123456', 'ptphong@gmail.com', '0900000003', NULL, 2),
(N'Đức Huy', 'duchuy', '123456', 'duchuy@gmail.com', '0900000004', NULL, 1);

INSERT INTO G9_DanhMuc (G9_TenDanhMuc, G9_MoTa)
VALUES
(N'Nhẫn', N'Trang sức nhẫn'),
(N'Dây chuyền', N'Trang sức cổ'),
(N'Bông tai', N'Trang sức tai');

INSERT INTO G9_SanPham 
(G9_TenSanPham, G9_MaDanhMuc, G9_ChatLieu, G9_Gia, G9_SoLuongTon, G9_HinhAnhChinh, G9_MoTa)
VALUES
(N'Nhẫn vàng 18K đính đá', 1, N'Vàng 18K', 3500000, 15, NULL, N'Nhẫn vàng cao cấp đính đá sang trọng'),
(N'Nhẫn bạc nữ kiểu Hàn', 1, N'Bạc', 450000, 30, NULL, N'Nhẫn bạc thiết kế trẻ trung'),
(N'Nhẫn kim cương cao cấp', 1, N'Kim cương', 15000000, 5, NULL, N'Nhẫn kim cương dành cho dịp đặc biệt'),
(N'Dây chuyền vàng 24K', 2, N'Vàng 24K', 8000000, 10, NULL, N'Dây chuyền vàng nguyên chất'),
(N'Dây chuyền bạc mặt trái tim', 2, N'Bạc', 1200000, 20, NULL, N'Thiết kế nhẹ nhàng, phù hợp nữ'),
(N'Dây chuyền ngọc trai', 2, N'Ngọc trai', 5000000, 8, NULL, N'Dây chuyền ngọc trai sang trọng'),
(N'Bông tai vàng đính đá', 3, N'Vàng', 2500000, 12, NULL, N'Bông tai đẹp, phù hợp dự tiệc'),
(N'Bông tai bạc đơn giản', 3, N'Bạc', 300000, 40, NULL, N'Phong cách tối giản, dễ phối đồ'),
(N'Bông tai kim cương nhỏ', 3, N'Kim cương', 7000000, 6, NULL, N'Bông tai kim cương tinh tế'),
(N'Lắc tay bạc nữ', 2, N'Bạc', 900000, 25, NULL, N'Lắc tay thời trang cho nữ');