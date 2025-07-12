# Skill Swap Platform

A full-stack web application that allows users to share and exchange skills. Users can offer skills they have and request to learn skills from others.

## Features

- **User Authentication**: Register, login, and profile management
- **Skill Management**: Add, edit, and delete skills you can teach
- **Skill Discovery**: Browse skills offered by other users
- **Request System**: Send and manage learning requests
- **Admin Panel**: Administrative tools for user and content management
- **Responsive Design**: Works on desktop and mobile devices

## Tech Stack

### Backend
- **Flask**: Python web framework
- **SQLAlchemy**: Database ORM
- **Flask-JWT-Extended**: JWT authentication
- **Flask-Bcrypt**: Password hashing
- **Flask-CORS**: Cross-origin resource sharing
- **SQLite**: Database (can be easily changed to PostgreSQL/MySQL)

### Frontend
- **React**: JavaScript library for building user interfaces
- **React Router**: Client-side routing
- **Axios**: HTTP client for API calls
- **CSS3**: Styling with modern CSS features

## Project Structure

```
skill-swap-platform/
├── backend/
│   ├── app.py              # Main Flask application
│   ├── init_db.py          # Database initialization script
│   ├── test_api.py         # API testing script
│   ├── requirements.txt    # Python dependencies
│   ├── .env               # Environment variables (create this)
│   └── instance/
│       └── skillswap.db   # SQLite database (auto-generated)
├── frontend/
│   ├── public/
│   │   └── index.html     # Main HTML file
│   ├── src/
│   │   ├── components/    # Reusable React components
│   │   ├── pages/         # Page components
│   │   ├── context/       # React context for state management
│   │   └── App.js         # Main React component
│   ├── package.json       # Node.js dependencies
│   └── README.md          # Frontend-specific documentation
└── README.md              # This file
```

## Installation and Setup

### Prerequisites
- Python 3.8 or higher
- Node.js 14 or higher
- npm or yarn

### Backend Setup

1. **Navigate to the backend directory:**
   ```bash
   cd skill-swap-platform/backend
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv .venv
   ```

3. **Activate the virtual environment:**
   - Windows:
     ```bash
     .venv\Scripts\activate
     ```
   - macOS/Linux:
     ```bash
     source .venv/bin/activate
     ```

4. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

5. **Create environment variables file:**
   Create a `.env` file in the backend directory with:
   ```
   SECRET_KEY=your-super-secret-key
   JWT_SECRET_KEY=your-jwt-secret-key
   DATABASE_URL=sqlite:///skillswap.db
   FLASK_ENV=development
   ```

6. **Initialize the database:**
   ```bash
   python init_db.py
   ```

7. **Start the backend server:**
   ```bash
   python app.py
   ```
   The server will run on `http://localhost:5000`

### Frontend Setup

1. **Navigate to the frontend directory:**
   ```bash
   cd skill-swap-platform/frontend
   ```

2. **Install Node.js dependencies:**
   ```bash
   npm install
   ```

3. **Start the development server:**
   ```bash
   npm start
   ```
   The application will open in your browser at `http://localhost:3000`

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
- `POST /api/requests` - Create a learning request
- `GET /api/requests/received` - Get received requests
- `GET /api/requests/sent` - Get sent requests
- `PUT /api/requests/<id>` - Update request status
- `DELETE /api/requests/<id>` - Delete a request

### Admin (Admin users only)
- `GET /api/admin/users` - Get all users
- `GET /api/admin/skills` - Get all skills
- `GET /api/admin/requests` - Get all requests
- `DELETE /api/admin/users/<id>` - Delete a user

## Sample Data

The database initialization script creates:
- **Admin user**: `admin@skillswap.com` / `admin123`
- **Sample users**: `john@example.com`, `jane@example.com`, `mike@example.com` (password: `password123`)
- **Sample skills**: React Development, UI/UX Design, Guitar Lessons, Python Programming, Digital Marketing, Spanish Language

## Testing

### Backend Testing
Run the API test script:
```bash
cd skill-swap-platform/backend
python test_api.py
```

### Frontend Testing
```bash
cd skill-swap-platform/frontend
npm test
```

## Deployment

### Backend Deployment
1. Set up a production database (PostgreSQL recommended)
2. Update environment variables for production
3. Use a WSGI server like Gunicorn
4. Set up reverse proxy with Nginx

### Frontend Deployment
1. Build the production version:
   ```bash
   npm run build
   ```
2. Deploy the `build` folder to your web server
3. Configure your web server to serve the React app

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License.

## Support

If you encounter any issues or have questions, please open an issue on GitHub. 