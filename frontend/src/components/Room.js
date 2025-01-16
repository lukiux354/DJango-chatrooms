import React, { useEffect, useState, useRef } from 'react';
import { useParams } from 'react-router-dom';
import API from '../api';

function Room() {
  const { id } = useParams();
  const [messages, setMessages] = useState([]); // To store the current messages being displayed
  const [newMessage, setNewMessage] = useState('');
  const [username, setUsername] = useState('');
  const [socket, setSocket] = useState(null);
  const [members, setMembers] = useState([]);
  const messageContainerRef = useRef(null); // Ref to the message container for scroll events
  const lastMessageRef = useRef(null); // Ref for the last message for scrolling

  useEffect(() => {
    // Fetch channel members when the component is mounted
    const fetchMembers = async () => {
      try {
        const response = await API.get(`/api/rooms/${id}/members/`);
        setMembers(response.data); // Set the members list from the API response
      } catch (err) {
        console.error('Error fetching members:', err);
      }
    };

    fetchMembers();

    // Create a WebSocket connection
    const ws = new WebSocket(`ws://127.0.0.1:8000/ws/chat/${id}/`);
    setSocket(ws);

    ws.onopen = () => {
      console.log('WebSocket connected');
    };

    ws.onmessage = (event) => {
      const data = JSON.parse(event.data);

      if (data.type === 'initial_messages') {
        setMessages(data.messages);
      } else if (data.type === 'new_message') {
        // Append new message
        setMessages((prevMessages) => [...prevMessages, data]);
      }
    };

    ws.onclose = () => {
      console.log('WebSocket disconnected');
    };
    ws.onerror = (e) => {
      console.error('WebSocket error:', e);
    };

    return () => {
      ws.close();
    };
  }, [id]);

  // Handle sending a message
  const handleSendMessage = () => {
    if (socket && newMessage) {
      console.log('Sending username:', localStorage.getItem('username'));
      socket.send(
        JSON.stringify({
          message: newMessage,
          username: localStorage.getItem('username'), // Ensure this matches your setup
        })
      );
      setNewMessage('');
    }
  };

  // Scroll to the bottom after sending a message
  useEffect(() => {
    if (lastMessageRef.current) {
      lastMessageRef.current.scrollIntoView({ behavior: 'smooth' });
    }
  }, [messages]); // Scroll when messages change

  // Handle adding a user to the room
  const handleAddUser = async () => {
    try {
      await API.post(`/api/rooms/${id}/add-user/`, { username });
      alert('User added');
      setUsername('');
      // Re-fetch members after adding a new user
      const response = await API.get(`/api/rooms/${id}/members/`);
      setMembers(response.data);
    } catch (err) {
      alert('Error adding user');
    }
  };

  // Load more messages when scrolling to the top
  const loadMoreMessages = async () => {
    if (messageContainerRef.current.scrollTop === 0) {
      // Fetch older messages
      try {
        const response = await API.get(`/api/rooms/${id}/messages/`, {
          params: {
            before: messages[0]?.timestamp, // Use the timestamp of the first message to fetch older ones
          },
        });
        const olderMessages = response.data;
        setMessages((prevMessages) => [...olderMessages, ...prevMessages]); // Prepend older messages
      } catch (err) {
        console.error('Error loading older messages:', err);
      }
    }
  };

  return (
    <div>
      <h2>Room Messages</h2>
      <div
        className="messages-container"
        ref={messageContainerRef}
        onScroll={loadMoreMessages}
        style={{ maxHeight: '400px', overflowY: 'auto' }}
      >
        <ul>
          {messages.map((msg, index) => (
            <li key={index} ref={index === messages.length - 1 ? lastMessageRef : null}>
              {msg.username}: {msg.message} ({msg.timestamp})
            </li>
          ))}
        </ul>
      </div>
      <input
        type="text"
        placeholder="New Message"
        value={newMessage}
        onChange={(e) => setNewMessage(e.target.value)}
      />
      <button onClick={handleSendMessage}>Send</button>

      <h3>Add User</h3>
      <input
        type="text"
        placeholder="Username"
        value={username}
        onChange={(e) => setUsername(e.target.value)}
      />
      <button onClick={handleAddUser}>Add</button>

      <h3>All Users</h3>
      <ul>
        {members.map((member, index) => (
          <li key={index}>{member.user_username}</li>
        ))}
      </ul>
    </div>
  );
}

export default Room;
