import { useState, useEffect } from 'react'

interface User {
  id: string
  email: string
  name?: string
  plan?: 'free' | 'starter' | 'pro' | 'business'
}

export function useAuth() {
  const [user, setUser] = useState<User | null>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    // TODO: Check for stored token and validate
    const token = localStorage.getItem('wikiask-token')
    if (token) {
      // TODO: Validate token with backend
      // For now, mock user
      setUser({
        id: '1',
        email: 'user@example.com',
        plan: 'free',
      })
    }
    setLoading(false)
  }, [])

  const login = async (email: string, password: string) => {
    // TODO: Implement login API call
    const mockUser: User = {
      id: '1',
      email,
      plan: 'free',
    }
    setUser(mockUser)
    localStorage.setItem('wikiask-token', 'mock-token')
  }

  const logout = () => {
    setUser(null)
    localStorage.removeItem('wikiask-token')
  }

  return { user, loading, login, logout, isAuthenticated: !!user }
}

