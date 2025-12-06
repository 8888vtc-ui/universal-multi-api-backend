'use client'

import { useState, useEffect } from 'react'
import { getSniperConfig, SniperConfig } from '@/lib/sniper-config'
import SearchBar from '@/components/search/SearchBar'
import SearchResults from '@/components/search/SearchResults'
import SeoContentBlock from '@/components/sniper/SeoContentBlock'
import { ArrowLeft } from 'lucide-react'
import Link from 'next/link'

interface SniperClientPageProps {
    params: {
        category: string
        query: string
        lang: string
    }
}

export default function SniperClientPage({ params }: SniperClientPageProps) {
    const { category, query, lang } = params
    const decodedQuery = decodeURIComponent(query).replace(/-/g, ' ')
    // Cast lang to any to avoid strict type checking issues if lang isn't exactly 'fr' | 'en' in the param type
    const config = getSniperConfig(category, lang as any)

    const [searchQueryState, setSearchQueryState] = useState(decodedQuery)
    const [results, setResults] = useState<any>(null)
    const [loading, setLoading] = useState(false)

    // Auto-search on mount
    useEffect(() => {
        if (decodedQuery) {
            handleSearch(decodedQuery)
        }
    }, [decodedQuery])

    const handleSearch = async (q: string) => {
        setSearchQueryState(q)
        setLoading(true)
        try {
            // Add category filter to the search
            const categoryParam = config.backendCategories.length > 0
                ? `&categories=${config.backendCategories.join(',')}`
                : ''
            const response = await fetch(
                `${process.env.NEXT_PUBLIC_API_URL || 'https://universal-api-hub.fly.dev'}/api/search/quick?q=${encodeURIComponent(q)}${categoryParam}`
            )
            const data = await response.json()
            setResults(data)
        } catch (error) {
            console.error('Search error:', error)
        } finally {
            setLoading(false)
        }
    }

    const Icon = config.icon

    return (
        <div className="max-w-7xl mx-auto px-6 py-8">
            {/* Sticky Header with Search */}
            <div className="sticky top-0 z-50 bg-white/80 backdrop-blur-md py-4 -mx-6 px-6 border-b border-slate-200/50 mb-8 transition-all duration-200">
                <div className="flex items-center gap-4 mb-4">
                    <Link
                        href="/"
                        className="inline-flex items-center justify-center w-10 h-10 rounded-full bg-slate-100 text-slate-500 hover:bg-slate-200 hover:text-slate-700 transition-colors"
                    >
                        <ArrowLeft className="w-5 h-5" />
                    </Link>

                    <div className="flex-1">
                        <SearchBar
                            onSearch={handleSearch}
                            loading={loading}
                            initialValue={decodedQuery}
                        />
                    </div>
                </div>

                <div className="flex items-center gap-3 text-sm text-slate-500 ml-14">
                    <Link href="/" className="hover:text-slate-800">Accueil</Link>
                    <span>/</span>
                    <span className={`font-medium ${config.theme.text}`}>{config.name}</span>
                    <span>/</span>
                    <span className="truncate max-w-[200px]">{decodedQuery}</span>
                </div>
            </div>

            {/* Title Section */}
            <div className="mb-8 ml-14">
                <div className="flex items-center gap-4">
                    <div className={`p-3 rounded-xl bg-${config.theme.primary}/10`}>
                        <Icon className={`w-8 h-8 text-${config.theme.primary}`} />
                    </div>
                    <div>
                        <h1 className={`text-3xl font-bold ${config.theme.text}`}>
                            {config.name}
                        </h1>
                        <p className="text-slate-500">
                            {config.seoTemplate.h1(decodedQuery)}
                        </p>
                    </div>
                </div>
            </div>

            {/* Results */}
            <div className="min-h-[400px]">
                {loading ? (
                    <div className="flex justify-center py-12">
                        <div className={`w-12 h-12 border-4 border-${config.theme.primary} border-t-transparent rounded-full animate-spin`}></div>
                    </div>
                ) : results ? (
                    <SearchResults results={results} query={searchQueryState} />
                ) : (
                    <div className="text-center py-12 text-slate-500">
                        Initialisation du sniper...
                    </div>
                )}
            </div>

            {/* SEO Content Block (Generated) */}
            <SeoContentBlock category={category} query={query} lang={lang} />
        </div>
    )
}
