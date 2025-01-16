import React from 'react';
import { Link } from 'react-router-dom';

function Header() {
  const isAuthenticated = localStorage.getItem('token');
  const handleLogout = () => {
    localStorage.removeItem('token');
    localStorage.removeItem('username');
    window.location.href = '/login';
  };

  return (
    <header className="header">
      <div className="logo">
        <Link to="/">My Chat App</Link>
      </div>
      <nav>
        {isAuthenticated ? (
          <>
            <button onClick={handleLogout}>Logout</button>
            <Link to="/">Main</Link>
          </>
        ) : (
          <>
            <Link to="/login">Login</Link>
            <Link to="/register">Register</Link>
          </>
        )}
      </nav>
    </header>
  );
}

export default Header;
