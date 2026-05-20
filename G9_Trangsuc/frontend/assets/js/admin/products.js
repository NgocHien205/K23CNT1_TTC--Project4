// ==============================
// FILE: admin/products.js
// CHỨC NĂNG:
// - Hiển thị danh sách sản phẩm
// - Thêm sản phẩm
// ==============================

async function loadAdminProducts() {
    const tbody = document.getElementById("productTable");

    try {
        const response = await fetch(`${API_BASE_URL}/products/`);
        const result = await response.json();

        tbody.innerHTML = "";

        result.data.forEach(product => {
            tbody.innerHTML += `
                <tr>
                    <td>${product.id}</td>
                    <td>
                        <img src="../assets/images/products/${product.image || 'default.jpg'}" width="60">
                    </td>
                    <td>${product.name}</td>
                    <td>${Number(product.price).toLocaleString()} VNĐ</td>
                    <td>${product.quantity}</td>
                    <td>${product.category_name || ""}</td>
                    <td>${product.status || ""}</td>
                    <td>
                        <button class="btn btn-sm btn-warning">Sửa</button>
                        <button class="btn btn-sm btn-danger">Xóa</button>
                    </td>
                </tr>
            `;
        });

    } catch (error) {
        tbody.innerHTML = `
            <tr>
                <td colspan="8" class="text-danger">Không tải được sản phẩm</td>
            </tr>
        `;
        console.error(error);
    }
}


// ==============================
// LOAD DANH MỤC VÀO SELECT
// ==============================
async function loadCategoriesToSelect() {
    const select = document.getElementById("categoryId");

    const response = await fetch(`${API_BASE_URL}/categories/`);
    const result = await response.json();

    select.innerHTML = `<option value="">-- Chọn danh mục --</option>`;

    result.data.forEach(category => {
        select.innerHTML += `
            <option value="${category.id}">
                ${category.name}
            </option>
        `;
    });
}


// ==============================
// THÊM SẢN PHẨM
// ==============================
const productForm = document.getElementById("productForm");

productForm.addEventListener("submit", async function (e) {
    e.preventDefault();

    const data = {
        name: document.getElementById("name").value,
        category_id: document.getElementById("categoryId").value,
        material: document.getElementById("material").value,
        price: document.getElementById("price").value,
        quantity: document.getElementById("quantity").value,
        image: document.getElementById("image").value,
        description: document.getElementById("description").value
    };

    const response = await fetch(`${API_BASE_URL}/products/`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(data)
    });

    const result = await response.json();

    alert(result.message);

    productForm.reset();
    loadAdminProducts();
});

loadAdminProducts();
loadCategoriesToSelect();