'use client'

import MainLayout from '@/components/layouts/MainLayout'
import ChatInterface from '@/components/chat/ChatInterface'

export default function ChatPage() {
  return (
    <MainLayout>
      <div className="max-w-5xl mx-auto px-6 py-8">
        <div className="mb-8">
          <h1 className="text-4xl font-bold mb-4 gradient-text">Chat IA</h1>
          <p className="text-dark-400">Conversation avec 10 providers IA disponibles</p>
        </div>
        <ChatInterface />
      </div>
    </MainLayout>
  )
}





