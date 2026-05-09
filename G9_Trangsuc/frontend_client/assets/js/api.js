// ==============================
// API CONFIG
// ==============================

const API_BASE_URL = "http://127.0.0.1:5000/api";


// ==============================
// HELPER FETCH GET
// ==============================

async function apiGet(endpoint) {

    try {

        const response = await fetch(
            `${API_BASE_URL}${endpoint}`
        );

        if (!response.ok) {

            throw new Error(
                `HTTP Error: ${response.status}`
            );
        }

        return await response.json();

    } catch (error) {

        console.error(
            "GET API ERROR:",
            error
        );

        return null;
    }
}


// ==============================
// HELPER FETCH POST
// ==============================

async function apiPost(endpoint, data = {}) {

    try {

        const response = await fetch(
            `${API_BASE_URL}${endpoint}`,
            {
                method: "POST",

                headers: {
                    "Content-Type": "application/json"
                },

                body: JSON.stringify(data)
            }
        );

        if (!response.ok) {

            throw new Error(
                `HTTP Error: ${response.status}`
            );
        }

        return await response.json();

    } catch (error) {

        console.error(
            "POST API ERROR:",
            error
        );

        return null;
    }
}


// ==============================
// HELPER FETCH PUT
// ==============================

async function apiPut(endpoint, data = {}) {

    try {

        const response = await fetch(
            `${API_BASE_URL}${endpoint}`,
            {
                method: "PUT",

                headers: {
                    "Content-Type": "application/json"
                },

                body: JSON.stringify(data)
            }
        );

        if (!response.ok) {

            throw new Error(
                `HTTP Error: ${response.status}`
            );
        }

        return await response.json();

    } catch (error) {

        console.error(
            "PUT API ERROR:",
            error
        );

        return null;
    }
}


// ==============================
// HELPER FETCH DELETE
// ==============================

async function apiDelete(endpoint) {

    try {

        const response = await fetch(
            `${API_BASE_URL}${endpoint}`,
            {
                method: "DELETE"
            }
        );

        if (!response.ok) {

            throw new Error(
                `HTTP Error: ${response.status}`
            );
        }

        return await response.json();

    } catch (error) {

        console.error(
            "DELETE API ERROR:",
            error
        );

        return null;
    }
}


// ==============================
// USER LOCAL STORAGE
// ==============================

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


// ==============================
// CART LOCAL STORAGE
// ==============================

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


function clearCart() {

    localStorage.removeItem("cart");
}


// ==============================
// FORMAT MONEY
// ==============================

function formatMoney(number) {

    return Number(number)
        .toLocaleString("vi-VN") + " VNĐ";
}


// ==============================
// CHECK LOGIN
// ==============================

function checkLogin() {

    const user = getUser();

    if (!user) {

        alert("Vui lòng đăng nhập");

        window.location.href =
            "login.html";
    }
}


// ==============================
// CHECK ADMIN
// ==============================

function checkAdmin() {

    const user = getUser();

    if (
        !user ||
        (user.roleId !== 1 &&
         user.roleId !== 2)
    ) {

        alert("Không có quyền truy cập");

        window.location.href =
            "../index.html";
    }
}


// ==============================
// ADD TO CART
// ==============================

function addToCart(product) {

    let cart = getCart();

    const existing =
        cart.find(
            item => item.id === product.id
        );

    if (existing) {

        existing.quantityCart += 1;

    } else {

        product.quantityCart = 1;

        cart.push(product);
    }

    saveCart(cart);

    alert("Đã thêm vào giỏ hàng");
}


// ==============================
// TOTAL CART
// ==============================

function getCartTotal() {

    let cart = getCart();

    let total = 0;

    cart.forEach(item => {

        total +=
            item.price *
            item.quantityCart;
    });

    return total;
}


// ==============================
// LOAD USER INFO
// ==============================

function loadUserInfo() {

    const user = getUser();

    if (user) {

        console.log(
            "Đã đăng nhập:",
            user.name
        );
    }
}


// ==============================
// AUTO LOAD
// ==============================

loadUserInfo();