# Django Chatrooms

A lightweight real-time chat application built with Django. This project allows users to create chat rooms, join existing conversations, and exchange messages instantly. It serves as a demonstration of building interactive web applications with Python and Django.

# Features

* **Real-time Messaging:** Send and receive messages instantly without refreshing the page.
* **Multi-Room Support:** Create separate rooms for different topics or groups.
* **User Authentication:** Secure login and registration system for users.
* **Message History:** Persistent chat logs so you never miss a conversation.
* **Responsive Design:** Simple and accessible interface for desktop and mobile.

# Tech Stack

* **Backend:** Python, Django
* **Database:** SQLite (Default)
* **Frontend:** HTML, CSS, JavaScript
* **Real-time:** [Django Channels / AJAX Polling] # Installation

Follow these steps to run the project locally:

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/lukiux354/DJango-chatrooms.git](https://github.com/lukiux354/DJango-chatrooms.git)
    cd DJango-chatrooms
    ```

2.  **Create a virtual environment:**
    ```bash
    python -m venv .venv
    source .venv/bin/activate  # On Windows use: .venv\Scripts\activate
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Apply migrations:**
    ```bash
    python manage.py migrate
    ```

5.  **Run the server:**
    ```bash
    python manage.py runserver
    ```

# Usage

1.  Open your browser and navigate to `http://127.0.0.1:8000/`.
2.  **Register** a new account or **Login**.
3.  Create a new room or select an existing one from the lobby.
4.  Start chatting!

# Visuals

Here is a preview of the chat interface:

<img width="800" alt="image" src="https://github.com/user-attachments/assets/7c74c355-de38-4ba6-903a-87d980763b61" />


Short demo video also available on YouTube: https://www.youtube.com/watch?v=sWR7cxr2Gb0

# License

This project is open-source and available for educational purposes.
