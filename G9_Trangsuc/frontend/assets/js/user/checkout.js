// ==============================
// FILE: checkout.js
// CHỨC NĂNG:
// - Gửi thông tin thanh toán
// - Tạo đơn hàng từ giỏ hàng
// ==============================

const checkoutForm = document.getElementById("checkoutForm");

checkoutForm.addEventListener("submit", async function (e) {
    e.preventDefault();

    const receiverName = document.getElementById("receiverName").value;
    const phone = document.getElementById("phone").value;
    const address = document.getElementById("address").value;
    const paymentMethod = document.getElementById("paymentMethod").value;

    try {
        const response = await fetch(`${API_BASE_URL}/orders/checkout`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                user_id: CURRENT_USER_ID,
                receiver_name: receiverName,
                phone: phone,
                address: address,
                payment_method: paymentMethod
            })
        });

        const result = await response.json();

        if (result.success) {
            alert("Đặt hàng thành công");
            window.location.href = `payment-success.html?order_id=${result.order_id}`;
        } else {
            alert(result.message);
        }

    } catch (error) {
        alert("Lỗi khi đặt hàng");
        console.error(error);
    }
});