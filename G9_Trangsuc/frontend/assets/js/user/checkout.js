async function checkout() {
    const user = getUser();

    if (!user) {
        alert("Vui lòng đăng nhập trước khi đặt hàng");
        window.location.href = "login.html";
        return;
    }

    const cart = getCart();

    if (cart.length === 0) {
        alert("Giỏ hàng đang trống");
        return;
    }

    const total = cart.reduce(
        (sum, item) => sum + item.price * item.quantityCart,
        0
    );

    const data = {
        userId: user.id,
        receiver: document.getElementById("receiver").value,
        phone: document.getElementById("phone").value,
        address: document.getElementById("address").value,
        paymentMethod: document.getElementById("paymentMethod").value,
        total: total,
        cart: cart.map(item => ({
            id: item.id,
            price: item.price,
            quantity: item.quantityCart
        }))
    };

    const response = await fetch(`${API_BASE_URL}/orders/create`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(data)
    });

    const result = await response.json();

    if (result.success) {
        clearCart();
        alert("Đặt hàng thành công");
        window.location.href = "index.html";
    } else {
        alert(result.message);
    }
}