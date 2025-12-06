'use client'

import { useState } from 'react'
import MainLayout from '@/components/layouts/MainLayout'
import APICategory from '@/components/explore/APICategory'
import { Bot, DollarSign, Newspaper, Globe, BookOpen, Laugh, Wrench } from 'lucide-react'

const API_CATEGORIES = [
  {
    id: 'ai',
    name: 'AI & LLM',
    icon: Bot,
    color: 'from-purple-500 to-pink-500',
    count: 10,
  },
  {
    id: 'finance',
    name: 'Finance',
    icon: DollarSign,
    color: 'from-emerald-500 to-teal-500',
    count: 5,
  },
  {
    id: 'news',
    name: 'News & Media',
    icon: Newspaper,
    color: 'from-blue-500 to-cyan-500',
    count: 6,
  },
  {
    id: 'geo',
    name: 'Géolocalisation',
    icon: Globe,
    color: 'from-green-500 to-emerald-500',
    count: 6,
  },
  {
    id: 'knowledge',
    name: 'Connaissance',
    icon: BookOpen,
    color: 'from-indigo-500 to-purple-500',
    count: 6,
  },
  {
    id: 'entertainment',
    name: 'Divertissement',
    icon: Laugh,
    color: 'from-yellow-500 to-orange-500',
    count: 8,
  },
  {
    id: 'utilities',
    name: 'Utilitaires',
    icon: Wrench,
    color: 'from-gray-500 to-slate-500',
    count: 10,
  },
]

export default function ExplorePage() {
  const [selectedCategory, setSelectedCategory] = useState<string | null>(null)

  return (
    <MainLayout>
      <div className="max-w-7xl mx-auto px-6 py-8">
        <div className="mb-8">
          <h1 className="text-4xl font-bold mb-4 gradient-text">Explorer 78+ APIs</h1>
          <p className="text-dark-400">Découvrez et testez toutes les APIs disponibles</p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mb-8">
          {API_CATEGORIES.map((category) => (
            <button
              key={category.id}
              onClick={() => setSelectedCategory(category.id)}
              className={`card card-hover text-left ${
                selectedCategory === category.id ? 'ring-2 ring-indigo-500' : ''
              }`}
            >
              <div className={`w-12 h-12 rounded-xl bg-gradient-to-r ${category.color} flex items-center justify-center mb-3`}>
                <category.icon className="w-6 h-6 text-white" />
              </div>
              <h3 className="font-semibold text-white mb-1">{category.name}</h3>
              <p className="text-sm text-dark-400">{category.count} APIs</p>
            </button>
          ))}
        </div>

        {selectedCategory && (
          <APICategory categoryId={selectedCategory} />
        )}

        {!selectedCategory && (
          <div className="text-center py-12 text-dark-400">
            <p>Sélectionnez une catégorie pour voir les APIs disponibles</p>
          </div>
        )}
      </div>
    </MainLayout>
  )
}

