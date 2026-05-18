function renderNavbar() {
    const user = JSON.parse(localStorage.getItem("user"));

    let authHtml = "";

    if (user) {
        authHtml = `
            <a href="profile.html" class="btn btn-outline-warning btn-sm nav-icon-btn">
                👋 ${user.name}
            </a>

            <button onclick="logout()" class="btn btn-danger btn-sm nav-icon-btn">
                🚪 Đăng xuất
            </button>
        `;
    } else {
        authHtml = `
            <a href="login.html" class="btn btn-light btn-sm nav-icon-btn">
                🔐 Đăng nhập
            </a>
        `;
    }

    document.getElementById("navbar").innerHTML = `
        <nav class="navbar navbar-expand-lg navbar-dark bg-dark shadow-sm py-3 sticky-top">
            <div class="container">

                <a href="index.html" class="navbar-brand text-warning fw-bold fs-3">
                    💍 G9 Trang Sức
                </a>

                <div class="d-flex align-items-center gap-2 flex-wrap">

                    <a href="products.html" class="btn btn-outline-light btn-sm nav-icon-btn">
                        💎 Sản phẩm
                    </a>

                    <a href="gold-price.html" class="btn btn-outline-warning btn-sm nav-icon-btn">
                        🪙 Giá vàng
                    </a>

                    <a href="news.html" class="btn btn-outline-info btn-sm nav-icon-btn">
                        📰 Tin tức
                    </a>

                    <a href="cart.html" class="btn btn-warning btn-sm nav-icon-btn">
                        🛒 Giỏ hàng
                    </a>

                    ${authHtml}

                </div>
            </div>
        </nav>
    `;
}

function logout() {
    localStorage.removeItem("user");
    localStorage.removeItem("cart");
    window.location.href = "login.html";
}

renderNavbar();