
CREATE DATABASE RollsRoyceShop;
GO

USE RollsRoyceShop;
/*Bảng phân quyền Roles*/
CREATE TABLE Roles (
    RoleID INT IDENTITY(1,1) PRIMARY KEY,
    RoleName NVARCHAR(50) NOT NULL UNIQUE,
    Description NVARCHAR(255) NULL
);
GO
/*Bảng người dùng Users*/
CREATE TABLE Users (
    UserID INT IDENTITY(1,1) PRIMARY KEY,
    FullName NVARCHAR(150) NOT NULL,
    Username VARCHAR(50) NOT NULL UNIQUE,
    PasswordHash VARCHAR(255) NOT NULL,
    Email VARCHAR(100) NOT NULL UNIQUE,
    Phone VARCHAR(15) NULL,
    Address NVARCHAR(255) NULL,
    Gender NVARCHAR(10) NULL,
    DateOfBirth DATE NULL,
    Avatar NVARCHAR(255) NULL,
    RoleID INT NOT NULL,
    Status NVARCHAR(30) NOT NULL DEFAULT N'Active',
    CreatedAt DATETIME NOT NULL DEFAULT GETDATE(),
    UpdatedAt DATETIME NULL,

    CONSTRAINT FK_Users_Roles
        FOREIGN KEY (RoleID) REFERENCES Roles(RoleID)
);
GO
/*6.4. Bảng danh mục Categories*/
CREATE TABLE Categories (
    CategoryID INT IDENTITY(1,1) PRIMARY KEY,
    CategoryName NVARCHAR(100) NOT NULL,
    Description NVARCHAR(255) NULL,
    Status NVARCHAR(30) NOT NULL DEFAULT N'Active',
    CreatedAt DATETIME NOT NULL DEFAULT GETDATE()
);
GO
/*6.5. Bảng sản phẩm Products*/
CREATE TABLE Products (
    ProductID INT IDENTITY(1,1) PRIMARY KEY,
    ProductName NVARCHAR(200) NOT NULL,
    CategoryID INT NOT NULL,
    Material NVARCHAR(100) NULL,           -- Vàng 18K, Vàng 24K, Bạc 925...
    Weight DECIMAL(10,2) NULL,             -- Trọng lượng
    StoneType NVARCHAR(100) NULL,          -- Loại đá
    Purity NVARCHAR(50) NULL,              -- Độ tinh khiết
    Price DECIMAL(18,2) NOT NULL,
    QuantityInStock INT NOT NULL DEFAULT 0,
    MainImage NVARCHAR(255) NULL,
    Description NVARCHAR(MAX) NULL,
    WarrantyPeriod INT NULL,               -- số tháng bảo hành
    IsFeatured BIT NOT NULL DEFAULT 0,
    Status NVARCHAR(30) NOT NULL DEFAULT N'Available',
    CreatedAt DATETIME NOT NULL DEFAULT GETDATE(),
    UpdatedAt DATETIME NULL,

    CONSTRAINT FK_Products_Categories
        FOREIGN KEY (CategoryID) REFERENCES Categories(CategoryID)
);
GO
/*6.6. Bảng ảnh phụ sản phẩm ProductImages*/
CREATE TABLE ProductImages (
    ImageID INT IDENTITY(1,1) PRIMARY KEY,
    ProductID INT NOT NULL,
    ImageURL NVARCHAR(255) NOT NULL,
    IsPrimary BIT NOT NULL DEFAULT 0,
    SortOrder INT NOT NULL DEFAULT 1,

    CONSTRAINT FK_ProductImages_Products
        FOREIGN KEY (ProductID) REFERENCES Products(ProductID)
        ON DELETE CASCADE
);
GO
/*6.7. Bảng giỏ hàng Carts*/
CREATE TABLE Carts (
    CartID INT IDENTITY(1,1) PRIMARY KEY,
    UserID INT NOT NULL,
    CreatedAt DATETIME NOT NULL DEFAULT GETDATE(),
    UpdatedAt DATETIME NULL,

    CONSTRAINT FK_Carts_Users
        FOREIGN KEY (UserID) REFERENCES Users(UserID)
);
GO
/*6.8. Bảng chi tiết giỏ hàng CartItems*/
CREATE TABLE CartItems (
    CartItemID INT IDENTITY(1,1) PRIMARY KEY,
    CartID INT NOT NULL,
    ProductID INT NOT NULL,
    Quantity INT NOT NULL CHECK (Quantity > 0),
    UnitPrice DECIMAL(18,2) NOT NULL,
    AddedAt DATETIME NOT NULL DEFAULT GETDATE(),

    CONSTRAINT FK_CartItems_Carts
        FOREIGN KEY (CartID) REFERENCES Carts(CartID)
        ON DELETE CASCADE,

    CONSTRAINT FK_CartItems_Products
        FOREIGN KEY (ProductID) REFERENCES Products(ProductID)
);
GO
/*6.9. Bảng khuyến mãi Promotions*/
CREATE TABLE Promotions (
    PromotionID INT IDENTITY(1,1) PRIMARY KEY,
    PromotionName NVARCHAR(150) NOT NULL,
    PromoCode VARCHAR(50) NOT NULL UNIQUE,
    DiscountType NVARCHAR(20) NOT NULL,      -- Percent / Fixed
    DiscountValue DECIMAL(18,2) NOT NULL,
    MinOrderValue DECIMAL(18,2) NULL,
    StartDate DATETIME NOT NULL,
    EndDate DATETIME NOT NULL,
    UsageLimit INT NULL,
    UsedCount INT NOT NULL DEFAULT 0,
    Status NVARCHAR(30) NOT NULL DEFAULT N'Active',
    Description NVARCHAR(255) NULL,
    CreatedAt DATETIME NOT NULL DEFAULT GETDATE()
);
GO
/*6.10. Bảng liên kết sản phẩm - khuyến mãi ProductPromotions*/
CREATE TABLE ProductPromotions (
    ProductPromotionID INT IDENTITY(1,1) PRIMARY KEY,
    ProductID INT NOT NULL,
    PromotionID INT NOT NULL,

    CONSTRAINT FK_ProductPromotions_Products
        FOREIGN KEY (ProductID) REFERENCES Products(ProductID)
        ON DELETE CASCADE,

    CONSTRAINT FK_ProductPromotions_Promotions
        FOREIGN KEY (PromotionID) REFERENCES Promotions(PromotionID)
        ON DELETE CASCADE
);
GO
/*6.11. Bảng đơn hàng Orders*/
CREATE TABLE Orders (
    OrderID INT IDENTITY(1,1) PRIMARY KEY,
    UserID INT NOT NULL,
    OrderCode VARCHAR(30) NOT NULL UNIQUE,
    ReceiverName NVARCHAR(150) NOT NULL,
    ReceiverPhone VARCHAR(15) NOT NULL,
    ShippingAddress NVARCHAR(255) NOT NULL,
    Note NVARCHAR(500) NULL,
    SubTotal DECIMAL(18,2) NOT NULL,
    DiscountAmount DECIMAL(18,2) NOT NULL DEFAULT 0,
    ShippingFee DECIMAL(18,2) NOT NULL DEFAULT 0,
    TotalAmount DECIMAL(18,2) NOT NULL,
    PromotionID INT NULL,
    PaymentMethod NVARCHAR(50) NOT NULL,     -- COD, Online Banking, Momo...
    PaymentStatus NVARCHAR(30) NOT NULL DEFAULT N'Unpaid',
    OrderStatus NVARCHAR(30) NOT NULL DEFAULT N'Pending',
    CreatedAt DATETIME NOT NULL DEFAULT GETDATE(),
    UpdatedAt DATETIME NULL,

    CONSTRAINT FK_Orders_Users
        FOREIGN KEY (UserID) REFERENCES Users(UserID),

    CONSTRAINT FK_Orders_Promotions
        FOREIGN KEY (PromotionID) REFERENCES Promotions(PromotionID)
);
GO
/*6.12. Bảng chi tiết đơn hàng OrderDetails*/
CREATE TABLE OrderDetails (
    OrderDetailID INT IDENTITY(1,1) PRIMARY KEY,
    OrderID INT NOT NULL,
    ProductID INT NOT NULL,
    Quantity INT NOT NULL CHECK (Quantity > 0),
    UnitPrice DECIMAL(18,2) NOT NULL,
    DiscountPercent DECIMAL(5,2) NOT NULL DEFAULT 0,
    TotalPrice AS (Quantity * UnitPrice * (1 - DiscountPercent / 100.0)) PERSISTED,

    CONSTRAINT FK_OrderDetails_Orders
        FOREIGN KEY (OrderID) REFERENCES Orders(OrderID)
        ON DELETE CASCADE,

    CONSTRAINT FK_OrderDetails_Products
        FOREIGN KEY (ProductID) REFERENCES Products(ProductID)
);
GO
/*6.13. Bảng giao dịch Transactions
CREATE TABLE Transactions (
    TransactionID INT IDENTITY(1,1) PRIMARY KEY,
    OrderID INT NOT NULL,
    TransactionCode VARCHAR(50) NOT NULL UNIQUE,
    PaymentGateway NVARCHAR(50) NULL,
    Amount DECIMAL(18,2) NOT NULL,
    TransactionStatus NVARCHAR(30) NOT NULL DEFAULT N'Pending',
    PaidAt DATETIME NULL,
    CreatedAt DATETIME NOT NULL DEFAULT GETDATE(),
    Note NVARCHAR(255) NULL,

    CONSTRAINT FK_Transactions_Orders
        FOREIGN KEY (OrderID) REFERENCES Orders(OrderID)
);
GO*/
/*6.14. Bảng đánh giá sản phẩm Reviews*/
CREATE TABLE Reviews (
    ReviewID INT IDENTITY(1,1) PRIMARY KEY,
    ProductID INT NOT NULL,
    UserID INT NOT NULL,
    Rating INT NOT NULL CHECK (Rating BETWEEN 1 AND 5),
    Comment NVARCHAR(1000) NULL,
    ReviewDate DATETIME NOT NULL DEFAULT GETDATE(),
    Status NVARCHAR(30) NOT NULL DEFAULT N'Visible',

    CONSTRAINT FK_Reviews_Products
        FOREIGN KEY (ProductID) REFERENCES Products(ProductID)
        ON DELETE CASCADE,

    CONSTRAINT FK_Reviews_Users
        FOREIGN KEY (UserID) REFERENCES Users(UserID)
);
GO
/*6.15. Bảng nhật ký kho InventoryLogs*/
CREATE TABLE InventoryLogs (
    InventoryLogID INT IDENTITY(1,1) PRIMARY KEY,
    ProductID INT NOT NULL,
    ChangedBy INT NULL,
    ChangeType NVARCHAR(30) NOT NULL,      -- Import, Export, Adjust
    QuantityChanged INT NOT NULL,
    QuantityBefore INT NOT NULL,
    QuantityAfter INT NOT NULL,
    Note NVARCHAR(255) NULL,
    CreatedAt DATETIME NOT NULL DEFAULT GETDATE(),

    CONSTRAINT FK_InventoryLogs_Products
        FOREIGN KEY (ProductID) REFERENCES Products(ProductID),

    CONSTRAINT FK_InventoryLogs_Users
        FOREIGN KEY (ChangedBy) REFERENCES Users(UserID)
);
GO
/*7. Dữ liệu mẫu
7.1. Roles*/
INSERT INTO Roles (RoleName, Description)
VALUES
(N'Admin', N'Quản trị toàn hệ thống'),
(N'Manager', N'Quản lý sản phẩm, đơn hàng, báo cáo'),
(N'Staff', N'Nhân viên xử lý đơn hàng và kho'),
(N'Customer', N'Khách hàng mua sắm');
GO
/*7.2. Users*/
INSERT INTO Users (FullName, Username, PasswordHash, Email, Phone, Address, RoleID, Status)
VALUES
(N'Nguyễn Ngọc Hiến', 'adminnnhien', 'hashed_password_123', 'admin@gmail.com', '0336076551', N'Thái Bình', 1, N'Active'),
(N'Trần Minh Anh', 'minhanh', 'hashed_password_456', 'anh@gmail.com', '0987654321', N'Hà Nội', 4, N'Active'),
(N'Lê Thu Trang', 'thutrang', 'hashed_password_789', 'trang@gmail.com', '0912345678', N'Hải Phòng', 4, N'Active');
GO
/*7.3. Categories*/
INSERT INTO Categories (CategoryName, Description)
VALUES
(N'Nhẫn', N'Danh mục nhẫn vàng bạc'),
(N'Dây chuyền', N'Danh mục dây chuyền'),
(N'Bông tai', N'Danh mục bông tai'),
(N'Vòng tay', N'Danh mục vòng tay');
GO
/*7.4. Products*/
INSERT INTO Products
(ProductName, CategoryID, Material, Weight, StoneType, Purity, Price, QuantityInStock, MainImage, Description, WarrantyPeriod, IsFeatured, Status)
VALUES
(N'Nhẫn vàng 18K đính đá', 1, N'Vàng 18K', 3.50, N'CZ', N'75%', 5500000, 20, 'nhan18k.jpg', N'Nhẫn vàng 18K thiết kế sang trọng', 12, 1, N'Available'),
(N'Dây chuyền bạc 925 nữ', 2, N'Bạc 925', 5.20, NULL, N'92.5%', 1200000, 30, 'dc_bac925.jpg', N'Dây chuyền bạc phong cách hiện đại', 6, 0, N'Available'),
(N'Bông tai vàng 24K', 3, N'Vàng 24K', 2.00, NULL, N'99.99%', 3200000, 15, 'bt24k.jpg', N'Bông tai vàng nguyên chất cao cấp', 12, 1, N'Available');
GO