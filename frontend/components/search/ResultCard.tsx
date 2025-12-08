'use client'

import { ExternalLink, Star, Share2 } from 'lucide-react'

interface ResultCardProps {
  result: any
  type: 'ai' | 'web' | 'api'
}

export default function ResultCard({ result, type }: ResultCardProps) {
  const getTypeColor = () => {
    switch (type) {
      case 'ai': return 'border-indigo-500/50'
      case 'web': return 'border-blue-500/50'
      case 'api': return 'border-purple-500/50'
    }
  }

  return (
    <div className={`card border-l-4 ${getTypeColor()}`}>
      <div className="flex items-start justify-between mb-2">
        <div className="flex-1">
          {result.title && (
            <h4 className="font-semibold text-white mb-1">{result.title}</h4>
          )}
          {result.url && (
            <a
              href={result.url}
              target="_blank"
              rel="noopener noreferrer"
              className="text-sm text-indigo-400 hover:text-indigo-300 flex items-center gap-1 mb-2"
            >
              {result.url}
              <ExternalLink className="w-3 h-3" />
            </a>
          )}
          {result.content && (
            <p className="text-sm text-dark-300 line-clamp-3">{result.content}</p>
          )}
          {result.data && (
            <pre className="text-xs text-dark-400 mt-2 overflow-x-auto">
              {JSON.stringify(result.data, null, 2).substring(0, 200)}...
            </pre>
          )}
        </div>
      </div>

      <div className="flex items-center gap-3 mt-3 pt-3 border-t border-dark-700/50">
        {result.source && (
          <span className="text-xs text-dark-400">Source: {result.source}</span>
        )}
        <div className="flex items-center gap-2 ml-auto">
          <button className="text-dark-400 hover:text-yellow-400 transition">
            <Star className="w-4 h-4" />
          </button>
          <button className="text-dark-400 hover:text-white transition">
            <Share2 className="w-4 h-4" />
          </button>
        </div>
      </div>
    </div>
  )
}





