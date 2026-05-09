function loadCart() {
    const cart = JSON.parse(localStorage.getItem("cart")) || [];

    let html = "";
    let total = 0;

    cart.forEach(item => {
        const money = item.price * item.quantityCart;
        total += money;

        html += `
            <tr>
                <td>${item.name}</td>
                <td>${item.price.toLocaleString()} VNĐ</td>
                <td>${item.quantityCart}</td>
                <td>${money.toLocaleString()} VNĐ</td>
            </tr>
        `;
    });

    document.getElementById("cart-body").innerHTML = html;
    document.getElementById("cart-total").innerText =
        "Tổng tiền: " + total.toLocaleString() + " VNĐ";
}

loadCart();