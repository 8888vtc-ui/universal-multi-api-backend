import { Metadata } from 'next'

export async function generateStaticParams() {
    return [{ lang: 'fr' }, { lang: 'en' }]
}

export const metadata: Metadata = {
    title: 'WikiAsk',
    description: 'WikiAsk',
}

export default function LangLayout({
    children,
    params,
}: {
    children: React.ReactNode
    params: { lang: string }
}) {
    return (
        <html lang={params.lang} className="dark">
            <body className="antialiased">{children}</body>
        </html>
    )
}
