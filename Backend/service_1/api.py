from flask import Flask, jsonify, request
import snowflake.connector
from snowflake.connector import errors
from flask_cors import CORS
import spacy

app = Flask(__name__)
CORS(app)


snowflake_user = 'METAGILE'
snowflake_password = 'Tresbavard2@'
snowflake_account = 'EFAYRLD-PD16606'
snowflake_database = 'BOUTIQUE'
snowflake_schema = 'public'
snowflake_warehouse = 'publique'  


conn = snowflake.connector.connect(
    user=snowflake_user,
    password=snowflake_password,
    account=snowflake_account,
    database=snowflake_database,
    schema=snowflake_schema,
    warehouse = snowflake_warehouse
)


# Endpoint de extract
@app.route('/spacyextract', methods=['POST'])
def spacy_extract():
    nlp = spacy.load("../modeles/model_prestige")
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
        return jsonify({'message': 'Login reussi', 'admin_id': admin_id, 'admin_nom': admin_nom}), 201
    else:
        return jsonify({'message': 'Echec de la connexion'}), 401

# Endpoint pour obtenir le nombre de Produit,Fournisseur et Client
@app.route('/statistiques', methods=['GET'])
def obtenir_statistiques():
    try:
        cursor = conn.cursor()

        cursor.execute("SELECT COUNT(*) FROM PRODUITS")
        nombre_produits = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM FOURNISSEURS")
        nombre_fournisseurs = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM CLIENTS")
        nombre_clients = cursor.fetchone()[0]

        cursor.close()

        return jsonify({
            'product': nombre_produits,
            'fournisseurs': nombre_fournisseurs,
            'clients': nombre_clients
        }), 201

    except Exception as e:
        return jsonify({'message': 'Erreur inattendue lors de la recupération des donnees : '  , 'erreur': str(e)}), 501

# Endpoint pour obtenir le dataset
@app.route('/dataset', methods=['GET'])
def obtenir_dataset():
    try:
        cursor = conn.cursor()
        query = """
            SELECT
                P.NOM_PRODUIT,
                P.PRIX_UNITAIRE,
                COALESCE(SUM(SE.QUANTITE_ENTREE), 0) AS QUANTITE_ENTREE,
                COALESCE(SUM(SS.QUANTITE_SORTIE), 0) AS QUANTITE_SORTIE,
                GREATEST(COALESCE(SUM(SE.QUANTITE_ENTREE), 0) - COALESCE(SUM(SS.QUANTITE_SORTIE), 0), 0) AS QUANTITE_RESTANTE
            FROM
                PRODUITS P
            LEFT JOIN
                STOCK_ENTREES SE ON P.ID_PRODUIT = SE.ID_PRODUIT
            LEFT JOIN
                STOCK_SORTIES SS ON P.ID_PRODUIT = SS.ID_PRODUIT
            GROUP BY
                P.NOM_PRODUIT, P.PRIX_UNITAIRE
        """
        cursor.execute(query)

        results = cursor.fetchall()

        cursor.close()

        dataset = []
        for row in results:
            dataset.append({
                'Nom': row[0],
                'price': row[1],
                'stentree': row[2],
                'stsortie': row[3],
                'stock': row[4]
            })

        return jsonify(dataset), 201
    except Exception as e:
        # Gestion des autres erreurs
        return jsonify({'error': f"Erreur inattendue : {str(e)}"}), 500


