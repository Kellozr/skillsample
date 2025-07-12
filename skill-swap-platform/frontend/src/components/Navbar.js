import React from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import './Navbar.css';

const Navbar = () => {
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  return (
    <nav className="navbar">
      <div className="navbar-brand">
        <Link to="/" className="navbar-logo">
          SkillSwap
        </Link>
      </div>
      
      <div className="navbar-menu">
        {user ? (
          <>
            <Link to="/browse" className="nav-link">Browse Skills</Link>
            <Link to="/requests" className="nav-link">My Requests</Link>
            <Link to="/profile" className="nav-link">Profile</Link>
            {user.role === 'admin' && (
              <Link to="/admin" className="nav-link">Admin</Link>
            )}
            <button onClick={handleLogout} className="nav-link logout-btn">
              Logout
            </button>
          </>
        ) : (
          <>
            <Link to="/login" className="nav-link">Login</Link>
            <Link to="/register" className="nav-link">Register</Link>
          </>
        )}
      </div>
    </nav>
  );
};

export default Navbar;
