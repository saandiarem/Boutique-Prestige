from flask import Flask, jsonify, request
import snowflake.connector
from snowflake.connector import errors
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
        with create_connection().cursor() as cursor:
            cursor.execute(query, (nom_fournisseur, adresse_fournisseur, contact_fournisseur))

        return jsonify({'message': 'Fournisseur créé avec succès'}), 201

    except errors.Error as e:
        return jsonify({'message': 'Erreur lors de l\'insertion du fournisseur : ' , 'erreur': str(e)}), 500

    except Exception as e:
        return jsonify({'message': 'Erreur inattendue lors de la création du fournisseur : '  , 'erreur': str(e)}), 500
    

# Endpoints pour afficher les données
@app.route('/afficher_fournisseur')
def afficher_fournisseur():
    try:
        query = 'SELECT * FROM FOURNISSEURS'
        with create_connection().cursor() as cursor:
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


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=6040)