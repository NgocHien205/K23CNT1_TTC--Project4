const API_BASE_URL = "http://127.0.0.1:5000/api";

function formatMoney(number) {

    return Number(number)
        .toLocaleString("vi-VN") + " VNĐ";
}

function saveUser(user) {

    localStorage.setItem(
        "user",
        JSON.stringify(user)
    );
}

function getUser() {

    return JSON.parse(
        localStorage.getItem("user")
    );
}

function logout() {

    localStorage.removeItem("user");

    window.location.href = "login.html";
}

function getCart() {

    return JSON.parse(
        localStorage.getItem("cart")
    ) || [];
}

function saveCart(cart) {

    localStorage.setItem(
        "cart",
        JSON.stringify(cart)
    );
}