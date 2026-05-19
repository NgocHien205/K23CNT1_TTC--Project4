const API_BASE_URL = "http://127.0.0.1:5000/api";

function formatMoney(number) {
    return Number(number).toLocaleString("vi-VN") + " VNĐ";
}

function getUser() {
    return JSON.parse(localStorage.getItem("user"));
}

function saveUser(user) {
    localStorage.setItem("user", JSON.stringify(user));
}

function logout() {
    localStorage.removeItem("user");
    localStorage.removeItem("cart");
    window.location.href = "../user/login.html";
}

function getCart() {
    return JSON.parse(localStorage.getItem("cart")) || [];
}

function saveCart(cart) {
    localStorage.setItem("cart", JSON.stringify(cart));
}

function clearCart() {
    localStorage.removeItem("cart");
}