# Endpoint Produit
@app.route('/add_product', methods=['POST'])
def add_product():
    try:
        data = request.json
        nom_produit = data.get('nom')
        prix_produit = data.get('prix')
        description_produit = data.get('desc')
        print(nom_produit, prix_produit, description_produit)
        query = '''
        INSERT INTO PRODUITS (NOM_PRODUIT, PRIX_UNITAIRE, DESCRIPTION)
        VALUES (%s, %s, %s)
        '''
        with conn.cursor() as cursor:
            cursor.execute(query, (nom_produit, prix_produit, description_produit))

        return jsonify({'message': 'Produit créé avec succès'}), 201

    except errors.Error as e:
        return jsonify({'message': 'Erreur lors de l\'insertion du Produit : ' , 'erreur': str(e)}), 500

    except Exception as e:
        return jsonify({'message': 'Erreur inattendue lors de l\'ajout du Produit : '  , 'erreur': str(e)}), 501

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
        return jsonify({'message': 'Erreur inattendue lors de la création du fournisseur : '  , 'erreur': str(e)}), 501

# Endpoint créer un client
@app.route('/add_client', methods=['POST'])
def creer_client():
    try:
        data = request.json
        nom_client = data.get('nom')
        adresse_client = data.get('adresse')
        contact_client = data.get('contact')

        query = '''
        INSERT INTO Clients (NOM_CLIENT, ADRESSE, CONTACT)
        VALUES (%s, %s, %s)
        '''
        with conn.cursor() as cursor:
            cursor.execute(query, (nom_client, adresse_client, contact_client))

        return jsonify({'message': 'Client créé avec succès'}), 201
    
    except errors.Error as e:
        return jsonify({'message': 'Erreur lors de l\'insertion du client : ' , 'erreur': str(e)}), 500

    except Exception as e:
        return jsonify({'message': 'Erreur inattendue lors de la création du client : '  , 'erreur': str(e)}), 501 


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

        return jsonify({'fournisseurs': fournisseurs_transformes}), 201
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
            
            cleints_transformes = [
            {
                'ID_CLIENT': row[0],
                'Nom_Client': row[1],
                'Adresse': row[2],
                'Contact': row[3]
            }
            for row in clients
        ]

        return jsonify({'clients': cleints_transformes})
    except errors.Error as e:
        return jsonify({'message': 'Erreur lors de la recupération des clients', 'errur': str(e)}), 500
    except Exception as e:
        return jsonify({'message': 'Erreur de connection', 'erreur':str(e)}), 501

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

# Endpoint pour insérer des données d'entrée
@app.route('/add_stock', methods=['POST'])
def inserer_stock_entree():
    nlp = spacy.load("../modeles/model_prestige")
    try:
        data = request.get_json()
        if 'text' not in data:
            return jsonify({'message': 'Clé manquante dans les données.'}), 400

        # Extraire les entités à partir du texte avec le modèle SpaCy
        doc = nlp(data['text'])
        entities_list = [{'text': ent.text, 'label': ent.label_} for ent in doc.ents]

        # Listes pour stocker les résultats
        failure_records = []

        # Traiter chaque ensemble d'entités
        for i in range(0, len(entities_list), 4):
            # Extraire les informations nécessaires pour une ligne
            nom_fournisseur = entities_list[i].get('text') if entities_list[i].get('label') == 'NomFournisseur' else None
            nom_produit = entities_list[i + 1].get('text') if entities_list[i + 1].get('label') == 'NomProduit' else None
            quantite_entree = entities_list[i + 2].get('text') if entities_list[i + 2].get('label') == 'Stock' else None
            date_entree = entities_list[i + 3].get('text') if entities_list[i + 3].get('label') == 'Date' else None

            # Récupérer l'ID du produit
            query_produit = 'SELECT ID_Produit FROM Produits WHERE Nom_Produit = %s'
            with conn.cursor() as cursor:
                cursor.execute(query_produit, (nom_produit,))
                id_produit = cursor.fetchone()[0] if cursor.rowcount > 0 else None

            # Récupérer l'ID du fournisseur
            query_fournisseur = 'SELECT ID_Fournisseur FROM Fournisseurs WHERE Nom_Fournisseur = %s'
            with conn.cursor() as cursor:
                cursor.execute(query_fournisseur, (nom_fournisseur,))
                id_fournisseur = cursor.fetchone()[0] if cursor.rowcount > 0 else None

            # Vérifier les IDs récupérés
            if id_produit is None or id_fournisseur is None:
                failure_records.append({
                    'message': f"le produit {nom_produit} ou le fournisseur {nom_fournisseur} est introuvable."
                })
            else:
                # Effectuer l'insertion après avoir vérifié et récupéré les IDs
                query_insert = '''
                INSERT INTO Stock_Entrees (ID_Produit, Quantite_Entree, Date_Entree, ID_Fournisseur)
                VALUES (%s, %s, %s, %s)
                '''
                with conn.cursor() as cursor:
                    cursor.execute(query_insert, (id_produit, quantite_entree, date_entree, id_fournisseur))

        # Retourner les résultats au frontend
        return jsonify({'message': failure_records}), 201

    except errors.Error as e:
        return jsonify({'message': 'Erreur lors de l\'insertion des données d\'entrée : ', 'erreur': str(e)}), 501

    except Exception as e:
        return jsonify({'message': 'Erreur inattendue lors de l\'insertion des données d\'entrée : ', 'erreur': str(e)}), 500


