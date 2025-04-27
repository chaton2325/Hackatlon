from flask import Flask, render_template, request, redirect, url_for, flash, session
import json
import os
from functools import wraps

app = Flask(__name__)
app.secret_key = 'votre_clef_secrete'
app.static_folder = 'static'  # Définir le dossier static

# Chemin du fichier JSON
DB_FILE = 'database.json'

# Initialiser la base de données si elle n'existe pas
def init_db():
    if not os.path.exists(DB_FILE):
        with open(DB_FILE, 'w') as f:
            json.dump({
                'etablissements': [],
                'admin': {'username': 'admin', 'password': 'admin123'}
            }, f)

# Charger les données
def load_data():
    with open(DB_FILE, 'r') as f:
        return json.load(f)

# Sauvegarder les données
def save_data(data):
    with open(DB_FILE, 'w') as f:
        json.dump(data, f, indent=4)

# Décorateur pour vérifier si l'utilisateur est admin
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'admin_logged_in' not in session:
            flash('Veuillez vous connecter en tant qu\'administrateur', 'danger')
            return redirect(url_for('admin_login'))
        return f(*args, **kwargs)
    return decorated_function

# Page d'accueil
@app.route('/')
def index():
    return render_template('index.html')

# Page d'ajout d'établissement
@app.route('/ajouter', methods=['GET', 'POST'])
def ajouter_etablissement():
    if request.method == 'POST':
        etablissement = {
            'id': len(load_data()['etablissements']) + 1,
            'nom': request.form['nom'],
            'lien_inscription': request.form['lien_inscription'],
            'contacts': request.form['contacts'],
            'lieu': request.form['lieu'],
            'pays': request.form['pays'],
            'valide': False,
            'lien_bot': ''
        }
        
        data = load_data()
        data['etablissements'].append(etablissement)
        save_data(data)
        
        flash('Établissement ajouté avec succès! Il sera visible après validation par l\'administrateur.', 'success')
        return redirect(url_for('index'))
        
    return render_template('ajouter.html')

# Page de liste des établissements validés
@app.route('/etablissements')
def liste_etablissements():
    data = load_data()
    etablissements = [e for e in data['etablissements'] if e['valide']]
    return render_template('etablissements.html', etablissements=etablissements)

# Page du bot pour un établissement spécifique
@app.route('/etablissement/<int:id>/bot')
def etablissement_bot(id):
    data = load_data()
    etablissement = next((e for e in data['etablissements'] if e['id'] == id and e['valide']), None)
    if not etablissement:
        flash('Établissement non trouvé ou non validé!', 'danger')
        return redirect(url_for('liste_etablissements'))
    return render_template('etablissement_bot.html', etablissement=etablissement)

# Login admin
@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        data = load_data()
        admin = data['admin']
        
        if username == admin['username'] and password == admin['password']:
            session['admin_logged_in'] = True
            flash('Connecté avec succès!', 'success')
            return redirect(url_for('admin_dashboard'))
        else:
            flash('Identifiants incorrects!', 'danger')
            
    return render_template('admin_login.html')

# Logout admin
@app.route('/admin/logout')
def admin_logout():
    session.pop('admin_logged_in', None)
    flash('Déconnecté avec succès!', 'success')
    return redirect(url_for('index'))

# Dashboard admin
@app.route('/admin/dashboard')
@admin_required
def admin_dashboard():
    data = load_data()
    etablissements = data['etablissements']
    return render_template('admin_dashboard.html', etablissements=etablissements)

# Valider un établissement
@app.route('/admin/valider/<int:id>', methods=['GET', 'POST'])
@admin_required
def valider_etablissement(id):
    if request.method == 'POST':
        lien_bot = request.form['lien_bot']
        
        data = load_data()
        for etablissement in data['etablissements']:
            if etablissement['id'] == id:
                etablissement['valide'] = True
                etablissement['lien_bot'] = lien_bot
                break
                
        save_data(data)
        flash('Établissement validé avec succès!', 'success')
        return redirect(url_for('admin_dashboard'))
        
    data = load_data()
    etablissement = next((e for e in data['etablissements'] if e['id'] == id), None)
    if not etablissement:
        flash('Établissement non trouvé!', 'danger')
        return redirect(url_for('admin_dashboard'))
        
    return render_template('valider.html', etablissement=etablissement)

# Supprimer un établissement
@app.route('/admin/supprimer/<int:id>')
@admin_required
def supprimer_etablissement(id):
    data = load_data()
    data['etablissements'] = [e for e in data['etablissements'] if e['id'] != id]
    save_data(data)
    flash('Établissement supprimé avec succès!', 'success')
    return redirect(url_for('admin_dashboard'))

if __name__ == '__main__':
    init_db()
    app.run(debug=True , host="10.7.100.25" , port=8000)