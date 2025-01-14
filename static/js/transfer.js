function sendTransfer() {
    const senderId = getCookie("id");
    const receiverId = document.getElementById("destinationId").value.trim();
    const amount = document.getElementById("amountTransfer").value.trim();

    if (!senderId || !receiverId || !amount) {
        alert("Please provide all required fields: sender ID, receiver ID, and amount.");
        return;
    }

    if (amount <= 0) {
        alert("Amount must be greater than zero.");
        return;
    }

    const transactionData = {
        sender_id: senderId,
        receiver_id: receiverId,
        amount: amount
    };


    fetch("/transactions", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(transactionData)
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert(data.message);
        } else {
            alert(data.message);
        }
    })
    .catch(error => {
        console.error("Error during transfer:", error);
        alert("Transfer failed. Please try again.");
    });
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
