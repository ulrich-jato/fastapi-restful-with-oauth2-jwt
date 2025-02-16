# fastapi-restful-with-oauth2-jwt
# FastAPI Application

This FastAPI application provides an authentication system and the ability to manage todos. It supports user registration, login, and role-based access control, allowing users to create, read, update, and delete their todos. Admin users can also manage todos for all users.

## Features

- User authentication and token-based session management using JWT.
- Role-based access control (admin and user).
- CRUD operations for todos.
- Secure password management with bcrypt hashing.
- Password and phone number update functionality for users.
- Health check endpoint to verify the server's status.

## Requirements

- Python 3.9+
- SQLAlchemy
- FastAPI
- Pydantic
- passlib
- python-dotenv
- JWT (JSON Web Token)
- SQLite/PostgreSQL/MySQL (configurable database)

## Installation

1. Clone the repository:

   ```bash
   git clone <repo_url>
   cd <repo_directory>
   ```
1. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

2. Create a `.env` file in the root directory with the following variables:

   ```env
   SECRET_KEY=<your_secret_key>
   ALGORITHM=<your_algorithm>
   DATABASE_URL=sqlite:///./test.db  # or PostgreSQL/MySQL connection string
   ```

3. Run the application:

   ```bash
   uvicorn main:app --reload
   ```

## Endpoints

### Authentication

#### POST /auth/
Create a new user.

**Request Body:**

```json
{
  "username": "string",
  "email": "string",
  "first_name": "string",
  "last_name": "string",
  "password": "string",
  "role": "string",
  "phone_number": "string"
}
```

**Response:**

- 201 Created if the user was created successfully.

#### POST /auth/token
Login and obtain a JWT access token.

**Request Body (Form Data):**

```
username: string
password: string
```

**Response:**

```json
{
  "access_token": "string",
  "token_type": "bearer"
}
```

### Todos

#### GET /todos/
Get all todos for the authenticated user.

**Response:**

- List of todos belonging to the authenticated user.

#### GET /todo/{todo_id}
Get a specific todo by ID for the authenticated user.

**Response:**

- 200 OK with todo details.
- 404 Not Found if todo does not exist.

#### POST /todo/
Create a new todo for the authenticated user.

**Request Body:**

```json
{
  "title": "string",
  "description": "string",
  "priority": 1,
  "complete": false
}
```

**Response:**

- 201 Created if the todo is successfully created.

#### PUT /todo/{todo_id}
Update an existing todo for the authenticated user.

**Request Body:**

```json
{
  "title": "string",
  "description": "string",
  "priority": 1,
  "complete": true
}
```

**Response:**

- 204 No Content if the todo was successfully updated.

#### DELETE /todo/{todo_id}
Delete a todo by ID for the authenticated user.

**Response:**

- 204 No Content if the todo was successfully deleted.

### User Management

#### GET /user/
Get the details of the authenticated user.

**Response:**

- 200 OK with user details.

#### PUT /user/password
Change the password for the authenticated user.

**Request Body:**

```json
{
  "old_password": "string",
  "new_password": "string"
}
```

**Response:**

- 204 No Content if the password was successfully changed.

#### PUT /user/phonenumber/{phone_number}
Update the phone number for the authenticated user.

**Response:**

- 204 No Content if the phone number was successfully updated.

### Admin

#### GET /admin/todo
Get all todos for all users (admin only).

**Response:**

- List of all todos in the system.

#### DELETE /admin/todo/{todo_id}
Delete a todo by ID (admin only).

**Response:**

- 204 No Content if the todo was successfully deleted.

### Health Check

#### GET /healthy
Check the health status of the server.

**Response:**

```json
{
  "status": "Healthy"
}
```

## Database Configuration

By default, the application connects to a SQLite database (test.db). However, it can be easily configured to connect to PostgreSQL or MySQL.

**SQLite**

```python
SQLALCHEMY_DATABASE_URL = 'sqlite:///./test.db'
```

**PostgreSQL**

```python
SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:yourpassword@localhost/TodoApplicationDatabase'
```

**MySQL**

```python
SQLALCHEMY_DATABASE_URL = 'mysql+pymysql://root:password@localhost:3306/todoapplicationdatabase'
```

## File Structure

```bash
├── .env               # Environment variables
├── main.py            # Main FastAPI app
├── models.py          # SQLAlchemy models
├── database.py        # Database connection setup
├── alembic/           # Alembic migration files
│   ├── versions/      # Migration scripts
│   └── env.py         # Alembic environment setup
├── alembic.ini        # Alembic configuration file
├── routers/           # API routes
│   ├── auth.py        # Authentication routes
│   ├── todos.py       # Todo-related routes
│   ├── users.py       # User-related routes
│   └── admin.py       # Admin routes
├── requirements.txt   # List of dependencies
└── README.md          # Documentation
```

## Security Notes

- Use a strong `SECRET_KEY` in your `.env` file.
- Do not store sensitive data like passwords or secret keys in public repositories.
- For production environments, use a proper database URL for PostgreSQL or MySQL.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
