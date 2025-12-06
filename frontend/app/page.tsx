'use client'

import Link from 'next/link'
import {
  Sparkles, Heart, TrendingUp, Plane, BookOpen, ChevronRight, MessageCircle,
  Utensils, Monitor, Film, Cloud, HeartHandshake, Gamepad2
} from 'lucide-react'

// Expert data matching backend expert_config.py - 12 experts
const EXPERTS = [
  // Row 1 - Original experts (renamed for legal)
  {
    id: 'health',
    name: 'Recherche Santé',
    emoji: '🔬',
    tagline: 'Moteur de recherche santé',
    description: 'Informations de santé issues de sources fiables.',
    color: 'from-emerald-400 to-teal-500',
    bgColor: 'bg-emerald-50',
    borderColor: 'border-emerald-200',
    textColor: 'text-emerald-700',
  },
  {
    id: 'sports',
    name: 'Coach Alex',
    emoji: '⚽',
    tagline: 'Sport et fitness',
    description: 'Actualités sportives et conseils fitness.',
    color: 'from-orange-400 to-amber-500',
    bgColor: 'bg-orange-50',
    borderColor: 'border-orange-200',
    textColor: 'text-orange-700',
  },
  {
    id: 'finance',
    name: 'Guide Finance',
    emoji: '📊',
    tagline: 'Infos financières',
    description: 'Marchés, cryptos et économie.',
    color: 'from-blue-400 to-indigo-500',
    bgColor: 'bg-blue-50',
    borderColor: 'border-blue-200',
    textColor: 'text-blue-700',
  },
  {
    id: 'tourism',
    name: 'Léa Voyage',
    emoji: '✈️',
    tagline: 'Guide de voyage',
    description: 'Destinations et conseils voyage.',
    color: 'from-pink-400 to-rose-500',
    bgColor: 'bg-pink-50',
    borderColor: 'border-pink-200',
    textColor: 'text-pink-700',
  },
  {
    id: 'general',
    name: 'Wiki',
    emoji: '📚',
    tagline: 'Culture générale',
    description: 'Votre encyclopédie vivante.',
    color: 'from-violet-400 to-purple-500',
    bgColor: 'bg-violet-50',
    borderColor: 'border-violet-200',
    textColor: 'text-violet-700',
  },
  {
    id: 'humor',
    name: 'Ricky Rire',
    emoji: '😂',
    tagline: 'Humour et détente',
    description: 'Blagues et bonne humeur !',
    color: 'from-yellow-400 to-amber-500',
    bgColor: 'bg-yellow-50',
    borderColor: 'border-yellow-200',
    textColor: 'text-yellow-700',
  },
  // Row 2 - New traffic-driving experts
  {
    id: 'cuisine',
    name: 'Chef Gourmand',
    emoji: '🍳',
    tagline: 'Recettes et cuisine',
    description: 'Recettes et astuces gourmandes.',
    color: 'from-red-400 to-rose-500',
    bgColor: 'bg-red-50',
    borderColor: 'border-red-200',
    textColor: 'text-red-700',
  },
  {
    id: 'tech',
    name: 'Tech Insider',
    emoji: '💻',
    tagline: 'Actualités tech',
    description: 'IA, gadgets et innovations.',
    color: 'from-indigo-400 to-violet-500',
    bgColor: 'bg-indigo-50',
    borderColor: 'border-indigo-200',
    textColor: 'text-indigo-700',
  },
  {
    id: 'cinema',
    name: 'Ciné Fan',
    emoji: '🎬',
    tagline: 'Films et séries',
    description: 'Critiques et recommandations.',
    color: 'from-rose-500 to-red-600',
    bgColor: 'bg-rose-50',
    borderColor: 'border-rose-200',
    textColor: 'text-rose-700',
  },
  {
    id: 'weather',
    name: 'Météo Pro',
    emoji: '☀️',
    tagline: 'Prévisions météo',
    description: 'Météo détaillée partout.',
    color: 'from-sky-400 to-blue-500',
    bgColor: 'bg-sky-50',
    borderColor: 'border-sky-200',
    textColor: 'text-sky-700',
  },
  {
    id: 'love',
    name: 'Love Coach',
    emoji: '💕',
    tagline: 'Conseils relationnels',
    description: 'Conseils bienveillants.',
    color: 'from-pink-500 to-rose-600',
    bgColor: 'bg-pink-50',
    borderColor: 'border-pink-300',
    textColor: 'text-pink-700',
  },
  {
    id: 'gaming',
    name: 'Gamer Zone',
    emoji: '🎮',
    tagline: 'Jeux vidéo',
    description: 'Gaming et esports.',
    color: 'from-green-400 to-emerald-500',
    bgColor: 'bg-green-50',
    borderColor: 'border-green-200',
    textColor: 'text-green-700',
  },
  // New: Real-time news
  {
    id: 'news',
    name: 'Actu Live',
    emoji: '📰',
    tagline: 'Actualités temps réel',
    description: 'Infos monde en direct.',
    color: 'from-slate-500 to-zinc-600',
    bgColor: 'bg-slate-50',
    borderColor: 'border-slate-200',
    textColor: 'text-slate-700',
  },
  {
    id: 'horoscope',
    name: 'Étoile',
    emoji: '🔮',
    tagline: 'Astrologie',
    description: 'Horoscope quotidien.',
    color: 'from-purple-500 to-violet-600',
    bgColor: 'bg-purple-50',
    borderColor: 'border-purple-200',
    textColor: 'text-purple-700',
  },
  {
    id: 'prenom',
    name: 'Prénom Expert',
    emoji: '👶',
    tagline: 'Signification prénoms',
    description: 'Origine des prénoms.',
    color: 'from-pink-500 to-rose-600',
    bgColor: 'bg-pink-50',
    borderColor: 'border-pink-200',
    textColor: 'text-pink-700',
  },
  {
    id: 'history',
    name: 'Ce Jour',
    emoji: '📅',
    tagline: 'Histoire du jour',
    description: 'Ce jour dans l\'histoire.',
    color: 'from-amber-600 to-orange-700',
    bgColor: 'bg-amber-50',
    borderColor: 'border-amber-200',
    textColor: 'text-amber-700',
  },
]

