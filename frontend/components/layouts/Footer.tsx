'use client'

export default function Footer() {
  return (
    <footer className="border-t border-dark-700/50 py-8 mt-12">
      <div className="max-w-7xl mx-auto px-6">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
          <div>
            <h3 className="text-lg font-bold gradient-text mb-4">WikiAsk</h3>
            <p className="text-sm text-dark-400">
              Ask Everything. Know Everything.
            </p>
          </div>
          <div>
            <h4 className="font-semibold text-white mb-4">Product</h4>
            <ul className="space-y-2 text-sm text-dark-400">
              <li><a href="/search" className="hover:text-white transition">Recherche</a></li>
              <li><a href="/ai-search" className="hover:text-white transition">Recherche IA</a></li>
              <li><a href="/chat" className="hover:text-white transition">Chat</a></li>
              <li><a href="/explore" className="hover:text-white transition">Explorer</a></li>
            </ul>
          </div>
          <div>
            <h4 className="font-semibold text-white mb-4">Resources</h4>
            <ul className="space-y-2 text-sm text-dark-400">
              <li><a href="/docs" className="hover:text-white transition">Centre d'aide</a></li>
              <li><a href="/pricing" className="hover:text-white transition">Accès Bêta</a></li>
              <li><a href="/history" className="hover:text-white transition">Historique</a></li>
            </ul>
          </div>
          <div>
            <h4 className="font-semibold text-white mb-4">Company</h4>
            <ul className="space-y-2 text-sm text-dark-400">
              <li><a href="/about" className="hover:text-white transition">À propos</a></li>
              <li><a href="/legal" className="hover:text-white transition">Mentions légales & RGPD</a></li>
              <li><a href="/support" className="hover:text-white transition">Support</a></li>
            </ul>
          </div>
        </div>
        <div className="mt-8 pt-8 border-t border-dark-700/50 text-center text-sm text-dark-400">
          <p>© 2024 WikiAsk - Tous droits réservés</p>
        </div>
      </div>
    </footer>
  )
}

