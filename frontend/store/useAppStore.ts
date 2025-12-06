import { create } from 'zustand'
import { persist } from 'zustand/middleware'

interface AppState {
  user: {
    id: string
    email: string
    plan: 'free' | 'starter' | 'pro' | 'business'
  } | null
  preferences: {
    language: string
    theme: 'dark' | 'light' | 'auto'
  }
  searchCache: Record<string, any>
  recentSearches: string[]
}

interface AppActions {
  setUser: (user: AppState['user']) => void
  setPreferences: (preferences: Partial<AppState['preferences']>) => void
  addToCache: (key: string, value: any) => void
  getFromCache: (key: string) => any
  addRecentSearch: (query: string) => void
  clearCache: () => void
}

export const useAppStore = create<AppState & AppActions>()(
  persist(
    (set, get) => ({
      user: null,
      preferences: {
        language: 'fr',
        theme: 'dark',
      },
      searchCache: {},
      recentSearches: [],

      setUser: (user) => set({ user }),

      setPreferences: (preferences) =>
        set((state) => ({
          preferences: { ...state.preferences, ...preferences },
        })),

      addToCache: (key, value) =>
        set((state) => ({
          searchCache: { ...state.searchCache, [key]: value },
        })),

      getFromCache: (key) => get().searchCache[key],

      addRecentSearch: (query) =>
        set((state) => ({
          recentSearches: [query, ...state.recentSearches.filter(q => q !== query)].slice(0, 10),
        })),

      clearCache: () => set({ searchCache: {} }),
    }),
    {
      name: 'wikiask-app-store',
    }
  )
)

