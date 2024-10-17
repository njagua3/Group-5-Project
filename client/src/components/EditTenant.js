import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom'; // Using useNavigate for navigation

const EditTenant = () => {
    const { id } = useParams(); // Get the tenant ID from the URL
    const navigate = useNavigate(); // Initialize useNavigate
    const [tenant, setTenant] = useState({ name: '', rent_amount: '', room_number: '', property_id: '' });

    useEffect(() => {
        // Fetch the tenant data based on the ID
        const fetchTenant = async () => {
            const response = await fetch(`http://localhost:5555/tenants/${id}`);
            const data = await response.json();
            setTenant(data);
        };

        fetchTenant(); // Fetch tenant data when the component loads
    }, [id]);

    // Handle form changes
    const handleChange = (e) => {
        const { name, value } = e.target;
        setTenant({ ...tenant, [name]: value });
    };

    // Handle form submission for updating the tenant
    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            await fetch(`http://localhost:5555/tenants/${id}`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(tenant),
            });
            navigate('/tenants'); // Redirect back to tenants list after editing
        } catch (error) {
            console.error('Error updating tenant:', error);
        }
    };

    return (
        <div className="container">
            <h1>Edit Tenant</h1>
            <form onSubmit={handleSubmit}>
                <input
                    type="text"
                    name="name"
                    value={tenant.name}
                    onChange={handleChange}
                    placeholder="Tenant Name"
                />
                <input
                    type="text"
                    name="rent_amount"
                    value={tenant.rent_amount}
                    onChange={handleChange}
                    placeholder="Rent Amount"
                />
                <input
                    type="text"
                    name="room_number"
                    value={tenant.room_number}
                    onChange={handleChange}
                    placeholder="Room Number"
                />
                <input
                    type="text"
                    name="property_id"
                    value={tenant.property_id}
                    onChange={handleChange}
                    placeholder="Property ID"
                />
                <button type="submit">Update Tenant</button>
            </form>
        </div>
    );
};

export default EditTenant;
