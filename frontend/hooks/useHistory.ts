import { useState, useEffect, useCallback } from 'react'

interface HistoryItem {
  id: string
  query: string
  type: 'search' | 'ai-search' | 'chat'
  timestamp: string
  results?: any
}

export function useHistory() {
  const [history, setHistory] = useState<HistoryItem[]>([])

  useEffect(() => {
    const stored = localStorage.getItem('wikiask-history')
    if (stored) {
      try {
        setHistory(JSON.parse(stored))
      } catch (e) {
        // Logger silencieux en production
        if (process.env.NODE_ENV === 'development') {
          console.error('Failed to load history:', e);
        }
      }
    }
  }, [])

  const addToHistory = useCallback((item: Omit<HistoryItem, 'id' | 'timestamp'>) => {
    const newItem: HistoryItem = {
      ...item,
      id: Date.now().toString(),
      timestamp: new Date().toISOString(),
    }
    setHistory(prev => {
      const updated = [newItem, ...prev].slice(0, 100) // Keep last 100 items
      localStorage.setItem('wikiask-history', JSON.stringify(updated))
      return updated
    })
  }, [])

  const clearHistory = useCallback(() => {
    setHistory([])
    localStorage.removeItem('wikiask-history')
  }, [])

  const removeFromHistory = useCallback((id: string) => {
    setHistory(prev => {
      const updated = prev.filter(item => item.id !== id)
      localStorage.setItem('wikiask-history', JSON.stringify(updated))
      return updated
    })
  }, [])

  return { history, addToHistory, clearHistory, removeFromHistory }
}


interface HistoryItem {
  id: string
  query: string
  type: 'search' | 'ai-search' | 'chat'
  timestamp: string
  results?: any
}

export function useHistory() {
  const [history, setHistory] = useState<HistoryItem[]>([])

  useEffect(() => {
    const stored = localStorage.getItem('wikiask-history')
    if (stored) {
      try {
        setHistory(JSON.parse(stored))
      } catch (e) {
        // Logger silencieux en production
        if (process.env.NODE_ENV === 'development') {
          console.error('Failed to load history:', e);
        }
      }
    }
  }, [])

  const addToHistory = useCallback((item: Omit<HistoryItem, 'id' | 'timestamp'>) => {
    const newItem: HistoryItem = {
      ...item,
      id: Date.now().toString(),
      timestamp: new Date().toISOString(),
    }
    setHistory(prev => {
      const updated = [newItem, ...prev].slice(0, 100) // Keep last 100 items
      localStorage.setItem('wikiask-history', JSON.stringify(updated))
      return updated
    })
  }, [])

  const clearHistory = useCallback(() => {
    setHistory([])
    localStorage.removeItem('wikiask-history')
  }, [])

  const removeFromHistory = useCallback((id: string) => {
    setHistory(prev => {
      const updated = prev.filter(item => item.id !== id)
      localStorage.setItem('wikiask-history', JSON.stringify(updated))
      return updated
    })
  }, [])

  return { history, addToHistory, clearHistory, removeFromHistory }
}

