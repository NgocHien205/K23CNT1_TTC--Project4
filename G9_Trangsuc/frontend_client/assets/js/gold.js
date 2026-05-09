async function loadGoldPrices() {
    const response = await fetch(`${API_BASE_URL}/bdh/gold/latest`);
    const prices = await response.json();

    let html = "";

    prices.forEach(item => {
        html += `
            <div class="col-md-4 mb-3">
                <div class="card border-warning">
                    <div class="card-body">
                        <h5>${item.type}</h5>
                        <p>Giá mua: ${item.buyPrice.toLocaleString()} VNĐ</p>
                        <p>Giá bán: ${item.sellPrice.toLocaleString()} VNĐ</p>
                        <small>Cập nhật: ${item.updatedAt}</small>
                    </div>
                </div>
            </div>
        `;
    });

    const goldList = document.getElementById("gold-list");

    if (goldList) {
        goldList.innerHTML = html;
    }
}

loadGoldPrices();