let goldData = [];

async function loadGoldAdmin() {
    const response = await fetch(`${API_BASE_URL}/bdh/gold/`);
    const goldList = await response.json();

    goldData = goldList;

    let html = "";

    goldList.forEach(item => {
        html += `
            <tr>
                <td>#${item.id}</td>

                <td>
                    <strong>${item.type}</strong>
                </td>

                <td class="text-success fw-bold">
                    ${formatMoney(item.buyPrice)}
                </td>

                <td class="text-danger fw-bold">
                    ${formatMoney(item.sellPrice)}
                </td>

                <td>
                    ${formatDate(item.updatedAt)}
                </td>

                <td>
                    <button onclick="editGold(${item.id})" class="btn btn-warning btn-sm">
                        Sửa
                    </button>

                    <button onclick="deleteGold(${item.id})" class="btn btn-danger btn-sm">
                        Xóa
                    </button>
                </td>
            </tr>
        `;
    });

    document.getElementById("gold-body").innerHTML = html;
}

function editGold(id) {
    const item = goldData.find(x => x.id === id);

    document.getElementById("goldId").value = item.id;
    document.getElementById("type").value = item.type;
    document.getElementById("buyPrice").value = item.buyPrice;
    document.getElementById("sellPrice").value = item.sellPrice;
}

async function saveGold() {
    const id = document.getElementById("goldId").value;

    const data = {
        type: document.getElementById("type").value,
        buyPrice: Number(document.getElementById("buyPrice").value),
        sellPrice: Number(document.getElementById("sellPrice").value)
    };

    let url = `${API_BASE_URL}/bdh/gold/create`;
    let method = "POST";

    if (id) {
        url = `${API_BASE_URL}/bdh/gold/update/${id}`;
        method = "PUT";
    }

    const response = await fetch(url, {
        method: method,
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(data)
    });

    const result = await response.json();

    alert(result.message);

    resetGoldForm();
    loadGoldAdmin();
}

async function deleteGold(id) {
    if (!confirm("Bạn có chắc muốn xóa giá vàng này?")) {
        return;
    }

    const response = await fetch(`${API_BASE_URL}/bdh/gold/delete/${id}`, {
        method: "DELETE"
    });

    const result = await response.json();

    alert(result.message);

    loadGoldAdmin();
}

function resetGoldForm() {
    document.getElementById("goldId").value = "";
    document.getElementById("type").value = "";
    document.getElementById("buyPrice").value = "";
    document.getElementById("sellPrice").value = "";
}

function formatDate(dateString) {
    const date = new Date(dateString);

    if (isNaN(date.getTime())) {
        return dateString;
    }

    return date.toLocaleString("vi-VN");
}

loadGoldAdmin();