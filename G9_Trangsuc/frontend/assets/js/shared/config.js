// ==============================
// FILE CẤU HÌNH DÙNG CHUNG
// ==============================

const API_BASE_URL = "http://127.0.0.1:5000/api";

// ==============================
// LẤY USER ĐANG ĐĂNG NHẬP
// ==============================
function getCurrentUser() {
    return JSON.parse(localStorage.getItem("user"));
}

// ==============================
// LẤY TOKEN
// ==============================
function getToken() {
    return localStorage.getItem("token");
}

// ==============================
// KIỂM TRA ĐĂNG NHẬP
// ==============================
function checkLogin() {
    const user = getCurrentUser();

    if (!user) {
        alert("Bạn cần đăng nhập trước");
        window.location.href = "../user/login.html";
    }
}

// ==============================
// KIỂM TRA QUYỀN ADMIN
// ==============================
function checkAdmin() {
    const user = getCurrentUser();

    if (!user || user.role.toLowerCase() !== "admin") {
        alert("Bạn không có quyền truy cập trang admin");
        window.location.href = "../user/login.html";
    }
}

// ==============================
// ĐĂNG XUẤT
// ==============================
function logout() {
    localStorage.removeItem("token");
    localStorage.removeItem("user");

    alert("Đăng xuất thành công");
    window.location.href = "../user/login.html";
}