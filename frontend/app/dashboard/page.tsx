'use client'

import MainLayout from '@/components/layouts/MainLayout'
import StatsWidget from '@/components/ui/StatsWidget'
import { Activity, Database, Zap, TrendingUp } from 'lucide-react'

export default function DashboardPage() {
  return (
    <MainLayout showSidebar={true}>
      <div className="max-w-7xl mx-auto px-6 py-8">
        <div className="mb-8">
          <h1 className="text-4xl font-bold mb-4 gradient-text">Dashboard</h1>
          <p className="text-dark-400">Vue d'ensemble de votre utilisation</p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          <StatsWidget
            title="Requêtes aujourd'hui"
            value="45"
            max={500}
            icon={Activity}
            color="indigo"
          />
          <StatsWidget
            title="Quota restant"
            value="91%"
            icon={Database}
            color="green"
          />
          <StatsWidget
            title="APIs utilisées"
            value="12"
            icon={Zap}
            color="purple"
          />
          <StatsWidget
            title="Temps moyen"
            value="1.2s"
            icon={TrendingUp}
            color="blue"
          />
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          <div className="card">
            <h3 className="text-xl font-semibold mb-4">Activité récente</h3>
            <div className="space-y-3">
              <div className="flex items-center justify-between p-3 bg-dark-800/50 rounded-lg">
                <span className="text-dark-300">Recherche: "Bitcoin"</span>
                <span className="text-xs text-dark-400">Il y a 5 min</span>
              </div>
              <div className="flex items-center justify-between p-3 bg-dark-800/50 rounded-lg">
                <span className="text-dark-300">Chat: "Météo Paris"</span>
                <span className="text-xs text-dark-400">Il y a 12 min</span>
              </div>
            </div>
          </div>

          <div className="card">
            <h3 className="text-xl font-semibold mb-4">APIs les plus utilisées</h3>
            <div className="space-y-3">
              <div className="flex items-center justify-between">
                <span className="text-dark-300">CoinGecko</span>
                <span className="text-indigo-400 font-semibold">23</span>
              </div>
              <div className="flex items-center justify-between">
                <span className="text-dark-300">Wikipedia</span>
                <span className="text-indigo-400 font-semibold">15</span>
              </div>
              <div className="flex items-center justify-between">
                <span className="text-dark-300">Groq AI</span>
                <span className="text-indigo-400 font-semibold">12</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </MainLayout>
  )
}





