import React, { useEffect, useState } from 'react';
import { useAuth } from '../context/AuthContext';
import { Alert } from 'react-bootstrap';
import 'bootstrap/dist/css/bootstrap.min.css';
import { useNavigate } from 'react-router-dom';
import { NavbarTools } from './Navbar.jsx';

export const UserPerfil = () => {
  const { getUserByEmail, user, email, errors, deleteUser, clearTokenAndEmail, ValidarToken, token } = useAuth();
  const [showConfirmation, setShowConfirmation] = useState(false);
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

    const loadUserProfile = async () => {
      await getUserByEmail(email);
    };

    loadUserProfile();
  }, [getUserByEmail, email, ValidarToken, navigate]);

  const handleConfirmDelete = async () => {
    try {
      clearTokenAndEmail();
      await deleteUser(email);
      navigate('/');
    } catch (error) {
      console.error('Error al eliminar la cuenta:', error);
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
          <h1 className='text-center mb-4'>Perfil del Usuario</h1>
          {errors && <p className="text-danger">{errors}</p>}
          {user && (
            <div>
              <p><strong>Email:</strong> {email}</p>
              <p><strong>Username:</strong> {user}</p>
            </div>
          )}
          <br />
          <br />
          <div className="d-flex justify-content-center">
            <button
              className="btn btn-primary mx-2"
              onClick={() => navigate('/updateusername')}
              disabled={formDisabled}
            >
              Modificar Username
            </button>
            <button
              className="btn btn-secondary mx-2"
              onClick={() => navigate('/updatepassword')}
              disabled={formDisabled}
            >
              Modificar Password
            </button>
            <button
              className="btn btn-danger"
              onClick={() => setShowConfirmation(true)}
              disabled={formDisabled}
            >
              Eliminar Cuenta
            </button>
          </div>
          {showConfirmation && (
            <div className="mt-4">
              <h2 className="text-danger font-weight-bold text-center mb-4'">
                ¿Estás seguro de que quieres eliminar tu cuenta? Esta acción es irreversible.
              </h2>
              <div className="d-flex justify-content-center">
                <button
                  className="btn btn-success mx-2"
                  onClick={() => setShowConfirmation(false)}
                >
                  Cancelar
                </button>
                <button
                  className="btn btn-danger mx-2"
                  onClick={handleConfirmDelete}
                >
                  Eliminar
                </button>
              </div>
            </div>
          )}
          {/* Alerta de token inválido */}
          <Alert variant="danger" show={showTokenAlert} onClose={handleTokenAlertClose} dismissible>
            El token de autenticación es inválido o ha caducado.
          </Alert>
        </div>
      </div>
    </div>
  );
};
