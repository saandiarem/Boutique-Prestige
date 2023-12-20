import React from 'react'
import Login from '../login/Login'
import {Routes,Route} from 'react-router-dom';

export default function Index({ setIsAuthenticated }) {
  return (
    <div className="container mt-3">
     <Routes>
            <Route index element={<Login setIsAuthenticated={setIsAuthenticated}/>}/>
    </Routes>
    </div>
  )
}
