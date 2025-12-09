'use client'

import { useState, KeyboardEvent } from 'react'
import { Send, Mic, Image as ImageIcon, Zap, BarChart3, Microscope } from 'lucide-react'

export type SearchMode = 'fast' | 'normal' | 'deep'

interface ChatInputProps {
  onSend: (message: string, mode: SearchMode) => void
  disabled?: boolean
}

const MODES = [
  {
    id: 'fast' as SearchMode,
    label: '⚡ Rapide',
    description: '< 1s - Réponse instantanée',
    icon: Zap,
    color: 'text-yellow-400',
    bgSelected: 'bg-yellow-500/20 border-yellow-500',
  },
  {
    id: 'normal' as SearchMode,
    label: '📊 Normal',
    description: '2-3s - Résultats équilibrés',
    icon: BarChart3,
    color: 'text-blue-400',
    bgSelected: 'bg-blue-500/20 border-blue-500',
  },
  {
    id: 'deep' as SearchMode,
    label: '🔬 Approfondi',
    description: '10-20s - Recherche complète (3000+ mots)',
    icon: Microscope,
    color: 'text-purple-400',
    bgSelected: 'bg-purple-500/20 border-purple-500',
  },
]

export default function ChatInput({ onSend, disabled = false }: ChatInputProps) {
  const [input, setInput] = useState('')
  const [mode, setMode] = useState<SearchMode>('normal')

  const handleSend = () => {
    if (input.trim() && !disabled) {
      onSend(input.trim(), mode)
      setInput('')
    }
  }

  const handleKeyDown = (e: KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      handleSend()
    }
  }

  const selectedMode = MODES.find(m => m.id === mode)!

  return (
    <div className="space-y-3">
      {/* Mode Selector - 3 Kings */}
      <div className="flex items-center gap-2 flex-wrap">
        <span className="text-xs text-dark-400 font-medium">Mode de recherche:</span>
        <div className="flex gap-1 flex-wrap">
          {MODES.map((m) => {
            const Icon = m.icon
            const isSelected = mode === m.id
            return (
              <button
                key={m.id}
                onClick={() => setMode(m.id)}
                disabled={disabled}
                className={`
                  flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-sm transition-all
                  border ${isSelected ? m.bgSelected : 'border-dark-600 hover:border-dark-500 bg-dark-800'}
                  ${disabled ? 'opacity-50 cursor-not-allowed' : 'cursor-pointer'}
                `}
                title={m.description}
              >
                <Icon className={`w-3.5 h-3.5 ${isSelected ? m.color : 'text-dark-400'}`} />
                <span className={isSelected ? m.color : 'text-dark-300'}>
                  {m.label}
                </span>
              </button>
            )
          })}
        </div>
      </div>

      {/* Mode Description */}
      <div className={`text-xs px-3 py-2 rounded-lg border ${selectedMode.bgSelected}`}>
        <span className={selectedMode.color}>{selectedMode.description}</span>
      </div>

      {/* Input Area */}
      <div className="flex gap-3">
        <div className="flex-1 relative">
          <textarea
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={handleKeyDown}
            placeholder="Posez votre question médicale..."
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
    </div>
  )
}

