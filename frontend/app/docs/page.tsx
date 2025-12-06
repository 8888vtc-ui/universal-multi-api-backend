'use client'

import MainLayout from '@/components/layouts/MainLayout'
import { BookOpen, Code, Zap, Key } from 'lucide-react'

export default function DocsPage() {
  return (
    <MainLayout>
      <div className="max-w-7xl mx-auto px-6 py-8">
        <div className="mb-8">
          <h1 className="text-4xl font-bold mb-4 gradient-text">Documentation</h1>
          <p className="text-dark-400">Guide complet de l'API WikiAsk</p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          <div className="card card-hover">
            <BookOpen className="w-8 h-8 text-indigo-400 mb-4" />
            <h3 className="font-semibold text-white mb-2">Quick Start</h3>
            <p className="text-sm text-dark-400">Commencez en 5 minutes</p>
          </div>
          <div className="card card-hover">
            <Code className="w-8 h-8 text-indigo-400 mb-4" />
            <h3 className="font-semibold text-white mb-2">API Reference</h3>
            <p className="text-sm text-dark-400">Tous les endpoints</p>
          </div>
          <div className="card card-hover">
            <Zap className="w-8 h-8 text-indigo-400 mb-4" />
            <h3 className="font-semibold text-white mb-2">Examples</h3>
            <p className="text-sm text-dark-400">Exemples de code</p>
          </div>
          <div className="card card-hover">
            <Key className="w-8 h-8 text-indigo-400 mb-4" />
            <h3 className="font-semibold text-white mb-2">Authentication</h3>
            <p className="text-sm text-dark-400">Gestion des clés API</p>
          </div>
        </div>

        <div className="card">
          <h2 className="text-2xl font-bold mb-4">API Base URL</h2>
          <div className="bg-dark-800 rounded-lg p-4 mb-4">
            <code className="text-indigo-400">
              {process.env.NEXT_PUBLIC_API_URL || 'https://universal-api-hub.fly.dev'}
            </code>
          </div>
          <p className="text-dark-400 mb-6">
            Toutes les requêtes doivent être faites à cette URL de base.
          </p>

          <h3 className="text-xl font-semibold mb-4">Endpoints Principaux</h3>
          <div className="space-y-4">
            <div>
              <code className="text-indigo-400">POST /api/chat</code>
              <p className="text-dark-400 text-sm mt-1">Chat avec l'IA</p>
            </div>
            <div>
              <code className="text-indigo-400">POST /api/ai-search/search</code>
              <p className="text-dark-400 text-sm mt-1">Recherche IA intelligente</p>
            </div>
            <div>
              <code className="text-indigo-400">GET /api/explore</code>
              <p className="text-dark-400 text-sm mt-1">Liste toutes les APIs</p>
            </div>
          </div>
        </div>
      </div>
    </MainLayout>
  )
}

