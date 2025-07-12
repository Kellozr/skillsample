# SkillSwap Backend

A Flask-based REST API for the SkillSwap platform that allows users to share and request skills.

## Features

- **User Authentication**: Register, login, and JWT-based authentication
- **Skill Management**: Create, view, and manage skills
- **Request System**: Send and manage skill requests
- **Admin Panel**: Admin-only routes for managing users, skills, and requests
- **Database**: SQLite database with SQLAlchemy ORM

## Setup Instructions

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Initialize Database

```bash
python init_db.py
```

This will:
- Create the database tables
- Create an admin user (admin@skillswap.com / admin123)
- Create sample users and skills

### 3. Start the Server

```bash
python app.py
```

The server will start on `http://localhost:5000`

## API Endpoints

### Authentication
- `POST /api/auth/register` - Register a new user
- `POST /api/auth/login` - Login user

### Profile
- `GET /api/profile` - Get user profile
- `PUT /api/profile` - Update user profile

### Skills
- `GET /api/skills` - Get all skills
- `POST /api/skills` - Create a new skill
- `GET /api/skills/my-skills` - Get user's skills
- `DELETE /api/skills/<id>` - Delete a skill

### Requests
- `POST /api/requests` - Create a skill request
- `GET /api/requests/received` - Get received requests
- `GET /api/requests/sent` - Get sent requests
- `PUT /api/requests/<id>` - Update request status
- `DELETE /api/requests/<id>` - Delete a request

### Admin (Admin only)
- `GET /api/admin/users` - Get all users
- `GET /api/admin/skills` - Get all skills
- `GET /api/admin/requests` - Get all requests
- `DELETE /api/admin/users/<id>` - Delete a user
- `DELETE /api/admin/skills/<id>` - Delete a skill
- `DELETE /api/admin/requests/<id>` - Delete a request

## Sample Data

After running `init_db.py`, you'll have:

### Admin User
- Email: admin@skillswap.com
- Password: admin123

### Sample Users
- john@example.com / password123
- jane@example.com / password123
- mike@example.com / password123

### Sample Skills
- React Development (Programming)
- UI/UX Design (Design)
- Guitar Lessons (Music)
- Python Programming (Programming)
- Digital Marketing (Marketing)
- Spanish Language (Languages)

## Database Schema

### Users
- id (Primary Key)
- name
- email (Unique)
- password_hash
- bio
- role (user/admin)
- created_at

### Skills
- id (Primary Key)
- name
- description
- category
- level
- owner_id (Foreign Key to Users)
- created_at

### Requests
- id (Primary Key)
- skill_id (Foreign Key to Skills)
- requester_id (Foreign Key to Users)
- message
- status (pending/accepted/rejected)
- created_at
- updated_at

## Environment Variables

Create a `.env` file in the backend directory:

```
SECRET_KEY=your-super-secret-key-change-this-in-production
JWT_SECRET_KEY=your-jwt-secret-key-change-this-in-production
DATABASE_URL=sqlite:///skillswap.db
FLASK_ENV=development
```

## Security Features

- Password hashing with bcrypt
- JWT token authentication
- Role-based access control
- Input validation
- CORS enabled for frontend integration 