'use client'

import { useState, useRef, useEffect } from 'react'
import { User, Settings, CreditCard, LogOut, ChevronDown } from 'lucide-react'
import Link from 'next/link'

export default function UserMenu() {
  const [isOpen, setIsOpen] = useState(false)
  const menuRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    function handleClickOutside(event: MouseEvent) {
      if (menuRef.current && !menuRef.current.contains(event.target as Node)) {
        setIsOpen(false)
      }
    }

    document.addEventListener('mousedown', handleClickOutside)
    return () => document.removeEventListener('mousedown', handleClickOutside)
  }, [])

  return (
    <div className="relative" ref={menuRef}>
      <button
        onClick={() => setIsOpen(!isOpen)}
        className="flex items-center gap-2 px-3 py-2 rounded-lg glass hover:glass-hover transition"
      >
        <div className="w-8 h-8 rounded-full bg-gradient-to-r from-indigo-500 to-purple-500 flex items-center justify-center">
          <User className="w-4 h-4 text-white" />
        </div>
        <ChevronDown className={`w-4 h-4 text-dark-300 transition-transform ${isOpen ? 'rotate-180' : ''}`} />
      </button>

      {isOpen && (
        <div className="absolute right-0 mt-2 w-56 glass rounded-xl p-2 shadow-xl border border-dark-700/50">
          <div className="px-3 py-2 border-b border-dark-700/50 mb-2">
            <p className="text-sm font-semibold text-white">Utilisateur</p>
            <p className="text-xs text-dark-400">user@example.com</p>
          </div>
          <Link
            href="/dashboard"
            className="flex items-center gap-3 px-3 py-2 rounded-lg hover:bg-dark-800/50 transition text-dark-300 hover:text-white"
            onClick={() => setIsOpen(false)}
          >
            <User className="w-4 h-4" />
            <span className="text-sm">Dashboard</span>
          </Link>
          <Link
            href="/settings"
            className="flex items-center gap-3 px-3 py-2 rounded-lg hover:bg-dark-800/50 transition text-dark-300 hover:text-white"
            onClick={() => setIsOpen(false)}
          >
            <Settings className="w-4 h-4" />
            <span className="text-sm">Paramètres</span>
          </Link>
          <Link
            href="/pricing"
            className="flex items-center gap-3 px-3 py-2 rounded-lg hover:bg-dark-800/50 transition text-dark-300 hover:text-white"
            onClick={() => setIsOpen(false)}
          >
            <CreditCard className="w-4 h-4" />
            <span className="text-sm">Abonnement</span>
          </Link>
          <div className="border-t border-dark-700/50 my-2"></div>
          <button
            className="w-full flex items-center gap-3 px-3 py-2 rounded-lg hover:bg-dark-800/50 transition text-dark-300 hover:text-red-400"
            onClick={() => setIsOpen(false)}
          >
            <LogOut className="w-4 h-4" />
            <span className="text-sm">Déconnexion</span>
          </button>
        </div>
      )}
    </div>
  )
}





