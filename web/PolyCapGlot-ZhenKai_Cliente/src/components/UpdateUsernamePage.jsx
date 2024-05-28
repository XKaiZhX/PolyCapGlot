import React, { useState, useEffect } from 'react';
import { useAuth } from '../context/AuthContext';
import { Alert } from 'react-bootstrap';
import 'bootstrap/dist/css/bootstrap.min.css';
import { useNavigate } from 'react-router-dom';
import { NavbarTools } from './Navbar.jsx';

export const UpdateUsernamePage = () => {
  const { updateUsername, errors, user, ValidarToken, token } = useAuth();
  const [newUsername, setNewUsername] = useState('');

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
  }, [ValidarToken, navigate]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await updateUsername({ newUsername });
      navigate('/perfil'); // O redirigir a la página de perfil actualizada
    } catch (error) {
      console.error('Error al actualizar el username:', error);
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
          <h1 className='text-center mb-4'>Actualizar Username</h1>
          {errors && <p className="text-danger">{errors}</p>}
          <form onSubmit={handleSubmit} disabled={formDisabled}>
            <div className="form-group">
              <label htmlFor="currentUsername">Username Actual:</label>
              <input
                type="text"
                className="form-control"
                id="currentUsername"
                value={user}
                readOnly
                disabled={formDisabled}
              />
            </div>
            <div className="form-group">
              <label htmlFor="newUsername">Nuevo Username:</label>
              <input
                type="text"
                className="form-control"
                id="newUsername"
                value={newUsername}
                onChange={(e) => setNewUsername(e.target.value)}
                required
                disabled={formDisabled}
              />
            </div>
            <button type="submit" className="btn btn-primary w-100 mt-3" disabled={formDisabled}>
              Enviar
            </button>
          </form>
          {/* Alerta de token inválido */}
          <Alert variant="danger" show={showTokenAlert} onClose={handleTokenAlertClose} dismissible>
            El token de autenticación es inválido o ha caducado.
          </Alert>
        </div>
      </div>
    </div>
  );
};
