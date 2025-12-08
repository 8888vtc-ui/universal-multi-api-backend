"use client";

import { useEffect, useState } from "react";
import Link from "next/link";

interface Expert {
  id: string;
  name: string;
  emoji: string;
  tagline: string;
  description: string;
  color: string;
}

interface CategoryData {
  category: {
    id: string;
    name: string;
    name_en: string;
    emoji: string;
    description: string;
    color: string;
  };
  experts: Expert[];
  count: number;
}

type GroupedExperts = Record<string, CategoryData>;

export default function ExplorePage() {
  const [grouped, setGrouped] = useState<GroupedExperts | null>(null);
  const [loading, setLoading] = useState(true);
  const [selectedCategory, setSelectedCategory] = useState<string | null>(null);

  useEffect(() => {
    fetch("/api/expert/grouped")
      .then((res) => res.json())
      .then((data) => {
        setGrouped(data);
        setLoading(false);
      })
      .catch((err) => {
        // Logger silencieux en production
        if (process.env.NODE_ENV === 'development') {
          console.error("Failed to load experts:", err);
        }
        setLoading(false);
      });
  }, []);

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-slate-950 via-purple-950 to-slate-950 flex items-center justify-center">
        <div className="text-white text-xl">Chargement des experts...</div>
      </div>
    );
  }

  if (!grouped) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-slate-950 via-purple-950 to-slate-950 flex items-center justify-center">
        <div className="text-white text-xl">Erreur de chargement</div>
      </div>
    );
  }

  const categories = Object.values(grouped);
  const filteredCategories = selectedCategory
    ? categories.filter(c => c.category.id === selectedCategory)
    : categories;

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-950 via-purple-950 to-slate-950">
      {/* Header */}
      <header className="border-b border-white/10 backdrop-blur-xl bg-black/30 sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-4 py-4 flex items-center justify-between">
          <Link href="/" className="text-2xl font-bold text-white flex items-center gap-3">
            <span className="text-3xl">🎯</span>
            <span className="bg-gradient-to-r from-purple-400 to-pink-400 bg-clip-text text-transparent">WikiAsk</span>
          </Link>
          <nav className="flex gap-6">
            <Link href="/" className="text-white/70 hover:text-white transition">Accueil</Link>
            <Link href="/explore" className="text-white font-semibold">Explorer</Link>
            <Link href="/about" className="text-white/70 hover:text-white transition">À propos</Link>
          </nav>
        </div>
      </header>

      {/* Hero */}
      <section className="py-16 px-4 text-center">
        <h1 className="text-5xl font-bold text-white mb-4">
          🧠 Explorez nos <span className="bg-gradient-to-r from-purple-400 to-pink-400 bg-clip-text text-transparent">16 Experts IA</span>
        </h1>
        <p className="text-white/60 text-xl max-w-2xl mx-auto">
          Chaque expert est spécialisé dans son domaine avec accès aux données en temps réel
        </p>
      </section>

      {/* Category Filter Pills */}
      <section className="max-w-7xl mx-auto px-4 pb-8">
        <div className="flex flex-wrap gap-3 justify-center">
          <button
            onClick={() => setSelectedCategory(null)}
            className={`px-6 py-2 rounded-full font-medium transition ${!selectedCategory
                ? 'bg-gradient-to-r from-purple-500 to-pink-500 text-white'
                : 'bg-white/10 text-white/70 hover:bg-white/20'
              }`}
          >
            Tous ({Object.values(grouped).reduce((acc, c) => acc + c.count, 0)})
          </button>
          {categories.map((cat) => (
            <button
              key={cat.category.id}
              onClick={() => setSelectedCategory(cat.category.id === selectedCategory ? null : cat.category.id)}
              className={`px-6 py-2 rounded-full font-medium transition flex items-center gap-2 ${cat.category.id === selectedCategory
                  ? 'text-white'
                  : 'bg-white/10 text-white/70 hover:bg-white/20'
                }`}
              style={cat.category.id === selectedCategory ? { backgroundColor: cat.category.color } : {}}
            >
              <span>{cat.category.emoji}</span>
              <span>{cat.category.name}</span>
              <span className="bg-black/20 px-2 py-0.5 rounded-full text-xs">{cat.count}</span>
            </button>
          ))}
        </div>
      </section>

      {/* Categories Grid */}
      <main className="max-w-7xl mx-auto px-4 pb-16">
        <div className="space-y-12">
          {filteredCategories.map((categoryData) => (
            <section key={categoryData.category.id} className="relative">
              {/* Category Header */}
              <div className="flex items-center gap-4 mb-6">
                <div
                  className="w-12 h-12 rounded-xl flex items-center justify-center text-2xl"
                  style={{ backgroundColor: categoryData.category.color + '30' }}
                >
                  {categoryData.category.emoji}
                </div>
                <div>
                  <h2 className="text-2xl font-bold text-white">{categoryData.category.name}</h2>
                  <p className="text-white/50">{categoryData.category.description}</p>
                </div>
              </div>

              {/* Experts Grid */}
              <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
                {categoryData.experts.map((expert) => (
                  <Link
                    key={expert.id}
                    href={`/expert/${expert.id}`}
                    className="group relative bg-white/5 border border-white/10 rounded-2xl p-6 hover:bg-white/10 hover:border-white/20 transition-all duration-300 hover:scale-[1.02] hover:shadow-xl"
                  >
                    {/* Expert Icon */}
                    <div
                      className="w-14 h-14 rounded-xl flex items-center justify-center text-3xl mb-4 group-hover:scale-110 transition-transform"
                      style={{ backgroundColor: expert.color + '30' }}
                    >
                      {expert.emoji}
                    </div>

                    {/* Expert Info */}
                    <h3 className="text-lg font-bold text-white mb-1">{expert.name}</h3>
                    <p className="text-sm text-white/50 mb-3">{expert.tagline}</p>
                    <p className="text-sm text-white/40 line-clamp-2">{expert.description}</p>

                    {/* Hover Arrow */}
                    <div className="absolute top-6 right-6 opacity-0 group-hover:opacity-100 transition-opacity">
                      <span className="text-white/50">→</span>
                    </div>

                    {/* Bottom Color Bar */}
                    <div
                      className="absolute bottom-0 left-0 right-0 h-1 rounded-b-2xl opacity-0 group-hover:opacity-100 transition-opacity"
                      style={{ backgroundColor: expert.color }}
                    />
                  </Link>
                ))}
              </div>
            </section>
          ))}
        </div>
      </main>

      {/* Stats */}
      <section className="border-t border-white/10 py-16 px-4">
        <div className="max-w-7xl mx-auto grid grid-cols-2 md:grid-cols-4 gap-8 text-center">
          <div>
            <div className="text-4xl font-bold text-white">16</div>
            <div className="text-white/50">Experts IA</div>
          </div>
          <div>
            <div className="text-4xl font-bold text-white">5</div>
            <div className="text-white/50">Catégories</div>
          </div>
          <div>
            <div className="text-4xl font-bold text-white">60+</div>
            <div className="text-white/50">APIs connectées</div>
          </div>
          <div>
            <div className="text-4xl font-bold text-white">11</div>
            <div className="text-white/50">Langues</div>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="border-t border-white/10 py-8 px-4">
        <div className="max-w-7xl mx-auto flex flex-col md:flex-row items-center justify-between gap-4">
          <p className="text-white/40 text-sm">© 2024 WikiAsk — ECOFUN DRIVE (SASU)</p>
          <div className="flex gap-6">
            <Link href="/mentions-legales" className="text-white/40 hover:text-white text-sm transition">Mentions légales</Link>
            <Link href="/confidentialite" className="text-white/40 hover:text-white text-sm transition">Confidentialité</Link>
            <Link href="/cookies" className="text-white/40 hover:text-white text-sm transition">Cookies</Link>
          </div>
        </div>
      </footer>
    </div>
  );
}



