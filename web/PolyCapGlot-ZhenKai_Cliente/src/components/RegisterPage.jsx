import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import 'bootstrap/dist/css/bootstrap.min.css';

export const Register = () => {
  const [username, setUsername] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const { register } = useAuth(); // Cambiar a register
  const [error, setError] = useState('');
  const [showAlert, setShowAlert] = useState(false); // Nuevo estado
  const navigate = useNavigate();

  const goLoginPage = () => {
    navigate('/');
  };

  const handleRegister = async (e) => {
    e.preventDefault();
    try {
      await register({ username, email, password }); // Cambiar a register
      console.log('Usuario registrado con éxito.');
      setShowAlert(true); // Mostrar ventana de aviso
    } catch (error) {
      console.error('Error al registrar usuario:', error);
    }
  };

  const handleAlertClose = () => {
    setShowAlert(false); // Cerrar ventana de aviso
    goLoginPage(); // Redirigir a la página de inicio de sesión
  };

  return (
    <div className='d-flex bg-primary align-items-center justify-content-center vh-100'>
      <h1 className='m-3'>PolyCapGlot</h1>
      <div className='p-3 rounded bg-white w-25'>
        <form>
          <h2>Registro</h2>
          <div className='mb-3'>
            <label htmlFor='username'><strong>Username: </strong></label>
            <input
              type="text"
              placeholder="Nombre de usuario"
              className='form-control rounded-0 border border-dark'
              value={username}
              onChange={(e) => setUsername(e.target.value)}
            />
          </div>
          <div className='mb-3'>
            <label htmlFor='email'><strong>Email: </strong></label>
            <input
              type="email"
              placeholder="Correo electrónico"
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
            <br/>
            <p>
              ¿Ya tienes una cuenta? <span onClick={goLoginPage} style={{ cursor: 'pointer', color: 'blue', borderBottom: '1px solid blue' }}>Inicia sesión aquí</span>.
            </p>

            {error && <p>{error}</p>}
            <button className='w-100 btn btn-primary rounded-0' onClick={handleRegister}>Registrarse</button>
          </div>
        </form>
      </div>
      
      {showAlert && ( // Ventana de aviso condicional
        <div className="alert alert-success alert-dismissible fade show position-fixed" role="alert" style={{ top: '10px', right: '10px' }}>
          Usuario registrado con éxito. {/* Mensaje de aviso */}
          <button type="button" className="btn-close" onClick={handleAlertClose}></button> {/* Botón de cerrar */}
        </div>
      )}
    </div>
  );
};
