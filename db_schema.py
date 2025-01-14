from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


#User:   id,     name,   password,   role,    balance
#       int,   string,       hash,    int,      float
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False, unique=True)
    password = db.Column(db.String(72), nullable=False)
    role = db.Column(db.Integer, nullable=False)
    balance=db.Column(db.Integer,nullable=False,default=0)
#user password should be hashed before being transmitted to the server (no plaintext credentials)
#the hashing algorithm for the password should be bcrypt


#Transaction:  id,    sender,    sender_h,   receiver,   receiver_h,   amount,   status,   timestamp
#             int,    string,        hash,     string,         hash,      int,   date
class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sender = db.Column(db.String(64), nullable=False)
    sender_h = db.Column(db.String(16), nullable=False)
    receiver = db.Column(db.String(64), nullable=False)
    receiver_h = db.Column(db.String(16), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    status = db.Column(db.Integer, nullable=False)
    timestamp = db.Column(db.DateTime, default=db.func.current_timestamp())
#transactions should have plaintext usernames in the db, but these values should not be displayed
#on the main dashboard, only the hashes. (hashed are stored as columns to save computation time)
#the hashing algorithm for the X_h fields should be md5


#Ticket:   id,     sender,   receiver,  amount,  status,   timestamp
#         int,       hash,       hash,   float,     int,   date
class Ticket(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    transaction_id = db.Column(db.Integer, db.ForeignKey('transaction.id'), nullable=False)
    reason = db.Column(db.String(1024), nullable=True)
    status = db.Column(db.Integer, default=1)   #0 for solved, 1 for pending, 2 in progress, 512 for suspicious

