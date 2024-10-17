import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { Formik, Form, Field } from 'formik';
import * as Yup from 'yup';

const Properties = () => {
    const [properties, setProperties] = useState([]);
    const [loading, setLoading] = useState(true);

    const fetchProperties = async () => {
        try {
            const response = await axios.get('http://localhost:5555/properties');
            setProperties(response.data);
        } catch (error) {
            console.error('Error fetching properties:', error);
        } finally {
            setLoading(false);
        }
    };

    const addProperty = async (values) => {
        try {
            await axios.post('http://localhost:5555/properties', values);
            fetchProperties();
        } catch (error) {
            console.error('Error adding property:', error);
        }
    };

    const deleteProperty = async (id) => {
        try {
            await axios.delete(`http://localhost:5555/properties/${id}`); // Fixed template literal
            fetchProperties();
        } catch (error) {
            console.error('Error deleting property:', error);
        }
    };

    useEffect(() => {
        fetchProperties();
    }, []);

    if (loading) return <p>Loading...</p>;

    return (
        <div className="container">
            <h1>Properties</h1>
            <Formik
                initialValues={{ name: '', landlord_id: '' }}
                validationSchema={Yup.object({
                    name: Yup.string().required('Required'),
                    landlord_id: Yup.string().required('Required'),
                })}
                onSubmit={addProperty}
            >
                {({ handleSubmit }) => (
                    <Form onSubmit={handleSubmit}>
                        <Field name="name" placeholder="Property Name" />
                        <Field name="landlord_id" placeholder="Landlord ID" />
                        <button type="submit">Add Property</button>
                    </Form>
                )}
            </Formik>
            <ul>
                {properties.map(property => (
                    <li key={property.id}>
                        {property.name} - Landlord ID: {property.landlord_id}
                        <button onClick={() => deleteProperty(property.id)}>Delete</button>
                    </li>
                ))}
            </ul>
        </div>
    );
};

export default Properties;
