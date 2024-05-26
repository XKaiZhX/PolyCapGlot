import React, { useEffect, useState } from 'react';
import { useAuth } from '../context/AuthContext';
import 'bootstrap/dist/css/bootstrap.min.css';
import {NavbarTools} from './Navbar.jsx'

export const VideoList = () => {
  const { requestVideosList, token } = useAuth();
  const [videos, setVideos] = useState([]);
  const [error, setError] = useState('');

  useEffect(() => {
    const fetchUserVideos = async () => {
      try {
        const response = await requestVideosList(token);
        setVideos(response);
      } catch (error) {
        setError('Error al cargar los videos del usuario.');
      }
    };

    fetchUserVideos();
  }, [token]);

  return (
    <div>
      <NavbarTools />
      <div className='container mt-4'>
        <h1>Mis Videos</h1>
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
  );
};
