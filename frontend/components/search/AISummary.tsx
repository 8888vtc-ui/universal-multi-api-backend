'use client'

import { Sparkles } from 'lucide-react'

interface AISummaryProps {
  summary: string
}

export default function AISummary({ summary }: AISummaryProps) {
  return (
    <div className="card border-2 border-indigo-500/50 bg-gradient-to-r from-indigo-500/10 to-purple-500/10">
      <div className="flex items-start gap-3">
        <div className="w-10 h-10 rounded-lg bg-gradient-to-r from-indigo-500 to-purple-500 flex items-center justify-center flex-shrink-0">
          <Sparkles className="w-5 h-5 text-white" />
        </div>
        <div className="flex-1">
          <h3 className="font-semibold text-white mb-2">Synthèse IA</h3>
          <p className="text-dark-200 leading-relaxed">{summary}</p>
        </div>
      </div>
    </div>
  )
}





