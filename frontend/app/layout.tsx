import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "WikiAsk - Moteur de Recherche IA",
  description: "Recherche intelligente multi-domaine avec accès aux données en temps réel.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="fr" className="dark">
      <head>
        <link rel="preconnect" href="https://fonts.googleapis.com" />
        <link rel="preconnect" href="https://fonts.gstatic.com" crossOrigin="anonymous" />
        <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet" />
        <meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1, user-scalable=0" />
      </head>
      <body className="antialiased min-h-screen bg-gradient-to-br from-slate-950 via-[#1e1b4b] to-slate-950 text-white selection:bg-indigo-500/30">
        {children}
      </body>
    </html>
  );
}
