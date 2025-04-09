# MVP Frontend

This is the frontend for the AI Engineering MVP Template built with Next.js.

## Development

### Local Development

```bash
npm install
npm run dev
```

### With Docker

```bash
# From the root directory
docker compose --env-file .env.development -f docker-compose.dev.yml up frontend-dev
```

## Project Structure

- **src/app**: Next.js App Router layout and pages
- **src/app/components**: Reusable React components
- **src/app/stores**: State management with Zustand
- **src/app/types**: TypeScript type definitions

## Adding New Pages

To add a new page, create a new directory in src/app with a page.tsx file, following the Next.js App Router conventions.