import { useEffect, useState } from "react";
import Link from "next/link";

interface Expert {
  id: string;
  name: string;
  emoji: string;
  tagline: string;
  description: string;
  color: string;
}

interface CategoryData {
  category: {
    id: string;
    name: string;
    name_en: string;
    emoji: string;
    description: string;
    color: string;
  };
  experts: Expert[];
  count: number;
}

type GroupedExperts = Record<string, CategoryData>;

export default function ExplorePage() {
  const [grouped, setGrouped] = useState<GroupedExperts | null>(null);
  const [loading, setLoading] = useState(true);
  const [selectedCategory, setSelectedCategory] = useState<string | null>(null);

  useEffect(() => {
    fetch("/api/expert/grouped")
      .then((res) => res.json())
      .then((data) => {
        setGrouped(data);
        setLoading(false);
      })
      .catch((err) => {
        // Logger silencieux en production
        if (process.env.NODE_ENV === 'development') {
          console.error("Failed to load experts:", err);
        }
        setLoading(false);
      });
  }, []);

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-slate-950 via-purple-950 to-slate-950 flex items-center justify-center">
        <div className="text-white text-xl">Chargement des experts...</div>
      </div>
    );
  }

  if (!grouped) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-slate-950 via-purple-950 to-slate-950 flex items-center justify-center">
        <div className="text-white text-xl">Erreur de chargement</div>
      </div>
    );
  }

  const categories = Object.values(grouped);
  const filteredCategories = selectedCategory
    ? categories.filter(c => c.category.id === selectedCategory)
    : categories;

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-950 via-purple-950 to-slate-950">
      {/* Header */}
      <header className="border-b border-white/10 backdrop-blur-xl bg-black/30 sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-4 py-4 flex items-center justify-between">
          <Link href="/" className="text-2xl font-bold text-white flex items-center gap-3">
            <span className="text-3xl">🎯</span>
            <span className="bg-gradient-to-r from-purple-400 to-pink-400 bg-clip-text text-transparent">WikiAsk</span>
          </Link>
          <nav className="flex gap-6">
            <Link href="/" className="text-white/70 hover:text-white transition">Accueil</Link>
            <Link href="/explore" className="text-white font-semibold">Explorer</Link>
            <Link href="/about" className="text-white/70 hover:text-white transition">À propos</Link>
          </nav>
        </div>
      </header>

      {/* Hero */}
      <section className="py-16 px-4 text-center">
        <h1 className="text-5xl font-bold text-white mb-4">
          🧠 Explorez nos <span className="bg-gradient-to-r from-purple-400 to-pink-400 bg-clip-text text-transparent">16 Experts IA</span>
        </h1>
        <p className="text-white/60 text-xl max-w-2xl mx-auto">
          Chaque expert est spécialisé dans son domaine avec accès aux données en temps réel
        </p>
      </section>

      {/* Category Filter Pills */}
      <section className="max-w-7xl mx-auto px-4 pb-8">
        <div className="flex flex-wrap gap-3 justify-center">
          <button
            onClick={() => setSelectedCategory(null)}
            className={`px-6 py-2 rounded-full font-medium transition ${!selectedCategory
                ? 'bg-gradient-to-r from-purple-500 to-pink-500 text-white'
                : 'bg-white/10 text-white/70 hover:bg-white/20'
              }`}
          >
            Tous ({Object.values(grouped).reduce((acc, c) => acc + c.count, 0)})
          </button>
          {categories.map((cat) => (
            <button
              key={cat.category.id}
              onClick={() => setSelectedCategory(cat.category.id === selectedCategory ? null : cat.category.id)}
              className={`px-6 py-2 rounded-full font-medium transition flex items-center gap-2 ${cat.category.id === selectedCategory
                  ? 'text-white'
                  : 'bg-white/10 text-white/70 hover:bg-white/20'
                }`}
              style={cat.category.id === selectedCategory ? { backgroundColor: cat.category.color } : {}}
            >
              <span>{cat.category.emoji}</span>
              <span>{cat.category.name}</span>
              <span className="bg-black/20 px-2 py-0.5 rounded-full text-xs">{cat.count}</span>
            </button>
          ))}
        </div>
      </section>

      {/* Categories Grid */}
      <main className="max-w-7xl mx-auto px-4 pb-16">
        <div className="space-y-12">
          {filteredCategories.map((categoryData) => (
            <section key={categoryData.category.id} className="relative">
              {/* Category Header */}
              <div className="flex items-center gap-4 mb-6">
                <div
                  className="w-12 h-12 rounded-xl flex items-center justify-center text-2xl"
                  style={{ backgroundColor: categoryData.category.color + '30' }}
                >
                  {categoryData.category.emoji}
                </div>
                <div>
                  <h2 className="text-2xl font-bold text-white">{categoryData.category.name}</h2>
                  <p className="text-white/50">{categoryData.category.description}</p>
                </div>
              </div>

              {/* Experts Grid */}
              <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
                {categoryData.experts.map((expert) => (
                  <Link
                    key={expert.id}
                    href={`/expert/${expert.id}`}
                    className="group relative bg-white/5 border border-white/10 rounded-2xl p-6 hover:bg-white/10 hover:border-white/20 transition-all duration-300 hover:scale-[1.02] hover:shadow-xl"
                  >
                    {/* Expert Icon */}
                    <div
                      className="w-14 h-14 rounded-xl flex items-center justify-center text-3xl mb-4 group-hover:scale-110 transition-transform"
                      style={{ backgroundColor: expert.color + '30' }}
                    >
                      {expert.emoji}
                    </div>

                    {/* Expert Info */}
                    <h3 className="text-lg font-bold text-white mb-1">{expert.name}</h3>
                    <p className="text-sm text-white/50 mb-3">{expert.tagline}</p>
                    <p className="text-sm text-white/40 line-clamp-2">{expert.description}</p>

                    {/* Hover Arrow */}
                    <div className="absolute top-6 right-6 opacity-0 group-hover:opacity-100 transition-opacity">
                      <span className="text-white/50">→</span>
                    </div>

                    {/* Bottom Color Bar */}
                    <div
                      className="absolute bottom-0 left-0 right-0 h-1 rounded-b-2xl opacity-0 group-hover:opacity-100 transition-opacity"
                      style={{ backgroundColor: expert.color }}
                    />
                  </Link>
                ))}
              </div>
            </section>
          ))}
        </div>
      </main>

      {/* Stats */}
      <section className="border-t border-white/10 py-16 px-4">
        <div className="max-w-7xl mx-auto grid grid-cols-2 md:grid-cols-4 gap-8 text-center">
          <div>
            <div className="text-4xl font-bold text-white">16</div>
            <div className="text-white/50">Experts IA</div>
          </div>
          <div>
            <div className="text-4xl font-bold text-white">5</div>
            <div className="text-white/50">Catégories</div>
          </div>
          <div>
            <div className="text-4xl font-bold text-white">60+</div>
            <div className="text-white/50">APIs connectées</div>
          </div>
          <div>
            <div className="text-4xl font-bold text-white">11</div>
            <div className="text-white/50">Langues</div>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="border-t border-white/10 py-8 px-4">
        <div className="max-w-7xl mx-auto flex flex-col md:flex-row items-center justify-between gap-4">
          <p className="text-white/40 text-sm">© 2024 WikiAsk — ECOFUN DRIVE (SASU)</p>
          <div className="flex gap-6">
            <Link href="/mentions-legales" className="text-white/40 hover:text-white text-sm transition">Mentions légales</Link>
            <Link href="/confidentialite" className="text-white/40 hover:text-white text-sm transition">Confidentialité</Link>
            <Link href="/cookies" className="text-white/40 hover:text-white text-sm transition">Cookies</Link>
          </div>
        </div>
      </footer>
    </div>
  );
}


