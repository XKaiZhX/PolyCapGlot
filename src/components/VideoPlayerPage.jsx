import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import { getDownloadURL, ref } from 'firebase/storage';
import { storage } from '../credenciales';
import { NavbarTools } from './Navbar.jsx';

export const VideoPlayer = () => {
    const { folder, fileName, fileExtension } = useParams();
    const [videoUrl, setVideoUrl] = useState('');

    useEffect(() => {
        const fetchVideoUrl = async () => {
            const videoPath = `${folder}/${fileName}.${fileExtension}`;
            const videoRef = ref(storage, videoPath);

            try {
                const url = await getDownloadURL(videoRef);
                setVideoUrl(url);
            } catch (error) {
                console.error('Error al obtener la URL del video:', error);
            }
        };

        fetchVideoUrl();
    }, [folder, fileName, fileExtension]);

    return (
        <div>
            <NavbarTools />
            <div className='d-flex bg-primary align-items-center justify-content-center vh-100'>
                
                <div className='p-3 rounded bg-white w-75'>
                    <h3 className='text-center mb-4'>Reproductor de Video</h3>
                    {videoUrl ? (
                        <video width="100%" height="auto" controls>
                            <source src={videoUrl} type={`video/${fileExtension}`} />
                            Tu navegador no soporta el elemento de video.
                        </video>
                    ) : (
                        <p>Cargando video...</p>
                    )}
                </div>
            </div>
        </div>
    );
};
