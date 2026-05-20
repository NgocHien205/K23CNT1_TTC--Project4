let dashboardChart = null;

async function loadDashboard() {
    try {
        const response = await fetch(
            `${API_BASE_URL}/bdh/dashboard/statistics`
        );

        const data = await response.json();

        document.getElementById("product-count").innerText =
            data.products || 0;

        document.getElementById("order-count").innerText =
            data.orders || 0;

        document.getElementById("user-count").innerText =
            data.users || 0;

        document.getElementById("revenue").innerText =
            formatMoney(data.revenue || 0);

        createChart(data);

    } catch (error) {
        console.error("Lỗi load dashboard:", error);
        alert("Không tải được dữ liệu dashboard");
    }
}

function createChart(data) {
    const ctx = document.getElementById("chart");

    if (dashboardChart) {
        dashboardChart.destroy();
    }

    dashboardChart = new Chart(ctx, {
        type: "bar",

        data: {
            labels: [
                "Sản phẩm",
                "Đơn hàng",
                "Người dùng",
                "Tin tức"
            ],

            datasets: [{
                label: "Thống kê hệ thống",

                data: [
                    data.products || 0,
                    data.orders || 0,
                    data.users || 0,
                    data.news || 0
                ],

                borderWidth: 1,
                borderRadius: 10
            }]
        },

        options: {
            responsive: true,
            plugins: {
                legend: {
                    display: true
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    ticks: {
                        stepSize: 1
                    }
                }
            }
        }
    });
}

loadDashboard();