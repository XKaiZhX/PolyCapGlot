import axios from './axios_instance.js';
import { jwtDecode } from "jwt-decode";

const API = 'http://127.0.0.1:9002';

export const RegisterRequest = user => axios.post(API + '/user/', user)
export const LoginRequest = user => axios.post(API + '/user/login', user)

export const requestVideo = async (videoData) => {
    try {
        const response = await axios.post(API + '/video/request', videoData);
        return response.data;
    } catch (error) {
        console.error('Error al solicitar el video:', error);
        throw new Error('Error al solicitar el video');
    }
};

export const uploadVideoRequest = async (videoData) => {
    try {
        const response = await axios.post(API + '/video/upload', videoData);
        return response.data;
    } catch (error) {
        console.error('Error al subir el video:', error);
        throw new Error('Error al subir el video');
    }
};

export const isTokenValid = (token) => {
    if (!token) return false;

    try {
        const decodedToken = jwtDecode(token);
        if (!decodedToken || !decodedToken.exp) return false;

        const fecha = new Date();
        const año = fecha.getFullYear();
        const mes = String(fecha.getMonth() + 1).padStart(2, '0');
        const dia = String(fecha.getDate()).padStart(2, '0');
        const horas = String(fecha.getHours()).padStart(2, '0');
        const minutos = String(fecha.getMinutes()).padStart(2, '0');
        const segundos = String(fecha.getSeconds()).padStart(2, '0');
        const milisegundos = String(fecha.getMilliseconds()).padStart(6, '0');

        const tiempoActual = `${año}-${mes}-${dia} ${horas}:${minutos}:${segundos}.${milisegundos}`;

        // Verificar si el tiempo de expiración es mayor que el tiempo actual
        return decodedToken.exp > tiempoActual;
    } catch (error) {
        console.error('Error decoding token:', error);
        return false;
    }
};

export const requestUserVideos = async (token) => {
    try {
      const response = await axios.post(API + '/video/user', {}, { headers: { 'x-access-token': token } });
      return response.data;
    } catch (error) {
      throw new Error('Error al cargar los videos del usuario.');
    }
};

export const requestUserPerfil = async (email) => {
    try {
        const response = await axios.get(API + `/user/${email}`);
        return response.data;
    } catch (error) {
        throw new Error('Error al cargar los datos del usuario.');
    }
};
  