function handleLogin() {
    const username = document.getElementById("username").value;

    if (username === "admin") {
        window.localStorage.setItem("role", "admin");
        window.location.href = "admin-dashboard.html";
    } else {
        window.localStorage.setItem("role", "user");
        window.location.href = "user-dashboard.html";
    }
}

function navigateTo(page) {
    const role = window.localStorage.getItem("role");
    if (page === "main") {
        window.location.href = "main-dashboard.html";
    } else if (page === "dashboard") {
        if (role === "admin") {
            window.location.href = "admin-dashboard.html";
        } else {
            window.location.href = "user-dashboard.html";
        }
    }
}
