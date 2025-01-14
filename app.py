from flask import Flask
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from db_schema import db

from flask.cli import with_appcontext

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = '173db02c31bc99a8c0f1350135a4ee31' #SecureBanking_2025CopyRight

db.init_app(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)

from routes import *

@app.cli.command("create-db")
@with_appcontext
def create_db():
    with app.app_context():
        print("Creating all tables...")
        db.create_all()
        print("Tables created successfully.")

if __name__ == "__main__":
    app.run(debug=True)
