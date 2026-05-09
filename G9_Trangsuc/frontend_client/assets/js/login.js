async function login() {

    const username =
        document.getElementById("username").value;

    const password =
        document.getElementById("password").value;

    const response = await fetch(
        "http://127.0.0.1:5000/api/nnh/auth/login",
        {
            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                username,
                password
            })
        }
    );

    const data = await response.json();

    alert(data.message);

    if(data.success){

        window.location.href = "index.html";
    }
    Swal.fire({
    icon: "success",
    title: "Đăng nhập thành công"
});
}