import type { Metadata } from 'next'
import './globals.css'

export const metadata: Metadata = {
  title: 'WikiAsk - Ask Everything. Know Everything.',
  description: 'Moteur de recherche IA intelligent qui agrège 78+ sources pour des résultats complets et précis',
  keywords: ['AI search', 'moteur de recherche', 'intelligence artificielle', 'source aggregator', 'wikiask'],
  authors: [{ name: 'WikiAsk' }],
  openGraph: {
    title: 'WikiAsk - Ask Everything. Know Everything.',
    description: 'Moteur de recherche IA intelligent avec 78+ sources intégrées',
    type: 'website',
  },
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="fr" className="dark">
      <body className="antialiased">{children}</body>
    </html>
  )
}
