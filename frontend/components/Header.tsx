'use client';

import { Language, getTranslations } from '@/lib/i18n';

interface HeaderProps {
    language: Language;
    onLanguageChange: (lang: Language) => void;
}

export default function Header({ language, onLanguageChange }: HeaderProps) {
    const t = getTranslations(language);

    return (
        <header className="border-b border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-900">
            <div className="container mx-auto px-4 py-4 flex items-center justify-between">
                <div className="flex items-center gap-3">
                    <div className="text-3xl">🌍</div>
                    <div>
                        <h1 className="text-xl font-bold">{t.appName}</h1>
                        <p className="text-xs text-gray-600 dark:text-gray-400">
                            {t.poweredBy}
                        </p>
                    </div>
                </div>

                {/* Language Switcher */}
                <div className="flex gap-2">
                    <button
                        onClick={() => onLanguageChange('he')}
                        className={`px-3 py-1 rounded-md text-sm font-medium transition-colors ${language === 'he'
                                ? 'bg-blue-600 text-white'
                                : 'bg-gray-100 dark:bg-gray-800 text-gray-700 dark:text-gray-300 hover:bg-gray-200 dark:hover:bg-gray-700'
                            }`}
                    >
                        עברית
                    </button>
                    <button
                        onClick={() => onLanguageChange('en')}
                        className={`px-3 py-1 rounded-md text-sm font-medium transition-colors ${language === 'en'
                                ? 'bg-blue-600 text-white'
                                : 'bg-gray-100 dark:bg-gray-800 text-gray-700 dark:text-gray-300 hover:bg-gray-200 dark:hover:bg-gray-700'
                            }`}
                    >
                        English
                    </button>
                </div>
            </div>
        </header>
    );
}
