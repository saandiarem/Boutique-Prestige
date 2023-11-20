from flask import Flask, jsonify, request
import snowflake.connector
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Informations de connexion à Snowflake
snowflake_user = 'METAGILE'
snowflake_password = 'Tresbavard2@'
snowflake_account = 'GOLUJUF-PX53325'
snowflake_database = 'PRESTIGE'
snowflake_schema = 'public'  # Remplacez par le schéma de votre choix

# Établir une connexion à Snowflake
conn = snowflake.connector.connect(
    user=snowflake_user,
    password=snowflake_password,
    account=snowflake_account,
    database=snowflake_database,
    schema=snowflake_schema
)

# Endpoint de login
@app.route('/login', methods=['POST'])
def login():
    # Récupérez les informations d'identification depuis la requête POST
    data = request.json
    username = data.get('username')
    password = data.get('password')

    # Vérifiez les informations d'identification dans la base de données
    query = 'SELECT ID_Admin, Nom FROM Admin WHERE Pseudo = %s AND Passeword = %s'
    with conn.cursor() as cursor:
        cursor.execute(query, (username, password))
        admin = cursor.fetchone()

    # Si les informations d'identification sont valides, retournez l'ID de l'admin et son nom
    if admin:
        admin_id, admin_nom = admin
        return jsonify({'message': 'Login reussi', 'admin_id': admin_id, 'admin_nom': admin_nom}), 200
    else:
        return jsonify({'message': 'Echec de la connexion'}), 401

# Endpoint pour créer un fournisseur
@app.route('/add_fournisseur', methods=['POST'])
def creer_fournisseur():
    # Récupérez les données du fournisseur depuis la requête POST
    data = request.json
    nom_fournisseur = data.get('nom_fournisseur')
    adresse_fournisseur = data.get('adresse_fournisseur')
    contact_fournisseur = data.get('contact_fournisseur')

    # Exécutez la requête pour insérer le fournisseur dans la base de données
    query = '''
    INSERT INTO Fournisseurs (Nom_Fournisseur, Adresse, Contact)
    VALUES (%s, %s, %s)
    '''
    with conn.cursor() as cursor:
        cursor.execute(query, (nom_fournisseur, adresse_fournisseur, contact_fournisseur))

    return jsonify({'message': 'Fournisseur créé avec succès'}), 201  # 201: Created

# Endpoint pour créer un client
@app.route('/creer_client', methods=['POST'])
def creer_client():
    # Récupérez les données du client depuis la requête POST
    data = request.json
    nom_client = data.get('nom_client')
    adresse_client = data.get('adresse_client')
    contact_client = data.get('contact_client')

    # Exécutez la requête pour insérer le client dans la base de données
    query = '''
    INSERT INTO Clients (Nom_Client, Adresse, Contact)
    VALUES (%s, %s, %s)
    '''
    with conn.cursor() as cursor:
        cursor.execute(query, (nom_client, adresse_client, contact_client))

    return jsonify({'message': 'Client créé avec succès'}), 201  # 201: Created


# Endpoints pour afficher les données
@app.route('/afficher_fournisseur')
def afficher_fournisseur():
    query = 'SELECT * FROM Fournisseurs'
    with conn.cursor() as cursor:
        cursor.execute(query)
        fournisseurs = cursor.fetchall()

    # Formater les résultats et les renvoyer au format JSON
    return jsonify({'fournisseurs': fournisseurs})

@app.route('/afficher_client')
def afficher_client():
    query = 'SELECT * FROM Clients'
    with conn.cursor() as cursor:
        cursor.execute(query)
        clients = cursor.fetchall()

    # Formater les résultats et les renvoyer au format JSON
    return jsonify({'clients': clients})

@app.route('/afficher_stock_entree')
def afficher_stock_entree():
    query = 'SELECT * FROM Stock_Entrees'
    with conn.cursor() as cursor:
        cursor.execute(query)
        stock_entree = cursor.fetchall()

    # Formater les résultats et les renvoyer au format JSON
    return jsonify({'stock_entree': stock_entree})

@app.route('/afficher_stock_sortie')
def afficher_stock_sortie():
    query = 'SELECT * FROM Stock_Sorties'
    with conn.cursor() as cursor:
        cursor.execute(query)
        stock_sortie = cursor.fetchall()

    # Formater les résultats et les renvoyer au format JSON
    return jsonify({'stock_sortie': stock_sortie})

# Endpoints pour insérer des données
@app.route('/inserer_stock_entree', methods=['POST'])
def inserer_stock_entree():
    # Récupérez les données d'entrée depuis la requête POST
    data = request.json
    id_produit = data.get('id_produit')
    quantite_entree = data.get('quantite_entree')
    date_entree = data.get('date_entree')
    id_fournisseur = data.get('id_fournisseur')

    # Exécutez la requête pour insérer les données d'entrée de stock dans Snowflake
    query = '''
    INSERT INTO Stock_Entrees (ID_Produit, Quantite_Entree, Date_Entree, ID_Fournisseur)
    VALUES (%s, %s, %s, %s)
    '''
    with conn.cursor() as cursor:
        cursor.execute(query, (id_produit, quantite_entree, date_entree, id_fournisseur))

    return jsonify({'message': 'Données d\'entrée insérées avec succès'}), 200

@app.route('/inserer_stock_sortie', methods=['POST'])
def inserer_stock_sortie():
    # Récupérez les données de sortie depuis la requête POST
    data = request.json
    id_produit = data.get('id_produit')
    quantite_sortie = data.get('quantite_sortie')
    date_sortie = data.get('date_sortie')
    id_client = data.get('id_client')

    # Exécutez la requête pour insérer les données de sortie de stock dans Snowflake
    query = '''
    INSERT INTO Stock_Sorties (ID_Produit, Quantite_Sortie, Date_Sortie, ID_Client)
    VALUES (%s, %s, %s, %s)
    '''
    with conn.cursor() as cursor:
        cursor.execute(query, (id_produit, quantite_sortie, date_sortie, id_client))

    return jsonify({'message': 'Données de sortie insérées avec succès'}), 200

# Exécutez l'application Flask
if __name__ == '__main__':
    app.run(debug=True, port=5000)
