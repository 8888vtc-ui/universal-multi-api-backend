'use client'

import { useState, useEffect } from 'react'
import Link from 'next/link'
import MainLayout from '@/components/layouts/MainLayout'
import SearchBar from '@/components/search/SearchBar'
import BottomNav from '@/components/navigation/BottomNav'
import {
  Sparkles, Search, MessageSquare, Globe,
  Zap, Database, Shield, Activity, Bot, TrendingUp, Target
} from 'lucide-react'
import { apiClient } from '@/lib/api'

export default function Home() {
  const [health, setHealth] = useState<any>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetchHealth()
  }, [])

  const fetchHealth = async () => {
    try {
      const data = await apiClient.health()
      setHealth(data)
    } catch (error) {
      console.error('Error fetching health:', error)
    } finally {
      setLoading(false)
    }
  }

  const handleSearch = (query: string) => {
    // Redirect to search page
    window.location.href = `/search?q=${encodeURIComponent(query)}`
  }

  return (
    <MainLayout>
      {/* Hero Section */}
      <section className="relative overflow-hidden py-20 lg:py-32">
        {/* Background Effects */}
        <div className="absolute inset-0 bg-[url('/grid.svg')] bg-center [mask-image:linear-gradient(180deg,white,rgba(255,255,255,0))]"></div>
        <div className="absolute inset-0 bg-gradient-to-b from-cyan-500/10 via-transparent to-transparent opacity-40"></div>

        <div className="max-w-7xl mx-auto px-6 relative z-10">
          <div className="text-center mb-16">
            <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full glass mb-8 border border-cyan-500/30">
              <span className="relative flex h-3 w-3">
                <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-cyan-400 opacity-75"></span>
                <span className="relative inline-flex rounded-full h-3 w-3 bg-cyan-500"></span>
              </span>
              <span className="text-cyan-300 text-sm font-medium tracking-wide uppercase">Système Opérationnel</span>
            </div>

            <h1 className="text-6xl md:text-7xl font-bold mb-8 tracking-tight">
              <span className="gradient-text">WikiAsk</span>
            </h1>

            <p className="text-3xl md:text-4xl font-light text-white mb-6">
              Outil de Recherche <span className="font-semibold text-cyan-400">Optimal Multichannel</span>
            </p>

            <p className="text-lg md:text-xl text-slate-400 max-w-2xl mx-auto leading-relaxed">
              Accédez à l'information avec une <span className="text-white font-medium">précision digne d'un sniper</span>.
              Agrégation intelligente de sources multiples pour des résultats instantanés et vérifiés.
            </p>
          </div>

          {/* Main Search Bar */}
          <div className="max-w-3xl mx-auto mb-16 relative group">
            <div className="absolute -inset-1 bg-gradient-to-r from-cyan-500 to-blue-600 rounded-2xl blur opacity-25 group-hover:opacity-50 transition duration-1000 group-hover:duration-200"></div>
            <div className="relative">
              <SearchBar onSearch={handleSearch} />
            </div>
          </div>

          {/* Quick Actions */}
          <div className="flex flex-wrap justify-center gap-4 mb-16">
            <Link href="/ai-search" className="flex items-center gap-3 px-8 py-4 rounded-xl glass hover:glass-hover transition group border border-slate-700/50">
              <Target className="w-5 h-5 text-cyan-400 group-hover:text-cyan-300 transition-colors" />
              <span className="text-slate-200 group-hover:text-white font-medium">Recherche Précise</span>
            </Link>
            <Link href="/chat" className="flex items-center gap-3 px-8 py-4 rounded-xl glass hover:glass-hover transition group border border-slate-700/50">
              <MessageSquare className="w-5 h-5 text-blue-400 group-hover:text-blue-300 transition-colors" />
              <span className="text-slate-200 group-hover:text-white font-medium">Chat Assistant</span>
            </Link>
            <Link href="/explore" className="flex items-center gap-3 px-8 py-4 rounded-xl glass hover:glass-hover transition group border border-slate-700/50">
              <Globe className="w-5 h-5 text-indigo-400 group-hover:text-indigo-300 transition-colors" />
              <span className="text-slate-200 group-hover:text-white font-medium">Explorer</span>
            </Link>
          </div>

          {/* Stats */}
          <div className="grid grid-cols-2 md:grid-cols-4 gap-6 max-w-4xl mx-auto">
            {[
              { label: 'Sources Connectées', value: '78+', icon: Database, color: 'text-cyan-400' },
              { label: 'Modèles Intelligents', value: health?.ai_providers ? Object.keys(health.ai_providers).length : '10', icon: Bot, color: 'text-blue-400' },
              { label: 'Requêtes / Jour', value: '200K+', icon: Activity, color: 'text-indigo-400' },
              { label: 'Fiabilité', value: '99.9%', icon: Shield, color: 'text-emerald-400' },
            ].map((stat, i) => (
              <div key={i} className="card text-center group hover:border-cyan-500/30 transition-colors">
                <stat.icon className={`w-8 h-8 mx-auto mb-3 ${stat.color} group-hover:scale-110 transition-transform duration-300`} />
                <div className="text-3xl font-bold text-white mb-1">{stat.value}</div>
                <div className="text-xs font-medium text-slate-400 uppercase tracking-wider">{stat.label}</div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="py-20 relative">
        <div className="absolute inset-0 bg-slate-900/50 skew-y-3 transform origin-bottom-left -z-10"></div>
        <div className="max-w-7xl mx-auto px-6">
          <h2 className="text-4xl font-bold text-center mb-16">
            <span className="gradient-text">Puissance Multichannel</span>
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            <div className="card group hover:bg-slate-800/50">
              <div className="w-14 h-14 rounded-2xl bg-cyan-500/10 flex items-center justify-center mb-6 group-hover:bg-cyan-500/20 transition-colors">
                <Target className="w-8 h-8 text-cyan-400" />
              </div>
              <h3 className="text-xl font-bold text-white mb-3">Précision Chirurgicale</h3>
              <p className="text-slate-400 leading-relaxed">
                Notre algorithme cible l'information pertinente parmi des millions de données pour une réponse exacte et immédiate.
              </p>
            </div>
            <div className="card group hover:bg-slate-800/50">
              <div className="w-14 h-14 rounded-2xl bg-blue-500/10 flex items-center justify-center mb-6 group-hover:bg-blue-500/20 transition-colors">
                <MessageSquare className="w-8 h-8 text-blue-400" />
              </div>
              <h3 className="text-xl font-bold text-white mb-3">Intelligence Fusionnée</h3>
              <p className="text-slate-400 leading-relaxed">
                Combinaison de 10 modèles d'intelligence artificielle pour une compréhension contextuelle supérieure.
              </p>
            </div>
            <div className="card group hover:bg-slate-800/50">
              <div className="w-14 h-14 rounded-2xl bg-indigo-500/10 flex items-center justify-center mb-6 group-hover:bg-indigo-500/20 transition-colors">
                <Globe className="w-8 h-8 text-indigo-400" />
              </div>
              <h3 className="text-xl font-bold text-white mb-3">Couverture Globale</h3>
              <p className="text-slate-400 leading-relaxed">
                Accès unifié à la finance, l'actualité, la littérature et bien plus, via une interface unique et fluide.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* Bottom Navigation for Mobile */}
      <BottomNav />
    </MainLayout>
  )
}
