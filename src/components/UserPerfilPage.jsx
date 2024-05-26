import React, { useEffect, useState } from 'react';
import { useAuth } from '../context/AuthContext';
import 'bootstrap/dist/css/bootstrap.min.css';

export const UserPerfil = () => {
  const { getUserByEmail, user, email, error } = useAuth();

  useEffect(() => {
    const loadUserProfile = async () => {
      const userEmail = email; 
      await getUserByEmail(userEmail);
    };

    loadUserProfile();
  }, [getUserByEmail]);

  return (
    <div className='container mt-4'>
      <h1>Perfil del Usuario</h1>
      {error && <p className="text-danger">{error}</p>}
      {user && (
        <div>
          <p><strong>Email:</strong> {user.email}</p>
          <p><strong>Username:</strong> {user.username}</p>
          {/* Otros detalles del usuario según la estructura del objeto de usuario */}
        </div>
      )}
    </div>
  );
};
