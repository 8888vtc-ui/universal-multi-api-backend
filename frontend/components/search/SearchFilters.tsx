'use client'

import { Filter } from 'lucide-react'

interface SearchFiltersProps {
  filters: {
    category: string
    language: string
  }
  onFiltersChange: (filters: { category: string; language: string }) => void
}

const CATEGORIES = [
  { value: 'all', label: 'Toutes les sources' },
  { value: 'ai', label: 'Intelligence Artificielle' },
  { value: 'finance', label: 'Finance & Crypto' },
  { value: 'news', label: 'Actualités & Média' },
  { value: 'weather', label: 'Météo & Espace' },
  { value: 'geo', label: 'Géographie & Lieux' },
  { value: 'knowledge', label: 'Savoir & Culture' },
  { value: 'entertainment', label: 'Divertissement' },
  { value: 'health', label: 'Santé & Sport' },
  { value: 'utilities', label: 'Outils & Services' },
]

const LANGUAGES = [
  { value: 'fr', label: 'Français' },
  { value: 'en', label: 'English' },
  { value: 'es', label: 'Español' },
  { value: 'de', label: 'Deutsch' },
]

export default function SearchFilters({ filters, onFiltersChange }: SearchFiltersProps) {
  return (
    <div className="card">
      <div className="flex items-center gap-2 mb-4">
        <Filter className="w-5 h-5 text-cyan-400" />
        <h3 className="font-semibold text-white">Filtres</h3>
      </div>

      <div className="space-y-4">
        <div>
          <label className="block text-sm font-medium text-dark-300 mb-2">
            Catégorie
          </label>
          <select
            value={filters.category}
            onChange={(e) => onFiltersChange({ ...filters, category: e.target.value })}
            className="input-dark w-full"
          >
            {CATEGORIES.map((cat) => (
              <option key={cat.value} value={cat.value}>
                {cat.label}
              </option>
            ))}
          </select>
        </div>

        <div>
          <label className="block text-sm font-medium text-dark-300 mb-2">
            Langue
          </label>
          <select
            value={filters.language}
            onChange={(e) => onFiltersChange({ ...filters, language: e.target.value })}
            className="input-dark w-full"
          >
            {LANGUAGES.map((lang) => (
              <option key={lang.value} value={lang.value}>
                {lang.label}
              </option>
            ))}
          </select>
        </div>
      </div>
    </div>
  )
}





