# Task Manager

A full-stack task management application built with **FastAPI** (backend) and **Streamlit** (frontend), featuring JWT authentication and PostgreSQL storage.

## Features

- **User Authentication** — Register, login, and JWT-based session management
- **Task CRUD** — Create, view, update, and delete personal tasks
- **Profile Management** — Update user details or delete account
- **Secure Passwords** — Hashed using `pwdlib` (argon2)
- **Token Authorization** — All protected routes require a Bearer token

## Tech Stack

| Layer    | Technology              |
|----------|-------------------------|
| Backend  | FastAPI, SQLAlchemy     |
| Frontend | Streamlit               |
| Database | PostgreSQL              |
| Auth     | JWT (PyJWT), pwdlib     |

## Project Structure

```
├── main.py                  # FastAPI app entry point
├── app.py                   # Streamlit UI
├── requirements.txt
├── .env                     # Environment variables (not committed)
└── src/
    ├── tasks/
    │   ├── controller.py    # Task business logic
    │   ├── dtos.py          # Pydantic schemas
    │   ├── model.py         # SQLAlchemy model
    │   └── router.py        # API routes
    ├── users/
    │   ├── controller.py    # User business logic
    │   ├── dtos.py          # Pydantic schemas
    │   ├── model.py         # SQLAlchemy model
    │   └── router.py        # API routes
    └── utils/
        ├── constants.py
        ├── database.py      # DB engine & session
        └── helper.py        # JWT authorization dependency
```

## API Endpoints

### Users

| Method | Endpoint              | Auth | Description          |
|--------|-----------------------|------|----------------------|
| POST   | `/users/create_user`  | No   | Register a new user  |
| POST   | `/users/login`        | No   | Login, returns JWT   |
| GET    | `/users/`             | No   | List all users       |
| PUT    | `/users/update_user`  | Yes  | Update own profile   |
| DELETE | `/users/delete_user`  | Yes  | Delete own account   |

### Tasks

| Method | Endpoint                    | Auth | Description        |
|--------|-----------------------------|------|--------------------|
| GET    | `/tasks/tasks`              | Yes  | Get all your tasks |
| POST   | `/tasks/create_tasks`       | Yes  | Create a task      |
| PUT    | `/tasks/update_tasks/{id}`  | Yes  | Update a task      |
| DELETE | `/tasks/delete_tasks/{id}`  | Yes  | Delete a task      |

## Setup

### Prerequisites

- Python 3.10+
- PostgreSQL

### Installation

1. **Clone the repository**
   ```bash
   git clone <repo-url>
   cd Task-Management
   ```

2. **Create and activate a virtual environment**
   ```bash
   python -m venv taskenv
   # Windows
   taskenv\Scripts\activate
   # macOS/Linux
   source taskenv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**

   Create a `.env` file in the project root:
   ```env
   DATABASE_URL=postgresql://username:password@localhost:5432/your_database
   SECRET_KEY=your-secret-key
   ALGORITHM=HS256
   ACCESS_TOKEN_EXPIRE_SECONDS=30
   ```

5. **Run the backend**
   ```bash
   uvicorn main:app --reload
   ```
   The API will be available at `http://127.0.0.1:8000`. Interactive docs at `http://127.0.0.1:8000/docs`.

6. **Run the frontend** (in a separate terminal)
   ```bash
   streamlit run app.py
   ```
   Opens in browser at `http://localhost:8501`.
