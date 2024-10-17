import React from 'react';
import { Link } from 'react-router-dom';
import '../styles.css'; // Ensure styles are imported

const Navbar = () => {
    return (
        <nav>
            <ul>
                <li><Link to="/">Home</Link></li>
                <li><Link to="/tenants">Tenants</Link></li>
                <li><Link to="/landlords">Landlords</Link></li>
                <li><Link to="/properties">Properties</Link></li>
            </ul>
        </nav>
    );
};

export default Navbar;
