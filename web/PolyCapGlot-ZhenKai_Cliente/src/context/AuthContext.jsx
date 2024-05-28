// AuthContext.jsx
import { createContext, useState, useContext } from "react";
import { RegisterRequest, LoginRequest, UpdateUsernameRequest, UpdatePasswordRequest, DeleteUserRequest, requestVideo, uploadVideoRequest, isTokenValid, requestUserVideos, requestUserPerfil } from "../api/auth.js";

export const AuthContext = createContext();

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error("useAuth debe ser usado dentro de un AuthProvider");
  }
  return context;
};

export const AuthProvider = ({ children }) => {
  const [errors, setErrors] = useState([]);
  const [token, setToken] = useState('');
  const [user, setUser] = useState('');
  const [email, setEmail] = useState('');
  const [videosList, setVideosList] = useState('');

  const register = async (userData) => {
    try {
      const res = await RegisterRequest(userData);
      console.log(res.data);
      setErrors([]);
      return res.data;
    } catch (error) {
      setErrors(error.response ? error.response.data : ['Error al registrar usuario']);
      throw error;
    }
  };

  const updateUsername = async (userData) => {
    try {
      const res = await UpdateUsernameRequest(userData);
      console.log(res.data);
      setErrors([]);
      return res.data;
    } catch (error) {
      setErrors(error.response ? error.response.data : ['Error al cambiar username']);
      throw error;
    }
  }

  const updatePassword = async (userData) => {
    try {
      const res = await UpdatePasswordRequest(userData);
      console.log(res.data);
      setErrors([]);
      return res.data;
    } catch (error) {
      setErrors(error.response ? error.response.data : ['Error al cambiar password']);
      throw error;
    }
  }

  const deleteUser = async (email) => {
    try {
        const response = await DeleteUserRequest(email)
        return response.data;
    } catch (error) {
        console.error('Error al eliminar el usuario:', error);
        throw new Error('Error al eliminar el usuario');
    }
  };

  const login = async (userData) => {
    try {
      const res = await LoginRequest(userData);
      console.log(res.data);
      setErrors([]);
      
      setToken(res.data.token);
      setEmail(res.data.email);
      setUser(res.data.username);

      if (!ValidarToken(token)) {
        throw new Error('Token inválido');
      } else {
        setToken(token);
        setEmail(email);
      }

      return res.data;
    } catch (error) {
      setErrors(error.response ? error.response.data : ['Error al iniciar sesión']);
      throw error;
    }
  };


  const ValidarToken = (token) => {
    try {
      if (isTokenValid(token)) {
        return true;
      } else {
        return false;
      }
    } catch (error) {
      console.error('Error al validar token:', error);
      throw new Error('Error al validar token');
    }  
  };

  const requestVideoFunc = async (videoData) => {
    try {
        const response = await requestVideo(videoData);
        if (response.message === 'proceed') {
            return response;
        } else {
            throw new Error('Error al procesar la solicitud de video');
        }
    } catch (error) {
        console.error('Error al solicitar el video:', error);
        throw new Error('Error al solicitar el video');
    }  
  };

  const uploadVideo = async (videoData) => {
    try {
      const response = await uploadVideoRequest(videoData);
      return response.data;
    } catch (error) {
      console.error('Error al subir el video:', error);
      return { success: false, message: 'Error al subir el video' };
    }
  };

  const clearTokenAndEmail = () => {
    setToken('');
    setEmail('');
    setUser('');
  };

  const requestVideosList = async (token) => {
    try {
      const response = requestUserVideos(token)
      setVideosList(response.data)
    } catch (error) {
      throw new Error('Error al cargar los videos del usuario.');
    }
  };

  const getUserByEmail = async (email) => {
    try {
      const response = requestUserPerfil(email);
      setUser(response.data);
    } catch (error) {
      setError('Error al cargar el perfil del usuario.');
    }
  };

  return (
    <AuthContext.Provider
      value={{
        register,
        login,
        updateUsername,
        updatePassword,
        deleteUser,
        requestVideo: requestVideoFunc,
        uploadVideo,
        token,
        email,
        ValidarToken,
        clearTokenAndEmail,
        requestVideosList,
        videosList,
        getUserByEmail,
        errors
      }}
    >
      {children}
    </AuthContext.Provider>
  );
};
