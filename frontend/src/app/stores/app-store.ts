import { create } from 'zustand';

interface AppState {
  // Add your application state properties here
  isLoading: boolean;
  setIsLoading: (isLoading: boolean) => void;
}

export const useAppStore = create<AppState>((set) => ({
  isLoading: false,
  setIsLoading: (isLoading: boolean) => set({ isLoading }),
}));
