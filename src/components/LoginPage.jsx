import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext'; // Importamos el contexto de autenticación
import 'bootstrap/dist/css/bootstrap.min.css';

export const Login = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const { login, ValidarToken,  clearTokenAndEmail, token } = useAuth(); // Usamos la función de login desde el contexto de autenticación
  const navigate = useNavigate();

  const goMainPage = () => {
    navigate('/preupload');
  };

  const goRegisterPage = () => {
    navigate('/register');
  };

  const handleLogin = async (e) => { // Agregamos el parámetro 'e'
    e.preventDefault(); // Evitar el comportamiento por defecto del formulario

    if (!email || !password) {
      setError('Por favor, ingresa un email y una contraseña.');
      return;
    }

    try {
      const res = await login({ email, password }); // Llamamos a la función de login desde el contexto de autenticación
      console.log('Inicio de sesión exitoso.');

      if (res) {
        if (token) {
          goMainPage();
        } else {
          clearTokenAndEmail();
          setError('Token inválido');
        }
      } else {
        setError('Error al verificar token.');
      }
    } catch (error) {
      console.error('Error al iniciar sesión:', error);
      setError('Error al iniciar sesión. Por favor, verifica tus credenciales.');
    }
  };

  return (
    <div className='d-flex bg-primary align-items-center justify-content-center vh-100'>
      <h1 className='m-3'>PolyCapGlot</h1>
      <div className='p-3 rounded bg-white w-25'>
        <form onSubmit={handleLogin}> {/* Manejamos el evento onSubmit del formulario */}
          <h2>Iniciar sesión</h2>
          <div className='mb-3'>
            <label htmlFor='email'><strong>Email: </strong></label>
            <input
              type="text"
              placeholder="Email de usuario"
              className='form-control rounded-0 border border-dark'
              value={email}
              onChange={(e) => setEmail(e.target.value)}
            />
          </div>
          <div className='mb-3'>
            <label htmlFor='password'><strong>Password: </strong></label>
            <input
              type="password"
              placeholder="Contraseña"
              className='form-control rounded-0 border border-dark'
              value={password}
              onChange={(e) => setPassword(e.target.value)}
            />
            <br />
            <p>
              ¿No tienes una cuenta? <span onClick={goRegisterPage} style={{ cursor: 'pointer', color: 'blue', borderBottom: '1px solid blue' }}>Regístrate aquí</span>
            </p>

            {error && <p>{error}</p>}
            <button type="submit" className='w-100 btn btn-success rounded-0'>Iniciar sesión</button> {/* Cambiamos onClick por type="submit" */}
          </div>
        </form>
      </div>
    </div>
  );
};
