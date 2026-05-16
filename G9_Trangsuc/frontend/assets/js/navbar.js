function renderNavbar() {

    const user = getUser();

    let authHtml = "";

    if (user) {

        authHtml = `
            <a href="profile.html" class="btn btn-outline-light btn-sm me-2">
                ${user.name}
            </a>

            <button onclick="logout()" class="btn btn-danger btn-sm">
                Đăng xuất
            </button>
        `;

    } else {

        authHtml = `
            <a href="login.html" class="btn btn-light btn-sm me-2">
                Đăng nhập
            </a>

            <a href="register.html" class="btn btn-warning btn-sm">
                Đăng ký
            </a>
        `;
    }

    const navbar = `
        <nav class="navbar navbar-expand-lg navbar-dark bg-dark shadow">

            <div class="container">

                <a class="navbar-brand text-warning fw-bold fs-3"
                   href="index.html">

                    G9 Trang Sức

                </a>

                <button class="navbar-toggler"
                        data-bs-toggle="collapse"
                        data-bs-target="#menu">

                    <span class="navbar-toggler-icon"></span>

                </button>

                <div class="collapse navbar-collapse" id="menu">

                    <ul class="navbar-nav me-auto">

                        <li class="nav-item">
                            <a class="nav-link" href="index.html">
                                Trang chủ
                            </a>
                        </li>

                        <li class="nav-item">
                            <a class="nav-link" href="products.html">
                                Sản phẩm
                            </a>
                        </li>

                        <li class="nav-item">
                            <a class="nav-link" href="gold-price.html">
                                Giá vàng
                            </a>
                        </li>

                        <li class="nav-item">
                            <a class="nav-link" href="news.html">
                                Tin tức
                            </a>
                        </li>

                    </ul>

                    <a href="cart.html"
                       class="btn btn-warning btn-sm me-3">

                        Giỏ hàng

                    </a>
                    <a href="wishlist.html" class="btn btn-outline-danger btn-sm me-2">
                        Yêu thích
                    </a>

                    ${authHtml}

                </div>

            </div>

        </nav>
    `;

    document.getElementById("navbar").innerHTML = navbar;
}

renderNavbar();