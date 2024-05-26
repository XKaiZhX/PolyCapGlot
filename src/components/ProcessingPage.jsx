import React, { useState, useEffect } from 'react';
import { ProgressBar } from 'react-bootstrap';
import { useNavigate, useParams } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

export const Processing = () => {
    const [progress, setProgress] = useState(0);
    const navigate = useNavigate();
    const { uploadVideo } = useAuth();
    const { fileName, language } = useParams();

    useEffect(() => {
        const simulateAndUpload = async () => {
            try {
                // Definir la duración total de carga (5 minutos - 1 segundo)
                const totalTimeInSeconds = (5 * 60) - 1;
                const updateInterval = 1000; // Actualizar cada 1 segundo
                const progressIncrement = 99 / (totalTimeInSeconds / (updateInterval / 1000)); // Incremento de progreso por intervalo

                // Simular la carga estableciendo el progreso en incrementos cada 1 segundo
                const interval = setInterval(() => {
                    setProgress(prevProgress => {
                        const newProgress = Math.min(prevProgress + progressIncrement, 99); // Evitar que el progreso supere el 99%
                        return newProgress;
                    });
                }, 1000);

                // Enviar la solicitud para cargar el video
                const response = await uploadVideo({ email: "Local@local.com", video_id: fileName, sub: language });

                // Verificar el estado de carga
                await checkUploadStatus();

                // Limpiar intervalo de simulación de carga
                clearInterval(interval);

                if (response.success) {

                    const uriParts = response.uri.split('/');
                    const folder = uriParts[0];
                    const fileName = uriParts[1].split('.')[0];
                    const fileExtension = uriParts[1].split('.')[1];
                    // Navegar a la página de video una vez completada la carga
                    navigate(`/videoplayer/${folder}/${fileName}/${fileExtension}`);
                }
                else
                {
                    navigate('/preupload');
                }
                

            } catch (error) {
                console.error('Error al subir el video:', error);
                // Volver a Main.jsx en caso de error
                navigate('/preupload');
            }
        };

        const checkUploadStatus = async () => {
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

                if (integerProgress % 10 === 0) { // Cada 10%, verificar si hay respuesta
                    try {
                        if (response !== null) { // Si hay respuesta, completar la barra
                            setProgress(100);
                            clearInterval(checkInterval); // Detener la verificación
                            clearInterval(interval); // Limpiar intervalo de simulación de carga
                            // Navegar a la página de video una vez completada la carga
                            navigate(`/videoplayer/${fileName}`);
                            return;
                        }
                    } catch (error) {
                        clearInterval(checkInterval);
                        clearInterval(interval); // Limpiar intervalo de simulación de carga
                        console.error('Error al verificar el estado de carga:', error);
                    }
                }

                try {
                    // Suponiendo que tienes una función para verificar el estado de carga
                    const status = await response;
                    
                    if (status === 200) {
                        clearInterval(checkInterval);
                        clearInterval(interval); // Limpiar intervalo de simulación de carga
                        // Navegar a la página de video una vez completada la carga
                        navigate(`/videoplayer/${fileName}`);
                    }
                } catch (error) {
                    clearInterval(checkInterval);
                    clearInterval(interval); // Limpiar intervalo de simulación de carga
                    console.error('Error al verificar el estado de carga:', error);
                }
            }, updateInterval * 1000);

            setTimeout(() => {
                clearInterval(checkInterval);
                clearInterval(interval); // Limpiar intervalo de simulación de carga
                console.error("Tiempo de carga agotado");
            }, (totalTimeInSeconds + additionalTime) * 1000); // Considerar el tiempo adicional en el tiempo total
        };

        simulateAndUpload();
    }, [uploadVideo, fileName, language, navigate]);

    return (
        <div className='d-flex bg-primary align-items-center justify-content-center vh-100'>
            <div className='p-3 rounded bg-white w-50'>
                <h3 className='text-center mb-4'>Procesando Video</h3>
                <ProgressBar now={progress} label={`${progress}%`} />
            </div>
        </div>
    );
};
