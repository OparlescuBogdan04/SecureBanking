function sendTicket() {

    const description = document.getElementById("ticketDescription").value.trim();
    const transactionId = document.getElementById("transactionId").value.trim() || getCookie("transaction_id");
    const userId = getCookie("id");

    if (!description) {
        alert("Please enter a description.");
        return;
    }

    if (!userId) {
        alert("User ID is missing. Please log in. AAAA");
        return;
    }

    if (!transactionId) {
        alert("Transaction ID is missing. Please provide a transaction ID.");
        return;
    }

    const ticketData = {
        reason: description,
        transaction_id: transactionId,
        user_id: userId,
    };

    fetch("/tickets", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify(ticketData),
    })
    .then(response => response.json())
    .then(data => {
        console.log("Ticket Created:", data.ticket);
        alert(data.message);
        document.getElementById("ticketForm").style.display = "none";
    })
    .catch(error => {
        console.error("Error creating ticket:", error);
        alert("Failed to create ticket. Please try again.");
    });
}

function getCookie(name) {
    alert('Getting cookie: ' + name);
    let value = `; ${document.cookie}`;
    let parts = value.split(`; ${name}=`);
    if (parts.length === 2) {
        let cookieValue = parts.pop().split(';').shift();
        alert(`Cookie ${name}: ` + cookieValue);
        return cookieValue;
    }
    alert(`Cookie ${name} not found.`);
    return null;
}

function setUserCookie(userId) {
    setCookie("id", userId, 7);
}

function setTransactionCookie(transactionId) {
    setCookie("transaction_id", transactionId, 7);
}

function setCookie(name, value, days) {
    const expires = new Date();
    expires.setTime(expires.getTime() + (days * 24 * 60 * 60 * 1000));
    document.cookie = `${name}=${value};expires=${expires.toUTCString()};path=/`;
}
