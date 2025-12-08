'use client'

import { useState, KeyboardEvent } from 'react'
import { Search as SearchIcon, Mic, Sparkles } from 'lucide-react'

interface SearchBarProps {
  onSearch: (query: string) => void
  loading?: boolean
  placeholder?: string
  showVoiceButton?: boolean
  initialValue?: string
}

export default function SearchBar({
  onSearch,
  loading = false,
  placeholder = "Rechercher...",
  showVoiceButton = true,
  initialValue = ''
}: SearchBarProps) {
  const [query, setQuery] = useState(initialValue)
  const [suggestions, setSuggestions] = useState<string[]>([])
  const [showSuggestions, setShowSuggestions] = useState(false)

  const handleSubmit = () => {
    if (query.trim() && !loading) {
      onSearch(query.trim())
      setShowSuggestions(false)
    }
  }

  const handleKeyDown = (e: KeyboardEvent<HTMLInputElement>) => {
    if (e.key === 'Enter') {
      handleSubmit()
    }
  }

  // TODO: Implement auto-completion
  const handleInputChange = (value: string) => {
    setQuery(value)
    // Mock suggestions
    if (value.length > 2) {
      setSuggestions(['Bitcoin prix', 'Météo Paris', 'Blague Python'])
      setShowSuggestions(true)
    } else {
      setSuggestions([])
      setShowSuggestions(false)
    }
  }

  return (
    <div className="relative">
      <div className="flex items-center gap-3">
        <div className="flex-1 relative">
          <SearchIcon className="absolute left-4 top-1/2 transform -translate-y-1/2 w-5 h-5 text-dark-400" />
          <input
            type="text"
            value={query}
            onChange={(e) => handleInputChange(e.target.value)}
            onKeyDown={handleKeyDown}
            onFocus={() => suggestions.length > 0 && setShowSuggestions(true)}
            placeholder={placeholder}
            className="input-dark w-full pl-12 pr-12 py-4 text-lg"
            disabled={loading}
          />
          {showVoiceButton && (
            <button
              className="absolute right-4 top-1/2 transform -translate-y-1/2 text-dark-400 hover:text-white transition"
              title="Recherche vocale"
            >
              <Mic className="w-5 h-5" />
            </button>
          )}
        </div>
        <button
          onClick={handleSubmit}
          disabled={loading || !query.trim()}
          className="btn-primary flex items-center gap-2 px-8 py-4 disabled:opacity-50 disabled:cursor-not-allowed"
        >
          {loading ? (
            <div className="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin" />
          ) : (
            <>
              <Sparkles className="w-5 h-5" />
              Rechercher
            </>
          )}
        </button>
      </div>

      {showSuggestions && suggestions.length > 0 && (
        <div className="absolute top-full left-0 right-0 mt-2 glass rounded-xl p-2 z-50">
          {suggestions.map((suggestion, i) => (
            <button
              key={i}
              onClick={() => {
                setQuery(suggestion)
                setShowSuggestions(false)
                onSearch(suggestion)
              }}
              className="w-full text-left px-4 py-2 rounded-lg hover:bg-dark-800/50 transition text-dark-300 hover:text-white"
            >
              {suggestion}
            </button>
          ))}
        </div>
      )}
    </div>
  )
}





