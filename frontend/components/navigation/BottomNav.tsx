'use client'

import Link from 'next/link'
import { usePathname } from 'next/navigation'
import { Search, Sparkles, MessageSquare, Globe, User } from 'lucide-react'

export default function BottomNav() {
  const pathname = usePathname()

  const navItems = [
    { href: '/search', icon: Search, label: 'Recherche' },
    { href: '/ai-search', icon: Sparkles, label: 'IA' },
    { href: '/chat', icon: MessageSquare, label: 'Chat' },
    { href: '/explore', icon: Globe, label: 'Explorer' },
    { href: '/dashboard', icon: User, label: 'Moi' },
  ]

  return (
    <nav className="md:hidden fixed bottom-0 left-0 right-0 border-t border-dark-700/50 backdrop-blur-xl bg-dark-900/50 z-50">
      <div className="flex items-center justify-around py-2">
        {navItems.map((item) => {
          const Icon = item.icon
          const isActive = pathname === item.href
          return (
            <Link
              key={item.href}
              href={item.href}
              className={`flex flex-col items-center gap-1 px-4 py-2 rounded-lg transition ${
                isActive
                  ? 'text-indigo-400'
                  : 'text-dark-400 hover:text-white'
              }`}
            >
              <Icon className="w-5 h-5" />
              <span className="text-xs">{item.label}</span>
            </Link>
          )
        })}
      </div>
    </nav>
  )
}





