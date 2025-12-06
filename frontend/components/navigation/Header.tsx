'use client'

import { useState } from 'react'
import Link from 'next/link'
import { Search, Sparkles, MessageSquare, Globe, Menu, X, User } from 'lucide-react'
import UserMenu from './UserMenu'

export default function Header() {
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false)

  return (
    <header className="border-b border-dark-700/50 backdrop-blur-xl bg-dark-900/50 sticky top-0 z-50">
      <div className="max-w-7xl mx-auto px-6 py-4">
        <div className="flex items-center justify-between">
          {/* Logo */}
          <Link href="/" className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-xl animated-gradient flex items-center justify-center">
              <Sparkles className="w-6 h-6 text-white" />
            </div>
            <div>
              <h1 className="text-xl font-bold gradient-text">WikiAsk</h1>
              <p className="text-xs text-dark-400">Ask Everything. Know Everything.</p>
            </div>
          </Link>

          {/* Desktop Navigation */}
          <nav className="hidden md:flex items-center gap-6">
            <Link href="/search" className="flex items-center gap-2 text-dark-300 hover:text-white transition">
              <Search className="w-4 h-4" />
              Recherche
            </Link>
            <Link href="/ai-search" className="flex items-center gap-2 text-dark-300 hover:text-white transition">
              <Sparkles className="w-4 h-4" />
              IA Search
            </Link>
            <Link href="/chat" className="flex items-center gap-2 text-dark-300 hover:text-white transition">
              <MessageSquare className="w-4 h-4" />
              Chat
            </Link>
            <Link href="/explore" className="flex items-center gap-2 text-dark-300 hover:text-white transition">
              <Globe className="w-4 h-4" />
              Explorer
            </Link>
            <Link href="/docs" className="text-dark-300 hover:text-white transition">
              Guide
            </Link>
            <UserMenu />
          </nav>

          {/* Mobile Menu Button */}
          <button
            className="md:hidden text-dark-300 hover:text-white"
            onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
          >
            {mobileMenuOpen ? <X className="w-6 h-6" /> : <Menu className="w-6 h-6" />}
          </button>
        </div>

        {/* Mobile Menu */}
        {mobileMenuOpen && (
          <nav className="md:hidden mt-4 pb-4 space-y-2">
            <Link href="/search" className="block px-4 py-2 text-dark-300 hover:text-white transition">
              Recherche
            </Link>
            <Link href="/ai-search" className="block px-4 py-2 text-dark-300 hover:text-white transition">
              IA Search
            </Link>
            <Link href="/chat" className="block px-4 py-2 text-dark-300 hover:text-white transition">
              Chat
            </Link>
            <Link href="/explore" className="block px-4 py-2 text-dark-300 hover:text-white transition">
              Explorer
            </Link>
            <Link href="/docs" className="block px-4 py-2 text-dark-300 hover:text-white transition">
              Guide
            </Link>
          </nav>
        )}
      </div>
    </header>
  )
}

