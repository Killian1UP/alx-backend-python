# Messaging App - Django REST Framework

This project is a messaging system built using Django and Django REST Framework. It is part of the **ALX Backend Python** curriculum and demonstrates model design, serializer implementation, API development using viewsets, and URL routing with nested resources.

---

## 🛠 Project Setup

- Initialized Django project: `django-admin startproject messaging_app`
- Installed Django REST Framework via `pip install djangorestframework`
- Added `'rest_framework'` to `INSTALLED_APPS` in `settings.py`
- Created a new app for messaging: `python manage.py startapp chats`

---

## 🧩 Models

Located in: `messaging_app/chats/models.py`

### `User`
- Extended from `AbstractUser`
- Fields: `user_id`, `first_name`, `last_name`, `email`, `password_hash`, `phone_number`, `role`, `created_at`

### `Conversation`
- Fields: `conversation_id`, `participants_id` (ManyToMany to User), `created_at`

### `Message`
- Fields: `message_id`, `sender_id` (ForeignKey to User), `conversation` (ForeignKey to Conversation), `message_body`, `sent_at`

---

## 🔄 Serializers

Located in: `messaging_app/chats/serializers.py`

- `UserSerializer`: Includes full name, email validation, password handling
- `ConversationSerializer`: Handles nested messages, many-to-many participants
- `MessageSerializer`: Handles linking sender and conversation by UUID

---

## 🔧 Views

Located in: `messaging_app/chats/views.py`

- `ConversationViewSet`: Lists and creates conversations
- `MessageViewSet`: Lists and sends messages to existing conversations
- Both viewsets use `IsAuthenticated` and `SessionAuthentication`

---

## 🌐 URL Routing

### `chats/urls.py`
- Used `DefaultRouter` to register:
  - `conversation/`
  - `message/`

### `messaging_app/urls.py`
- Included the `chats` app routes with path `'api/'`
- Added `api-auth/` for session login via browsable API

---

## 🚀 Running the Application

To run and test the application:

```bash
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```

Check the API endpoints in your browser at `http://127.0.0.1:8000/api/`

---

## ✅ Features Implemented

- User model extending AbstractUser with custom fields
- Conversation with multiple participants
- Messaging system with conversation linking
- Full CRUD API for conversations and messages using DRF ViewSets
- Nested serializers for rich API responses
- Authenticated routes with DRF permissions

---

## 📁 Directory Structure

```
messaging_app/
│
├── chats/
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── urls.py
│
├── messaging_app/
│   ├── settings.py
│   ├── urls.py
│
├── manage.py
```

---

## 🧪 Testing and Debugging

- Verified all API routes using Django's browsable API
- Applied migrations after model changes
- Handled validation errors in serializers
- Ensured `runserver` started with no errors

---

## 📜 License

This project is for educational purposes under ALX Africa.