# models.py

from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime

db = SQLAlchemy()

# Définir d'abord le modèle User
class User(UserMixin, db.Model):  # Modèle pour l'utilisateur
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(20), nullable=False, default='client')

# Ensuite définir LoanRequest après User
class LoanRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'))
    request_date = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(20), default='en attente')

    # Ici, la relation avec User et Book
    user = db.relationship('User', backref='loan_requests')
    book = db.relationship('Book', backref='loan_requests')

# Définir les autres modèles comme Book, Member, Borrow...
class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    author = db.Column(db.String(100))
    available = db.Column(db.Integer, default=1)

    # Définir la relation avec Borrow
    borrows = db.relationship('Borrow', backref='book', lazy=True)


class Member(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(20), nullable=False, default='client')

class Borrow(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  
    borrow_date = db.Column(db.DateTime, nullable=False)
    return_date = db.Column(db.DateTime, nullable=True)

    # Définir la relation avec Book et User
    user = db.relationship('User', backref='borrows', lazy=True)
    book = db.relationship('Book', backref='borrows', lazy=True)
