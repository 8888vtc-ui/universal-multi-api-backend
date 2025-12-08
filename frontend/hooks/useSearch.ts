import { useState, useCallback } from 'react'
import { apiClient, SearchRequest, SearchResponse } from '@/lib/api'

export function useSearch() {
  const [results, setResults] = useState<SearchResponse | null>(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const search = useCallback(async (request: SearchRequest) => {
    setLoading(true)
    setError(null)
    try {
      const response = await apiClient.search(request)
      setResults(response)
      return response
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Search failed'
      setError(errorMessage)
      throw err
    } finally {
      setLoading(false)
    }
  }, [])

  return { results, loading, error, search }
}





