// ==============================
// FILE: cart.js
// CHỨC NĂNG:
// - Hiển thị giỏ hàng
// - Cập nhật số lượng
// - Xóa sản phẩm khỏi giỏ
// ==============================

async function loadCart() {
    const cartBody = document.getElementById("cartBody");
    const totalBox = document.getElementById("totalBox");

    try {
        const response = await fetch(`${API_BASE_URL}/cart/${CURRENT_USER_ID}`);
        const result = await response.json();

        cartBody.innerHTML = "";

        let grandTotal = 0;

        result.data.forEach(item => {
            grandTotal += Number(item.total);

            cartBody.innerHTML += `
                <tr>
                    <td>
                        <img src="../assets/images/products/${item.image || 'default.jpg'}"
                             width="70">
                    </td>

                    <td>${item.product_name}</td>

                    <td>${Number(item.price).toLocaleString()} VNĐ</td>

                    <td>
                        <input type="number" min="1" value="${item.quantity}"
                               class="form-control"
                               onchange="updateCart(${item.cart_detail_id}, this.value)">
                    </td>

                    <td>${Number(item.total).toLocaleString()} VNĐ</td>

                    <td>
                        <button class="btn btn-danger btn-sm"
                                onclick="deleteCartItem(${item.cart_detail_id})">
                            Xóa
                        </button>
                    </td>
                </tr>
            `;
        });

        totalBox.innerHTML = `
            Tổng tiền: ${grandTotal.toLocaleString()} VNĐ
        `;

    } catch (error) {
        cartBody.innerHTML = `
            <tr>
                <td colspan="6" class="text-danger">
                    Không tải được giỏ hàng
                </td>
            </tr>
        `;
        console.error(error);
    }
}

async function updateCart(cartDetailId, quantity) {
    await fetch(`${API_BASE_URL}/cart/update/${cartDetailId}`, {
        method: "PUT",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ quantity: quantity })
    });

    loadCart();
}

async function deleteCartItem(cartDetailId) {
    if (!confirm("Bạn có chắc muốn xóa sản phẩm này?")) return;

    await fetch(`${API_BASE_URL}/cart/delete/${cartDetailId}`, {
        method: "DELETE"
    });

    loadCart();
}

loadCart();