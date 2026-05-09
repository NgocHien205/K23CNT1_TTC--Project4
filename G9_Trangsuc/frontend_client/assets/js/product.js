async function loadProducts() {
    const response = await fetch(`${API_BASE_URL}/bdh/products/`);
    const products = await response.json();

    let html = "";

    products.forEach(product => {
        html += `
            <div class="col-md-4 mb-4">
                <div class="card h-100">
                    <img src="assets/img/${product.image}" class="card-img-top" style="height:250px; object-fit:cover;">

                    <div class="card-body">
                        <h5>${product.name}</h5>
                        <p>Chất liệu: ${product.material}</p>
                        <p class="text-danger fw-bold">${product.price.toLocaleString()} VNĐ</p>

                        <a href="product-detail.html?id=${product.id}" class="btn btn-dark btn-sm">
                            Xem chi tiết
                        </a>

                        <button onclick='addToCart(${JSON.stringify(product)})' class="btn btn-warning btn-sm">
                            Thêm giỏ hàng
                        </button>
                    </div>
                </div>
            </div>
        `;
    });

    const productList = document.getElementById("product-list");

    if (productList) {
        productList.innerHTML = html;
    }
}

function addToCart(product) {
    let cart = JSON.parse(localStorage.getItem("cart")) || [];

    const existing = cart.find(item => item.id === product.id);

    if (existing) {
        existing.quantityCart += 1;
    } else {
        product.quantityCart = 1;
        cart.push(product);
    }

    localStorage.setItem("cart", JSON.stringify(cart));

    alert("Đã thêm vào giỏ hàng");
}

loadProducts();