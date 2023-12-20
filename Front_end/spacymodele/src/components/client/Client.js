import React from 'react';
import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';

const Client = () => {
    const navigate = useNavigate();
    const [nom, setNom] = useState('');
    const [adresse, setAdresse] = useState('');
    const [contact, setContact] = useState('');
    const [listeClients, setListeClients] = useState([]);
    const [error, setError] = useState('');
    const [textInput, setTextInput] = useState('');
    const [responseMessage, setResponseMessage] = useState('');
    const [isFormVisible, setFormVisible] = useState(false);
    const [btnlabel, setBtnlabel] = useState('+');

    const handleNomChange = (e) => {
        setNom(e.target.value);
    };

    const handleAdresseChange = (e) => {
        setAdresse(e.target.value);
    };

    const handleContactChange = (e) => {
        setContact(e.target.value);
    };

    const handleTextChange = (event) => {
        setTextInput(event.target.value);
    };

    useEffect(() => {
        const fetchData = async () => {
        try {
            const response = await axios.get('http://localhost:5000/afficher_client');
            setListeClients(response.data.clients);
            console.log(response.data.clients)
        } catch (error) {
            console.error('Erreur lors de la récupération de la liste des fournisseurs:', error);
        }
    };
        fetchData();
    }, []);

    const toggleForm = () => {
        setFormVisible(!isFormVisible);
        setBtnlabel(isFormVisible ? '+' : '-');
    };

    const sendDataClient = async (e) => {
        e.preventDefault();
        if (textInput.trim() !== '') {
            // Envoyez le texte au backend
            axios.post('http://localhost:5000/out_stock', { text: textInput })
              .then((response) => {
                const messages = response.data.message
                if (messages) {
                    console.log('Réponse du serveur:', messages);
                    console.log('------');
                    console.log(messages.length);
                    if (messages.length === 0){
                        setTextInput("");
                        navigate("/dashbord");
                    }
                    else{
                        navigate("/manageClient");
                        setResponseMessage(messages);
                    }
                  } else {
                    console.log('Insertion réussie!');
                };
              })
              .catch((error) => {
                console.error('Erreur lors de la requête au serveur:', error);
      
                // Mettez à jour le message de réponse en cas d'erreur
                setResponseMessage('Une erreur s\'est produite lors de la requête au serveur.');
              });
          } else {
            // Mettez à jour le message de réponse si le champ de texte est vide
            setResponseMessage('Veuillez saisir du texte dans le champ ci-dessus.');
          }
    };

    const onSubmit = async (e) => {
        e.preventDefault();
        try {
            const response = await axios.post('http://localhost:5000/add_client', {
            nom: nom,
            adresse: adresse,
            contact: contact,
            });
          
          if (response.status === 201) {
            console.log(response.data.admin_nom)
            setAdresse('');
            setContact('');
            setNom('');
            navigate('/dashbord');
            console.log(response.data);
          }
        } catch (error) {
            console.error('Error during add client:', error);
            setError('Information incorrecte.');
        }
    };

    return (
        <div className="container"><br/>
        <div className='row'>
            <div className='col-md-6 col-12'>
            <h3>Ajouter un nouveau Client</h3><br/>
                <form onSubmit={onSubmit}>
                    <div className="mb-3">
                        <label className="form-label"><strong>Nom</strong></label>
                        <input type="text" className="form-control w-50"
                        value={nom}
                        name="marque"
                        onChange={handleNomChange}
                        required/>
                    </div>
                    <div className="mb-3">
                        <label className="form-label"><strong>Adresse</strong></label>
                        <input type="text" className="form-control w-50"
                        value={adresse}
                        name="marque"
                        onChange={handleAdresseChange}
                        required/>
                    </div>
                    <div className="mb-3">
                        <label className="form-label"><strong>Contact</strong></label>
                        <input type="text" className="form-control w-50"
                        value={contact}
                        name="marque"
                        onChange={handleContactChange}
                        required/>
                    </div>
                    <div className="mb-3">
                        {error && <p className="text-danger">{error}</p>}
                    </div>
                    <button type="submit" className="btn btn-primary">Ajout</button>
                </form><br/>
            </div>
            <div className="col-md-4 col-12">
                    <h3>Enregistrer des ventes</h3><br/>
                    <button onClick={toggleForm} className="btn btn-info"><strong>{btnlabel}</strong></button><br/>
                        {isFormVisible && (
                        <div>
                            <form onSubmit={sendDataClient}>
                                <div className="form-group">
                                <label htmlFor="exampleTextarea"></label>
                                <textarea className="form-control" id="exampleTextarea" rows="4"
                                value={textInput} 
                                onChange={handleTextChange}/><br/>
                                </div>
                                <button type="submit" className="btn btn-primary">Submit</button>
                            </form>
                            <div className="mb-3">
                                    {Array.isArray(responseMessage) && <div >{responseMessage.map((message, index) => (
                                    <li key={index} className="text-danger">{message.message}</li>
                                ))}</div>}
                            </div>
                        </div>
                    )};
            </div>
            </div>
                <div className='row mt-2'>
                    <h3>Liste des Clients</h3>
                    <div className="row mt-2">
                        {listeClients.map(OneClient => (
                        <div key={OneClient.ID_CLIENT} className="col-sm-12 col-md-6 col-lg-4">
                            <div className="card mb-5" id="divCard" 
                            onMouseEnter={e => e.currentTarget.style.border = 'solid 4px #008080'}
                            onMouseLeave={e => e.currentTarget.style.border = 'solid 4px #f5f5f5'}
                            >
                            <h5 className="card-title"><strong>Nom : </strong>{OneClient.Nom_Client} </h5>
                            <p className="card-text"><strong>Adresse: </strong>{OneClient.Adresse} </p>
                            <p className="card-text"><strong>Contact: </strong>{OneClient.Contact} </p>
                            <p className="card-text d-none">id: {OneClient.ID_CLIENT}</p>
                            <div id="divEdit">
                                <Link id="idEdit" to={"/edit/" + OneClient.ID_CLIENT}>Edit</Link>
                            </div>
                            </div>
                        </div>
                        ))}
                    </div>
                </div>  
            </div>
    );
};

export default Client;

