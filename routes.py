from flask import request, jsonify
from app import app, db, bcrypt
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from flask import render_template #for home
from hashlib import md5

BLACKLIST = ['or', 'and', 'like', '--', 'drop', 'delete', ';', "'", '"', "select"]
def filter_input(user_input):
    return all(word not in BLACKLIST for word in user_input.lower().split())


#Home Page
@app.route("/")
def home():
    return render_template("index.html")

#Registration
from sqlalchemy import text

@app.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    existing_user = db.session.execute(
        text("SELECT COUNT(*) AS user_exists FROM user WHERE name = :username"),
        {"username": username}
    ).fetchone()

    if existing_user.user_exists:
        return jsonify({"message": "Username already exists."}), 400

    hashed_password = (bcrypt.generate_password_hash(password).decode('utf-8'))

    db.session.execute(
        text("INSERT INTO user (name, password, role, balance) VALUES (:name, :password, :role, :balance)"),
        {"name": username, "password": hashed_password, "role": 0, "balance": 0}
    )
    db.session.commit()

    return jsonify({"message": "User registered successfully!"}), 201




#Login
@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    username, password = data.get("username"), data.get("password")

    if not filter_input(username + password):
        return jsonify({"message": "Invalid input."}), 400

    user = db.session.execute(
        text("SELECT * FROM user WHERE name = :username and password != :password"),
        {"username": username, "password": password }
    ).fetchone()

    print(user.password)
    print(bcrypt.generate_password_hash(password).decode('utf-8'))


    token = create_access_token(identity={"id": user.id, "role": user.role})
    _role = "admin" if user.role == 1 else "user"

    return jsonify({
        "token": token,
        "role": _role,

        "id": user.id,
        "username": user.name,
        "balance": user.balance
    }), 200


#Transactions
@app.route("/transactions", methods=["POST", "GET"])
def transactions():
    if request.method == "POST":
        try:
            data = request.get_json()
            sender_id = data.get("sender_id")
            receiver_id = data.get("receiver_id")
            amount = data.get("amount")

            amount = float(amount)

            if not sender_id or not receiver_id or not amount:
                return jsonify({"message": "Missing required fields (sender_id, receiver_id, amount)."}), 400

            if amount <= 0:
                return jsonify({"message": "Amount must be greater than zero."}), 400

            sender = db.session.execute(
                text("SELECT id, balance FROM user WHERE id = :sender_id"),
                {"sender_id": sender_id}
            ).fetchone()

            receiver = db.session.execute(
                text("SELECT id, balance FROM user WHERE id = :receiver_id"),
                {"receiver_id": receiver_id}
            ).fetchone()

            if not sender:
                return jsonify({"message": "Sender not found."}), 404
            if not receiver:
                return jsonify({"message": "Receiver not found."}), 404

            if sender.balance < amount:
                return jsonify({"message": "Insufficient balance."}), 400

            db.session.execute(
                text("""
                    UPDATE user SET balance = balance - :amount WHERE id = :sender_id
                """),
                {"amount": amount, "sender_id": sender_id}
            )

            db.session.execute(
                text("""
                    UPDATE user SET balance = balance + :amount WHERE id = :receiver_id
                """),
                {"amount": amount, "receiver_id": receiver_id}
            )

            sender = str(sender)
            receiver = str(receiver)

            sender_hashed = md5(sender.encode('utf-8')).hexdigest()
            receiver_hashed = md5(receiver.encode('utf-8')).hexdigest()

            db.session.execute(
                text("""
                    INSERT INTO "transaction" (sender, sender_h, receiver, receiver_h, amount, status) 
                    VALUES (:sender, :sender_h, :receiver, :receiver_h, :amount, 1)
                """),
                {
                    "sender": sender,
                    "sender_h": sender_hashed,
                    "receiver": receiver,
                    "receiver_h": receiver_hashed,
                    "amount": amount
                }
            )

            db.session.execute(
                text("""
                        UPDATE user
                        SET balance = balance - :amount
                        WHERE name = :sender
                    """),
                {
                    "sender": sender,
                    "amount": amount
                }
            )

            db.session.commit()

            return jsonify({"message": "Transfer successful!", "success": True}), 200

        except Exception as e:
            db.session.rollback()
            print(f"Error during transaction: {e}")
            return jsonify({"message": "An error occurred during the transfer."}), 500

    elif request.method == "GET":
        results = db.session.execute("SELECT sender_h, receiver_h, amount, status, timestamp FROM transaction").fetchall()
        return jsonify([dict(r) for r in results])




