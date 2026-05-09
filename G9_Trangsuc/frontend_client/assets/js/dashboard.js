async function loadDashboard() {
    const response = await fetch(`${API_BASE_URL}/bdh/dashboard/statistics`);
    const data = await response.json();

    document.getElementById("product-count").innerText = data.products;
    document.getElementById("order-count").innerText = data.orders;
    document.getElementById("user-count").innerText = data.users;
    document.getElementById("news-count").innerText = data.news;

    document.getElementById("revenue").innerText =
        "Tổng doanh thu: " + data.revenue.toLocaleString() + " VNĐ";
}

loadDashboard();