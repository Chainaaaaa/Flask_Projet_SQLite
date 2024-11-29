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

def user():
    return session.get('user_A')

@app.route('/')
def hello_world():
    return render_template('hello.html')

@app.route('/lecture')
def lecture():
    if est_authentifie():
        return "<h1>Bonjour Administrateur</h1>"
    elif user():
        return "<h1>Bonjour Utilisateur</h1>"
    else:
        return redirect(url_for('authentification'))

  # Si l'utilisateur est authentifié
    return "<h2>Bravo, vous êtes authentifié</h2>"

@app.route('/authentification', methods=['GET', 'POST'])
def authentification():
    if request.method == 'POST':
        # Vérifier les identifiants
        if request.form['username'] == 'admin' and request.form['password'] == 'password': # password à cacher par la suite
            session['authentifie'] = True
            session['user_A'] = False
            # Rediriger vers la route lecture après une authentification réussie
            return redirect(url_for('lecture'))
        elif request.form['username'] == 'user' and request.form['password'] == '12345':
            session['user_A'] = True
            session['authentifie'] = False
            return redirect(url_for('lecture'))
        else:
            # Afficher un message d'erreur si les identifiants sont incorrects
            return render_template('formulaire_authentification.html', error=True)

    return render_template('formulaire_authentification.html', error=False)

@app.route('/fiche_client/<int:post_id>')
def Readfiche(post_id):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM clients WHERE id = ?', (post_id,))
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
    cursor.execute('INSERT INTO clients (nom, prenom, adresse) VALUES (?, ?, ?)', (nom, prenom, "ICI"))
    conn.commit()
    conn.close()
    return redirect('/consultation/')  # Rediriger vers la page d'accueil après l'enregistrement

@app.route('/supprimer_client/<int:id>')
def supprimer_client(id):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    cursor.execute('DELETE FROM clients WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect('/consultation/')

@app.route('/fiche_nom/<string:nom>')
def fiche_nom(nom):
    if user():
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()

        cursor.execute('SELECT * FROM clients WHERE nom = ?', (nom,))
        data = cursor.fetchall()
        conn.close
        return render_template('read_data.html', data=data)
    else:
        return '<h1>non identifié</h1>'


@app.route('/consultation_livre/')
def BDD_livre():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM livres;')
    data = cursor.fetchall()
    conn.close()
    return render_template('read_livre.html', data=data)

@app.route('/enregistrer_livre', methods=['GET'])
def formulaire_livre():
    return render_template('formulaire_livre.html')  # afficher le formulaire

@app.route('/enregistrer_livre', methods=['POST'])
def enregistrer_livre():
    nom = request.form['nom']
    auteur = request.form['auteur']

    # Connexion à la base de données
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    # Exécution de la requête SQL pour insérer un nouveau client
    cursor.execute('INSERT INTO livres (nom,auteur) VALUES (?,?)', (nom,auteur))
    conn.commit()
    conn.close()
    return redirect('/consultation_livre/')

@app.route('/supprimer_livre/<int:id>')
def supprimer_livre(id):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    cursor.execute('DELETE FROM livres WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect('/consultation_livre/')

@app.route('/fiche_livre_id/<int:post_id>')
def fiche_livre_id(post_id):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM livres WHERE id = ?', (post_id,))
    data = cursor.fetchall()
    conn.close()
    return render_template('read_livre.html', data=data)

@app.route('/fiche_livre_nom/<string:nom>')
def fiche_livre_nom(nom):
    if user():
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()

        cursor.execute('SELECT * FROM clients WHERE nom = ?', (nom,))
        data = cursor.fetchall()
        conn.close
        return render_template('read_livre.html', data=data)
    else:
        return '<h1>non identifié</h1>'



@app.route('/consultation_emprunts/')
def BDD_emprunt():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM emprunts;')
    data = cursor.fetchall()
    conn.close()
    return render_template('read_emprunt.html', data=data)

@app.route('/enregistrer_emprunt', methods=['GET'])
def formulaire_emprunt():
    return render_template('formulaire_emprunt.html')  # afficher le formulaire

@app.route('/enregistrer_emprunt', methods=['POST'])
def enregistrer_emprunt():
    id_client = request.form['id_client']
    id_livre = request.form['id_livre']

    # Connexion à la base de données
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    # Exécution de la requête SQL pour insérer un nouveau client
    cursor.execute('INSERT INTO emprunts (id_client,id_livre) VALUES (?,?)', (id_client,id_livre,))
    conn.commit()
    conn.close()
    return redirect('/consultation_emprunts/')

@app.route('/retour/<int:id>')
def retour(id):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    # Exécution de la requête SQL pour insérer un nouveau client
    cursor.execute('UPDATE emprunts SET date_fin = CURRENT_TIMESTAMP WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect('/consultation_emprunts/')
                                                                                                                                       
if __name__ == "__main__":
  app.run(debug=True)
