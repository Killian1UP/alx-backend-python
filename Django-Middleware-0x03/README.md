# Django Middleware Project: Messaging App

This project is a continuation of the `messaging_app` built in the `Building Robust APIs` module. The focus here is on implementing custom Django middleware to enhance functionality and control over user interactions within the application.

## Project Structure

- **Repository:** `alx-backend-python`
- **Directory:** `Django-Middleware-0x03`
- **App:** `chats`
- **Entry Point:** `Django-Middleware-0x03/chats/middleware.py`

---

## 1. Logging User Requests

**Objective:** Log each user’s request to a log file.

### Implementation:
- Created a class `RequestLoggingMiddleware` with `__init__` and `__call__` methods.
- Logs the request time, user, and path to `requests.log`.
- Example log: `2025-07-27 12:45:23 - User: johndoe - Path: /api/messages/`

**File:** `chats/middleware.py`  
**Log File:** `requests.log`

---

## 2. Restrict Chat Access by Time

**Objective:** Restrict chat access to users only between 6PM and 9PM.

### Implementation:
- Created a class `RestrictAccessByTimeMiddleware`.
- Checks server time using `datetime.now().hour`.
- Denies access (HTTP 403) if request time is outside 18:00 to 21:00.

**File:** `chats/middleware.py`

---

## 3. Detect and Block Offensive Language (Rate Limiting)

**Objective:** Limit the number of chat messages a user can send per minute.

### Implementation:
- Created a class `OffensiveLanguageMiddleware`.
- Tracks number of POST requests to `/api/messages/` per IP.
- Denies access (HTTP 403) if more than 5 messages are sent within a minute.

**File:** `chats/middleware.py`

---

## 4. Enforce Chat User Role Permissions

**Objective:** Allow only admins to access certain actions.

### Implementation:
- Created a class `RolepermissionMiddleware`.
- Checks if the user role is `admin`.
- Restricts access to paths starting with `/api/messages/` for non-admin users.

**File:** `chats/middleware.py`

---

## Middleware Configuration

All middleware classes were added to the `MIDDLEWARE` list in `settings.py` in the following order (below built-in middleware):

```
MIDDLEWARE = [
    ...
    'chats.middleware.RequestLoggingMiddleware',
    'chats.middleware.RestrictAccessByTimeMiddleware',
    'chats.middleware.OffensiveLanguageMiddleware',
    'chats.middleware.RolepermissionMiddleware',
]
```

---

## How to Run

1. Clone the repo:
```bash
git clone https://github.com/Killian1UP/alx-backend-python.git
cd Django-Middleware-0x03
```

2. Set up the virtual environment and install dependencies.

3. Run the server:
```bash
python manage.py runserver
```

---

## Author

Ikaelelo Motlhako