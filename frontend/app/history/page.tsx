'use client'

import { useState, useEffect } from 'react'
import MainLayout from '@/components/layouts/MainLayout'
import { Clock, Search, Sparkles, MessageSquare, Trash2 } from 'lucide-react'

interface HistoryItem {
  id: string
  query: string
  type: 'search' | 'ai-search' | 'chat'
  timestamp: string
  results?: any
}

export default function HistoryPage() {
  const [history, setHistory] = useState<HistoryItem[]>([])
  const [filter, setFilter] = useState<'all' | 'search' | 'ai-search' | 'chat'>('all')

  useEffect(() => {
    // TODO: Load history from API or localStorage
    const stored = localStorage.getItem('wikiask-history')
    if (stored) {
      setHistory(JSON.parse(stored))
    }
  }, [])

  const filteredHistory = history.filter(item => 
    filter === 'all' || item.type === filter
  )

  const getIcon = (type: string) => {
    switch (type) {
      case 'search': return Search
      case 'ai-search': return Sparkles
      case 'chat': return MessageSquare
      default: return Clock
    }
  }

  const formatDate = (timestamp: string) => {
    const date = new Date(timestamp)
    const now = new Date()
    const diff = now.getTime() - date.getTime()
    const hours = Math.floor(diff / (1000 * 60 * 60))
    
    if (hours < 1) return 'Il y a moins d\'une heure'
    if (hours < 24) return `Il y a ${hours} heure${hours > 1 ? 's' : ''}`
    return date.toLocaleDateString('fr-FR')
  }

  return (
    <MainLayout>
      <div className="max-w-7xl mx-auto px-6 py-8">
        <div className="mb-8 flex items-center justify-between">
          <div>
            <h1 className="text-4xl font-bold mb-4 gradient-text">Historique</h1>
            <p className="text-dark-400">Toutes vos recherches et conversations</p>
          </div>
          <button className="btn-secondary flex items-center gap-2">
            <Trash2 className="w-4 h-4" />
            Effacer tout
          </button>
        </div>

        <div className="flex gap-4 mb-6">
          {(['all', 'search', 'ai-search', 'chat'] as const).map((f) => (
            <button
              key={f}
              onClick={() => setFilter(f)}
              className={`px-4 py-2 rounded-lg transition ${
                filter === f
                  ? 'bg-indigo-600 text-white'
                  : 'glass text-dark-300 hover:text-white'
              }`}
            >
              {f === 'all' ? 'Tout' : f === 'ai-search' ? 'IA Search' : f.charAt(0).toUpperCase() + f.slice(1)}
            </button>
          ))}
        </div>

        <div className="space-y-4">
          {filteredHistory.length === 0 ? (
            <div className="text-center py-12 text-dark-400">
              <Clock className="w-16 h-16 mx-auto mb-4 opacity-50" />
              <p>Aucun historique pour le moment</p>
            </div>
          ) : (
            filteredHistory.map((item) => {
              const Icon = getIcon(item.type)
              return (
                <div key={item.id} className="card card-hover">
                  <div className="flex items-start justify-between">
                    <div className="flex items-start gap-4 flex-1">
                      <div className="w-10 h-10 rounded-lg bg-dark-800 flex items-center justify-center">
                        <Icon className="w-5 h-5 text-indigo-400" />
                      </div>
                      <div className="flex-1">
                        <p className="text-white mb-1">{item.query}</p>
                        <p className="text-sm text-dark-400">{formatDate(item.timestamp)}</p>
                      </div>
                    </div>
                    <button className="text-dark-400 hover:text-white transition">
                      <Trash2 className="w-4 h-4" />
                    </button>
                  </div>
                </div>
              )
            })
          )}
        </div>
      </div>
    </MainLayout>
  )
}

