'use client'

import { useState, KeyboardEvent } from 'react'
import { Send, Mic, Image as ImageIcon } from 'lucide-react'

interface ChatInputProps {
  onSend: (message: string) => void
  disabled?: boolean
}

export default function ChatInput({ onSend, disabled = false }: ChatInputProps) {
  const [input, setInput] = useState('')

  const handleSend = () => {
    if (input.trim() && !disabled) {
      onSend(input.trim())
      setInput('')
    }
  }

  const handleKeyDown = (e: KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      handleSend()
    }
  }

  return (
    <div className="flex gap-3">
      <div className="flex-1 relative">
        <textarea
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder="Posez votre question..."
          className="input-dark w-full resize-none min-h-[60px] max-h-[200px] py-3 pr-20"
          disabled={disabled}
          rows={1}
        />
        <div className="absolute right-2 bottom-2 flex items-center gap-2">
          <button
            className="text-dark-400 hover:text-white transition"
            title="Recherche vocale"
          >
            <Mic className="w-4 h-4" />
          </button>
          <button
            className="text-dark-400 hover:text-white transition"
            title="Ajouter une image"
          >
            <ImageIcon className="w-4 h-4" />
          </button>
        </div>
      </div>
      <button
        onClick={handleSend}
        disabled={disabled || !input.trim()}
        className="btn-primary flex items-center gap-2 px-6 disabled:opacity-50 disabled:cursor-not-allowed"
      >
        <Send className="w-5 h-5" />
      </button>
    </div>
  )
}





