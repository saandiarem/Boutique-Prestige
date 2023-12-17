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
        with create_connection().cursor() as cursor:
            cursor.execute(query, (nom_client, adresse_client, contact_client))

        return jsonify({'message': 'Client créé avec succès'}), 201
    
    except errors.Error as e:
        return jsonify({'message': 'Erreur lors de l\'insertion du client : ' , 'erreur': str(e)}), 500

    except Exception as e:
        return jsonify({'message': 'Erreur inattendue lors de la création du client : '  , 'erreur': str(e)}), 500 


@app.route('/afficher_client')
def afficher_client():
    try:
        query = 'SELECT * FROM Clients'
        with create_connection().cursor() as cursor:
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
        return jsonify({'message': 'Erreur de connection', 'erreur':str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5080)