'use client';

import { ChakraProvider, createSystem, defaultConfig } from '@chakra-ui/react';

const system = createSystem(defaultConfig, {
  theme: {
    tokens: {
      colors: {
        brand: {
          pink: { value: '#eb088a' },
          purple: { value: '#8a08eb' },
        },
      },
    },
  },
  globalCss: {
    'body': {
      bg: 'white',
    },
  },
});

export function Providers({ children }: { children: React.ReactNode }) {
  return <ChakraProvider value={system}>{children}</ChakraProvider>;
}
