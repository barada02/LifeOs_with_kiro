# LifeOS Foundation

A productivity and life management application built with React + Vite frontend and FastAPI backend.

## Project Structure

```
lifeos/
├── frontend/          # React + Vite frontend application
├── backend/           # FastAPI backend application
├── .gitignore        # Git ignore rules
└── README.md         # This file
```

## Prerequisites

Before setting up the project, ensure you have the following installed:

- **Node.js** (v18 or higher) - for frontend development
- **Python** (v3.9 or higher) - for backend development
- **Git** - for version control

## Setup Instructions

### 1. Clone the Repository

```bash
git clone <repository-url>
cd lifeos
```

### 2. Frontend Setup

Navigate to the frontend directory and install dependencies:

```bash
cd frontend
npm install
```

Start the development server:

```bash
npm run dev
```

The frontend will be available at `http://localhost:5173`

### 3. Backend Setup

Navigate to the backend directory and create a virtual environment:

```bash
cd backend
python -m venv venv
```

Activate the virtual environment:

**Windows:**
```bash
venv\Scripts\activate
```

**macOS/Linux:**
```bash
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Start the backend server:

```bash
uvicorn app.main:app --reload --port 8000
```

The backend API will be available at `http://localhost:8000`

### 4. Database Setup

The application uses SQLite for local development. The database will be automatically created when you first run the backend server.

## Development Workflow

1. **Start Backend**: Run the FastAPI server on port 8000
2. **Start Frontend**: Run the Vite dev server on port 5173
3. **Access Application**: Open `http://localhost:5173` in your browser

## API Documentation

When the backend is running, you can access the interactive API documentation at:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Environment Variables

Create `.env` files in both frontend and backend directories as needed:

**Frontend (.env):**
```
VITE_API_BASE_URL=http://localhost:8000
```

**Backend (.env):**
```
DATABASE_URL=sqlite:///./lifeos.db
JWT_SECRET_KEY=your-secret-key-here
```

## Available Scripts

### Frontend
- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run preview` - Preview production build
- `npm run lint` - Run ESLint

### Backend
- `uvicorn app.main:app --reload` - Start development server
- `python -m pytest` - Run tests
- `alembic upgrade head` - Run database migrations

## Technology Stack

**Frontend:**
- React 18 with TypeScript
- Vite for build tooling
- Tailwind CSS for styling
- Axios for HTTP requests
- React Router for navigation

**Backend:**
- FastAPI with Python
- SQLAlchemy for ORM
- SQLite for database
- Pydantic for data validation
- Uvicorn as ASGI server

## Contributing

1. Create a feature branch from main
2. Make your changes
3. Test your changes thoroughly
4. Submit a pull request

## License

This project is licensed under the MIT License.