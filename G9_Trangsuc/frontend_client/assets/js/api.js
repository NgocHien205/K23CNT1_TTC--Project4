async function loadProducts() {

    const response =
        await fetch("http://127.0.0.1:5000/api/bdh/products/");

    const products = await response.json();

    let html = "";

    products.forEach(product => {

        html += `
            <div class="col-md-4">
                <div class="card mb-3">

                    <img src="../assets/img/${product.image}"
                         class="card-img-top">

                    <div class="card-body">

                        <h5>${product.name}</h5>

                        <p>${product.price} VNĐ</p>

                    </div>

                </div>
            </div>
        `;
    });

    document.getElementById("product-list").innerHTML = html;
}

loadProducts();