# AI Engineering MVP Template

This template repository helps you quickly bootstrap MVP applications with a
professional, production-ready foundation.

## ✨ Why Use This Template?

- **Save time**: Skip boilerplate configuration and start building immediately
- **Best practices**: Follows industry standards for Docker, CI/CD, and application architecture
- **Flexibility**: Easily customize while maintaining a solid foundation
- **Full-stack**: Includes both frontend (Next.js) and backend (FastAPI) with proper integration

## 🚀 Getting Started

### Using This Template

1. Click the "Use this template" button at the top of this repository
2. Name your new repository and create it
3. Clone your new repository locally
4. Customize according to your project needs (see Customization Guide below)

### Prerequisites

- Docker & Docker Compose (v20.10.0+)
- Python (3.11+)
- Node.js (18.0.0+)

## 🏗️ What's Included

### Architecture

- **Frontend**: Next.js with TypeScript, ready for modern UI development
- **Backend**: FastAPI for building high-performance APIs
- **Docker**: Development and production configurations
- **Environment Management**: Properly separated dev/prod environments

### Directory Structure

```
/
├── frontend/                # Next.js frontend application
│   ├── src/
│   │   ├── app/             # Next.js App Router
│   │   │   ├── components/  # React components
│   │   │   ├── stores/      # State management
│   │   │   └── types/       # TypeScript type definitions
│   ├── Dockerfile           # Production Docker configuration
│   └── Dockerfile.dev       # Development Docker configuration
│
├── backend/                 # FastAPI backend application
│   ├── api/                 # API endpoints and configuration
│   ├── services/            # Business logic and services
│   ├── Dockerfile           # Production Docker configuration
│   └── Dockerfile.dev       # Development Docker configuration
│
├── scripts/                 # Utility scripts for setup/management
├── docs/                    # Documentation
│   └── assets/              # Images and other documentation assets
│
├── docker-compose.yml       # Production Docker Compose configuration
├── docker-compose.dev.yml   # Development Docker Compose configuration
└── .env.example             # Example environment variables
```

## 🔧 Customization Guide

### 1. Configure Environment Variables

Copy the `.env.example` file to both `.env.development` and `.env`:

```bash
cp .env.example .env.development
cp .env.example .env
```

The `.env` file is used by Docker Compose for variable substitution in the compose files. The `.env.development` file can be used for any additional environment-specific configuration.

Edit these files to add your specific API keys and configuration.

### 2. Update Project Information

- Update this README.md with your project details
- Modify the package.json and pyproject.toml with your project name/details

### 3. Extend the Backend

The backend is organized to make extension easy:
- Add new endpoints in `backend/api/routes.py`
- Create new services in `backend/services/`
- Configure API settings in `backend/api/config.py`

### 4. Customize the Frontend

The frontend uses Next.js App Router architecture:
- Add components in `frontend/src/app/components/`
- Create new pages by adding folders to `frontend/src/app/`
- Define types in `frontend/src/app/types/`
- Manage state with Zustand in `frontend/src/app/stores/`

## 🚢 Running the Application

### Development

Start the development environment:

```bash
docker compose -f docker-compose.dev.yml up
```

Or rebuild containers (needed after dependency changes):

```bash
docker compose -f docker-compose.dev.yml up --build
```

The application will be available at:
- Frontend: http://localhost:3000
- Backend: http://localhost:8000
- Backend API docs: http://localhost:8000/docs

To stop the containers:

```bash
docker compose -f docker-compose.dev.yml down
```

### Production

```bash
docker compose -f docker-compose.yml up
```

**Note**: Make sure to create and configure a `.env.production` file for production deployments.

## 🔍 Troubleshooting

### Docker Compose environment variable errors

If you see errors like `'${BACKEND_PORT}' is not a valid integer` or variables not being set:

1. Ensure you have created a `.env` file (not just `.env.development`):
   ```bash
   cp .env.example .env
   ```

2. If you previously built containers with incorrect configuration, rebuild them:
   ```bash
   docker compose -f docker-compose.dev.yml down
   docker compose -f docker-compose.dev.yml up --build
   ```

### Frontend dependency conflicts

If you encounter ESLint or dependency version conflicts:

- The `eslint-config-next` version should match your Next.js version
- Check `frontend/package.json` and ensure version compatibility
- Run `npm install` in the frontend directory to regenerate `package-lock.json`

## 📚 Additional Resources

- [Next.js Documentation](https://nextjs.org/docs)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Docker Documentation](https://docs.docker.com/)

## 📝 License

This template is released under the Apache-2.0 License. See the LICENSE file for details.
