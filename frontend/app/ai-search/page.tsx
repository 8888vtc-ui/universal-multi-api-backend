'use client'

import { useState } from 'react'
import MainLayout from '@/components/layouts/MainLayout'
import SearchBar from '@/components/search/SearchBar'
import AISummary from '@/components/search/AISummary'
import SearchResults from '@/components/search/SearchResults'

export default function AISearchPage() {
  const [query, setQuery] = useState('')
  const [results, setResults] = useState<any>(null)
  const [loading, setLoading] = useState(false)

  const handleAISearch = async (searchQuery: string) => {
    setQuery(searchQuery)
    setLoading(true)
    try {
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL || ''}/api/ai-search/search`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ query: searchQuery }),
      })
      const data = await response.json()
      setResults(data)
    } catch (error) {
      // Logger silencieux en production
      if (process.env.NODE_ENV === 'development') {
        console.error('AI Search error:', error);
      }
    } finally {
      setLoading(false)
    }
  }

  return (
    <MainLayout>
      <div className="max-w-7xl mx-auto px-6 py-8">
        <div className="mb-8">
          <h1 className="text-4xl font-bold mb-4 gradient-text">Recherche IA</h1>
          <p className="text-dark-400">Recherche intelligente avec synthèse IA et données en temps réel</p>
        </div>

        <div className="mb-6">
          <SearchBar onSearch={handleAISearch} loading={loading} placeholder="Posez votre question..." />
        </div>

        {loading && (
          <div className="text-center py-12">
            <div className="w-12 h-12 border-4 border-cyan-500 border-t-transparent rounded-full animate-spin mx-auto mb-4"></div>
            <p className="text-dark-400">Analyse IA en cours...</p>
          </div>
        )}

        {results && (
          <div className="space-y-6">
            {results.ai_synthesis && (
              <AISummary summary={results.ai_synthesis} />
            )}
            {results.data && (
              <SearchResults results={results.data} query={query} />
            )}
          </div>
        )}

        {!results && !loading && (
          <div className="text-center py-12 text-dark-400">
            <p>Posez une question pour obtenir une réponse intelligente</p>
          </div>
        )}
      </div>
    </MainLayout>
  )
}




import { useState } from 'react'
import MainLayout from '@/components/layouts/MainLayout'
import SearchBar from '@/components/search/SearchBar'
import AISummary from '@/components/search/AISummary'
import SearchResults from '@/components/search/SearchResults'

export default function AISearchPage() {
  const [query, setQuery] = useState('')
  const [results, setResults] = useState<any>(null)
  const [loading, setLoading] = useState(false)

  const handleAISearch = async (searchQuery: string) => {
    setQuery(searchQuery)
    setLoading(true)
    try {
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL || ''}/api/ai-search/search`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ query: searchQuery }),
      })
      const data = await response.json()
      setResults(data)
    } catch (error) {
      // Logger silencieux en production
      if (process.env.NODE_ENV === 'development') {
        console.error('AI Search error:', error);
      }
    } finally {
      setLoading(false)
    }
  }

  return (
    <MainLayout>
      <div className="max-w-7xl mx-auto px-6 py-8">
        <div className="mb-8">
          <h1 className="text-4xl font-bold mb-4 gradient-text">Recherche IA</h1>
          <p className="text-dark-400">Recherche intelligente avec synthèse IA et données en temps réel</p>
        </div>

        <div className="mb-6">
          <SearchBar onSearch={handleAISearch} loading={loading} placeholder="Posez votre question..." />
        </div>

        {loading && (
          <div className="text-center py-12">
            <div className="w-12 h-12 border-4 border-cyan-500 border-t-transparent rounded-full animate-spin mx-auto mb-4"></div>
            <p className="text-dark-400">Analyse IA en cours...</p>
          </div>
        )}

        {results && (
          <div className="space-y-6">
            {results.ai_synthesis && (
              <AISummary summary={results.ai_synthesis} />
            )}
            {results.data && (
              <SearchResults results={results.data} query={query} />
            )}
          </div>
        )}

        {!results && !loading && (
          <div className="text-center py-12 text-dark-400">
            <p>Posez une question pour obtenir une réponse intelligente</p>
          </div>
        )}
      </div>
    </MainLayout>
  )
}



