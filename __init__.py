from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'  # Clé secrète pour les sessions

# Fonction pour vérifier si l'utilisateur est un administrateur
def est_admin():
    return session.get('admin')

# Fonction pour vérifier si l'utilisateur est un utilisateur simple
def est_utilisateur():
    return session.get('utilisateur')

@app.route('/')
def accueil():
    return render_template('accueil.html')

@app.route('/tableau_de_bord')
def tableau_de_bord():
    if est_admin():
        return "<h1>Bienvenue Administrateur</h1>"
    elif est_utilisateur():
        return "<h1>Bienvenue Utilisateur</h1>"
    else:
        return redirect(url_for('connexion'))

@app.route('/connexion', methods=['GET', 'POST'])
def connexion():
    if request.method == 'POST':
        if request.form['identifiant'] == 'admin' and request.form['mot_de_passe'] == 'password':
            session['admin'] = True
            session['utilisateur'] = False
            return redirect(url_for('tableau_de_bord'))
        elif request.form['identifiant'] == 'utilisateur' and request.form['mot_de_passe'] == '12345':
            session['utilisateur'] = True
            session['admin'] = False
            return redirect(url_for('tableau_de_bord'))
        else:
            return render_template('connexion.html', erreur=True)
    return render_template('connexion.html', erreur=False)

@app.route('/clients/<int:id_client>')
def afficher_client(id_client):
    conn = sqlite3.connect('base_de_donnees.db')
    curseur = conn.cursor()
    curseur.execute('SELECT * FROM clients WHERE id = ?', (id_client,))
    donnees = curseur.fetchall()
    conn.close()
    return render_template('fiche_client.html', donnees=donnees)

@app.route('/clients')
def liste_clients():
    conn = sqlite3.connect('base_de_donnees.db')
    curseur = conn.cursor()
    curseur.execute('SELECT * FROM clients;')
    donnees = curseur.fetchall()
    conn.close()
    return render_template('liste_clients.html', donnees=donnees)

@app.route('/ajouter_client', methods=['GET', 'POST'])
def ajouter_client():
    if request.method == 'POST':
        nom = request.form['nom']
        prenom = request.form['prenom']
        conn = sqlite3.connect('base_de_donnees.db')
        curseur = conn.cursor()
        curseur.execute('INSERT INTO clients (nom, prenom, adresse) VALUES (?, ?, ?)', (nom, prenom, "Adresse"))
        conn.commit()
        conn.close()
        return redirect(url_for('liste_clients'))
    return render_template('ajouter_client.html')

@app.route('/supprimer_client/<int:id_client>')
def supprimer_client(id_client):
    conn = sqlite3.connect('base_de_donnees.db')
    curseur = conn.cursor()
    curseur.execute('DELETE FROM clients WHERE id = ?', (id_client,))
    conn.commit()
    conn.close()
    return redirect(url_for('liste_clients'))

@app.route('/livres')
def liste_livres():
    conn = sqlite3.connect('base_de_donnees.db')
    curseur = conn.cursor()
    curseur.execute('SELECT * FROM livres;')
    donnees = curseur.fetchall()
    conn.close()
    return render_template('liste_livres.html', donnees=donnees)

@app.route('/ajouter_livre', methods=['GET', 'POST'])
def ajouter_livre():
    if request.method == 'POST':
        titre = request.form['titre']
        auteur = request.form['auteur']
        conn = sqlite3.connect('base_de_donnees.db')
        curseur = conn.cursor()
        curseur.execute('SELECT * FROM livres WHERE titre = ? AND auteur = ?', (titre, auteur))
        livre = curseur.fetchone()
        if livre:
            curseur.execute('UPDATE livres SET quantite = quantite + 1 WHERE titre = ? AND auteur = ?', (titre, auteur))
        else:
            curseur.execute('INSERT INTO livres (titre, auteur) VALUES (?, ?)', (titre, auteur))
        conn.commit()
        conn.close()
        return redirect(url_for('liste_livres'))
    return render_template('ajouter_livre.html')

@app.route('/supprimer_livre/<int:id_livre>')
def supprimer_livre(id_livre):
    conn = sqlite3.connect('base_de_donnees.db')
    curseur = conn.cursor()
    curseur.execute('SELECT quantite FROM livres WHERE id = ?', (id_livre,))
    quantite = curseur.fetchone()[0]
    if quantite > 1:
        curseur.execute('UPDATE livres SET quantite = quantite - 1 WHERE id = ?', (id_livre,))
    else:
        curseur.execute('DELETE FROM livres WHERE id = ?', (id_livre,))
    conn.commit()
    conn.close()
    return redirect(url_for('liste_livres'))

@app.route('/emprunts')
def liste_emprunts():
    conn = sqlite3.connect('base_de_donnees.db')
    curseur = conn.cursor()
    curseur.execute('SELECT * FROM emprunts;')
    donnees = curseur.fetchall()
    conn.close()
    return render_template('liste_emprunts.html', donnees=donnees)

@app.route('/ajouter_emprunt', methods=['GET', 'POST'])
def ajouter_emprunt():
    if request.method == 'POST':
        id_client = request.form['id_client']
        id_livre = request.form['id_livre']
        conn = sqlite3.connect('base_de_donnees.db')
        curseur = conn.cursor()
        curseur.execute('SELECT quantite FROM livres WHERE id = ?', (id_livre,))
        livre = curseur.fetchone()
        if livre and livre[0] > 0:
            curseur.execute('INSERT INTO emprunts (id_client, id_livre, statut) VALUES (?, ?, ?)', (id_client, id_livre, 1))
            curseur.execute('UPDATE livres SET quantite = quantite - 1 WHERE id = ?', (id_livre,))
        conn.commit()
        conn.close()
        return redirect(url_for('liste_emprunts'))
    return render_template('ajouter_emprunt.html')

@app.route('/retour_emprunt/<int:id_emprunt>')
def retour_emprunt(id_emprunt):
    conn = sqlite3.connect('base_de_donnees.db')
    curseur = conn.cursor()
    curseur.execute('SELECT id_livre FROM emprunts WHERE id = ? AND statut = 1', (id_emprunt,))
    emprunt = curseur.fetchone()
    if emprunt:
        curseur.execute('UPDATE livres SET quantite = quantite + 1 WHERE id = ?', (emprunt[0],))
        curseur.execute('UPDATE emprunts SET statut = 0, date_retour = CURRENT_TIMESTAMP WHERE id = ?', (id_emprunt,))
    conn.commit()
    conn.close()
    return redirect(url_for('liste_emprunts'))

if __name__ == "__main__":
    app.run(debug=True)



