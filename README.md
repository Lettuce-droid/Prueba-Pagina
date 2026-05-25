# Imagenes Chistosas

A REST API and web application for sharing images, built with FastAPI, SQLAlchemy, and SQLite.

## What it does

- User registration and login with JWT authentication
- Upload and share images with a title and description
- Users can only delete their own posts
- Public feed to view all images without login
- Responsive design for mobile and desktop

## Requirements

- Python 3.13+

## Setup

1. Clone the repository:
   git clone https://github.com/Lettuce-droid/Prueba-Pagina.git
   cd Prueba-Pagina

2. Install dependencies:
   pip install fastapi uvicorn sqlalchemy pytest httpx python-jose[cryptography] passlib[bcrypt]==4.0.1 python-multipart python-dotenv

3. Create a `.env` file in the root folder:
SECRET_KEY=your-secret-key-here
DATABASE_URL=sqlite:///./books.db

4. Run the application:
   python -m uvicorn main:app --reload

5. Open your browser at:
   http://localhost:8000

## Running the tests

   python -m pytest tests/ -v

## Demo credentials

Register a new account through the frontend at http://localhost:8000

## API Endpoints

| Method | Endpoint | Auth required | Description |
|--------|----------|---------------|-------------|
| POST   | /users/register | No | Register a new user |
| POST   | /users/login | No | Login and get token |
| GET    | /posts/ | No | Get all posts |
| POST   | /posts/ | Yes | Create a post with image |
| PUT    | /posts/{id} | Yes | Update a post |
| DELETE | /posts/{id} | Yes | Delete a post |
| GET    | /health | No | Health check |

## Project Structure

```
├── main.py          # App entry point
├── database.py      # Database connection
├── models.py        # Database tables
├── schemas.py       # Data validation
├── auth.py          # Authentication logic
├── routers/
│   ├── users.py     # User endpoints
│   └── posts.py     # Post endpoints
├── tests/
│   └── test_books.py # Tests
└── index.html       # Frontend
```