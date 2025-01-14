function sendWithdraw() {
    const userId = getCookie("id");
    const amountString = document.getElementById("amountWithdraw").value.trim();
    const amount = parseFloat(amountString);
    if (!userId || isNaN(amount) || amount <= 0) {
        alert("Please provide a valid user ID and a positive amount.");
        return;
    }

    const payload = {
        user_id: userId,
        amount: amount
    };

    fetch("/withdraw", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(payload)
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            alert(data.error);
        } else {
            alert(data.message);
        }
    })
    .catch(error => {
        console.error("Error:", error);
        alert("An error occurred. Please try again later.");
    });
    alert('Withdraw Successful!')
}

function getCookie(name) {
    let value = `; ${document.cookie}`;
    let parts = value.split(`; ${name}=`);
    if (parts.length === 2) {
        let cookieValue = parts.pop().split(';').shift();
        return cookieValue;
    }
    return null;
}