export default function Home() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-amber-50 via-white to-rose-50">
      {/* Navigation */}
      <nav className="bg-white/80 backdrop-blur-md border-b border-amber-100 sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-amber-400 to-orange-500 flex items-center justify-center">
                <Sparkles className="w-6 h-6 text-white" />
              </div>
              <span className="text-2xl font-bold bg-gradient-to-r from-amber-600 to-orange-600 bg-clip-text text-transparent">
                WikiAsk
              </span>
            </div>
            <div className="hidden md:flex items-center gap-6">
              <Link href="/about" className="text-gray-600 hover:text-amber-600 transition">À propos</Link>
              <Link
                href="/chat"
                className="px-4 py-2 bg-gradient-to-r from-amber-500 to-orange-500 text-white rounded-full font-medium hover:shadow-lg hover:shadow-amber-200 transition"
              >
                Chat Libre
              </Link>
            </div>
          </div>
        </div>
      </nav>

      {/* Hero Section */}
      <section className="pt-12 pb-8 px-4 sm:px-6 lg:px-8">
        <div className="max-w-4xl mx-auto text-center">
          <h1 className="text-4xl sm:text-5xl font-bold text-gray-900 mb-4 leading-tight">
            Discutez avec nos
            <span className="block bg-gradient-to-r from-amber-500 via-orange-500 to-rose-500 bg-clip-text text-transparent">
              Experts Intelligents
            </span>
          </h1>

          <p className="text-lg text-gray-600 max-w-2xl mx-auto mb-4">
            Chaque expert a sa personnalité et ses connaissances spécialisées.
          </p>

          {/* Slogan */}
          <div className="flex flex-col sm:flex-row items-center justify-center gap-2 mb-8">
            <span className="text-sm font-medium text-amber-700 bg-amber-100 px-3 py-1 rounded-full">
              🇫🇷 Pensez. Discutez. Maîtrisez.
            </span>
            <span className="text-sm font-medium text-gray-600 bg-gray-100 px-3 py-1 rounded-full">
              🇬🇧 Think. Chat. Master.
            </span>
          </div>
          <p className="text-xs text-gray-500">
            Données humaines + Précision IA
          </p>
        </div>
      </section>

      {/* Expert Cards Grid - 12 experts */}
      <section className="pb-16 px-4 sm:px-6 lg:px-8">
        <div className="max-w-7xl mx-auto">
          <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-4 xl:grid-cols-6 gap-4">
            {EXPERTS.map((expert) => (
              <Link
                key={expert.id}
                href={`/expert/${expert.id}`}
                className={`group relative overflow-hidden rounded-2xl ${expert.bgColor} ${expert.borderColor} border-2 p-4 hover:shadow-xl transition-all duration-300 hover:-translate-y-1`}
              >
                {/* Avatar */}
                <div className={`w-14 h-14 rounded-xl bg-gradient-to-br ${expert.color} flex items-center justify-center text-2xl shadow-lg mb-3 mx-auto`}>
                  {expert.emoji}
                </div>

                {/* Content */}
                <h3 className={`text-sm font-bold ${expert.textColor} text-center mb-1`}>
                  {expert.name}
                </h3>
                <p className="text-xs text-gray-500 text-center line-clamp-2">
                  {expert.description}
                </p>

                {/* Hover arrow */}
                <div className="absolute top-2 right-2 opacity-0 group-hover:opacity-100 transition-opacity">
                  <ChevronRight className={`w-4 h-4 ${expert.textColor}`} />
                </div>
              </Link>
            ))}
          </div>
        </div>
      </section>

      {/* Trust Section */}
      <section className="py-12 bg-white/50 backdrop-blur-sm border-t border-amber-100">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <h2 className="text-xl font-bold text-gray-900 mb-6">
            Pourquoi WikiAsk ?
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div className="p-4">
              <div className="text-3xl mb-2">🎯</div>
              <h3 className="font-semibold text-gray-900 mb-1">Spécialisés</h3>
              <p className="text-gray-600 text-sm">Chaque expert maîtrise son domaine.</p>
            </div>
            <div className="p-4">
              <div className="text-3xl mb-2">💬</div>
              <h3 className="font-semibold text-gray-900 mb-1">Naturels</h3>
              <p className="text-gray-600 text-sm">Des réponses humaines et personnalisées.</p>
            </div>
            <div className="p-4">
              <div className="text-3xl mb-2">⚡</div>
              <h3 className="font-semibold text-gray-900 mb-1">Rapides</h3>
              <p className="text-gray-600 text-sm">Réponses instantanées 24h/24.</p>
            </div>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="py-6 border-t border-amber-100 bg-white/30">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <p className="text-amber-700 font-medium text-sm mb-1">
            Pensez. Discutez. Maîtrisez. — Human Data, AI Precision
          </p>
          <p className="text-gray-400 text-xs">
            © 2024 WikiAsk
          </p>
        </div>
      </footer>
    </div>
  )
}
