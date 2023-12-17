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


def create_connection():
    return snowflake.connector.connect(
        user=snowflake_user,
        password=snowflake_password,
        account=snowflake_account,
        database=snowflake_database,
        schema=snowflake_schema,
        warehouse=snowflake_warehouse
    )

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
        with create_connection().cursor() as cursor:
            cursor.execute(query, (nom_produit, prix_produit, description_produit))

        return jsonify({'message': 'Produit créé avec succès'}), 201

    except errors.Error as e:
        return jsonify({'message': 'Erreur lors de l\'insertion du Produit : ' , 'erreur': str(e)}), 500

    except Exception as e:
        return jsonify({'message': 'Erreur inattendue lors de l\'ajout du Produit : '  , 'erreur': str(e)}), 500


#Endpoint pour ajouter du stock
@app.route('/add_stock', methods=['POST'])
def inserer_stock_entree():
    nlp = spacy.load("./model_prestige")
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
            with create_connection().cursor() as cursor:
                cursor.execute(query_produit, (nom_produit,))
                id_produit = cursor.fetchone()[0] if cursor.rowcount > 0 else None

            # Récupérer l'ID du fournisseur
            query_fournisseur = 'SELECT ID_Fournisseur FROM Fournisseurs WHERE Nom_Fournisseur = %s'
            with create_connection().cursor() as cursor:
                cursor.execute(query_fournisseur, (nom_fournisseur,))
                id_fournisseur = cursor.fetchone()[0] if cursor.rowcount > 0 else None

            # Vérifier les IDs récupérés
            if id_produit is None or id_fournisseur is None:
                failure_records.append({
                    'message': f"Enregistrement échoué. l'ID de {nom_produit} ou de {nom_fournisseur} est introuvable."
                })
            else:
                # Effectuer l'insertion après avoir vérifié et récupéré les IDs
                query_insert = '''
                INSERT INTO Stock_Entrees (ID_Produit, Quantite_Entree, Date_Entree, ID_Fournisseur)
                VALUES (%s, %s, %s, %s)
                '''
                with create_connection().cursor() as cursor:
                    cursor.execute(query_insert, (id_produit, quantite_entree, date_entree, id_fournisseur))

        # Retourner les résultats au frontend
        return jsonify({'message': failure_records}), 200

    except errors.Error as e:
        return jsonify({'message': 'Erreur lors de l\'insertion des données d\'entrée : ', 'erreur': str(e)}), 501

    except Exception as e:
        return jsonify({'message': 'Erreur inattendue lors de l\'insertion des données d\'entrée : ', 'erreur': str(e)}), 500
    

#Endpoint pour un ou des sorties de stock
@app.route('/out_stock', methods=['POST'])
def inserer_stock_sortie():
    nlp = spacy.load("./model_prestige")
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
            with create_connection().cursor() as cursor:
                cursor.execute(query_produit, (nom_produit,))
                id_produit = cursor.fetchone()[0] if cursor.rowcount > 0 else None

            # Récupérer l'ID du client
            query_client = 'SELECT ID_CLIENT FROM CLIENTS WHERE NOM_CLIENT = %s'
            with create_connection().cursor() as cursor:
                cursor.execute(query_client, (nom_client,))
                id_client = cursor.fetchone()[0] if cursor.rowcount > 0 else None

            # Vérifier les IDs récupérés
            if id_produit is None or id_client is None:
                failure_records.append({
                    'message': f"Enregistrement échoué. l'ID du produit {nom_produit} ou du client {nom_client} est introuvable."
                })
            else:
                # Effectuer l'insertion après avoir vérifié et récupéré les IDs
                query_insert = '''
                INSERT INTO STOCK_SORTIES (ID_PRODUIT, QUANTITE_SORTIE, DATE_SORTIE, ID_CLIENT)
                VALUES (%s, %s, %s, %s)
                '''
                with create_connection().cursor() as cursor:
                    cursor.execute(query_insert, (id_produit, quantite_entree, date_sortie, id_client))

        # Retourner les résultats au frontend
        return jsonify({'message': failure_records}), 200

    except errors.Error as e:
        return jsonify({'message': 'Erreur lors de l\'insertion des données d\'entrée : ', 'erreur': str(e)}), 501

    except Exception as e:
        return jsonify({'message': 'Erreur inattendue lors de l\'insertion des données d\'entrée : ', 'erreur': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=6080)