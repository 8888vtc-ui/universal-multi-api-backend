'use client'

import { useState } from 'react'
import { Zap, BarChart3, Microscope } from 'lucide-react'

export type SearchMode = 'fast' | 'normal' | 'deep'

interface SearchModeSelectorProps {
    value: SearchMode
    onChange: (mode: SearchMode) => void
    disabled?: boolean
}

const MODES = [
    {
        id: 'fast' as SearchMode,
        label: 'Rapide',
        labelEn: 'Fast',
        icon: Zap,
        description: '< 1s',
        color: 'text-yellow-500',
        bgColor: 'bg-yellow-500/10',
        borderColor: 'border-yellow-500',
    },
    {
        id: 'normal' as SearchMode,
        label: 'Normal',
        labelEn: 'Normal',
        icon: BarChart3,
        description: '2-3s',
        color: 'text-blue-500',
        bgColor: 'bg-blue-500/10',
        borderColor: 'border-blue-500',
    },
    {
        id: 'deep' as SearchMode,
        label: 'Approfondi',
        labelEn: 'Deep',
        icon: Microscope,
        description: '10-20s',
        color: 'text-purple-500',
        bgColor: 'bg-purple-500/10',
        borderColor: 'border-purple-500',
    },
]

export default function SearchModeSelector({
    value,
    onChange,
    disabled = false
}: SearchModeSelectorProps) {
    return (
        <div className="flex items-center gap-1 p-1 bg-dark-800 rounded-lg border border-dark-700">
            {MODES.map((mode) => {
                const Icon = mode.icon
                const isSelected = value === mode.id

                return (
                    <button
                        key={mode.id}
                        onClick={() => !disabled && onChange(mode.id)}
                        disabled={disabled}
                        className={`
              flex items-center gap-2 px-3 py-2 rounded-md transition-all duration-200
              ${isSelected
                                ? `${mode.bgColor} ${mode.color} ${mode.borderColor} border font-medium`
                                : 'text-dark-400 hover:text-white hover:bg-dark-700'
                            }
              ${disabled ? 'opacity-50 cursor-not-allowed' : 'cursor-pointer'}
            `}
                        title={`${mode.label} - ${mode.description}`}
                    >
                        <Icon className="w-4 h-4" />
                        <span className="text-sm hidden sm:inline">{mode.label}</span>
                        <span className="text-xs opacity-60 hidden md:inline">({mode.description})</span>
                    </button>
                )
            })}
        </div>
    )
}

// Compact version for mobile
export function SearchModeSelectorCompact({
    value,
    onChange,
    disabled = false
}: SearchModeSelectorProps) {
    const selectedMode = MODES.find(m => m.id === value)!
    const Icon = selectedMode.icon

    return (
        <div className="relative">
            <select
                value={value}
                onChange={(e) => onChange(e.target.value as SearchMode)}
                disabled={disabled}
                className={`
          appearance-none pl-8 pr-4 py-2 rounded-lg 
          ${selectedMode.bgColor} ${selectedMode.color} 
          border ${selectedMode.borderColor}
          bg-dark-800 font-medium text-sm
          cursor-pointer focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-offset-dark-900
          ${disabled ? 'opacity-50 cursor-not-allowed' : ''}
        `}
            >
                {MODES.map((mode) => (
                    <option key={mode.id} value={mode.id}>
                        {mode.label} ({mode.description})
                    </option>
                ))}
            </select>
            <Icon className={`absolute left-2 top-1/2 -translate-y-1/2 w-4 h-4 ${selectedMode.color}`} />
        </div>
    )
}
