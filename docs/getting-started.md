# Getting Started

This guide will help you get started with the AI Engineering MVP Template.

## Prerequisites

Before you begin, make sure you have the following installed:

- Docker & Docker Compose (v20.10.0+)
- Python (3.12+)
- Node.js (18.0.0+)
- `uv` for Python package management

## Using This Template

### 1. Create a New Repository

Start by clicking the "Use this template" button at the top of the repository page on GitHub. This will create a new repository with all the template files.

### 2. Clone Your New Repository

```bash
git clone https://github.com/yourusername/your-new-repo.git
cd your-new-repo
```

### 3. Configure Environment Variables

Copy the example environment file and customize it for your project:

```bash
cp .env.example .env.development
```

Edit the `.env.development` file to set your project-specific values.

### 4. Start Development Services

The easiest way to start development is with Docker Compose:

```bash
docker compose --env-file .env.development -f docker-compose.dev.yml up
```

This will start both the frontend and backend services in development mode with hot reloading.

### 5. Access the Services

- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Documentation: http://localhost:8000/docs

## Development Without Docker

If you prefer to run the services directly on your machine:

### Frontend

```bash
cd frontend
npm install
npm run dev
```

### Backend

```bash
cd backend
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
uv pip install -e ".[dev]"
uvicorn api.main:app --reload
```

## Next Steps

Once you have the template set up, you can start customizing it for your specific application needs:

1. Update the README.md with your project information
2. Customize the frontend UI components
3. Add your business logic to the backend services
4. Set up your CI/CD pipeline

See the [Backend Development](backend-development.md) and [Frontend Development](frontend-development.md) guides for more details.
