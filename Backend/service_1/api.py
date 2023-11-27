from flask import Flask, jsonify, request
import snowflake.connector
from snowflake.connector import errors
from flask_cors import CORS
import spacy

app = Flask(__name__)
CORS(app)


snowflake_user = 'METAGILE'
snowflake_password = 'Tresbavard2@'
snowflake_account = 'GOLUJUF-PX53325'
snowflake_database = 'BOUTIQUE'
snowflake_schema = 'public'  


conn = snowflake.connector.connect(
    user=snowflake_user,
    password=snowflake_password,
    account=snowflake_account,
    database=snowflake_database,
    schema=snowflake_schema
)


# Endpoint de extract
@app.route('/spacyextract', methods=['POST'])
def spacy_extract():
    nlp = spacy.load("../model/model_prestige")
    try:
        data = request.get_json()
        if 'text' not in data:
            return jsonify({'message': 'Clé manquante dans les données.'}), 400

        doc = nlp(data['text'])
        #categories = [ent.label_ for ent in doc.ents]
        entities = [{'text': ent.text, 'label': ent.label_} for ent in doc.ents]
        print(entities)

        return jsonify({'message': 'OK', 'categories': entities}), 200

    except Exception as e:
        return jsonify({'message': 'Erreur lors du traitement : ' + str(e)}), 500

# Endpoint de login
@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    query = 'SELECT ID_Admin, Nom FROM PRESTIGE_ADMIN WHERE Pseudo = %s AND Passeword = %s'
    with conn.cursor() as cursor:
        cursor.execute(query, (username, password))
        admin = cursor.fetchone()

    if admin:
        admin_id, admin_nom = admin
        return jsonify({'message': 'Login reussi', 'admin_id': admin_id, 'admin_nom': admin_nom}), 200
    else:
        return jsonify({'message': 'Echec de la connexion'}), 401

# Endpoint fournisseur
@app.route('/add_fournisseur', methods=['POST'])
def creer_fournisseur():
    try:
        data = request.json
        nom_fournisseur = data.get('nom')
        adresse_fournisseur = data.get('adresse')
        contact_fournisseur = data.get('contact')
        print(nom_fournisseur, adresse_fournisseur, contact_fournisseur)
        query = '''
        INSERT INTO Fournisseurs (Nom_Fournisseur, Adresse, Contact)
        VALUES (%s, %s, %s)
        '''
        with conn.cursor() as cursor:
            cursor.execute(query, (nom_fournisseur, adresse_fournisseur, contact_fournisseur))

        return jsonify({'message': 'Fournisseur créé avec succès'}), 201

    except errors.Error as e:
        return jsonify({'message': 'Erreur lors de l\'insertion du fournisseur : ' , 'erreur': str(e)}), 500

    except Exception as e:
        return jsonify({'message': 'Erreur inattendue lors de la création du fournisseur : '  , 'erreur': str(e)}), 500

# Endpoint créer un client
@app.route('/creer_client', methods=['POST'])
def creer_client():
    try:
        data = request.json
        nom_client = data.get('nom')
        adresse_client = data.get('adresse')
        contact_client = data.get('contact')

        query = '''
        INSERT INTO Clients (Nom_Client, Adresse, Contact)
        VALUES (%s, %s, %s)
        '''
        with conn.cursor() as cursor:
            cursor.execute(query, (nom_client, adresse_client, contact_client))

        return jsonify({'message': 'Client créé avec succès'}), 201
    
    except errors.Error as e:
        return jsonify({'message': 'Erreur lors de l\'insertion du client : ' , 'erreur': str(e)}), 500

    except Exception as e:
        return jsonify({'message': 'Erreur inattendue lors de la création du client : '  , 'erreur': str(e)}), 500 


# Endpoints pour afficher les données
@app.route('/afficher_fournisseur')
def afficher_fournisseur():
    try:
        query = 'SELECT * FROM FOURNISSEURS'
        with conn.cursor() as cursor:
            cursor.execute(query)
            fournisseurs = cursor.fetchall()

            fournisseurs_transformes = [
            {
                'ID_Fournisseur': row[0],
                'Nom_Fournisseur': row[1],
                'Adresse': row[2],
                'Contact': row[3]
            }
            for row in fournisseurs
        ]

        return jsonify({'fournisseurs': fournisseurs_transformes})
    except errors.Error as e:
        return jsonify({'message': 'Erreur lors de la récupération des fournisseurs', 'erreur': str(e)}), 500
    except Exception as e:
        return jsonify({'message': 'Erreur de connexion', 'erreur': str(e)}), 500

@app.route('/afficher_client')
def afficher_client():
    try:
        query = 'SELECT * FROM Clients'
        with conn.cursor() as cursor:
            cursor.execute(query)
            clients = cursor.fetchall()

        return jsonify({'clients': clients})
    except errors.Error as e:
        return jsonify({'message': 'Erreur lors de la recupération des clients', 'errur': str(e)}), 500
    except Exception as e:
        return jsonify({'message': 'Erreur de connection', 'erreur':str(e)}), 500

@app.route('/afficher_stock_entree')
def afficher_stock_entree():
    query = 'SELECT * FROM Stock_Entrees'
    with conn.cursor() as cursor:
        cursor.execute(query)
        stock_entree = cursor.fetchall()

    return jsonify({'stock_entree': stock_entree})

@app.route('/afficher_stock_sortie')
def afficher_stock_sortie():
    query = 'SELECT * FROM Stock_Sorties'
    with conn.cursor() as cursor:
        cursor.execute(query)
        stock_sortie = cursor.fetchall()

    return jsonify({'stock_sortie': stock_sortie})

# Endpoints pour insérer des données
@app.route('/inserer_stock_entree', methods=['POST'])
def inserer_stock_entree():
    data = request.json
    id_produit = data.get('id_produit')
    quantite_entree = data.get('quantite_entree')
    date_entree = data.get('date_entree')
    id_fournisseur = data.get('id_fournisseur')

    query = '''
    INSERT INTO Stock_Entrees (ID_Produit, Quantite_Entree, Date_Entree, ID_Fournisseur)
    VALUES (%s, %s, %s, %s)
    '''
    with conn.cursor() as cursor:
        cursor.execute(query, (id_produit, quantite_entree, date_entree, id_fournisseur))

    return jsonify({'message': 'Données d\'entrée insérées avec succès'}), 200

@app.route('/inserer_stock_sortie', methods=['POST'])
def inserer_stock_sortie():
    data = request.json
    id_produit = data.get('id_produit')
    quantite_sortie = data.get('quantite_sortie')
    date_sortie = data.get('date_sortie')
    id_client = data.get('id_client')

    query = '''
    INSERT INTO Stock_Sorties (ID_Produit, Quantite_Sortie, Date_Sortie, ID_Client)
    VALUES (%s, %s, %s, %s)
    '''
    with conn.cursor() as cursor:
        cursor.execute(query, (id_produit, quantite_sortie, date_sortie, id_client))

    return jsonify({'message': 'Données de sortie insérées avec succès'}), 200

if __name__ == '__main__':
    app.run(debug=True, port=5000)
