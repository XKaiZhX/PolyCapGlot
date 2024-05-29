import React, { useState, useEffect } from 'react';
import { Form, Button, Alert } from 'react-bootstrap';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import {NavbarTools} from './Navbar.jsx'

export const VideoRequestPage = () => {
    const [error, setError] = useState('');
    const [showTokenAlert, setShowTokenAlert] = useState(false);
    const [formDisabled, setFormDisabled] = useState(false);
    const { requestVideoFunc, email, ValidarToken, token } = useAuth();
    const navigate = useNavigate();

    const supportedLanguages = [
        { id: 'AR', name: 'Árabe' },
        { id: 'BG', name: 'Búlgaro' },
        { id: 'CS', name: 'Checo' },
        { id: 'DA', name: 'Danés' },
        { id: 'DE', name: 'Alemán' },
        { id: 'EL', name: 'Griego' },
        { id: 'EN', name: 'Inglés' },
        { id: 'ES', name: 'Español' },
        { id: 'ET', name: 'Estonio' },
        { id: 'FI', name: 'Finlandés' },
        { id: 'FR', name: 'Francés' },
        { id: 'HU', name: 'Húngaro' },
        { id: 'ID', name: 'Indonesio' },
        { id: 'IT', name: 'Italiano' },
        { id: 'JA', name: 'Japonés' },
        { id: 'KO', name: 'Coreano' },
        { id: 'LT', name: 'Lituano' },
        { id: 'LV', name: 'Letón' },
        { id: 'NB', name: 'Noruego (Bokmål)' },
        { id: 'NL', name: 'Holandés' },
        { id: 'PL', name: 'Polaco' },
        { id: 'PT', name: 'Portugués (todas las variedades de portugués mixtas)' },
        { id: 'RO', name: 'Rumano' },
        { id: 'RU', name: 'Ruso' },
        { id: 'SK', name: 'Eslovaco' },
        { id: 'SL', name: 'Esloveno' },
        { id: 'SV', name: 'Sueco' },
        { id: 'TR', name: 'Turco' },
        { id: 'UK', name: 'Ucraniano' },
        { id: 'ZH', name: 'Chino' }
    ];

    useEffect(() => {
        const checkTokenValidity = async () => {
            if (!ValidarToken(token)) {
                setShowTokenAlert(true); // Mostrar el alerta de token si es inválido
                setFormDisabled(true);
            }
        };

        checkTokenValidity();
    }, [ValidarToken, navigate]);

    const handleSubmit = async (e) => {
        e.preventDefault();
        const title = e.target.title.value;
        const language = e.target.language.value;

        if (!title || !language || !email) {
            setError('Por favor, complete todos los campos.');
            return;
        }

        const isValidLanguage = supportedLanguages.some(lang => lang.id === language);
        if (!isValidLanguage) {
            setError('Por favor, seleccione un idioma válido.');
            return;
        }

        const requestData = {
            email: email,
            title: title,
            language: language
        };

        try {
            const response = await requestVideoFunc(requestData);
            if (response.uri) {
                // Si la solicitud es exitosa, redirigimos a MainPage
                const uriParts = response.uri.split('/');
                const folder = uriParts[0];
                const fileName = uriParts[1].split('.')[0];
                const fileExtension = uriParts[1].split('.')[1];
                navigate(`/main/${folder}/${fileName}/${fileExtension}`);
            } else {
                throw new Error('Error al procesar la solicitud de video');
            }
        } catch (error) {
            setError(error.message);
        }
    };

    const handleTokenAlertClose = () => {
        setShowTokenAlert(false); // Cerrar el alerta de token
        navigate('/'); // Redirigir a la página de inicio
    };

    return (
        <div>
            <NavbarTools />
            <div className='d-flex bg-primary align-items-center justify-content-center vh-100'>
                <div className='p-3 rounded bg-white w-50'>
                    <h3 className='text-center mb-4'>Solicitud de Video</h3>
                    <Form onSubmit={handleSubmit} disabled={formDisabled}>
                        <Form.Group controlId="formTitle">
                            <Form.Label>Título del Video</Form.Label>
                            <Form.Control
                                type="text"
                                placeholder="Ingrese el título del video"
                                required
                                name="title"
                                disabled={formDisabled}
                            />
                        </Form.Group>
                        <Form.Group controlId="formLanguage">
                            <Form.Label>Idioma del Video</Form.Label>
                            <Form.Control
                                as="select"
                                required
                                name="language"
                                disabled={formDisabled}
                            >
                                <option value="">Seleccione un idioma</option>
                                {supportedLanguages.map(lang => (
                                    <option key={lang.id} value={lang.id}>{`${lang.id} - ${lang.name}`}</option>
                                ))}
                            </Form.Control>
                        </Form.Group>
                        <Form.Group controlId="formEmail">
                            <Form.Label>Email del Usuario</Form.Label>
                            <Form.Control
                                type="email"
                                placeholder="Ingrese su email"
                                required
                                name="email"
                                value={email}
                                readOnly
                                disabled={formDisabled}
                            />
                        </Form.Group>
                        <Button className='w-100 btn btn-primary mt-3' type="submit" disabled={formDisabled}>
                            Enviar Solicitud de Video
                        </Button>
                    </Form>
                    {error && <p style={{ color: 'red' }}>{error}</p>}
                    {/* Alerta de token inválido */}
                    <Alert variant="danger" show={showTokenAlert} onClose={handleTokenAlertClose} dismissible>
                        El token de autenticación es inválido o ha caducado.
                    </Alert>
                </div>
            </div>
        </div>
    );
};
