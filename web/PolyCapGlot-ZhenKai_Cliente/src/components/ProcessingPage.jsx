import React, { useState, useEffect } from 'react';
import { ProgressBar } from 'react-bootstrap';
import { useNavigate, useParams } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

export const Processing = () => {
    const [progress, setProgress] = useState(0);
    const [error, setError] = useState(null); // Nuevo estado para almacenar el error
    const [response, setResponse] = useState(null); // Estado para almacenar la respuesta
    const navigate = useNavigate();
    const { uploadVideo, email, requestVideosList, videosList, ValidarToken, token } = useAuth();
    const { fileName, language } = useParams();

    useEffect(() => {
        const totalTimeInSeconds = (5 * 60) - 1;
        const updateInterval = 1000; // Actualizar cada 1 segundo
        let interval = null;

        const simulateAndUpload = async () => {
            try {
                // Definir la duración total de carga (5 minutos - 1 segundo)
                const progressIncrement = 99 / (totalTimeInSeconds / (updateInterval / 1000)); // Incremento de progreso por intervalo

                // Simular la carga estableciendo el progreso en incrementos cada 1 segundo
                interval = setInterval(() => {
                    setProgress(prevProgress => {
                        const newProgress = Math.min(prevProgress + progressIncrement, 99); // Evitar que el progreso supere el 99%
                        return newProgress;
                    });
                }, 1000);

                // Enviar la solicitud para cargar el video
                const response = await uploadVideo({ email: email, video_id: fileName, sub: language });
                setResponse(response); // Establecer la respuesta en el estado

                // Limpiar intervalo de simulación de carga
                clearInterval(interval);

                // Verificar el estado de carga
                await checkUploadStatus(response);

            } catch (error) {
                setError('Error al subir el video: ' + error.message); // Establecer el error
            }
        };

        const checkUploadStatus = async (response) => {
            let additionalTime = 0; // Tiempo adicional a agregar en segundos

            const checkInterval = setInterval(async () => {
                const integerProgress = Math.floor(progress);

                if (integerProgress === 99 && response === null) { // Si alcanza el 99% y aún no hay resultado
                    clearInterval(checkInterval); // Detener la verificación
                    return;
                }

                if (integerProgress > 60 && integerProgress % 5 === 0) { // Después del 60%, verificar cada 5%
                    additionalTime += 180; // Agregar 3 minutos adicionales (180 segundos)
                    console.log("Adding 3 minutes to progress bar...");
                }
            }, updateInterval * 1000);

            setTimeout(() => {
                clearInterval(checkInterval);
                clearInterval(interval); // Limpiar intervalo de simulación de carga
                setError('Tiempo de carga agotado'); // Establecer el error
            }, (totalTimeInSeconds + additionalTime) * 1000); // Considerar el tiempo adicional en el tiempo total
        };

        simulateAndUpload();
    }, []);

    // useEffect(() => {
    //     const verifyUploaded = async () => {
    //         try {
    //             ValidarToken();

    //             // Obtener la lista de videos
    //             await requestVideosList();

    //             // Obtener el video de la lista
    //             const video = videosList.find(video => video.firebase_uri === 'raw_videos/' + fileName + '.mp4');

    //             if (video) {
    //                 // Si el video está en la lista, buscar la traducción
    //                 const translation = video.translations.find(trans => trans.sub_language === language);
    //                 if (translation) {
    //                     const firebaseUri = translation.firebase_uri;
    //                     const uriParts = firebaseUri.split('/');
    //                     const folder = uriParts[0];
    //                     const newFileName = uriParts[1].split('.')[0];
    //                     const fileExtension = uriParts[1].split('.')[1];

    //                     navigate(`/videoplayer/${folder}/${newFileName}/${fileExtension}`);
    //                     setProgress(100);
    //                     return;
    //                 } else {
    //                     throw new Error('Translation not found for the given language.');
    //                 }
    //             } else {
    //                 throw new Error('Video not found.');
    //             }
    //         } catch (error) {
    //             setError(error.message);
    //         }
    //     };

    //     if (response != null) {
    //         verifyUploaded();
    //     }

    // }, [ValidarToken, requestVideosList, response, fileName, language, navigate, videosList]);

    return (
        <div className='d-flex bg-primary align-items-center justify-content-center vh-100'>
            <div className='p-3 rounded bg-white w-50'>
                <h3 className='text-center mb-4'>Procesando Video</h3>
                {error && <div className="alert alert-danger" role="alert">{error}</div>} {/* Mostrar error si existe */}
                <ProgressBar now={progress} label={`${progress}%`} />
            </div>
        </div>
    );
};
