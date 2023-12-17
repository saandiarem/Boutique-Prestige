from flask import Flask, jsonify, request
import snowflake.connector
from flask_cors import CORS

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

# Endpoint de login
@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    query = 'SELECT ID_Admin, Nom FROM PRESTIGE_ADMIN WHERE Pseudo = %s AND Passeword = %s'
    with create_connection().cursor() as cursor:
        cursor.execute(query, (username, password))
        admin = cursor.fetchone()

    if admin:
        admin_id, admin_nom = admin
        return jsonify({'message': 'Login reussi', 'admin_id': admin_id, 'admin_nom': admin_nom}), 200
    else:
        return jsonify({'message': 'Echec de la connexion'}), 401

# Endpoint pour obtenir le nombre de Produit, Fournisseur et Client
@app.route('/statistiques', methods=['GET'])
def obtenir_statistiques():
    try:
        with create_connection().cursor() as cursor:
            cursor.execute("SELECT COUNT(*) FROM PRODUITS")
            nombre_produits = cursor.fetchone()[0]

            cursor.execute("SELECT COUNT(*) FROM FOURNISSEURS")
            nombre_fournisseurs = cursor.fetchone()[0]

            cursor.execute("SELECT COUNT(*) FROM CLIENTS")
            nombre_clients = cursor.fetchone()[0]

        return jsonify({
            'product': nombre_produits,
            'fournisseurs': nombre_fournisseurs,
            'clients': nombre_clients
        }), 201

    except Exception as e:
        return jsonify({'message': 'Erreur inattendue lors de la récupération des données : ', 'erreur': str(e)}), 501

# Endpoint pour obtenir le dataset
@app.route('/dataset', methods=['GET'])
def obtenir_dataset():
    try:
        with create_connection().cursor() as cursor:
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
        return jsonify({'error': f"Erreur inattendue : {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5040)