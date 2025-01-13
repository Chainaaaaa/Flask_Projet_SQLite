from flask import Flask, render_template, jsonify, request, redirect, url_for, session
import sqlite3

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'  # Clé secrète pour les sessions

# Helper: Gestion de la connexion à la base de données
def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row  # Pour accéder aux colonnes par nom
    return conn

# Helper: Vérifier si l'utilisateur est authentifié
def est_authentifie():
    return session.get('authentifie')

def user():
    return session.get('user_A')

@app.route('/')
def home():
    return render_template('hello.html')

@app.route('/lecture')
def lecture():
    if est_authentifie():
        return "<h1>Bonjour Administrateur</h1>"
    elif user():
        return "<h1>Bonjour Utilisateur</h1>"
    else:
        return redirect(url_for('authentification'))

@app.route('/authentification', methods=['GET', 'POST'])
def authentification():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == 'admin' and password == 'password':  # Utilisez un système sécurisé à l'avenir
            session['authentifie'] = True
            session['user_A'] = False
            return redirect(url_for('lecture'))
        elif username == 'user' and password == '12345':
            session['user_A'] = True
            session['authentifie'] = False
            return redirect(url_for('lecture'))
        else:
            return render_template('formulaire_authentification.html', error=True)

    return render_template('formulaire_authentification.html', error=False)

# Gestion des clients
@app.route('/consultation/')
def read_clients():
    conn = get_db_connection()
    clients = conn.execute('SELECT * FROM clients').fetchall()
    conn.close()
    return render_template('read_data.html', data=clients)

@app.route('/enregistrer_client', methods=['GET', 'POST'])
def enregistrer_client():
    if request.method == 'POST':
        nom = request.form['nom']
        prenom = request.form['prenom']
        conn = get_db_connection()
        conn.execute('INSERT INTO clients (nom, prenom, adresse) VALUES (?, ?, ?)', (nom, prenom, "Adresse à définir"))
        conn.commit()
        conn.close()
        return redirect('/consultation/')
    return render_template('formulaire.html')

@app.route('/supprimer_client/<int:id>')
def supprimer_client(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM clients WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect('/consultation/')

# Gestion des livres
@app.route('/consultation_livre/')
def read_books():
    conn = get_db_connection()
    livres = conn.execute('SELECT * FROM livres').fetchall()
    conn.close()
    return render_template('read_livre.html', data=livres)

@app.route('/enregistrer_livre', methods=['GET', 'POST'])
def enregistrer_livre():
    if request.method == 'POST':
        nom = request.form['nom']
        auteur = request.form['auteur']
        conn = get_db_connection()
        livre = conn.execute('SELECT * FROM livres WHERE nom = ? AND auteur = ?', (nom, auteur)).fetchone()
        if livre is None:
            conn.execute('INSERT INTO livres (nom, auteur, quantite) VALUES (?, ?, ?)', (nom, auteur, 1))
        else:
            conn.execute('UPDATE livres SET quantite = quantite + 1 WHERE nom = ? AND auteur = ?', (nom, auteur))
        conn.commit()
        conn.close()
        return redirect('/consultation_livre/')
    return render_template('formulaire_livre.html')

@app.route('/supprimer_livre/<int:id>')
def supprimer_livre(id):
    conn = get_db_connection()
    livre = conn.execute('SELECT quantite FROM livres WHERE id = ?', (id,)).fetchone()
    if livre and livre['quantite'] > 0:
        conn.execute('UPDATE livres SET quantite = quantite - 1 WHERE id = ?', (id,))
        conn.commit()
    conn.close()
    return redirect('/consultation_livre/')

# Gestion des emprunts
@app.route('/consultation_emprunts/')
def read_emprunts():
    conn = get_db_connection()
    emprunts = conn.execute('SELECT * FROM emprunts').fetchall()
    conn.close()
    return render_template('read_emprunt.html', data=emprunts)

@app.route('/enregistrer_emprunt', methods=['GET', 'POST'])
def enregistrer_emprunt():
    if request.method == 'POST':
        id_client = request.form['id_client']
        id_livre = request.form['id_livre']
        conn = get_db_connection()
        livre = conn.execute('SELECT quantite FROM livres WHERE id = ?', (id_livre,)).fetchone()
        client = conn.execute('SELECT * FROM clients WHERE id = ?', (id_client,)).fetchone()
        if livre and client and livre['quantite'] > 0:
            conn.execute('INSERT INTO emprunts (id_client, id_livre, state) VALUES (?, ?, ?)', (id_client, id_livre, 1))
            conn.execute('UPDATE livres SET quantite = quantite - 1 WHERE id = ?', (id_livre,))
            conn.commit()
        conn.close()
        return redirect('/consultation_emprunts/')
    return render_template('formulaire_emprunt.html')

@app.route('/retour/<int:id>')
def retour(id):
    conn = get_db_connection()
    emprunt = conn.execute('SELECT id_livre, state FROM emprunts WHERE id = ?', (id,)).fetchone()
    if emprunt and emprunt['state'] == 1:
        conn.execute('UPDATE livres SET quantite = quantite + 1 WHERE id = ?', (emprunt['id_livre'],))
        conn.execute('UPDATE emprunts SET state = 0, date_fin = CURRENT_TIMESTAMP WHERE id = ?', (id,))
        conn.commit()
    conn.close()
    return redirect('/consultation_emprunts/')

if __name__ == "__main__":
    app.run(debug=True)

