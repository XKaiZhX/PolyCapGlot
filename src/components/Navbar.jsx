import React from 'react';
import { useNavigate } from 'react-router-dom';
import { Container, Nav, Navbar, NavDropdown } from 'react-bootstrap';
import { useAuth } from '../context/AuthContext';

export const NavbarTools = () => {

    const { email } = useAuth();
    const navigate = useNavigate();

    const handleNavigate = (path) => {
        navigate(path);
    };

    return (
        <Navbar collapseOnSelect expand="lg" className="bg-body-tertiary">
            <Container>
                <Navbar.Brand onClick={() => handleNavigate('/preupload')}>PolyCapGlot</Navbar.Brand>
                <Navbar.Toggle aria-controls="responsive-navbar-nav" />
                <Navbar.Collapse id="responsive-navbar-nav">
                    <Nav className="me-auto">
                        <Nav.Link onClick={() => handleNavigate('/preupload')}>Upload Video</Nav.Link>
                        <Nav.Link onClick={() => handleNavigate('/misvideos')}>Mis Videos</Nav.Link>
                    </Nav>
                    <Nav>
                        <NavDropdown title="Usuario" id="collapsible-nav-dropdown">
                            <NavDropdown.Item onClick={() => handleNavigate(`/perfil/'${email}`)}>Mis Perfiles</NavDropdown.Item>
                            <NavDropdown.Item onClick={() => handleNavigate('/changeusername')}>Cambiar Username</NavDropdown.Item>
                            <NavDropdown.Item onClick={() => handleNavigate('/changepassword')}>Cambiar Contraseña</NavDropdown.Item>
                            <NavDropdown.Divider />
                            <NavDropdown.Item onClick={() => handleNavigate('/deleteuser')}>Eliminar Cuenta</NavDropdown.Item>
                        </NavDropdown>
                    </Nav>
                </Navbar.Collapse>
            </Container>
        </Navbar>
    );
}