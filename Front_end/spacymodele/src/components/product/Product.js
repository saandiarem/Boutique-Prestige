import React from 'react';
import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import pic1 from './pic1.png';

export default function Product() {
    const navigate = useNavigate();
    const [nom_produit, setNom_produit] = useState('');
    const [description, setDescription] = useState('');
    const [price, setPrice] = useState('');
    const [error, setError] = useState('');

    const handleNameChange = (e) => {
        setNom_produit(e.target.value);
    };
    const handleDescChange = (e) => {
        setDescription(e.target.value);
    };
    const handlePriceChange = (e) => {
        setPrice(e.target.value);
    };

    const onSubmit = async (e) => {
        e.preventDefault();
        try {
            const response = await axios.post('http://localhost:5000/add_product', {
            nom: nom_produit,
            desc: description,
            prix: price,
            });
          console.log(nom_produit,description,price);
          if (response.status === 201) {
            navigate('/dashbord');
            console.log(response.data);
            setNom_produit('');
            setDescription('');
            setPrice('');
          }
        } catch (error) {
            console.error('Error during add product:', error);
            setError('Information incorrecte.');
        }
      };

  return (
    <div className='container'>
        <div className="row mt-5">
        <div className="col-md-6 col-12">
            <h3>Enregistrer un Produit</h3><br/>
                <form onSubmit={onSubmit}>
                    <div className="mb-3">
                        <label className="form-label"><strong>Nom</strong></label>
                        <input type="text" className="form-control w-50"
                        value={nom_produit}
                        onChange={handleNameChange}
                        required/>
                    </div>
                    <div className="mb-3">
                        <label className="form-label"><strong>Prix</strong></label>
                        <input type="number" className="form-control w-25"
                        value={price}
                        onChange={handlePriceChange}
                        required/>
                    </div>
                    <div className="mb-3">
                        <label className="form-label"><strong>Description</strong></label>
                        <textarea className="form-control w-50" id="exampleTextarea" rows="4"
                            value={description} 
                            onChange={handleDescChange}
                            required/><br/>
                    </div>
                    <div className="mb-3">
                        {error && <p className="text-danger">{error}</p>}
                    </div>
                    <button type="submit" className="btn btn-primary">Ajout</button>
                </form><br/>
        </div>
        <div className="col-md-4 col-12">
            <img src={pic1} width="100%" alt=""/>
        </div>
        </div>
    </div>
    )
}
