async function loadHomeProducts() {
    const response = await fetch(`${API_BASE_URL}/products/`);
    const products = await response.json();

    let html = "";

    products.slice(0, 6).forEach(product => {
        html += `
            <div class="col-md-4 mb-4">
                <div class="card product-card h-100">

                    <img src="../assets/images/${product.image}" class="card-img-top">

                    <div class="card-body">
                        <h5>${product.name}</h5>

                        <p>Chất liệu: ${product.material || "Đang cập nhật"}</p>

                        <p class="product-price">
                            ${formatMoney(product.price)}
                        </p>

                        <button onclick='addToCart(${JSON.stringify(product)})'
                                class="btn btn-warning btn-sm">
                            🛒 Thêm giỏ hàng
                        </button>
                    </div>

                </div>
            </div>
        `;
    });

    document.getElementById("product-list").innerHTML = html;
}

async function loadHomeGold() {
    const response = await fetch(`${API_BASE_URL}/gold/latest`);
    const prices = await response.json();

    let html = "";

    prices.slice(0, 3).forEach(item => {
        html += `
            <div class="col-md-4 mb-4">
                <div class="card product-card">
                    <div class="card-body">
                        <h5 class="text-warning">🪙 ${item.type}</h5>
                        <p>Giá mua: <strong>${formatMoney(item.buyPrice)}</strong></p>
                        <p>Giá bán: <strong>${formatMoney(item.sellPrice)}</strong></p>
                    </div>
                </div>
            </div>
        `;
    });

    document.getElementById("gold-list").innerHTML = html;
}

async function loadHomeNews() {
    const response = await fetch(`${API_BASE_URL}/news/`);
    const news = await response.json();

    let html = "";

    news.slice(0, 3).forEach(item => {
        html += `
            <div class="col-md-4 mb-4">
                <div class="card product-card h-100">

                    <img src="../assets/images/${item.image}" class="card-img-top">

                    <div class="card-body">
                        <h5>${item.title}</h5>
                        <p>${item.shortDescription || ""}</p>
                    </div>

                </div>
            </div>
        `;
    });

    document.getElementById("news-list").innerHTML = html;
}

function addToCart(product) {
    let cart = getCart();

    const existed = cart.find(item => item.id === product.id);

    if (existed) {
        existed.quantityCart += 1;
    } else {
        product.quantityCart = 1;
        cart.push(product);
    }

    saveCart(cart);
    alert("Đã thêm vào giỏ hàng");
}

loadHomeProducts();
loadHomeGold();
loadHomeNews();