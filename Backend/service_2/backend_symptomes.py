from flask import Flask,request
import pickle
import json
import numpy as np
from flask_cors import CORS

load_model = pickle.load(open('../modeles/logisticReg_prestigeboutique.pickle','rb'))
# Create Flask application

app = Flask(__name__)
CORS(app)
# Define routes
#fisrt methode
@app.route('/predict',methods=['POST'])
def fct():
    request_data = request.get_json(force=True)
    age = request_data['Age']
    fievre = request_data['fièvre']
    frissons = request_data['frissons']
    maut_d_tete = request_data['maux de tête']
    fatigue = request_data['fatigue']
    nausee = request_data['nausées']
    nez_ki_coule = request_data['nez qui coule']
    eternuements = request_data['éternuements']
    maux_de_gorge = request_data['maux de gorge']
    fievre_legere = request_data['fièvre légère']
    # create numpy array from user Input
    data = np.array([[age,fievre,frissons,maut_d_tete,fatigue,nausee,nez_ki_coule,eternuements,maux_de_gorge,fievre_legere]])
    # get prediction and probability
    prediction = load_model.predict(data)
    probability = load_model.predict_proba(data)
    result = json.dumps({'pred': prediction[0],'proba':float(probability[0][1])})
    print(result)
    return result


if __name__ == '__main__':
    app.run(port=5010,debug=True)