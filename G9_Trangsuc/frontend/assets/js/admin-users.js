async function loadUsers() {
    const response = await fetch(`${API_BASE_URL}/bdh/users/`);
    const users = await response.json();

    let html = "";

    users.forEach(user => {
        html += `
            <tr>
                <td>${user.id}</td>
                <td>${user.name}</td>
                <td>${user.username}</td>
                <td>${user.email}</td>
                <td>${user.phone}</td>
                <td>${user.role}</td>
                <td>${user.status}</td>
                <td>
                    <select class="form-control" onchange="updateUserStatus(${user.id}, this.value)">
                        <option value="">Chọn</option>
                        <option value="Hoạt động">Hoạt động</option>
                        <option value="Khóa">Khóa</option>
                    </select>
                </td>
            </tr>
        `;
    });

    document.getElementById("user-body").innerHTML = html;
}

async function updateUserStatus(id, status) {
    if (!status) return;

    const response = await fetch(`${API_BASE_URL}/bdh/users/update-status/${id}`, {
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

    loadUsers();
}

loadUsers();