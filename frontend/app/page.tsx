'use client';

import { useState, useEffect } from 'react';
import { Language, getDirection } from '@/lib/i18n';
import Header from '@/components/Header';
import ChatInterface from '@/components/ChatInterface';

export default function Home() {
  const [language, setLanguage] = useState<Language>('he');
  const [mounted, setMounted] = useState(false);

  useEffect(() => {
    setMounted(true);
    // Load language from localStorage
    const savedLang = localStorage.getItem('language') as Language;
    if (savedLang && (savedLang === 'he' || savedLang === 'en')) {
      setLanguage(savedLang);
    }
  }, []);

  const handleLanguageChange = (lang: Language) => {
    setLanguage(lang);
    localStorage.setItem('language', lang);
  };

  if (!mounted) {
    return null; // Prevent hydration mismatch
  }

  const direction = getDirection(language);

  return (
    <div dir={direction} className={`h-screen flex flex-col ${language === 'he' ? 'font-hebrew' : 'font-latin'}`}>
      <Header language={language} onLanguageChange={handleLanguageChange} />
      <main className="flex-1 overflow-hidden">
        <ChatInterface language={language} />
      </main>
    </div>
  );
}
