'use client'

import { useState } from 'react'
import Link from 'next/link'
import { ArrowLeft, Calendar, Clock, MessageCircle } from 'lucide-react'
import { Article } from '@/data/articles'

interface ArticleClientProps {
    slug: string
    article: Article
}

export default function ArticleClient({ slug, article }: ArticleClientProps) {
    // Language state - could be dynamic based on user preference
    const [lang, setLang] = useState<'fr' | 'en'>('fr')
    const content = article[lang]

    return (
        <div className="min-h-screen bg-gradient-to-br from-amber-50 via-white to-rose-50">
            {/* Header */}
            <header className="bg-white/80 backdrop-blur-md border-b border-amber-100 sticky top-0 z-50">
                <div className="max-w-4xl mx-auto px-4 py-4">
                    <div className="flex items-center justify-between">
                        <div className="flex items-center gap-4">
                            <Link href="/blog" className="p-2 rounded-full hover:bg-amber-100 transition text-amber-600">
                                <ArrowLeft className="w-5 h-5" />
                            </Link>
                            <span className="text-sm font-medium text-amber-700 bg-amber-100 px-3 py-1 rounded-full">
                                {article.emoji} {content.categoryName}
                            </span>
                        </div>

                        {/* Language Switcher */}
                        <div className="flex gap-1 bg-gray-100 rounded-full p-1">
                            <button
                                onClick={() => setLang('fr')}
                                className={`px-3 py-1 rounded-full text-xs font-medium transition ${lang === 'fr' ? 'bg-white shadow text-amber-600' : 'text-gray-500 hover:text-gray-700'}`}
                            >
                                🇫🇷 FR
                            </button>
                            <button
                                onClick={() => setLang('en')}
                                className={`px-3 py-1 rounded-full text-xs font-medium transition ${lang === 'en' ? 'bg-white shadow text-amber-600' : 'text-gray-500 hover:text-gray-700'}`}
                            >
                                🇬🇧 EN
                            </button>
                        </div>
                    </div>
                </div>
            </header>

            {/* Article */}
            <article className="max-w-4xl mx-auto px-4 py-12">
                {/* Title */}
                <h1 className="text-3xl md:text-4xl font-bold text-gray-900 mb-4 leading-tight">
                    {content.title}
                </h1>

                {/* Meta */}
                <div className="flex items-center gap-4 text-sm text-gray-500 mb-8">
                    <span className="flex items-center gap-1">
                        <Calendar className="w-4 h-4" />
                        {new Date(article.date).toLocaleDateString(lang === 'fr' ? 'fr-FR' : 'en-US', {
                            year: 'numeric',
                            month: 'long',
                            day: 'numeric'
                        })}
                    </span>
                    <span className="flex items-center gap-1">
                        <Clock className="w-4 h-4" />
                        {article.readTime} min
                    </span>
                </div>

                {/* Content */}
                <div className="prose prose-lg prose-amber max-w-none">
                    <div
                        className="text-gray-700 leading-relaxed"
                        dangerouslySetInnerHTML={{
                            __html: content.content
                                .replace(/## (.*)/g, '<h2 class="text-2xl font-bold text-gray-900 mt-8 mb-4">$1</h2>')
                                .replace(/### (.*)/g, '<h3 class="text-xl font-semibold text-gray-800 mt-6 mb-3">$1</h3>')
                                .replace(/\*\*(.*?)\*\*/g, '<strong class="font-semibold text-gray-900">$1</strong>')
                                .replace(/- (.*)/g, '<li class="ml-4 mb-2">$1</li>')
                                .replace(/⚠️ (.*)/g, '<div class="bg-amber-50 border-l-4 border-amber-400 p-4 my-6 text-amber-800">⚠️ $1</div>')
                                .replace(/📅 (.*)/g, '<div class="bg-blue-50 border-l-4 border-blue-400 p-4 my-6 text-blue-800">📅 $1</div>')
                                .replace(/🎆 (.*)/g, '<div class="bg-purple-50 border-l-4 border-purple-400 p-4 my-6 text-purple-800">🎆 $1</div>')
                                .replace(/\n\n/g, '</p><p class="mb-4">')
                        }}
                    />
                </div>

                {/* CTA Box */}
                <div className="mt-12 p-6 bg-gradient-to-r from-amber-100 to-orange-100 rounded-2xl">
                    <h3 className="text-xl font-bold text-gray-900 mb-2">
                        {lang === 'fr' ? 'Vous avez des questions ?' : 'Have questions?'}
                    </h3>
                    <p className="text-gray-600 mb-4">
                        {lang === 'fr'
                            ? 'Notre IA peut répondre à vos questions en temps réel avec des données actualisées.'
                            : 'Our AI can answer your questions in real-time with updated data.'
                        }
                    </p>
                    <Link
                        href={`/expert/${article.expertId}`}
                        className="inline-flex items-center gap-2 px-6 py-3 bg-gradient-to-r from-amber-500 to-orange-500 text-white rounded-full font-medium hover:shadow-lg transition"
                    >
                        <MessageCircle className="w-4 h-4" />
                        {content.cta}
                    </Link>
                </div>

                {/* Related Articles placeholder */}
                <div className="mt-12 pt-8 border-t border-gray-200">
                    <h3 className="text-lg font-bold text-gray-900 mb-4">
                        {lang === 'fr' ? 'Articles similaires' : 'Related Articles'}
                    </h3>
                    <div className="flex gap-4">
                        <Link href="/blog" className="text-amber-600 hover:text-amber-700 text-sm font-medium">
                            ← {lang === 'fr' ? 'Voir tous les articles' : 'View all articles'}
                        </Link>
                    </div>
                </div>
            </article>

            {/* Footer */}
            <footer className="py-6 border-t border-amber-100 bg-white/30">
                <div className="max-w-4xl mx-auto px-4 text-center">
                    <p className="text-amber-700 font-medium text-sm mb-1">
                        Pensez. Discutez. Maîtrisez. — Human Data, AI Precision
                    </p>
                    <p className="text-gray-400 text-xs">© 2024 WikiAsk</p>
                </div>
            </footer>
        </div>
    )
}
