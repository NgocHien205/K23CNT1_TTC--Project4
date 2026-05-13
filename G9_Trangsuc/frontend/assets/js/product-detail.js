const params = new URLSearchParams(window.location.search);
const productId = params.get("id");

let currentProduct = null;

async function loadProductDetail() {
    const response = await fetch(`${API_BASE_URL}/bdh/products/${productId}`);
    const product = await response.json();

    currentProduct = product;

    document.getElementById("product-image").src = `assets/img/${product.image}`;
    document.getElementById("product-name").innerText = product.name;
    document.getElementById("product-price").innerText = formatMoney(product.price);
    document.getElementById("product-material").innerText = "Chất liệu: " + product.material;
    document.getElementById("product-description").innerText = product.description;
}

document.getElementById("btn-cart").addEventListener("click", function () {
    let cart = getCart();

    const existing = cart.find(item => item.id === currentProduct.id);

    if (existing) {
        existing.quantityCart += 1;
    } else {
        currentProduct.quantityCart = 1;
        cart.push(currentProduct);
    }

    saveCart(cart);

    alert("Đã thêm vào giỏ hàng");
});

loadProductDetail();