import React, { useState } from 'react';
import "bootstrap/dist/css/bootstrap.min.css";
import Sidebar from "./components/sidebar/Sidebar";
import './App.css';
import Index from "./components/approuter";
function App() {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  return (
    <div className="">
      {isAuthenticated ? <Sidebar setIsAuthenticated={setIsAuthenticated} /> : <Index setIsAuthenticated={setIsAuthenticated} />}
    </div>
  );
}

export default App;
