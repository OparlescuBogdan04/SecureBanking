function setCookie(name, value, days) {
    const expires = new Date();
    expires.setTime(expires.getTime() + days * 24 * 60 * 60 * 1000);
    document.cookie = `${name}=${value};expires=${expires.toUTCString()};path=/`;
}

function getCookie(name) {
    const nameEQ = `${name}=`;
    const ca = document.cookie.split(';');
    for (let c of ca) {
        while (c.charAt(0) === ' ') c = c.substring(1);
        if (c.indexOf(nameEQ) === 0) return c.substring(nameEQ.length, c.length);
    }
    return null;
}

async function handleLogin() {
    const username = document.getElementById("loginUsername").value;
    const password = document.getElementById("loginPassword").value;
    try {
        const response = await fetch("/login", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
                username,
                password,
            }),
        });

        if (response.ok) {
            const data = await response.json();

            setCookie("role", data.role, 7);
            setCookie("token", data.token, 7);
            setCookie("username", data.username, 7);
            setCookie("id", data.id, 7);
            setCookie("balance", data.balance, 7);

            navigateTo("dashboard");
            return;
        }
        alert("Invalid login. Please try again.");
    } catch (error) {
        console.error("Login error:", error);
        alert("An error occurred during login.");
    }
}

async function handleRegister() {
    const username = document.getElementById("registerUsername").value;
    const password = document.getElementById("registerPassword").value;
    try {
        const response = await fetch("/register", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
                username,
                password,
            }),
        });

        if (response.ok) {
            const data = await response.json();
            alert("Registration successful! Please login.");
        } else {
            const error = await response.json();
            if (error.message)
                alert(`Registration failed: ${error.message}`);
            else
                alert("Registration failed: Unknown error.");
        }
    } catch (error) {
        console.error("Registration error:", error);

        if (error instanceof TypeError)
            alert("Network error: Please check your internet connection.");
        else if (error.message.includes("database"))
            alert("Database error: There was an issue with saving your information. Please try again later.");
        else
            alert("An unexpected error occurred during registration.");
    }
}

function navigateTo(page) {
    const role = getCookie("role");

    if (page === "main") {
        window.location.href = "main-dashboard.html";
    } else if (page === "dashboard") {
        if (role === "admin")
            window.location.href = "admin-dashboard.html";
        else
            window.location.href = "user-dashboard.html";
    }
}
