'use client'

import MainLayout from '@/components/layouts/MainLayout'
import { Check, Shield, Zap } from 'lucide-react'
import Link from 'next/link'

export default function PricingPage() {
  return (
    <MainLayout>
      <div className="max-w-7xl mx-auto px-6 py-16">
        <div className="text-center mb-16">
          <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full glass mb-6 border border-cyan-500/30">
            <span className="relative flex h-3 w-3">
              <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-cyan-400 opacity-75"></span>
              <span className="relative inline-flex rounded-full h-3 w-3 bg-cyan-500"></span>
            </span>
            <span className="text-cyan-300 text-sm font-medium tracking-wide uppercase">Phase de Calibrage</span>
          </div>

          <h1 className="text-5xl font-bold mb-6 gradient-text">Accès Bêta Public</h1>
          <p className="text-slate-400 text-xl max-w-2xl mx-auto leading-relaxed">
            Nous calibrons actuellement la précision de notre moteur.
            L'accès est <span className="text-white font-semibold">gratuit</span> pour tous les utilisateurs pendant cette période.
          </p>
        </div>

        <div className="max-w-md mx-auto">
          <div className="card relative ring-2 ring-cyan-500 shadow-2xl shadow-cyan-500/20 overflow-hidden">
            {/* Background decorative elements */}
            <div className="absolute top-0 right-0 -mr-16 -mt-16 w-64 h-64 bg-cyan-500/10 rounded-full blur-3xl"></div>
            <div className="absolute bottom-0 left-0 -ml-16 -mb-16 w-64 h-64 bg-blue-500/10 rounded-full blur-3xl"></div>

            <div className="relative z-10">
              <div className="text-center mb-8">
                <h3 className="text-2xl font-bold text-white mb-2">Licence Sniper Bêta</h3>
                <div className="flex items-baseline justify-center gap-1 mb-4">
                  <span className="text-5xl font-bold gradient-text">0€</span>
                  <span className="text-slate-500">/mois</span>
                </div>
                <p className="text-cyan-400 text-sm font-medium bg-cyan-500/10 inline-block px-3 py-1 rounded-full border border-cyan-500/20">
                  Valable jusqu'à la version 1.0
                </p>
              </div>

              <div className="space-y-6 mb-8">
                <div className="flex items-start gap-4 p-4 rounded-xl bg-slate-800/50 border border-slate-700/50">
                  <Shield className="w-6 h-6 text-cyan-400 flex-shrink-0" />
                  <div>
                    <h4 className="text-white font-semibold text-sm">Accès Sécurisé</h4>
                    <p className="text-slate-400 text-xs">Validation humaine requise</p>
                  </div>
                </div>

                <div className="flex items-start gap-4 p-4 rounded-xl bg-slate-800/50 border border-slate-700/50">
                  <Zap className="w-6 h-6 text-yellow-400 flex-shrink-0" />
                  <div>
                    <h4 className="text-white font-semibold text-sm">Quota Journalier</h4>
                    <p className="text-slate-400 text-xs">Limité à 50 recherches de haute précision / jour</p>
                  </div>
                </div>

                <ul className="space-y-3 pl-2">
                  {[
                    'Accès à toutes les sources (78+)',
                    'Moteur de recherche Multichannel',
                    'Chat Assistant IA',
                    'Support prioritaire Discord',
                    'Statut "Early Adopter" (Badges futurs)'
                  ].map((feature, i) => (
                    <li key={i} className="flex items-center gap-3">
                      <div className="w-5 h-5 rounded-full bg-cyan-500/20 flex items-center justify-center flex-shrink-0">
                        <Check className="w-3 h-3 text-cyan-400" />
                      </div>
                      <span className="text-slate-300 text-sm">{feature}</span>
                    </li>
                  ))}
                </ul>
              </div>

              <Link href="/register" className="block w-full">
                <button className="w-full btn-primary py-4 text-lg shadow-xl shadow-cyan-500/20 hover:shadow-cyan-500/40 transform hover:-translate-y-1 transition-all duration-300">
                  Obtenir mon accès
                </button>
              </Link>

              <p className="text-center text-xs text-slate-500 mt-4">
                Aucune carte bancaire requise.
              </p>
            </div>
          </div>
        </div>
      </div>
    </MainLayout>
  )
}




