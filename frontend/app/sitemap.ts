import { MetadataRoute } from 'next'
import { SNIPER_CONFIGS } from '@/lib/sniper-config'
import cities from '@/data/cities-fr.json'
import drugs from '@/data/drugs-top500.json'
import cryptos from '@/data/cryptos-top200.json'
import books from '@/data/books-classics.json'

export default function sitemap(): MetadataRoute.Sitemap {
    const baseUrl = 'https://wikiask.net'

    // Static routes
    const routes = [
        '',
        '/search',
        '/pricing',
        '/ai-search',
    ].map((route) => ({
        url: `${baseUrl}${route}`,
        lastModified: new Date(),
        changeFrequency: 'daily' as const,
        priority: 1,
    }))

    const languages = ['fr', 'en']
    const sniperRoutes: MetadataRoute.Sitemap = []

    languages.forEach(lang => {
        // 1. Generate Health Pages (Drugs)
        drugs.forEach((drug) => {
            const slug = drug.name.toLowerCase().replace(/\s+/g, '-')
            const patterns = ['notice', 'effets-secondaires', 'posologie']

            patterns.forEach(pattern => {
                sniperRoutes.push({
                    url: `${baseUrl}/${lang}/sniper/sante/${pattern}-${slug}`,
                    lastModified: new Date(),
                    changeFrequency: 'weekly' as const,
                    priority: 0.8,
                })
            })
        })

        // 2. Generate Local Pages (Cities)
        cities.forEach((city) => {
            const slug = city.name.toLowerCase().replace(/\s+/g, '-')
            const patterns = ['meteo', 'lever-soleil']

            patterns.forEach(pattern => {
                sniperRoutes.push({
                    url: `${baseUrl}/${lang}/sniper/local/${pattern}-${slug}`,
                    lastModified: new Date(),
                    changeFrequency: 'daily' as const,
                    priority: 0.7,
                })
            })
        })

        // 3. Generate Finance Pages (Cryptos)
        cryptos.forEach((crypto) => {
            const slug = crypto.id
            const patterns = ['cours', 'convertisseur']

            patterns.forEach(pattern => {
                const urlSuffix = pattern === 'convertisseur' ? '-euro' : ''
                sniperRoutes.push({
                    url: `${baseUrl}/${lang}/sniper/finance/${pattern}-${slug}${urlSuffix}`,
                    lastModified: new Date(),
                    changeFrequency: 'always' as const,
                    priority: 0.9,
                })
            })
        })

        // 4. Generate Knowledge Pages (Books)
        books.forEach((book) => {
            const slug = book.title.toLowerCase().replace(/['\s]+/g, '-')
            sniperRoutes.push({
                url: `${baseUrl}/${lang}/sniper/savoir/resume-${slug}`,
                lastModified: new Date(),
                changeFrequency: 'monthly' as const,
                priority: 0.6,
            })
        })
    })

    return [...routes, ...sniperRoutes]
}
