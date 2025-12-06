import { Metadata } from 'next'
import { notFound } from 'next/navigation'
// import { ARTICLES, getArticle } from '@/data/articles' // Removed

import ArticleClient from './ArticleClient'

interface Props {
    params: { slug: string }
}

import { apiClient } from '@/lib/api'

interface Props {
    params: { slug: string }
}

// Generate static paths - For 15k articles, we can't build them all.
// Return empty to use ISR (blocking or true)
export async function generateStaticParams() {
    return []
}

// Dynamic SEO metadata
export async function generateMetadata({ params }: Props): Promise<Metadata> {
    const article = await apiClient.getBlogArticle(params.slug)

    if (!article) {
        return {
            title: 'Article non trouvé | WikiAsk Blog',
        }
    }

    const content = article.fr // Default to French for SEO

    return {
        title: `${content.title} | WikiAsk Blog`,
        description: content.excerpt,
        keywords: article.keywords.join(', '),
        authors: [{ name: 'WikiAsk AI' }],
        openGraph: {
            title: content.title,
            description: content.excerpt,
            type: 'article',
            publishedTime: article.date,
            authors: ['WikiAsk'],
            tags: article.keywords,
            siteName: 'WikiAsk',
            locale: 'fr_FR',
            alternateLocale: 'en_US',
        },
        twitter: {
            card: 'summary_large_image',
            title: content.title,
            description: content.excerpt,
        },
        alternates: {
            canonical: `https://wikiask.net/blog/${params.slug}`,
            languages: {
                'fr': `https://wikiask.net/blog/${params.slug}`,
                'en': `https://wikiask.net/en/blog/${params.slug}`,
            },
        },
    }
}

// Schema.org structured data for article
function generateArticleSchema(slug: string, article: any) {
    const content = article.fr
    return {
        '@context': 'https://schema.org',
        '@type': 'Article',
        headline: content.title,
        description: content.excerpt,
        datePublished: article.date,
        dateModified: article.date,
        author: {
            '@type': 'Organization',
            name: 'WikiAsk',
            url: 'https://wikiask.net',
        },
        publisher: {
            '@type': 'Organization',
            name: 'WikiAsk',
            logo: {
                '@type': 'ImageObject',
                url: 'https://wikiask.net/logo.png',
            },
        },
        mainEntityOfPage: {
            '@type': 'WebPage',
            '@id': `https://wikiask.net/blog/${slug}`,
        },
        keywords: article.keywords.join(', '),
        // articleSection: content.categoryName, // Removed as backend doesn't send categoryName specifically in fr object yet
        wordCount: content.content ? content.content.split(/\s+/).length : 0,
        timeRequired: `PT${article.readTime}M`,
    }
}

export default async function ArticlePage({ params }: Props) {
    const article = await apiClient.getBlogArticle(params.slug)

    if (!article) {
        notFound()
    }

    const articleSchema = generateArticleSchema(params.slug, article)

    return (
        <>
            {/* Schema.org JSON-LD */}
            <script
                type="application/ld+json"
                dangerouslySetInnerHTML={{ __html: JSON.stringify(articleSchema) }}
            />
            <ArticleClient slug={params.slug} article={article} />
        </>
    )
}

