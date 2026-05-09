async function checkout() {
    const user = JSON.parse(localStorage.getItem("user"));

    if (!user) {
        Swal.fire({
            icon: "warning",
            title: "Vui lòng đăng nhập trước khi đặt hàng"
        });

        return;
    }

    const cartLocal = JSON.parse(localStorage.getItem("cart")) || [];

    const cart = cartLocal.map(item => ({
        id: item.id,
        price: item.price,
        quantity: item.quantityCart
    }));

    const response = await fetch(`${API_BASE_URL}/bdh/orders/checkout`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            userId: user.id,
            receiver: document.getElementById("receiver").value,
            phone: document.getElementById("phone").value,
            address: document.getElementById("address").value,
            paymentMethod: document.getElementById("paymentMethod").value,
            cart: cart
        })
    });

    const data = await response.json();

    if (data.success) {
        localStorage.removeItem("cart");

        Swal.fire({
            icon: "success",
            title: data.message
        });

        setTimeout(() => {
            window.location.href = "index.html";
        }, 1500);
    }
}