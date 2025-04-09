# Frontend Development

This guide covers the key aspects of frontend development using Next.js in this template.

## Environment Setup

```bash
# Navigate to the frontend directory
cd frontend

# Install dependencies
npm install

# Start the development server
npm run dev
```

This will start the Next.js development server with hot reloading at http://localhost:3000.

## Project Structure

The frontend is organized following the Next.js App Router structure:

```
frontend/
├── public/              # Static files
├── src/
│   ├── app/            # Next.js App Router
│   │   ├── components/ # React components
│   │   ├── stores/     # Zustand state management
│   │   ├── types/      # TypeScript types
│   │   ├── globals.css # Global styles
│   │   ├── layout.tsx  # Root layout
│   │   └── page.tsx    # Home page
├── next.config.mjs     # Next.js configuration
├── package.json        # Dependencies and scripts
├── tailwind.config.ts  # Tailwind CSS configuration
└── tsconfig.json       # TypeScript configuration
```

## Key Features

### Components

The template includes several example components:

- `Header`: A simple header component
- `ApiExample`: An example component that fetches data from the backend API

### State Management

The template uses Zustand for state management, which is a lightweight state management library.

Example state in `src/app/stores/app-store.ts`:

```typescript
import { create } from 'zustand';

interface AppState {
  isLoading: boolean;
  setIsLoading: (isLoading: boolean) => void;
}

export const useAppStore = create<AppState>((set) => ({
  isLoading: false,
  setIsLoading: (isLoading: boolean) => set({ isLoading }),
}));
```

### TypeScript Types

The template uses TypeScript for type safety. Common types are defined in the `src/app/types` directory.

### Styling

The template uses Tailwind CSS for styling.

## API Communication

The template includes an example of how to communicate with the backend API:

```typescript
const fetchApiExample = async () => {
  try {
    const backendHost = process.env.NEXT_PUBLIC_BACKEND_HOST || 'localhost';
    const backendPort = process.env.NEXT_PUBLIC_BACKEND_PORT || '8000';
    const response = await fetch(`http://${backendHost}:${backendPort}/api/example`);

    if (!response.ok) {
      throw new Error(`API request failed with status ${response.status}`);
    }

    const data = await response.json();
    return data;
  } catch (err) {
    console.error('Error fetching API example:', err);
    throw err;
  }
};
```

## Adding New Pages

With Next.js App Router, creating new pages is straightforward:

1. Create a new directory under `src/app`
2. Add a `page.tsx` file in that directory

For example, to create an "About" page:

```
src/app/about/page.tsx
```

```tsx
export default function AboutPage() {
  return (
    <div className="container mx-auto py-8">
      <h1 className="text-2xl font-bold">About</h1>
      <p className="mt-4">This is the about page.</p>
    </div>
  );
}
```

## Building for Production

To build the frontend for production:

```bash
npm run build
```

The built files will be in the `.next` directory.

## Code Quality

The template includes configuration for several code quality tools:

- **ESLint**: For linting
- **TypeScript**: For type checking

To run linting:

```bash
npm run lint
```

## Testing

You can add tests to the frontend using testing libraries like Jest and React Testing Library:

1. Install testing dependencies:

```bash
npm install --save-dev jest @testing-library/react @testing-library/jest-dom
```

2. Create a test file, e.g., `src/app/components/Header.test.tsx`

## Customizing the Template

### Changing Theme and Styling

The template uses Tailwind CSS for styling. You can customize the theme in `tailwind.config.ts`:

```typescript
import type { Config } from "tailwindcss";

const config: Config = {
  content: [
    "./src/pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/components/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        primary: "#0070f3",
        secondary: "#1f2937",
      },
    },
  },
  plugins: [],
};
export default config;
```
