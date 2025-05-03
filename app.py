from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from models import LoanRequest
from datetime import datetime


import os

# Configuration de l'application Flask
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

#  l'authentification
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    role = db.Column(db.String(50), default='emprunteur')  

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Autres modèles
class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    author = db.Column(db.String(150), nullable=False)

class Member(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)

class Borrow(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'), nullable=False)
    member_id = db.Column(db.Integer, nullable=False)
    borrow_date = db.Column(db.String(50), nullable=False)

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add_book', methods=['GET', 'POST'])
@login_required
def add_book():
    if current_user.role != 'admin':
        flash('Accès refusé : administrateurs uniquement.', 'danger')
        return redirect(url_for('index'))

    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']
        new_book = Book(title=title, author=author)
        db.session.add(new_book)
        db.session.commit()
        flash('Livre ajouté avec succès!', 'success')
        return redirect(url_for('admin_dashboard'))

    return render_template('add_book.html')

@app.route('/list_books')
def list_books():
    books = Book.query.order_by(Book.title).all()
    return render_template('list_books.html', books=books)

@app.route('/admin_dashboard', methods=['GET', 'POST'])
@login_required
def admin_dashboard():
    if current_user.role != 'admin':
        return redirect(url_for('index'))

    if request.method == 'POST':
        books = Book.query.all()
        for book in books:
            available_key = f"available_{book.id}"
            if available_key in request.form:
                try:
                    new_available = int(request.form[available_key])
                    book.available = new_available
                except ValueError:
                    flash(f"Valeur invalide pour le livre : {book.title}", "danger")

        db.session.commit()
        flash("Le nombre d'exemplaires a été mis à jour avec succès.", "success")

    books = Book.query.all()
    return render_template('admin_dashboard.html', books=books)




@app.route('/client_dashboard')
@login_required
def client_dashboard():
    if current_user.role != 'emprunteur':
        return redirect(url_for('index'))
    books = Book.query.all()
    return render_template('client_dashboard.html', books=books)

@app.route('/list_borrows')
@login_required
def list_borrows():
    borrows = Borrow.query.filter_by(user_id=current_member_id).all()  # Utiliser user_id
    return render_template('list_borrows.html', borrows=borrows)


@app.route('/borrow_book/<int:book_id>', methods=['GET', 'POST'])
@login_required
def borrow_book(book_id):
    try:
        book = Book.query.get_or_404(book_id)

        if current_user.role != 'emprunteur':
            flash("Seuls les emprunteurs peuvent emprunter un livre.", "danger")
            return redirect(url_for('index'))

        
        if request.method == 'POST':
            # Créer un nouvel emprunt
            borrow = Borrow(book_id=book.id, member_id=current_user.id, borrow_date=datetime.utcnow())
            db.session.add(borrow)
            db.session.commit()
            flash(f"Vous avez emprunté le livre '{book.title}'", "success")
            return redirect(url_for('borrow_book.html'))  # Redirection vers la même page
    except Exception as e:
        db.session.rollback()
        flash(f"Une erreur est survenue : {str(e)}", "danger")
        return redirect(url_for('client_dashboard'))
    return render_template('borrow_book.html', book=book)



@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        role = request.form['role']

        if User.query.filter_by(username=username).first():
            flash("Nom d'utilisateur déjà utilisé", "danger")
            return redirect(url_for('register'))

        user = User(username=username, role=role)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        flash("Inscription réussie ! Connectez-vous maintenant.", "success")
        return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            login_user(user)
            flash('Connexion réussie', 'success')
            return redirect(url_for('admin_dashboard' if user.role == 'admin' else 'client_dashboard'))

        flash("Identifiants invalides", "danger")

    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("Déconnexion réussie", "success")
    return redirect(url_for('login'))

@app.route('/update_book/<int:book_id>', methods=['GET', 'POST'])
@login_required
def update_book(book_id):
    if current_user.role != 'admin':
        flash('Accès refusé : administrateurs uniquement.', 'danger')
        return redirect(url_for('index'))

    book = Book.query.get_or_404(book_id)

    if request.method == 'POST':
        # Mettre à jour le nombre de livres disponibles
        book.available = request.form['available']
        db.session.commit()
        flash('Le nombre de copies a été mis à jour.', 'success')
        return redirect(url_for('admin_dashboard'))

    return render_template('update_book.html', book=book)

@app.route('/loan_requests')
@login_required
def loan_requests():
    # Vérification que l'utilisateur est un administrateur
    if current_user.role != 'admin':
        flash("Vous n'avez pas les autorisations nécessaires pour accéder à cette page.", "danger")
        return redirect(url_for('index'))

    try:
        # Récupérer toutes les demandes de prêt
        requests = LoanRequest.query.all()

        # Si aucune demande n'est trouvée, tu peux afficher un message
        if not requests:
            flash("Aucune demande d'emprunt trouvée.", "info")

        return render_template('demande.html', requests=requests)

    except Exception as e:
        # Gestion des erreurs
        flash(f"Une erreur est survenue lors de la récupération des demandes: {e}", "danger")
        return redirect(url_for('index'))


# Démarrage de l'application
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
    app.config['DEBUG'] = True

