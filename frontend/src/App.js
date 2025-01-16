import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Login from './components/Login';
import Register from './components/Register';
import MainScreen from './components/MainScreen';
import Room from './components/Room';
import Header from './components/Header'; // Import Header component
import Footer from './components/Footer'; // Import Footer component
import './styles.css'; // Import your custom styles


function App() {
  return (
    <Router>
      <Header />
      <div className="main-content">
        <Routes>
          <Route path="/" element={<MainScreen />} />
          <Route path="/login" element={<Login />} />
          <Route path="/register" element={<Register />} />
          <Route path="/room/:id" element={<Room />} />
        </Routes>
      </div>
      <Footer />
    </Router>
  );
}

export default App;
