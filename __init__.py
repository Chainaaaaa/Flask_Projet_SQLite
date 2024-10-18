from flask import Flask, render_template_string, render_template, jsonify, request, redirect, url_for, session
from flask import render_template
from flask import json
from urllib.request import urlopen
from werkzeug.utils import secure_filename
import sqlite3

app = Flask(__name__)                                                                                                                  
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'  # Clé secrète pour les sessions

# Fonction pour créer une clé "authentifie" dans la session utilisateur
def est_authentifie():
    return session.get('authentifie')

@app.route('/')
def hello_world():
    return render_template('hello.html')

@app.route('/lecture')
def lecture():
    if not est_authentifie():
        # Rediriger vers la page d'authentification si l'utilisateur n'est pas authentifié
        return redirect(url_for('authentification'))

  # Si l'utilisateur est authentifié
    return "<h2>Bravo, vous êtes authentifié</h2>"

@app.route('/authentification', methods=['GET', 'POST'])
def authentification():
    if request.method == 'POST':
        # Vérifier les identifiants
        if request.form['username'] == 'user' and request.form['password'] == '12345': # password à cacher par la suite
            session['authentifie'] = True
            # Rediriger vers la route lecture après une authentification réussie
            return redirect(url_for('lecture'))
        else:
            # Afficher un message d'erreur si les identifiants sont incorrects
            return render_template('formulaire_authentification.html', error=True)

    return render_template('formulaire_authentification.html', error=False)

@app.route('/fiche_nom/<string:id>')
def Readfiche(id):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM clients WHERE nom = ?', (id,))
    data = cursor.fetchall()
    conn.close()
    # Rendre le template HTML et transmettre les données
    return render_template('read_data.html', data=data)

@app.route('/consultation/')
def ReadBDD():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM clients;')
    data = cursor.fetchall()
    conn.close()
    return render_template('read_data.html', data=data)

@app.route('/enregistrer_client', methods=['GET'])
def formulaire_client():
    return render_template('formulaire.html')  # afficher le formulaire

@app.route('/enregistrer_client', methods=['POST'])
def enregistrer_client():
    nom = request.form['nom']
    prenom = request.form['prenom']

    # Connexion à la base de données
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    # Exécution de la requête SQL pour insérer un nouveau client
    cursor.execute('INSERT INTO clients (created, nom, prenom, adresse) VALUES (?, ?, ?, ?)', (1002938, nom, prenom, "ICI"))
    conn.commit()
    conn.close()
    return redirect('/consultation/')  # Rediriger vers la page d'accueil après l'enregistrement
                                                                                                
if __name__ == "__main__":
  app.run(debug=True)

from flask import Flask, jsonify, request
import sqlite3

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'  # Clé secrète pour les sessions

# Helper pour la connexion à la base de données
def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row  # Pour un accès par clé
    return conn

# Créer la table 'books' si elle n'existe pas déjà
def create_books_table():
    conn = get_db_connection()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            author TEXT NOT NULL,
            year INTEGER
        )
    ''')
    conn.commit()
    conn.close()

# Route pour récupérer tous les livres
@app.route('/api/books', methods=['GET'])
def get_books():
    conn = get_db_connection()
    books = conn.execute('SELECT * FROM books').fetchall()
    conn.close()

    books_list = [dict(book) for book in books]
    return jsonify(books_list)

# Route pour récupérer un livre par ID
@app.route('/api/books/<int:id>', methods=['GET'])
def get_book(id):
    conn = get_db_connection()
    book = conn.execute('SELECT * FROM books WHERE id = ?', (id,)).fetchone()
    conn.close()

    if book is None:
        return jsonify({"error": "Book not found"}), 404

    return jsonify(dict(book))

# Route pour ajouter un nouveau livre
@app.route('/api/books', methods=['POST'])
def add_book():
    data = request.get_json()

    # Vérification des données
    if 'title' not in data or 'author' not in data or 'year' not in data:
        return jsonify({"error": "Invalid data"}), 400

    title = data['title']
    author = data['author']
    year = data['year']

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO books (title, author, year) VALUES (?, ?, ?)',
                   (title, author, year))
    conn.commit()
    conn.close()

    return jsonify({"message": "Book added successfully"}), 201

# Route pour supprimer un livre par ID
@app.route('/api/books/<int:id>', methods=['DELETE'])
def delete_book(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM books WHERE id = ?', (id,))
    book = cursor.fetchone()

    if book is None:
        conn.close()
        return jsonify({"error": "Book not found"}), 404

    cursor.execute('DELETE FROM books WHERE id = ?', (id,))
    conn.commit()
    conn.close()

    return jsonify({"message": "Book deleted successfully"}), 200

if __name__ == "__main__":
    create_books_table()  # Créer la table si elle n'existe pas
    app.run(debug=True)
