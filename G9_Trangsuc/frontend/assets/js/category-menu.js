async function loadCategoryMenu() {
    const response = await fetch(`${API_BASE_URL}/bdh/categories/`);
    const categories = await response.json();

    let html = `
        <li>
            <button class="dropdown-item active"
                    onclick="filterAllProducts()">
                Tất cả danh mục
            </button>
        </li>
    `;

    categories.forEach(item => {
        if (item.status === "Ẩn") {
            return;
        }

        html += `
            <li>
                <button class="dropdown-item"
                        onclick="filterByCategory(${item.id}, '${item.name}')">
                    ${item.name}
                </button>
            </li>
        `;
    });

    document.getElementById("category-dropdown").innerHTML = html;
}

function filterAllProducts() {
    loadProducts();
}

async function filterByCategory(categoryId, categoryName) {
    const response = await fetch(
        `${API_BASE_URL}/bdh/products/category/${categoryId}`
    );

    const products = await response.json();

    renderProducts(products);
}

loadCategoryMenu();