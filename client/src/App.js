import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Route, Routes, Link } from 'react-router-dom';
import './styles.css'; // Custom styles
import Tenants from './components/Tenants';
import Landlords from './components/Landlords';
import Properties from './components/Properties';
import EditTenant from './components/EditTenant';

const App = () => {
    const [landlords, setLandlords] = useState([]);
    const [properties, setProperties] = useState([]);
    const [tenants, setTenants] = useState([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const fetchData = async () => {
            await Promise.all([fetchLandlords(), fetchProperties(), fetchTenants()]);
            setLoading(false);
        };

        fetchData();
    }, []);

    const fetchLandlords = async () => {
        const response = await fetch('http://localhost:5555/landlords');
        const data = await response.json();
        setLandlords(data);
    };

    const fetchProperties = async () => {
        const response = await fetch('http://localhost:5555/properties');
        const data = await response.json();
        setProperties(data);
    };

    const fetchTenants = async () => {
        const response = await fetch('http://localhost:5555/tenants');
        const data = await response.json();
        setTenants(data);
    };

    if (loading) return <p>Loading...</p>; // Display loading state

    return (
        <Router>
            <div>
                <nav className="navbar">
                    <div className="navbar-container">
                        <Link to="/" className="navbar-logo">
                            RINGBELT REAL ESTATE
                        </Link>
                        <ul className="nav-menu">
                            <li className="nav-item">
                                <Link to="/tenants" className="nav-links">Tenants</Link>
                            </li>
                            <li className="nav-item">
                                <Link to="/landlords" className="nav-links">Landlords</Link>
                            </li>
                            <li className="nav-item">
                                <Link to="/properties" className="nav-links">Properties</Link>
                            </li>
                        </ul>
                    </div>
                </nav>

                <div className="main-container">
                    <h1 className="main-title">RINGBELT REAL ESTATE AGENTS</h1>
                    <h2 className="subtitle">Tenant Management System</h2>

                    <Routes>
                        <Route path="/tenants" element={<Tenants tenants={tenants} />} />
                        <Route path="/landlords" element={<Landlords landlords={landlords} />} />
                        <Route path="/properties" element={<Properties properties={properties} />} />
                        <Route path="/edit-tenant/:id" element={<EditTenant tenants={tenants} />} />
                    </Routes>
                </div>
            </div>
        </Router>
    );
};

export default App;