#Endpoint pour un ou des sorties de stock
@app.route('/out_stock', methods=['POST'])
def inserer_stock_sortie():
    nlp = spacy.load("../modeles/model_prestige")
    try:
        data = request.get_json()
        if 'text' not in data:
            return jsonify({'message': 'Clé manquante dans les données.'}), 400

        # Extraire les entités à partir du texte avec le modèle SpaCy
        doc = nlp(data['text'])
        entities_list = [{'text': ent.text, 'label': ent.label_} for ent in doc.ents]

        # Listes pour stocker les résultats
        failure_records = []

        # Traiter chaque ensemble d'entités
        for i in range(0, len(entities_list), 4):
            # Extraire les informations nécessaires pour une ligne
            nom_client = entities_list[i].get('text') if entities_list[i].get('label') == 'NomFournisseur' else None
            nom_produit = entities_list[i + 1].get('text') if entities_list[i + 1].get('label') == 'NomProduit' else None
            quantite_entree = entities_list[i + 2].get('text') if entities_list[i + 2].get('label') == 'Stock' else None
            date_sortie = entities_list[i + 3].get('text') if entities_list[i + 3].get('label') == 'Date' else None

            # Récupérer l'ID du produit
            query_produit = 'SELECT ID_Produit FROM Produits WHERE Nom_Produit = %s'
            with conn.cursor() as cursor:
                cursor.execute(query_produit, (nom_produit,))
                id_produit = cursor.fetchone()[0] if cursor.rowcount > 0 else None

            # Récupérer l'ID du client
            query_client = 'SELECT ID_CLIENT FROM CLIENTS WHERE NOM_CLIENT = %s'
            with conn.cursor() as cursor:
                cursor.execute(query_client, (nom_client,))
                id_client = cursor.fetchone()[0] if cursor.rowcount > 0 else None

            # Vérifier les IDs récupérés
            if id_produit is None or id_client is None:
                failure_records.append({
                    'message': f"le produit {nom_produit} ou le client {nom_client} est introuvable."
                })
            else:
                # Effectuer l'insertion après avoir vérifié et récupéré les IDs
                query_insert = '''
                INSERT INTO STOCK_SORTIES (ID_PRODUIT, QUANTITE_SORTIE, DATE_SORTIE, ID_CLIENT)
                VALUES (%s, %s, %s, %s)
                '''
                with conn.cursor() as cursor:
                    cursor.execute(query_insert, (id_produit, quantite_entree, date_sortie, id_client))

        # Retourner les résultats au frontend
        return jsonify({'message': failure_records}), 201

    except errors.Error as e:
        return jsonify({'message': 'Erreur lors de l\'insertion des données d\'entrée : ', 'erreur': str(e)}), 501

    except Exception as e:
        return jsonify({'message': 'Erreur inattendue lors de l\'insertion des données d\'entrée : ', 'erreur': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
