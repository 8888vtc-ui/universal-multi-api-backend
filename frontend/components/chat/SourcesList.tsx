'use client'

import { ExternalLink } from 'lucide-react'

interface SourcesListProps {
  sources: any[]
}

export default function SourcesList({ sources }: SourcesListProps) {
  if (!sources || sources.length === 0) return null

  return (
    <div className="mt-2 ml-11">
      <p className="text-xs text-dark-400 mb-2">Sources:</p>
      <div className="flex flex-wrap gap-2">
        {sources.map((source, i) => (
          <a
            key={i}
            href={source.url || source}
            target="_blank"
            rel="noopener noreferrer"
            className="text-xs text-indigo-400 hover:text-indigo-300 flex items-center gap-1 px-2 py-1 rounded glass"
          >
            {typeof source === 'string' ? source : source.title || source.url}
            <ExternalLink className="w-3 h-3" />
          </a>
        ))}
      </div>
    </div>
  )
}





