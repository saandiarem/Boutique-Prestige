import React from 'react';
import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import './login.css';
import back_log from './back_log.avif';
import axios from 'axios';

export default function Login({ setIsAuthenticated }) {
    const navigate = useNavigate();
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState('');

    const handlePseudoChange = (e) => {
        setEmail(e.target.value);
    };

    const handlePasswordChange = (e) => {
        setPassword(e.target.value);
    };

    const onSubmit = async (e) => {
      e.preventDefault();
        try {
          const response = await axios.post('http://localhost:5000/login', {
            username: email,
            password: password,
          });
          
          if (response.status === 201) {
            setIsAuthenticated(true);
            navigate('/dashbord');
            console.log(response.data.admin_nom)
          }
        } catch (error) {
            console.error('Error during login:', error);
            setError('Information incorrecte.');
        }
      };

    return (
        <section className="vh-100">
      <div className="container">
        <div className="row">
          <div className="col-sm-6 text-black">
            <div className="px-5 ms-xl-4">
              <i className="fas fa-handshake fa-2x me-3 pt-5 mt-xl-4" style={{ color: '#709085' }}></i>
              <span className="h1 fw-bold mb-0">Bichri Prestige</span>
            </div>

            <div className="d-flex align-items-center h-custom-2 px-5 ms-xl-4 mt-5 pt-5 pt-xl-0 mt-xl-n5">
              <form onSubmit={onSubmit} style={{ width: '23rem' }}>
                <h3 className="fw-normal mb-3 pb-3" style={{ letterSpacing: '1px' }}>Log in</h3>

                <div className="form-outline mb-4">
                  <input type="text" id="form2Example18" className="form-control form-control-lg" 
                  value={email}
                  onChange={handlePseudoChange}
                  />
                  <label className="form-label" htmlFor="form2Example18">Email address</label>
                </div>

                <div className="form-outline mb-4">
                  <input type="password" id="form2Example28" className="form-control form-control-lg" 
                  value={password}
                  onChange={handlePasswordChange}
                  />
                  <label className="form-label" htmlFor="form2Example28">Password</label>
                  {error && <p className="text-danger">{error}</p>}
                </div>

                <div className="pt-1 mb-4">
                  <button className="btn btn-info btn-lg btn-block" type="submit"
                  >Login</button>
                </div>

                <p className="small mb-5 pb-lg-2"><a className="text-muted" href="#!">Forgot password?</a></p>
                <p>Don't have an account? <a href="#!" className="link-info">Register here</a></p>
              </form>
            </div>
          </div>

          <div className="col-sm-6 px-0 d-none d-sm-block">
            <img src={back_log} alt="Login" className="img-fluid"/>
          </div>
        </div>
      </div>
    </section>
    );
};