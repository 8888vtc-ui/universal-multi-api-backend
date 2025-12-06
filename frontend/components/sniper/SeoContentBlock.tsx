import { getSniperConfig } from '@/lib/sniper-config'
import Link from 'next/link'
import cities from '@/data/cities-fr.json'
import drugs from '@/data/drugs-top500.json'
import cryptos from '@/data/cryptos-top200.json'
import books from '@/data/books-classics.json'

interface SeoContentBlockProps {
    category: string
    query: string
    lang: string
}

export default function SeoContentBlock({ category, query, lang }: SeoContentBlockProps) {
    const config = getSniperConfig(category, lang as any)
    const decodedQuery = decodeURIComponent(query).replace(/-/g, ' ')

    // Generate content from template
    const htmlContent = config.seoTemplate.content(decodedQuery)

    // Smart Cross-Linking Logic
    const getRelatedLinks = () => {
        const links: { title: string, url: string }[] = []

        // Helper to get random items
        const getRandom = (arr: any[], count: number) => {
            const shuffled = [...arr].sort(() => 0.5 - Math.random())
            return shuffled.slice(0, count)
        }

        if (category === 'sante') {
            const relatedDrugs = getRandom(drugs, 6)
            relatedDrugs.forEach((drug: any) => {
                const slug = drug.name.toLowerCase().replace(/\s+/g, '-')
                links.push({ title: `Notice ${drug.name}`, url: `/sniper/sante/notice-${slug}` })
            })
        } else if (category === 'local') {
            const relatedCities = getRandom(cities, 6)
            relatedCities.forEach((city: any) => {
                const slug = city.name.toLowerCase().replace(/\s+/g, '-')
                links.push({ title: `Météo ${city.name}`, url: `/sniper/local/meteo-${slug}` })
            })
        } else if (category === 'finance') {
            const relatedCryptos = getRandom(cryptos, 6)
            relatedCryptos.forEach((crypto: any) => {
                links.push({ title: `Cours ${crypto.name}`, url: `/sniper/finance/cours-${crypto.id}` })
            })
        } else if (category === 'savoir') {
            const relatedBooks = getRandom(books, 6)
            relatedBooks.forEach((book: any) => {
                const slug = book.title.toLowerCase().replace(/['\s]+/g, '-')
                links.push({ title: `Résumé ${book.title}`, url: `/sniper/savoir/resume-${slug}` })
            })
        }

        return links
    }

    const relatedLinks = getRelatedLinks()

    if (!htmlContent) return null

    return (
        <div className="w-full bg-slate-50 border-t border-slate-200 mt-20 py-16">
            <div className="max-w-4xl mx-auto px-6">
                <div
                    className="prose prose-slate max-w-none 
            prose-headings:text-slate-800 prose-headings:font-bold
            prose-h2:text-2xl prose-h2:mb-6 prose-h2:mt-0
            prose-h3:text-xl prose-h3:text-slate-700 prose-h3:mt-8 prose-h3:mb-4
            prose-p:text-slate-600 prose-p:leading-relaxed
            prose-li:text-slate-600 prose-li:marker:text-slate-400
            prose-strong:text-slate-800"
                    dangerouslySetInnerHTML={{ __html: htmlContent }}
                />

                {/* Smart Cross-Linking Section */}
                {relatedLinks.length > 0 && (
                    <div className="mt-16 pt-12 border-t border-slate-200">
                        <h3 className={`text-xl font-bold mb-6 ${config.theme.text}`}>
                            Voir aussi dans {config.name}
                        </h3>
                        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                            {relatedLinks.map((link, i) => (
                                <Link
                                    key={i}
                                    href={link.url}
                                    className="group flex items-center gap-2 p-3 rounded-lg hover:bg-white hover:shadow-sm border border-transparent hover:border-slate-200 transition-all"
                                >
                                    <div className={`w-1.5 h-1.5 rounded-full bg-${config.theme.primary}/40 group-hover:bg-${config.theme.primary}`}></div>
                                    <span className="text-slate-600 group-hover:text-slate-900 text-sm font-medium">
                                        {link.title}
                                    </span>
                                </Link>
                            ))}
                        </div>
                    </div>
                )}

                {/* Semantic Keywords Cloud (SEO Reinforcement) */}
                <div className="mt-12 flex flex-wrap gap-2">
                    {config.keywords.map((kw, i) => (
                        <span key={i} className="px-3 py-1 bg-slate-100 text-slate-500 text-xs rounded-full">
                            #{kw}
                        </span>
                    ))}
                </div>

                <div className="mt-12 pt-8 border-t border-slate-200 text-sm text-slate-500">
                    <p>
                        Les informations fournies par {config.name} sont agrégées automatiquement à partir de sources publiques.
                        Vérifiez toujours les informations auprès de sources officielles.
                    </p>
                </div>
            </div>
        </div>
    )
}
