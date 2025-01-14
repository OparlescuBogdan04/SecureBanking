
        function fetchUserDetails() {
            const token = window.localStorage.getItem('token');
            if (!token) {
                alert("You need to log in first!");
                window.location.href = "/login.html";
                return;
            }

            fetch('/user-dashboard', {
                method: 'GET',
                headers: {
                    'Authorization': `Bearer ${token}`,
                }
            })
            .then(response => response.json())
            .then(data => {
                document.getElementById("usernameDisplay").innerText = data.username || "User";
                document.getElementById("userIdDisplay").innerText = data.id || "N/A";
                document.getElementById("userBalanceDisplay").innerText = data.balance || "0.00";

                window.localStorage.setItem("username", data.username);
                window.localStorage.setItem("id", data.id);
                window.localStorage.setItem("balance", data.balance);
            })
            .catch(error => {
                console.error('Error fetching user details:', error);
                alert("Failed to fetch user details. Please try again.");
            });
        }

        window.onload = fetchUserDetails;

        function transferMoney() {
            document.getElementById("transferForm").style.display = 'block';
            document.getElementById("withdrawForm").style.display = 'none';
            document.getElementById("ticketForm").style.display = 'none';
        }

        function withdrawMoney() {
            document.getElementById("transferForm").style.display = 'none';
            document.getElementById("withdrawForm").style.display = 'block';
            document.getElementById("ticketForm").style.display = 'none';
        }

        function fileTicket() {
            document.getElementById("transferForm").style.display = 'none';
            document.getElementById("withdrawForm").style.display = 'none';
            document.getElementById("ticketForm").style.display = 'block';
        }


function setCookie(name, value, days) {
    const expires = new Date();
    expires.setTime(expires.getTime() + (days * 24 * 60 * 60 * 1000));
    document.cookie = `${name}=${value};expires=${expires.toUTCString()};path=/`;
}

function getCookie(name) {
    const nameEQ = name + "=";
    const ca = document.cookie.split(';');
    for (let i = 0; i < ca.length; i++) {
        let c = ca[i];
        while (c.charAt(0) === ' ') c = c.substring(1, c.length);
        if (c.indexOf(nameEQ) === 0) return c.substring(nameEQ.length, c.length);
    }
    return null;
}

function displayUserDetailsFromCookies() {
    const username = getCookie("username");
    const userId = getCookie("id");
    const balance = getCookie("balance");

    document.getElementById("username").innerText = username || "User";
    document.getElementById("usernameDisplay").innerText = username || "User";
    document.getElementById("userIdDisplay").innerText = userId || "N/A";
    document.getElementById("userBalanceDisplay").innerText = balance || "0.00";
}

function loadUserDetails() {
    const username = getCookie("username");
    const userId = getCookie("id");
    const balance = getCookie("balance");

    displayUserDetailsFromCookies();
}

window.onload = fetchUserDetails;
window.onload = loadUserDetails;
