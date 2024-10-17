import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { Formik, Form, Field } from 'formik';
import * as Yup from 'yup';

const Landlords = () => {
    const [landlords, setLandlords] = useState([]);
    const [loading, setLoading] = useState(true);

    const fetchLandlords = async () => {
        try {
            const response = await axios.get('http://localhost:5555/landlords');
            setLandlords(response.data);
        } catch (error) {
            console.error('Error fetching landlords:', error);
        } finally {
            setLoading(false);
        }
    };

    const addLandlord = async (values) => {
        try {
            await axios.post('http://localhost:5555/landlords', values);
            fetchLandlords();
        } catch (error) {
            console.error('Error adding landlord:', error);
        }
    };

    const deleteLandlord = async (id) => {
        try {
            await axios.delete(`http://localhost:5555/landlords/${id}`); // Fixed template literal
            fetchLandlords();
        } catch (error) {
            console.error('Error deleting landlord:', error);
        }
    };

    useEffect(() => {
        fetchLandlords();
    }, []);

    if (loading) return <p>Loading...</p>;

    return (
        <div className="container">
            <h1>Landlords</h1>
            <Formik
                initialValues={{ name: '' }}
                validationSchema={Yup.object({
                    name: Yup.string().required('Required'),
                })}
                onSubmit={addLandlord}
            >
                {({ handleSubmit }) => (
                    <Form onSubmit={handleSubmit}>
                        <Field name="name" placeholder="Landlord Name" />
                        <button type="submit">Add Landlord</button>
                    </Form>
                )}
            </Formik>
            <ul>
                {landlords.map(landlord => (
                    <li key={landlord.id}>
                        {landlord.name}
                        <button onClick={() => deleteLandlord(landlord.id)}>Delete</button>
                    </li>
                ))}
            </ul>
        </div>
    );
};

export default Landlords;
