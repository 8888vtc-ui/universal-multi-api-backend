import { Metadata } from 'next'
import { getSniperConfig } from '@/lib/sniper-config'
import SniperClientPage from './SniperClientPage'
import SeoContentBlock from '@/components/sniper/SeoContentBlock'
import MainLayout from '@/components/layouts/MainLayout'

interface PageProps {
    params: {
        category: string
        query: string
        lang: string
    }
}

export async function generateMetadata({ params }: PageProps): Promise<Metadata> {
    const config = getSniperConfig(params.category, params.lang as any)
    const decodedQuery = decodeURIComponent(params.query).replace(/-/g, ' ')

    return {
        title: config.seoTemplate.title(decodedQuery),
        description: config.seoTemplate.description(decodedQuery),
        keywords: [...config.keywords, decodedQuery, `${config.name} ${decodedQuery}`],
        openGraph: {
            title: config.seoTemplate.title(decodedQuery),
            description: config.seoTemplate.description(decodedQuery),
            type: 'website',
        }
    }
}

export default function SniperPage({ params }: PageProps) {
    const config = getSniperConfig(params.category, params.lang as any)
    const decodedQuery = decodeURIComponent(params.query).replace(/-/g, ' ')

    return (
        <MainLayout>
            <div className={`min-h-screen bg-gradient-to-b ${config.theme.bgGradient}`}>
                <SniperClientPage params={params} />

                <SeoContentBlock
                    category={params.category}
                    query={params.query}
                    lang={params.lang}
                />
            </div>
        </MainLayout>
    )
}
