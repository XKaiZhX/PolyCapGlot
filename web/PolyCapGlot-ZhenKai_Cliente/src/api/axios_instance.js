// axios-instance.js

import axios from 'axios';

const instance = axios.create({
  baseURL: 'http://127.0.0.1:9002', // Cambia esto por la URL de tu servidor Flask
  headers: {
    'Content-Type': 'application/json', // Asegúrate de establecer el tipo de contenido correctamente
    'Access-Control-Allow-Origin': '*', // Esto permitirá solicitudes desde cualquier origen
    // Otros encabezados CORS si es necesario
  }
});

export default instance;
