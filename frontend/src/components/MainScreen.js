import React, { useEffect, useState } from 'react';
import API from '../api';
import { useNavigate } from 'react-router-dom';

function MainScreen() {
  const [rooms, setRooms] = useState([]);
  const [roomName, setRoomName] = useState('');
  const navigate = useNavigate();

  useEffect(() => {
    const fetchRooms = async () => {
      try {
        const response = await API.get('/api/rooms/');
        setRooms(response.data);
      } catch (err) {
        //alert('Error fetching rooms');
      }
    };
    fetchRooms();
  }, []);

  const handleCreateRoom = async () => {
    try {
      await API.post('/api/rooms/', { name: roomName });
      //alert('Room created');
      setRoomName('');
      window.location.href = ``;
    } catch (err) {
      alert('Error creating room');
    }
  };

  return (
    <div>
      <h2>Your Rooms</h2>
      <ul>
        {rooms.map((room) => (
          <li key={room.id} onClick={() => navigate(`/room/${room.id}`)}>
            {room.name}
          </li>
        ))}
      </ul>
      <h3>Create a Room</h3>
      <input
        type="text"
        placeholder="Room Name"
        value={roomName}
        onChange={(e) => setRoomName(e.target.value)}
      />
      <button onClick={handleCreateRoom}>Create</button>
    </div>
  );
}

export default MainScreen;
