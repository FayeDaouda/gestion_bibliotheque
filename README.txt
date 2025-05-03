==================================================
         APPLICATION DE GESTION DE BIBLIOTHÈQUE
==================================================

📌 Description
--------------
Ce projet est une application web de gestion de bibliothèque développée avec Flask.
Il permet aux clients de consulter et d’emprunter des livres, tandis que les administrateurs peuvent gérer les livres et valider les emprunts.

👥 Types d’utilisateurs
------------------------
1. ADMINISTRATEUR
   - Gère les livres (ajouter, modifier, supprimer)
   - Gère les emprunts (valider ou refuser une demande)
   - Accède au tableau de bord administrateur

2. CLIENT (ou EMPRUNTEUR)
   - Peut créer un compte et se connecter
   - Consulte les livres disponibles
   - Fait des demandes d’emprunt
   - Accède à son propre tableau de bord

🎯 Fonctionnalités
------------------
- Authentification sécurisée (connexion/inscription)
- Gestion des rôles (admin / client)
- Gestion des livres (CRUD pour l’admin)
- Gestion des emprunts (demande par client, validation par admin)
- Interface simple, intuitive et responsive

🛠️ Technologies utilisées
--------------------------
- Python 3
- Flask (microframework web)
- Flask-SQLAlchemy (ORM)
- Flask-Login (authentification)
- SQLite (base de données légère)
- HTML/CSS avec Bootstrap (interface utilisateur)

📦 Installation
---------------
1. Cloner le projet :
   git clone https://github.com/ton-utilisateur/nom-du-projet.git

2. Accéder au dossier du projet :
   cd nom-du-projet

3. Créer un environnement virtuel :
   python -m venv venv

4. Activer l’environnement :
   - Windows : venv\Scripts\activate
   - macOS/Linux : source venv/bin/activate

5. Installer les dépendances :
   pip install -r requirements.txt

6. Lancer l’application :
   flask run

7. Accéder dans le navigateur :
   http://127.0.0.1:5000/

🗂️ Structure du projet
--------------------------
GESTION_BIBLIOTHEQUE/
│
├── __pycache__/
├── database/                        # Répertoire de base de données
│   └── db.sqlite
├── instance/
│   └── database.db
├── static/                          # Fichiers CSS/JS si ajoutés
├── templates/                       # Gabarits HTML
│   ├── add_book.html
│   ├── admin_dashboard.html
│   ├── base.html
│   ├── borrow_book.html
│   ├── client_dashboard.html
│   ├── demande.html
│   ├── index.html
│   ├── list_books.html
│   ├── list_borrows.html
│   ├── login.html
│   └── register.html
│
├── venv/                            # Environnement virtuel
├── app.py                           # Fichier principal Flask
├── config.py                        # Configuration Flask
├── models.py                        # Définition des modèles (User, Book, Borrow)
├── requirements.txt                 # Dépendances
├── your_database.db                 # Base de données alternative
└── README.txt                       # Ce fichier


👤 Accès de démonstration
--------------------------
- Administrateur :
  - Nom d'utilisateur : Admin
  - Mot de passe : admin123

- Client :
  - Nom d'utilisateur : Client
  - Mot de passe : client123

🔧 Personnalisation
--------------------
Vous pouvez facilement adapter ce projet à d'autres types de gestion (bibliothèque scolaire, médiathèque, etc.).

🤝 Contributions
----------------
Contributions bienvenues ! Forkez le projet, créez une branche, et proposez une Pull Request.

📄 Licence
----------
Ce projet est sous licence MIT. Consultez le fichier LICENSE pour plus d’informations.

📧 Contact
----------
Développeur : Daouda faye
Email : daouda.faye@ism.edu.sn
GitHub : https://github.com/FayeDaouda/gestion_bibliotheque