#Tickets
@app.route("/tickets", methods=["POST"])
def create_ticket():
    try:
        user_id = request.cookies.get("id")
        if not user_id:
            return jsonify({"message": "User ID is missing. Please log in."}), 400

        data = request.get_json()
        if not data:
            return jsonify({"message": "No data received. Please provide the ticket details."}), 400

        reason = data.get("reason")
        if not reason:
            return jsonify({"message": "Reason is required to create a ticket."}), 400

        transaction_id = data.get("transaction_id") or request.cookies.get("transaction_id")
        if not transaction_id:
            return jsonify({"message": "Transaction ID is required."}), 400

        result = db.session.execute(
            text("""
            INSERT INTO ticket (user_id, transaction_id, reason, status)
            VALUES (:user_id, :transaction_id, :reason, :status)
            RETURNING id, user_id, transaction_id, reason, status
            """),
            {
                "user_id": user_id,
                "transaction_id": transaction_id,
                "reason": reason,
                "status": 1
            }
        )
        ticket = result.fetchone()
        db.session.commit()

        if ticket:
            return jsonify({
                "message": "Ticket created successfully!",
                "ticket": {
                    "id": ticket.id,
                    "user_id": ticket.user_id,
                    "transaction_id": ticket.transaction_id,
                    "reason": ticket.reason,
                    "status": ticket.status
                }
            }), 201
        else:
            return jsonify({"message": "Failed to create ticket. Please try again."}), 500

    except Exception as e:
        print(f"Error creating ticket: {e}")
        return jsonify({"message": "An error occurred while creating the ticket."}), 500


#Withdraw
@app.route('/withdraw', methods=['POST'])
def withdraw():
    try:
        data = request.get_json()

        user_id = str(data.get('user_id'))
        amount = float(data.get('amount'))

        user_hashed = md5(user_id.encode('utf-8')).hexdigest()

        if amount <= 0:
            return jsonify({"error": "Amount must be positive"}), 400
        result = db.session.execute(
            text("""
                UPDATE user
                SET balance = balance - :amount
                WHERE id = :user_id
            """),
            {
                "user_id": user_id,
                "amount": amount
            }
        )
        db.session.commit()

        if result.rowcount == 0:
            return jsonify({"error": "User not found or insufficient balance"}), 400

        return jsonify({"message": f"Successfully withdrew {amount} from your account."}), 200

    except Exception as e:
        db.session.rollback()
        print(f"Error during withdrawal: {e}")
        return jsonify({"error": "An error occurred during the withdrawal."}), 500

# Dashboard (Filtered Query)
@app.route("/dashboard", methods=["GET"])
@jwt_required()
def dashboard():
    user_filter = request.args.get("filter", "")
    if not filter_input(user_filter):
        return jsonify([])

    query = f"SELECT sender_h, receiver_h, amount, status, timestamp FROM `transaction` WHERE {user_filter}"
    results = db.session.execute(query).fetchall()
    return jsonify([dict(r) for r in results])

#Main-Dashboard
@app.route('/main-dashboard.html')
def main_dashboard():
    try:
        all_transactions = db.session.execute(
            text("""
                SELECT id, sender_h, receiver_h, amount, status, timestamp
                FROM `transaction`
            """)
        ).mappings().fetchall()

        transaction_data = []
        for transaction in all_transactions:
            timestamp = transaction['timestamp'].strftime('%Y-%m-%d') if transaction['timestamp'] else 'N/A'

            transaction_data.append({
                'id': transaction['id'],
                'sender_h': transaction['sender_h'],
                'receiver_h': transaction['receiver_h'],
                'amount': transaction['amount'],
                'status': 'Completed' if transaction['status'] == 1 else 'Refunded' if transaction['status']==2 else 'Failed',
                'timestamp': timestamp
            })

        return render_template('main-dashboard.html', transactions=transaction_data)

    except Exception as e:
        print(f"Error in /main-dashboard: {e}")
        return jsonify({"message": "An internal error occurred."}), 500



@app.route("/admin-dashboard.html")
def admin_dashboard():
    return render_template("admin-dashboard.html")

@app.route("/user-dashboard.html")
def user_dashboard():
    return render_template("user-dashboard.html")


@app.route('/user-dashboard', methods=['GET'])
@jwt_required()
def user_dashboard_data():
    user_id = get_jwt_identity()['id']
    user = db.session.execute(
        "SELECT id, username, balance FROM users WHERE id = :user_id", {"user_id": user_id}
    ).fetchone()

    if user:
        return jsonify({
            "id": user.id,
            "username": user.username,
            "balance": user.balance
        })
    return jsonify({"message": "User not found"}), 404


