'use client'

import { useState, useEffect } from 'react'
import { Shield, X } from 'lucide-react'

export default function CookieConsent() {
    const [isVisible, setIsVisible] = useState(false)

    useEffect(() => {
        // Check if user has already consented
        const consent = localStorage.getItem('wikiask-cookie-consent')
        if (!consent) {
            setIsVisible(true)
        }
    }, [])

    const handleAccept = () => {
        localStorage.setItem('wikiask-cookie-consent', 'accepted')
        setIsVisible(false)
    }

    const handleDecline = () => {
        localStorage.setItem('wikiask-cookie-consent', 'declined')
        setIsVisible(false)
    }

    if (!isVisible) return null

    return (
        <div className="fixed bottom-0 left-0 right-0 z-50 p-4 md:p-6 animate-in slide-in-from-bottom-full duration-500">
            <div className="max-w-4xl mx-auto glass border border-cyan-500/30 rounded-2xl p-6 shadow-2xl shadow-cyan-900/50 backdrop-blur-xl bg-slate-900/90">
                <div className="flex flex-col md:flex-row items-start md:items-center gap-6">
                    <div className="flex-shrink-0 p-3 bg-cyan-500/10 rounded-xl">
                        <Shield className="w-8 h-8 text-cyan-400" />
                    </div>

                    <div className="flex-1">
                        <h3 className="text-lg font-bold text-white mb-2">Calibrage de Précision (Cookies)</h3>
                        <p className="text-slate-400 text-sm leading-relaxed">
                            Nous utilisons des traceurs pour optimiser la précision de nos résultats et assurer la sécurité du système.
                            Ces données sont essentielles pour le maintien de notre niveau de performance "Sniper".
                        </p>
                    </div>

                    <div className="flex flex-col sm:flex-row gap-3 w-full md:w-auto">
                        <button
                            onClick={handleDecline}
                            className="px-6 py-3 rounded-xl border border-slate-700 text-slate-300 hover:bg-slate-800 hover:text-white transition-colors text-sm font-medium whitespace-nowrap"
                        >
                            Refuser
                        </button>
                        <button
                            onClick={handleAccept}
                            className="px-6 py-3 rounded-xl bg-gradient-to-r from-cyan-600 to-blue-600 text-white hover:opacity-90 transition-opacity shadow-lg shadow-cyan-500/20 text-sm font-bold whitespace-nowrap"
                        >
                            Accepter & Continuer
                        </button>
                    </div>
                </div>
            </div>
        </div>
    )
}
