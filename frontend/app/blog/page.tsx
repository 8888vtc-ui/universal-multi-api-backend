import { Metadata } from 'next'
import { CATEGORIES, ARTICLES, getArticleSlugs } from '@/data/articles'

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

// Force dynamic rendering to avoid build timeout
export const dynamic = 'force-dynamic'
export const revalidate = 3600 // Revalidate every hour

import { apiClient } from '@/lib/api'

// Helper function to fetch articles with timeout and fallback
async function fetchArticlesWithFallback() {
    try {
        // Set a timeout of 5 seconds for the API call
        const timeoutPromise = new Promise((_, reject) => 
            setTimeout(() => reject(new Error('Timeout')), 5000)
        );
        
        const apiPromise = apiClient.getBlogArticles(1, 100, 'fr');
        const { articles } = await Promise.race([apiPromise, timeoutPromise]) as any;
        
        if (articles && articles.length > 0) {
            return articles;
        }
    } catch (error) {
        // Logger silencieux en production
        if (process.env.NODE_ENV === 'development') {
          console.warn('Failed to fetch articles from API, using static fallback:', error);
        }
    }
    
    // Fallback to static articles from data/articles.ts
    const slugs = getArticleSlugs();
    return slugs.map(slug => {
        const article = ARTICLES[slug];
        const content = article.fr;
        return {
            slug,
            title: content.title,
            excerpt: content.excerpt,
            expertId: article.expertId,
            date: article.date,
            readTime: article.readTime
        };
    });
}

export default async function BlogPage() {
    // Fetch articles with fallback to static data
    const articles = await fetchArticlesWithFallback();

    // Transform backend simplified model to frontend preview model
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

