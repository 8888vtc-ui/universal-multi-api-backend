'use client'

import { LucideIcon } from 'lucide-react'

interface StatsWidgetProps {
  title: string
  value: string | number
  max?: number
  icon: LucideIcon
  color?: 'indigo' | 'green' | 'purple' | 'blue' | 'red'
}

export default function StatsWidget({
  title,
  value,
  max,
  icon: Icon,
  color = 'indigo',
}: StatsWidgetProps) {
  const colorClasses = {
    indigo: 'text-indigo-400',
    green: 'text-green-400',
    purple: 'text-purple-400',
    blue: 'text-blue-400',
    red: 'text-red-400',
  }

  const percentage = max ? (typeof value === 'number' ? (value / max) * 100 : 0) : null

  return (
    <div className="card">
      <div className="flex items-center justify-between mb-4">
        <h3 className="text-sm font-medium text-dark-400">{title}</h3>
        <Icon className={`w-5 h-5 ${colorClasses[color]}`} />
      </div>
      <div className="mb-2">
        <div className="text-3xl font-bold gradient-text">{value}</div>
        {max && typeof value === 'number' && (
          <div className="text-sm text-dark-400 mt-1">
            {value} / {max}
          </div>
        )}
      </div>
      {percentage !== null && (
        <div className="w-full bg-dark-800 rounded-full h-2">
          <div
            className={`h-2 rounded-full bg-gradient-to-r ${
              color === 'indigo' ? 'from-indigo-500 to-purple-500' :
              color === 'green' ? 'from-green-500 to-emerald-500' :
              color === 'purple' ? 'from-purple-500 to-pink-500' :
              color === 'blue' ? 'from-blue-500 to-cyan-500' :
              'from-red-500 to-orange-500'
            }`}
            style={{ width: `${Math.min(percentage, 100)}%` }}
          />
        </div>
      )}
    </div>
  )
}





