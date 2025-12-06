import { Metadata } from 'next'
import { CATEGORIES } from '@/data/articles'

import BlogClient from './BlogClient'

export const metadata: Metadata = {
    title: 'Blog WikiAsk | Comprendre l\'IA et vos données',
    description: 'Découvrez comment WikiAsk utilise l\'intelligence artificielle et des sources fiables (PubMed, CoinGecko, etc.) pour vous fournir des réponses précises. Articles sur la santé, finance, astrologie et plus.',
    keywords: 'blog IA, WikiAsk, PubMed, CoinGecko, recherche santé, crypto, horoscope, prénoms, histoire',
    openGraph: {
        title: 'Blog WikiAsk | Comprendre l\'IA et vos données',
        description: 'Découvrez comment WikiAsk utilise l\'intelligence artificielle pour analyser des sources fiables.',
        type: 'website',
        siteName: 'WikiAsk',
        locale: 'fr_FR',
    },
    twitter: {
        card: 'summary_large_image',
        title: 'Blog WikiAsk',
        description: 'Comprendre comment l\'IA analyse vos données',
    },
    alternates: {
        canonical: 'https://wikiask.net/blog',
    },
}

// Schema moved inside component


import { apiClient } from '@/lib/api'

// ... (keep metadata)

// Transform ARTICLES to array format for client (Removed static transform)

export default async function BlogPage() {
    // Fetch articles from API
    // Note: In production we might want to cache this or use ISR
    const { articles } = await apiClient.getBlogArticles(1, 100, 'fr');

    // Transform backend simplified model to frontend preview model if needed
    // Backend returns: { slug, title, excerpt, expertId, date, readTime }
    // Frontend expects: { slug, title, excerpt, category, categoryName, emoji, date, readTime }

    // We need to map expertId to category/emoji. 
    // We can rely on CATEGORIES from @/data/articles or fetch them.
    // For now we map manually or simplisticly.

    const mappedArticles = articles.map((a: any) => {
        const cat = CATEGORIES.find(c => c.id === a.expertId) || CATEGORIES[0];
        return {
            slug: a.slug,
            title: a.title,
            excerpt: a.excerpt,
            category: a.expertId,
            categoryName: cat ? cat.name : a.expertId,
            emoji: cat ? cat.emoji : '📄',
            date: a.date,
            readTime: a.readTime
        };
    });

    const blogSchema = {
        '@context': 'https://schema.org',
        '@type': 'Blog',
        name: 'Blog WikiAsk',
        description: 'Articles sur l\'utilisation de l\'IA et des données fiables',
        url: 'https://wikiask.net/blog',
        publisher: {
            '@type': 'Organization',
            name: 'WikiAsk',
            url: 'https://wikiask.net',
        },
        blogPost: articles.map((article: any) => ({
            '@type': 'BlogPosting',
            headline: article.title,
            description: article.excerpt,
            datePublished: article.date,
            url: `https://wikiask.net/blog/${article.slug}`,
        })),
    }

    return (
        <>
            <script
                type="application/ld+json"
                dangerouslySetInnerHTML={{ __html: JSON.stringify(blogSchema) }}
            />
            <BlogClient articles={mappedArticles} categories={CATEGORIES} />
        </>
    )
}

