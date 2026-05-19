async function login() {
    const username = document.getElementById("username").value;
    const password = document.getElementById("password").value;

    const response = await fetch(`${API_BASE_URL}/auth/login`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            username,
            password
        })
    });

    const data = await response.json();

    if (data.success) {
        saveUser(data.user);

        if (Number(data.user.roleId) === 1 || Number(data.user.roleId) === 2) {
            window.location.href = "../admin/dashboard.html";
        } else {
            window.location.href = "index.html";
        }
    } else {
        alert(data.message);
    }
}