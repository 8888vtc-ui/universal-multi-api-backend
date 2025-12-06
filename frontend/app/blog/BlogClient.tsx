'use client'

import Link from 'next/link'
import { ArrowLeft, Calendar, Clock, ChevronRight } from 'lucide-react'

interface ArticlePreview {
    slug: string
    title: string
    excerpt: string
    category: string
    categoryName: string
    emoji: string
    date: string
    readTime: number
}

interface Category {
    id: string
    name: string
    nameEn: string
    emoji: string
}

interface BlogClientProps {
    articles: ArticlePreview[]
    categories: Category[]
}

export default function BlogClient({ articles, categories }: BlogClientProps) {
    return (
        <div className="min-h-screen bg-gradient-to-br from-amber-50 via-white to-rose-50">
            {/* Header */}
            <header className="bg-white/80 backdrop-blur-md border-b border-amber-100 sticky top-0 z-50">
                <div className="max-w-6xl mx-auto px-4 py-4">
                    <div className="flex items-center gap-4">
                        <Link href="/" className="p-2 rounded-full hover:bg-amber-100 transition text-amber-600">
                            <ArrowLeft className="w-5 h-5" />
                        </Link>
                        <div>
                            <h1 className="text-2xl font-bold text-gray-900">Blog WikiAsk</h1>
                            <p className="text-sm text-gray-500">Données humaines + Précision IA</p>
                        </div>
                    </div>
                </div>
            </header>

            {/* Hero */}
            <section className="py-12 px-4">
                <div className="max-w-4xl mx-auto text-center">
                    <h2 className="text-3xl font-bold text-gray-900 mb-4">
                        Comprendre comment <span className="text-amber-600">l&apos;IA analyse vos données</span>
                    </h2>
                    <p className="text-gray-600">
                        Nos articles expliquent d&apos;où viennent nos informations (PubMed, CoinGecko, etc.)
                        et comment notre IA les transforme en réponses fiables.
                    </p>
                </div>
            </section>

            {/* Categories */}
            <section className="px-4 pb-8">
                <div className="max-w-6xl mx-auto">
                    <div className="flex flex-wrap gap-2 justify-center">
                        {categories.map((cat) => (
                            <button
                                key={cat.id}
                                className="px-4 py-2 rounded-full text-sm font-medium bg-white border border-gray-200 hover:border-amber-300 hover:bg-amber-50 transition"
                            >
                                {cat.emoji} {cat.name}
                            </button>
                        ))}
                    </div>
                </div>
            </section>

            {/* Articles Grid */}
            <section className="px-4 pb-16">
                <div className="max-w-6xl mx-auto">
                    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                        {articles.map((article) => (
                            <Link
                                key={article.slug}
                                href={`/blog/${article.slug}`}
                                className="group bg-white rounded-2xl border border-gray-200 overflow-hidden hover:shadow-xl hover:border-amber-200 transition-all duration-300"
                            >
                                {/* Category Header */}
                                <div className="bg-gradient-to-r from-amber-50 to-orange-50 px-4 py-3 border-b border-gray-100">
                                    <span className="text-sm font-medium text-amber-700">
                                        {article.emoji} {article.categoryName}
                                    </span>
                                </div>

                                {/* Content */}
                                <div className="p-5">
                                    <h3 className="font-bold text-gray-900 mb-2 group-hover:text-amber-600 transition line-clamp-2">
                                        {article.title}
                                    </h3>
                                    <p className="text-sm text-gray-600 mb-4 line-clamp-3">
                                        {article.excerpt}
                                    </p>

                                    {/* Meta */}
                                    <div className="flex items-center gap-4 text-xs text-gray-400">
                                        <span className="flex items-center gap-1">
                                            <Calendar className="w-3 h-3" />
                                            {new Date(article.date).toLocaleDateString('fr-FR')}
                                        </span>
                                        <span className="flex items-center gap-1">
                                            <Clock className="w-3 h-3" />
                                            {article.readTime} min
                                        </span>
                                    </div>
                                </div>

                                {/* Footer */}
                                <div className="px-5 py-3 bg-gray-50 border-t border-gray-100 flex justify-between items-center">
                                    <span className="text-xs text-amber-600 font-medium">Lire l&apos;article</span>
                                    <ChevronRight className="w-4 h-4 text-amber-400 group-hover:translate-x-1 transition" />
                                </div>
                            </Link>
                        ))}
                    </div>
                </div>
            </section>

            {/* CTA */}
            <section className="py-12 px-4 bg-gradient-to-r from-amber-100 to-orange-100">
                <div className="max-w-4xl mx-auto text-center">
                    <h3 className="text-2xl font-bold text-gray-900 mb-4">
                        Posez vos questions à nos experts IA
                    </h3>
                    <p className="text-gray-600 mb-6">
                        16 experts spécialisés à votre service, 24h/24
                    </p>
                    <Link
                        href="/"
                        className="inline-flex items-center gap-2 px-6 py-3 bg-gradient-to-r from-amber-500 to-orange-500 text-white rounded-full font-medium hover:shadow-lg transition"
                    >
                        Découvrir les experts
                        <ChevronRight className="w-4 h-4" />
                    </Link>
                </div>
            </section>

            {/* Footer */}
            <footer className="py-6 border-t border-amber-100 bg-white/30">
                <div className="max-w-6xl mx-auto px-4 text-center">
                    <p className="text-amber-700 font-medium text-sm mb-1">
                        Pensez. Discutez. Maîtrisez. — Human Data, AI Precision
                    </p>
                    <p className="text-gray-400 text-xs">© 2024 WikiAsk</p>
                </div>
            </footer>
        </div>
    )
}
