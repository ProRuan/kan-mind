# Kanmind App – REST API Documentation

Welcome to the API documentation for **Kanmind**, a minimal task management
app built using Django and Django REST Framework. This app allows users to
create boards, tasks, and manage their status and deadlines in a Kanban-style
workflow.

---

## 🌐 Base URL

This project is under development.

> Open the project in **Visual Studio Code**.
> Open a new terminal and enter

```
git clone git@github.com:ProRuan/kan-mind.git

cd ./kan-mind/

python -m venv env

"env/Scripts/activate"

pip install -r requirements.txt

pip freeze

python manage.py makemigrations

python manage.py migrate

python manage.py runserver
```

> Use your local domain or localhost (e.g. `http://127.0.0.1:8000/api/`).

---

## ❗ Kanmind Frontend

You can find the kanmind frontend project here:

**GitHub**: https://github.com/Developer-Akademie-Backendkurs/project.KanMind

If you would like to use the guest account, update the config.js which you can
find at the "shared" folder. There you could set your guest login as below:

```
const GUEST_LOGIN = {
    "email": "morgan.taylor@example.com",
    "password": "Test123!"
}
```

---

## 🔐 Authentication

This API uses **token-based authentication**.

- Obtain a token via `/api/registration/` endpoint (POST).
- Include the token in the `Authorization` header for all requests:

```
Authorization: Token your_token_here
```

---

## 📋 Endpoints Overview

### 🧾 Authentication

- `POST /api/registration/` – Register a user
- `POST /api/login/` – Log in a user

### 🧾 Boards

- `GET /boards/` – List all boards
- `POST /boards/` – Create a new board
- `GET /boards/{board_id}/` – Retrieve a board
- `PATCH /boards/{board_id}/` – Update a board
- `DELETE /boards/{board_id}/` – Delete a board
- `GET /api/email-check/` – Verifies an email that is already added to a board

### ✅ Tasks

- `GET /api/tasks/assigned-to-me/` – List all boards mentioning a user as assignee
- `GET /api/tasks/reviewing/` – List all boards mentioning a user as reviever
- `POST /api/tasks/` – Create a new task
- `PATCH /api/tasks/{task_id}/` – Update a task
- `DELETE /api/tasks/{task_id}/` – Delete a task
- `GET /api/tasks/{task_id}/comments/` – List all task comments
- `POST /api/tasks/{task_id}/comments/` – Create a task comment
- `DELETE /api/tasks/{task_id}/comments/{comment_id}/` – Delete a task commentar

---

## 🚫 Permissions

- Only **authenticated users** can access the API.
- Users can only **view and modify** boards and tasks they created or are
  assigned to.

---

## 📣 Contact

If you encounter issues or have questions, please contact the developer:

**Name**: Rudolf Johann Sachslehner
**Email**: rudolf.sachslehner@gmx.at
**GitHub**: https://github.com/ProRuan
