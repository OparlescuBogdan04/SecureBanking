function displayUsers() {
    document.getElementById("transactionsTableContainer").style.display = "none";
    document.getElementById("ticketsTableContainer").style.display = "none";
    document.getElementById("refundTransactionForm").style.display = "none";

    const usersTableContainer = document.getElementById("usersTableContainer");
    usersTableContainer.style.display = 'block';

    fetchUsers()
        .then(data => {
            const usersTableBody = document.getElementById("usersTable").getElementsByTagName('tbody')[0];
            usersTableBody.innerHTML = '';
            data.forEach(user => {
                const row = usersTableBody.insertRow();
                row.innerHTML = `
                    <td>${user.id}</td>
                    <td>${user.name}</td>
                    <td>${user.role === 1 ? 'Admin' : 'User'}</td>
                    <td>${user.balance}</td>
                `;
            });
        })
        .catch(error => {
            console.error("Error fetching users:", error);
            alert("An error occurred while fetching users.");
        });
}

function displayTransactions() {
    document.getElementById("usersTableContainer").style.display = "none";
    document.getElementById("ticketsTableContainer").style.display = "none";
    document.getElementById("refundTransactionForm").style.display = "none";

    const transactionsTableContainer = document.getElementById("transactionsTableContainer");
    transactionsTableContainer.style.display = 'block';

    fetchTransactions()
        .then(data => {
            const transactionsTableBody = document.getElementById("transactionsTable").getElementsByTagName('tbody')[0];
            transactionsTableBody.innerHTML = '';
            data.forEach(transaction => {
                const row = transactionsTableBody.insertRow();
                row.innerHTML = `
                    <td>${transaction.id}</td>
                    <td>${transaction.sender}</td>
                    <td>${transaction.receiver}</td>
                    <td>${transaction.amount}</td>
                    <td>${transaction.status}</td>
                    <td>${transaction.timestamp}</td>
                `;
            });
        })
        .catch(error => {
            console.error("Error fetching transactions:", error);
            alert("An error occurred while fetching transactions.");
        });
}

function displayTickets() {
    document.getElementById("usersTableContainer").style.display = "none";
    document.getElementById("transactionsTableContainer").style.display = "none";
    document.getElementById("refundTransactionForm").style.display = "none";

    const ticketsTableContainer = document.getElementById("ticketsTableContainer");
    ticketsTableContainer.style.display = 'block';

    fetchTickets()
        .then(data => {
            const ticketsTableBody = document.getElementById("ticketsTable").getElementsByTagName('tbody')[0];
            ticketsTableBody.innerHTML = '';
            data.forEach(ticket => {
                const row = ticketsTableBody.insertRow();
                row.innerHTML = `
                    <td>${ticket.id}</td>
                    <td>${ticket.user_id}</td>
                    <td>${ticket.transaction_id}</td>
                    <td>${ticket.reason}</td>
                    <td>${ticket.status}</td>
                `;
            });
        })
        .catch(error => {
            console.error("Error fetching tickets:", error);
            alert("An error occurred while fetching tickets.");
        });
}

function fetchUsers() {
    return fetch("/admin/users")
        .then(response => response.json())
        .catch(error => { throw error });
}

function fetchTransactions() {
    return fetch("/admin/transactions")
        .then(response => response.json())
        .catch(error => { throw error });
}

function fetchTickets() {
    return fetch("/admin/tickets")
        .then(response => response.json())
        .catch(error => { throw error });
}

function displayRefund()
{
    document.getElementById("usersTableContainer").style.display = "none";
    document.getElementById("transactionsTableContainer").style.display = "none";
    document.getElementById("ticketsTableContainer").style.display = "none";

    const refundTransactionForm = document.getElementById("refundTransactionForm");
    refundTransactionForm.style.display = 'block';
}

function refundTransaction() {
    const transactionId = document.getElementById("transactionIdInput").value;

    if (!transactionId) {
        alert("Please provide a transaction ID.");
        return;
    }

    fetch("/admin/refund_transaction", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ transaction_id: transactionId })
    })
    .then(response => response.json())
    .then(data => {
        alert(data.message);
        displayTransactions();
    })
    .catch(error => {
        console.error("Error refunding transaction:", error);
        alert("An error occurred while refunding the transaction.");
    });
}
document.getElementById("refundTransactionButton").addEventListener("click", refundTransaction);


document.getElementById("viewUsersButton").onclick = displayUsers;
document.getElementById("viewTransactionsButton").onclick = displayTransactions;
document.getElementById("viewTicketsButton").onclick = displayTickets;
document.getElementById("viewRefundButton").onclick = displayRefund;
