function loadCart() {
    const cart = getCart();

    let html = "";
    let total = 0;

    cart.forEach((item, index) => {
        const money = item.price * item.quantityCart;
        total += money;

        html += `
            <tr>
                <td>
                    <strong>${item.name}</strong>
                </td>

                <td>${formatMoney(item.price)}</td>

                <td>${item.quantityCart}</td>

                <td class="text-danger fw-bold">
                    ${formatMoney(money)}
                </td>

                <td>
                    <button onclick="removeCartItem(${index})" class="btn btn-danger btn-sm">
                        Xóa
                    </button>
                </td>
            </tr>
        `;
    });

    document.getElementById("cart-body").innerHTML = html;
    document.getElementById("cart-total").innerText =
        "Tổng tiền: " + formatMoney(total);
}

function removeCartItem(index) {
    const cart = getCart();

    cart.splice(index, 1);

    saveCart(cart);

    loadCart();
}

loadCart();