'use client'

import { useState } from 'react'
import { Zap, CheckCircle, XCircle, TestTube } from 'lucide-react'
import APITester from './APITester'

interface APICardProps {
  api: {
    id: string
    name: string
    quota: string
    status: 'active' | 'inactive'
  }
}

export default function APICard({ api }: APICardProps) {
  const [showTester, setShowTester] = useState(false)

  return (
    <div className="card card-hover">
      <div className="flex items-start justify-between mb-3">
        <div className="flex-1">
          <h3 className="font-semibold text-white mb-1">{api.name}</h3>
          <p className="text-sm text-dark-400">Quota: {api.quota}</p>
        </div>
        {api.status === 'active' ? (
          <CheckCircle className="w-5 h-5 text-green-400" />
        ) : (
          <XCircle className="w-5 h-5 text-red-400" />
        )}
      </div>

      <div className="flex items-center gap-2">
        <button
          onClick={() => setShowTester(!showTester)}
          className="flex-1 btn-secondary flex items-center justify-center gap-2 text-sm"
        >
          <TestTube className="w-4 h-4" />
          Tester
        </button>
        <button className="px-3 py-2 glass rounded-lg hover:glass-hover transition">
          <Zap className="w-4 h-4 text-indigo-400" />
        </button>
      </div>

      {showTester && (
        <div className="mt-4 pt-4 border-t border-dark-700/50">
          <APITester apiId={api.id} />
        </div>
      )}
    </div>
  )
}





