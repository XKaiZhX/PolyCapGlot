import React, { useState, useEffect } from 'react';
import { NavbarTools } from './Navbar.jsx';
import { Form, Button } from 'react-bootstrap';
import { useNavigate, useParams } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { Processing } from './ProcessingPage.jsx';

import { appFirebase } from '../credenciales'
import { getStorage, ref, uploadBytes, getDownloadURL } from 'firebase/storage'

const storage = getStorage(appFirebase)

export const Main = () => {
    const [error, setError] = useState('');
    const [videoTitle, setVideoTitle] = useState('');
    const [selectedFile, setSelectedFile] = useState(null);
    const { folder, fileName, fileExtension } = useParams();
    const { uploadVideo } = useAuth();
    const navigate = useNavigate();
    
    useEffect(() => {
        const fullFileName = `${fileName}.${fileExtension}`;
        setVideoTitle(fullFileName);
    }, [fileName, fileExtension]);

    const targetLanguages = [
        { id: 'AR', name: 'Arabic' },
        { id: 'BG', name: 'Bulgarian' },
        { id: 'CS', name: 'Czech' },
        { id: 'DA', name: 'Danish' },
        { id: 'DE', name: 'German' },
        { id: 'EL', name: 'Greek' },
        { id: 'EN', name: 'English (unspecified variant for backward compatibility; please select EN-GB or EN-US instead)' },
        { id: 'EN-GB', name: 'English (British)' },
        { id: 'EN-US', name: 'English (American)' },
        { id: 'ES', name: 'Spanish' },
        { id: 'ET', name: 'Estonian' },
        { id: 'FI', name: 'Finnish' },
        { id: 'FR', name: 'French' },
        { id: 'HU', name: 'Hungarian' },
        { id: 'ID', name: 'Indonesian' },
        { id: 'IT', name: 'Italian' },
        { id: 'JA', name: 'Japanese' },
        { id: 'KO', name: 'Korean' },
        { id: 'LT', name: 'Lithuanian' },
        { id: 'LV', name: 'Latvian' },
        { id: 'NB', name: 'Norwegian Bokmål' },
        { id: 'NL', name: 'Dutch' },
        { id: 'PL', name: 'Polish' },
        { id: 'PT', name: 'Portuguese (unspecified variant for backward compatibility; please select PT-BR or PT-PT instead)' },
        { id: 'PT-BR', name: 'Portuguese (Brazilian)' },
        { id: 'PT-PT', name: 'Portuguese (all Portuguese varieties excluding Brazilian Portuguese)' },
        { id: 'RO', name: 'Romanian' },
        { id: 'RU', name: 'Russian' },
        { id: 'SK', name: 'Slovak' },
        { id: 'SL', name: 'Slovenian' },
        { id: 'SV', name: 'Swedish' },
        { id: 'TR', name: 'Turkish' },
        { id: 'UK', name: 'Ukrainian' },
        { id: 'ZH', name: 'Chinese (simplified)' }
    ];

    const validarArchivo = (file) => {
        if (!file) {
            setError('Por favor, seleccione un archivo de video.');
            return false;
        }

        const validExtensions = ['.mp4'];
        const fileExtension = file.name.substring(file.name.lastIndexOf('.')).toLowerCase();
        if (!validExtensions.includes(fileExtension)) {
            setError('Solo se permiten archivos de video MP4.');
            return false;
        }

        if (file.size > 140 * 1024 * 1024) {
            setError('El archivo no puede superar los 140 MB de tamaño.');
            return false;
        }

        return true;
    };

    const fileHandler = async (e) => {
        const file = e.target.files[0];
        if (validarArchivo(file)) {
            setSelectedFile(file);
            setError('');
        }
    };

    const guardarInfo = async (e) => {
        e.preventDefault();

        if (!videoTitle || !selectedFile) {
            setError('Por favor, complete todos los campos.');
            return;
        }

        try {
            const filePath = `${folder}/${videoTitle}`;
            //cargar archivo a storage
            const refArchivo = ref(storage, filePath)

            //subir video a referencia indicado
            await uploadBytes(refArchivo, selectedFile)

            const language = e.target.language.value;

            navigate(`/processing/${fileName}/${language}`);

        } catch (error) {
            console.error('Error al subir el video:', error);
            setError('Error al subir el video. Inténtalo de nuevo.');
        }
    };

    return (
        <div>
            <NavbarTools />
            <div className='d-flex bg-primary align-items-center justify-content-center vh-100'>
                <div className='p-3 rounded bg-white w-50'>
                    <h3 className='text-center mb-4'>Agregar Video</h3>
                    <Form onSubmit={guardarInfo}>
                        <Form.Group controlId="formTitle">
                            <Form.Label>Título del Video</Form.Label>
                            <Form.Control
                                type="text"
                                placeholder="Ingrese el título del video"
                                required
                                value={videoTitle}
                                readOnly // Hacer el campo readonly
                            />
                        </Form.Group>
                        <Form.Group controlId="formLanguage">
                            <Form.Label>Idioma del Video</Form.Label>
                            <Form.Control
                                as="select"
                                required
                                name="language"
                            >
                                <option value="">Seleccione un idioma</option>
                                {targetLanguages.map(lang => (
                                    <option key={lang.id} value={lang.id}>{`${lang.id} - ${lang.name}`}</option>
                                ))}
                            </Form.Control>
                        </Form.Group>
                        <Form.Group controlId="formFile">
                            <Form.Label>Agregar Video</Form.Label>
                            <Form.Control
                                type="file"
                                placeholder="Video"
                                onChange={fileHandler}
                                required
                            />
                        </Form.Group>
                        <br/>
                        {error && <p style={{ color: 'red' }}>{error}</p>}
                        <br/>
                        <Button className='w-100 btn btn-primary mt-3' type="submit">
                            Upload
                        </Button>
                    </Form>
                </div>
            </div>
        </div>
    )
}
