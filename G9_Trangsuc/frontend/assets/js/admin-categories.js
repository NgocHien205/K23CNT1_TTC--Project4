async function loadCategories() {
    const response = await fetch(`${API_BASE_URL}/bdh/categories/`);
    const categories = await response.json();

    let html = "";

    categories.forEach(item => {
        html += `
            <tr>
                <td>${item.id}</td>
                <td>${item.name}</td>
                <td>${item.description || ""}</td>
                <td>${item.parentId || "Không có"}</td>
                <td>${item.status}</td>
                <td>
                    <button onclick="deleteCategory(${item.id})" class="btn btn-danger btn-sm">
                        Xóa
                    </button>
                </td>
            </tr>
        `;
    });

    document.getElementById("category-body").innerHTML = html;
}

async function createCategory() {
    const parentValue = document.getElementById("parentId").value;

    const data = {
        name: document.getElementById("name").value,
        description: document.getElementById("description").value,
        parentId: parentValue === "" ? null : Number(parentValue)
    };

    const response = await fetch(`${API_BASE_URL}/bdh/categories/create`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(data)
    });

    const result = await response.json();

    alert(result.message);

    loadCategories();
}

async function deleteCategory(id) {
    if (!confirm("Bạn có chắc muốn xóa danh mục này?")) {
        return;
    }

    const response = await fetch(`${API_BASE_URL}/bdh/categories/delete/${id}`, {
        method: "DELETE"
    });

    const result = await response.json();

    alert(result.message);

    loadCategories();
}

loadCategories();