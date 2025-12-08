'use client'

import { ReactNode } from 'react'
import Header from '../navigation/Header'
import Footer from './Footer'

import CookieConsent from '../legal/CookieConsent'

interface MainLayoutProps {
  children: ReactNode
  showSidebar?: boolean
}

export default function MainLayout({ children, showSidebar = false }: MainLayoutProps) {
  return (
    <div className="min-h-screen flex flex-col">
      <Header />
      <main className="flex-1">
        {showSidebar ? (
          <div className="flex">
            <aside className="w-64 border-r border-dark-700/50 p-6">
              {/* Sidebar content will be added later */}
            </aside>
            <div className="flex-1">{children}</div>
          </div>
        ) : (
          children
        )}
      </main>
      <Footer />
      <CookieConsent />
    </div>
  )
}





