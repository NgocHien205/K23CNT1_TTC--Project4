let newsData = [];

function getNewsBadge(status) {
    if (status === "Hiển thị") return "bg-success";
    if (status === "Ẩn") return "bg-secondary";

    return "bg-dark";
}

async function loadNewsCategories() {
    const response = await fetch(`${API_BASE_URL}/bdh/news/categories`);
    const categories = await response.json();

    let html = "";

    categories.forEach(item => {
        html += `
            <option value="${item.id}">
                ${item.name}
            </option>
        `;
    });

    document.getElementById("categoryId").innerHTML = html;
}

async function loadAdminNews() {
    const response = await fetch(`${API_BASE_URL}/bdh/news/`);
    const news = await response.json();

    newsData = news;

    let html = "";

    news.forEach(item => {
        html += `
            <tr>
                <td>#${item.id}</td>

                <td>
                    <img src="../assets/img/${item.image}"
                         width="80"
                         height="60"
                         style="object-fit:cover; border-radius:8px;">
                </td>

                <td>
                    <strong>${item.title}</strong>
                    <br>
                    <small>${item.shortDescription || ""}</small>
                </td>

                <td>
                    ${item.category || ""}
                </td>

                <td>
                    ${item.author || ""}
                </td>

                <td>
                    <span class="badge ${getNewsBadge(item.status)}">
                        ${item.status}
                    </span>
                </td>

                <td>
                    ${formatDate(item.createdAt)}
                </td>

                <td>
                    <button onclick="editNews(${item.id})" class="btn btn-warning btn-sm">
                        Sửa
                    </button>

                    <button onclick="hideNews(${item.id})" class="btn btn-secondary btn-sm">
                        Ẩn
                    </button>

                    <button onclick="deleteNews(${item.id})" class="btn btn-danger btn-sm">
                        Xóa
                    </button>
                </td>
            </tr>
        `;
    });

    document.getElementById("news-body").innerHTML = html;
}

function editNews(id) {
    const item = newsData.find(x => x.id === id);

    document.getElementById("newsId").value = item.id;
    document.getElementById("title").value = item.title;
    document.getElementById("shortDescription").value = item.shortDescription || "";
    document.getElementById("content").value = item.content || "";
    document.getElementById("image").value = item.image || "";
    document.getElementById("status").value = item.status || "Hiển thị";
}

async function saveNews() {
    const id = document.getElementById("newsId").value;
    const user = getUser();

    const data = {
        title: document.getElementById("title").value,
        shortDescription: document.getElementById("shortDescription").value,
        content: document.getElementById("content").value,
        image: document.getElementById("image").value,
        categoryId: Number(document.getElementById("categoryId").value),
        status: document.getElementById("status").value,
        userId: user ? user.id : 1
    };

    let url = `${API_BASE_URL}/bdh/news/create`;
    let method = "POST";

    if (id) {
        url = `${API_BASE_URL}/bdh/news/update/${id}`;
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

    resetNewsForm();
    loadAdminNews();
}

async function hideNews(id) {
    const response = await fetch(`${API_BASE_URL}/bdh/news/update-status/${id}`, {
        method: "PUT",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            status: "Ẩn"
        })
    });

    const result = await response.json();

    alert(result.message);

    loadAdminNews();
}

async function deleteNews(id) {
    if (!confirm("Bạn có chắc muốn xóa tin tức này?")) {
        return;
    }

    const response = await fetch(`${API_BASE_URL}/bdh/news/delete/${id}`, {
        method: "DELETE"
    });

    const result = await response.json();

    alert(result.message);

    loadAdminNews();
}

function resetNewsForm() {
    document.getElementById("newsId").value = "";
    document.getElementById("title").value = "";
    document.getElementById("shortDescription").value = "";
    document.getElementById("content").value = "";
    document.getElementById("image").value = "";
    document.getElementById("status").value = "Hiển thị";
}

function formatDate(dateString) {
    const date = new Date(dateString);

    if (isNaN(date.getTime())) {
        return dateString;
    }

    return date.toLocaleString("vi-VN");
}

loadNewsCategories();
loadAdminNews();