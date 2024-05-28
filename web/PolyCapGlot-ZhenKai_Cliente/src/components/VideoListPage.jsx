import React, { useEffect, useState } from 'react';
import { useAuth } from '../context/AuthContext';
import 'bootstrap/dist/css/bootstrap.min.css';
import { NavbarTools } from './Navbar.jsx'
import { useNavigate } from 'react-router-dom';

export const VideoList = () => {
  const { requestVideosList, token, ValidarToken } = useAuth();
  const [videos, setVideos] = useState([]);
  const [error, setError] = useState('');
  const [showAlert, setShowAlert] = useState(false);
  const navigate = useNavigate();

  useEffect(() => {
    const fetchUserVideos = async () => {
      try {
        if (!ValidarToken(token)) {
          throw new Error('Token inválido');
        }
        
        const response = await requestVideosList(token);
        setVideos(response);
      } catch (error) {
        setError('Error al cargar los videos del usuario.');
        if (error.message === 'Token inválido') {
          setShowAlert(true); // Mostrar el alerta si el token es inválido
        }
      }
    };

    fetchUserVideos();
  }, [token, ValidarToken]);

  const handleAlertClose = () => {
    setShowAlert(false); // Cerrar el alerta
    navigate('/');
  };

  return (
    <div>
      <NavbarTools />
      <div className='d-flex bg-primary align-items-center justify-content-center vh-100'>
        <div className='p-3 rounded bg-white w-50'>
          <h1 className='text-center mb-4'>Mis Videos</h1>
          {error && <p className="text-danger">{error}</p>}
          <div className="row">
            {videos && videos.map((video, index) => ( // Verifica que videos esté definido antes de mapearlo
              <div className='col-md-4 mb-4' key={index}>
                <div className='card'>
                  <div className='card-body'>
                    <h5 className='card-title'>{video.title}</h5>
                    <p className='card-text'>{video.language}</p>
                    <p className='card-text'>{video.firebase_uri}</p>
                    <p className='card-text'>{video.translations}</p>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
      {showAlert && ( // Mostrar el alerta si showAlert es verdadero
        <div className="alert alert-danger alert-dismissible fade show position-fixed" role="alert" style={{ top: '10px', right: '10px' }}>
          El token de autenticación es inválido o ha caducado.
          <button type="button" className="btn-close" onClick={handleAlertClose}></button>
        </div>
      )}
    </div>
  );
};
