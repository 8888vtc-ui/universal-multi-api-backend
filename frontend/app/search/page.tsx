'use client'

import { useState } from 'react'
import MainLayout from '@/components/layouts/MainLayout'
import SearchBar from '@/components/search/SearchBar'
import SearchResults from '@/components/search/SearchResults'
import SearchFilters from '@/components/search/SearchFilters'

export default function SearchPage() {
  const [query, setQuery] = useState('')
  const [results, setResults] = useState<any>(null)
  const [loading, setLoading] = useState(false)
  const [filters, setFilters] = useState({
    category: 'all',
    language: 'fr',
  })

  const handleSearch = async (searchQuery: string) => {
    setQuery(searchQuery)
    setLoading(true)
    try {
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL || ''}/api/search?q=${encodeURIComponent(searchQuery)}`)
      const data = await response.json()
      setResults(data)
    } catch (error) {
      // Logger silencieux en production
      if (process.env.NODE_ENV === 'development') {
        console.error('Search error:', error);
      }
    } finally {
      setLoading(false)
    }
  }

  return (
    <MainLayout>
      <div className="max-w-7xl mx-auto px-6 py-8">
        <div className="mb-8">
          <h1 className="text-4xl font-bold mb-4 gradient-text">Recherche</h1>
          <p className="text-slate-400">Recherchez dans 78+ sources intégrées</p>
        </div>

        <div className="mb-6">
          <SearchBar onSearch={handleSearch} loading={loading} />
        </div>

        <div className="flex gap-6">
          <aside className="w-64 hidden lg:block">
            <SearchFilters filters={filters} onFiltersChange={setFilters} />
          </aside>

          <main className="flex-1">
            {results && <SearchResults results={results} query={query} />}
            {!results && !loading && (
              <div className="text-center py-12 text-dark-400">
                <p>Entrez une recherche pour commencer</p>
              </div>
            )}
          </main>
        </div>
      </div>
    </MainLayout>
  )
}




import { useState } from 'react'
import MainLayout from '@/components/layouts/MainLayout'
import SearchBar from '@/components/search/SearchBar'
import SearchResults from '@/components/search/SearchResults'
import SearchFilters from '@/components/search/SearchFilters'

export default function SearchPage() {
  const [query, setQuery] = useState('')
  const [results, setResults] = useState<any>(null)
  const [loading, setLoading] = useState(false)
  const [filters, setFilters] = useState({
    category: 'all',
    language: 'fr',
  })

  const handleSearch = async (searchQuery: string) => {
    setQuery(searchQuery)
    setLoading(true)
    try {
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL || ''}/api/search?q=${encodeURIComponent(searchQuery)}`)
      const data = await response.json()
      setResults(data)
    } catch (error) {
      // Logger silencieux en production
      if (process.env.NODE_ENV === 'development') {
        console.error('Search error:', error);
      }
    } finally {
      setLoading(false)
    }
  }

  return (
    <MainLayout>
      <div className="max-w-7xl mx-auto px-6 py-8">
        <div className="mb-8">
          <h1 className="text-4xl font-bold mb-4 gradient-text">Recherche</h1>
          <p className="text-slate-400">Recherchez dans 78+ sources intégrées</p>
        </div>

        <div className="mb-6">
          <SearchBar onSearch={handleSearch} loading={loading} />
        </div>

        <div className="flex gap-6">
          <aside className="w-64 hidden lg:block">
            <SearchFilters filters={filters} onFiltersChange={setFilters} />
          </aside>

          <main className="flex-1">
            {results && <SearchResults results={results} query={query} />}
            {!results && !loading && (
              <div className="text-center py-12 text-dark-400">
                <p>Entrez une recherche pour commencer</p>
              </div>
            )}
          </main>
        </div>
      </div>
    </MainLayout>
  )
}



