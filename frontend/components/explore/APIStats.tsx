'use client'

import { Activity, TrendingUp, Clock } from 'lucide-react'

interface APIStatsProps {
  apiId: string
  stats?: {
    requests: number
    successRate: number
    avgResponseTime: number
  }
}

export default function APIStats({ apiId, stats }: APIStatsProps) {
  if (!stats) {
    return (
      <div className="card">
        <p className="text-dark-400 text-sm">Aucune statistique disponible</p>
      </div>
    )
  }

  return (
    <div className="card">
      <h4 className="font-semibold text-white mb-4">Statistiques</h4>
      <div className="space-y-3">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-2">
            <Activity className="w-4 h-4 text-indigo-400" />
            <span className="text-sm text-dark-300">Requêtes</span>
          </div>
          <span className="text-white font-semibold">{stats.requests}</span>
        </div>
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-2">
            <TrendingUp className="w-4 h-4 text-green-400" />
            <span className="text-sm text-dark-300">Taux de succès</span>
          </div>
          <span className="text-white font-semibold">{stats.successRate}%</span>
        </div>
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-2">
            <Clock className="w-4 h-4 text-blue-400" />
            <span className="text-sm text-dark-300">Temps moyen</span>
          </div>
          <span className="text-white font-semibold">{stats.avgResponseTime}ms</span>
        </div>
      </div>
    </div>
  )
}





