import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";

const inter = Inter({ subsets: ["latin"], variable: '--font-latin' });

export const metadata: Metadata = {
  title: "מדריך תיירות ישראלי | Israeli Travel Guide",
  description: "המדריך החכם שלך לטיולים בטוחים ומותאמים אישית | Your smart guide for safe and personalized trips",
  keywords: "travel, israel, guide, tourism, kosher, safety, AI",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="he">
      <head>
        <link rel="preconnect" href="https://fonts.googleapis.com" />
        <link rel="preconnect" href="https://fonts.gstatic.com" crossOrigin="anonymous" />
        <link href="https://fonts.googleapis.com/css2?family=Assistant:wght@300;400;600;700&family=Heebo:wght@300;400;600;700&family=Inter:wght@300;400;600;700&display=swap" rel="stylesheet" />
      </head>
      <body className={`${inter.variable} antialiased`}>
        {children}
      </body>
    </html>
  );
}
