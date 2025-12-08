'use client'

import { useState, useEffect } from 'react'
import APICard from './APICard'

interface APICategoryProps {
  categoryId: string
}

const API_MAP: Record<string, any[]> = {
  ai: [
    { id: 'groq', name: 'Groq', quota: '14,000/jour', status: 'active' },
    { id: 'mistral', name: 'Mistral', quota: '100,000/jour', status: 'active' },
    { id: 'anthropic', name: 'Anthropic', quota: '1,000/jour', status: 'active' },
    { id: 'gemini', name: 'Gemini', quota: '1,500/jour', status: 'active' },
  ],
  finance: [
    { id: 'coingecko', name: 'CoinGecko', quota: '10,000/mois', status: 'active' },
    { id: 'coincap', name: 'CoinCap', quota: 'Illimité', status: 'active' },
  ],
  news: [
    { id: 'newsapi', name: 'NewsAPI', quota: '100/jour', status: 'active' },
    { id: 'omdb', name: 'OMDB', quota: '1,000/jour', status: 'active' },
  ],
}

export default function APICategory({ categoryId }: APICategoryProps) {
  const [apis, setApis] = useState<any[]>([])

  useEffect(() => {
    // TODO: Fetch from API
    setApis(API_MAP[categoryId] || [])
  }, [categoryId])

  return (
    <div>
      <h2 className="text-2xl font-bold mb-6">APIs {categoryId}</h2>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {apis.map((api) => (
          <APICard key={api.id} api={api} />
        ))}
      </div>
    </div>
  )
}





