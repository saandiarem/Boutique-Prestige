import React from 'react';
import {Routes,Route} from 'react-router-dom';
import Fournisseur from '../fournisseur/Fournisseur';
import Client from '../client/Client';
import Product from '../product/Product';
import Symptomes from '../prediction/Symptomes';
import Dashbord from '../dashbord/Dashbord';

export default function Approuter() {
  return (
    <div>
        <Routes>
            <Route path='/dashbord' element={<Dashbord/>}/>
            <Route path='/manageFournisseur' element={<Fournisseur/>}/>
            <Route path='/manageClient' element={<Client/>}/>
            <Route path='/addProduct' element={<Product/>}/>
            <Route path='/checkDisease' element={<Symptomes/>}/>
        </Routes>
    </div>
  )
}
