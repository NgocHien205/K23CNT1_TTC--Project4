async function loadAdminOrders() {
    const response = await fetch(`${API_BASE_URL}/bdh/orders/`);
    const orders = await response.json();

    let html = "";

    orders.forEach(order => {
        html += `
            <tr>
                <td>${order.id}</td>
                <td>${order.customer}</td>
                <td>${formatMoney(order.total)}</td>
                <td>${order.status}</td>
                <td>${order.date}</td>
                <td>
                    <select class="form-control" onchange="updateStatus(${order.id}, this.value)">
                        <option value="">Chọn trạng thái</option>
                        <option value="Chờ xác nhận">Chờ xác nhận</option>
                        <option value="Đã xác nhận">Đã xác nhận</option>
                        <option value="Đang giao">Đang giao</option>
                        <option value="Hoàn thành">Hoàn thành</option>
                        <option value="Đã hủy">Đã hủy</option>
                    </select>
                </td>
            </tr>
        `;
    });

    document.getElementById("admin-order-body").innerHTML = html;
}

async function updateStatus(id, status) {
    if (!status) return;

    const response = await fetch(`${API_BASE_URL}/bdh/orders/update-status/${id}`, {
        method: "PUT",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            status
        })
    });

    const data = await response.json();

    alert(data.message);

    loadAdminOrders();
}

loadAdminOrders();