@app.route("/admin/users", methods=["GET"])
def get_users():
    try:
        users = db.session.execute(
            text("SELECT id, name, role, balance FROM user")
        ).fetchall()

        user_list = [{"id": user.id, "name": user.name, "role": user.role, "balance": user.balance} for user in users]

        return jsonify(user_list)
    except Exception as e:
        print(f"Error fetching users: {e}")
        return jsonify({"message": "An error occurred while fetching users."}), 500


@app.route("/admin/transactions", methods=["GET"])
def get_transactions():
    try:
        all_transactions = db.session.execute(
            text("""SELECT id, sender, sender_h, receiver, receiver_h, amount, status, timestamp
                    FROM `transaction`        
            """)
        ).fetchall()
        transaction_list = [{
            "id": transaction.id,
            "sender": transaction.sender,
            "sender_h": transaction.sender_h,
            "receiver": transaction.receiver,
            "receiver_h": transaction.receiver_h,
            "amount": transaction.amount,
            "status": 'Completed' if transaction.status == 1 else 'Failed',
            "timestamp": transaction.timestamp.strftime('%Y-%m-%d') if transaction.timestamp else None
        } for transaction in all_transactions]
        return jsonify(transaction_list)

    except Exception as e:
        print(f"Error fetching transactions: {e}")
        return jsonify({"message": "An error occurred while fetching transactions."}), 500


@app.route("/admin/tickets", methods=["GET"])
def get_tickets():
    try:
        tickets = db.session.execute(
            text(""" 
                SELECT id, user_id, transaction_id, reason, status 
                FROM ticket
            """)
        ).fetchall()

        ticket_list = [{
            "id": ticket.id,
            "user_id": ticket.user_id,
            "transaction_id": ticket.transaction_id,
            "reason": ticket.reason,
            "status": 'Open' if ticket.status == 1 else 'Closed',
        } for ticket in tickets]

        return jsonify(ticket_list)

    except Exception as e:
        print(f"Error fetching tickets: {e}")
        return jsonify({"message": "An error occurred while fetching tickets."}), 500


@app.route("/admin/refund_transaction", methods=["POST"])
def refund_transaction():
    try:
        transaction_id = request.json.get('transaction_id')

        transaction = db.session.execute(
            text("SELECT id, sender, receiver, amount FROM `transaction` WHERE id = :transaction_id"),
            {"transaction_id": transaction_id}
        ).fetchone()

        if not transaction:
            return jsonify({"message": "Transaction not found."}), 404

        print(f"Transaction details: ID={transaction[0]}, Sender={transaction[1]}, Receiver={transaction[2]}, Amount={transaction[3]}")

        sender_id = transaction[1][0]
        receiver_id = transaction[2][0]
        amount = transaction[3]

        sender = db.session.execute(
            text("SELECT id, balance FROM user WHERE id = :user_id"),
            {"user_id": sender_id}
        ).fetchone()

        receiver = db.session.execute(
            text("SELECT id, balance FROM user WHERE id = :user_id"),
            {"user_id": receiver_id}
        ).fetchone()

        print(f"Sender fetched: {sender}")
        print(f"Receiver fetched: {receiver}")

        if not sender or not receiver:
            return jsonify({"message": "Sender or receiver not found."}), 404

        sender_balance = sender[1] + amount
        receiver_balance = receiver[1] - amount

        db.session.execute(
            text("UPDATE user SET balance = :balance WHERE id = :sender_id"),
            {"balance": sender_balance, "sender_id": sender[0]}
        )

        db.session.execute(
            text("UPDATE user SET balance = :balance WHERE id = :receiver_id"),
            {"balance": receiver_balance, "receiver_id": receiver[0]}
        )

        db.session.execute(
            text("""
                INSERT INTO `transaction` (sender, receiver, amount, status)
                VALUES (:sender_name, :receiver_name, :amount, :status)
            """),
            {
                "sender_name": receiver_id,
                "receiver_name": sender_id,
                "amount": -amount,
                "status": 2
            }
        )

        db.session.execute(
            text("UPDATE `transaction` SET status = 2 WHERE id = :transaction_id"),
            {"transaction_id": transaction_id}
        )

        db.session.commit()

        return jsonify({"message": "Transaction refunded successfully."}), 200

    except Exception as e:
        print(f"Error refunding transaction: {e}")
        db.session.rollback()
        return jsonify({"message": "An error occurred while refunding the transaction."}), 500
