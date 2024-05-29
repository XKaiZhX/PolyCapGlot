import React, { useState, useEffect } from 'react';
import { Alert } from 'react-bootstrap';
import { useAuth } from '../context/AuthContext';
import 'bootstrap/dist/css/bootstrap.min.css';
import { useNavigate } from 'react-router-dom';
import { NavbarTools } from './Navbar.jsx';

export const UpdatePasswordPage = () => {
  const { login, updatePassword, errors, ValidarToken, token, email } = useAuth();
  const [emails, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [newPassword, setNewPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [isVerified, setIsVerified] = useState(false);

  const [showTokenAlert, setShowTokenAlert] = useState(false);
  const [formDisabled, setFormDisabled] = useState(false);

  const navigate = useNavigate();

  useEffect(() => {
    const checkTokenValidity = async () => {
        if (!ValidarToken(token)) {
            setShowTokenAlert(true); // Mostrar el alerta de token si es inválido
            setFormDisabled(true);
        }
    };

    checkTokenValidity();
}, []);

  const handleLogin = async (e) => {
    e.preventDefault();
    try {
      await login({ "email": emails, "password": password });
      setIsVerified(true);
    } catch (error) {
      console.error('Error al iniciar sesión:', error);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await updatePassword({ "email": email, "password": newPassword });
      navigate('/perfil/' + email); // O redirigir a la página de perfil actualizada
    } catch (error) {
      console.error('Error al actualizar la contraseña:', error);
    }
  };

  const handleTokenAlertClose = () => {
    setShowTokenAlert(false); // Cerrar el alerta de token
    navigate('/'); // Redirigir a la página de inicio
  };

  return (
    <div>
      <NavbarTools />
      <div className='d-flex bg-primary align-items-center justify-content-center vh-100'>
        <div className='p-3 rounded bg-white w-50'>
          <h1 className='text-center mb-4'>Actualizar Contraseña</h1>
          {errors && <p className="text-danger">{errors}</p>}
          {!isVerified ? (
            <form onSubmit={handleLogin} disabled={formDisabled}>
              <div className="form-group">
                <label htmlFor="email">Correo Electrónico:</label>
                <input
                  type="email"
                  className="form-control"
                  id="email"
                  value={emails}
                  onChange={(e) => setEmail(e.target.value)}
                  required
                  disabled={formDisabled}
                />
              </div>
              <div className="form-group">
                <label htmlFor="password">Contraseña:</label>
                <input
                  type="password"
                  className="form-control"
                  id="password"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  required
                  disabled={formDisabled}
                />
              </div>
              <button type="submit" className="btn btn-primary w-100 mt-3" disabled={formDisabled}>
                Verificar
              </button>
            </form>
          ) : (
            <form onSubmit={handleSubmit}>
              <div className="form-group">
                <label htmlFor="newPassword">Nueva Contraseña:</label>
                <input
                  type="password"
                  className="form-control"
                  id="newPassword"
                  value={newPassword}
                  onChange={(e) => setNewPassword(e.target.value)}
                  required
                />
              </div>
              <div className="form-group">
                <label htmlFor="confirmPassword">Confirmar Contraseña:</label>
                <input
                  type="password"
                  className="form-control"
                  id="confirmPassword"
                  value={confirmPassword}
                  onChange={(e) => setConfirmPassword(e.target.value)}
                  required
                />
              </div>
              <button type="submit" className="btn btn-primary w-100 mt-3">
                Enviar
              </button>
            </form>
          )}
          <Alert variant="danger" show={showTokenAlert} onClose={handleTokenAlertClose} dismissible>
            El token de autenticación es inválido o ha caducado.
          </Alert>
        </div>
      </div>
    </div>
  );
};
