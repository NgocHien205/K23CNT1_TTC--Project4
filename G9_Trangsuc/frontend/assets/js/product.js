async function loadProducts() {

    const response = await fetch(
        `${API_BASE_URL}/bdh/products/`
    );

    const products = await response.json();

    let html = "";

    products.forEach(product => {

        html += `

            <div class="col-md-4 mb-4">

                <div class="card h-100 shadow-sm">

                    <img src="assets/img/${product.image}"
                         class="card-img-top">

                    <div class="card-body">

                        <h5>${product.name}</h5>

                        <p>
                            ${product.material}
                        </p>

                        <p class="product-price">
                            ${formatMoney(product.price)}
                        </p>

                        <button class="btn btn-dark w-100">
                            Xem chi tiết
                        </button>

                    </div>

                </div>

            </div>
        `;
    });

    document.getElementById(
        "product-list"
    ).innerHTML = html;
}

loadProducts();