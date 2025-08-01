# Message App

A Django REST Framework-based messaging application that supports conversations, threaded message replies, unread message tracking, and caching for performance optimization.

## Features

- **Custom User Model**: UUID primary key, user roles (Guest, Host, Admin), and secure password hashing.
- **JWT Authentication**: Uses `rest_framework_simplejwt` for token-based authentication.
- **Conversations**: Multiple participants per conversation.
- **Messages**:
  - Threaded replies via self-referential `parent_message`.
  - Read/unread status tracking.
  - Optimized queries using `select_related` and `prefetch_related`.
- **Message History**: Tracks edits to messages with timestamps and editors.
- **Notifications**: Linked to messages for specific users.
- **Unread Messages Manager**: Custom manager to quickly filter unread messages for a user.
- **Caching**:
  - Configured `LocMemCache`.
  - Cached list of messages in a conversation for 60 seconds using `cache_page`.
- **Pagination and Filtering**: Django Filter and DRF pagination for conversations and messages.

## API Endpoints

### Authentication
- `POST /token/` - Obtain JWT token
- `POST /token/refresh/` - Refresh JWT token

### Users
- `GET /users/` - List all users
- `POST /users/` - Create a new user
- `DELETE /users/delete/` - Delete the authenticated user

### Conversations
- `GET /conversations/` - List user conversations
- `POST /conversations/` - Create a conversation

### Messages
- `GET /conversations/{conversation_id}/messages/` - List messages in a conversation
- `POST /conversations/{conversation_id}/messages/` - Send a new message
- `GET /conversations/{conversation_id}/messages/{message_id}/thread/` - Get a message with all its replies (threaded)
- `GET /conversations/{conversation_id}/messages/unread/` - List unread messages for the user

### Notifications
- `GET /notifications/` - List user notifications

### Message History
- `GET /messagehistory/` - List message edit history for the authenticated user

## Installation

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd message_app
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   venv\Scripts\activate   # Windows
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables** in `.env`:
   ```env
   DJANGO_SECRET_KEY=your_secret_key
   DB_NAME=your_db_name
   DB_PASSWORD=your_db_password
   ```

5. **Run migrations**
   ```bash
   python manage.py migrate
   ```

6. **Create superuser**
   ```bash
   python manage.py createsuperuser
   ```

7. **Run server**
   ```bash
   python manage.py runserver
   ```

## Technologies Used
- Django
- Django REST Framework
- MySQL
- Simple JWT
- Django Filters
- LocMemCache
