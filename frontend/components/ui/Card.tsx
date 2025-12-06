'use client'

import { ReactNode } from 'react'
import { clsx } from 'clsx'

interface CardProps {
  children: ReactNode
  className?: string
  hover?: boolean
}

export default function Card({ children, className, hover = false }: CardProps) {
  return (
    <div className={clsx('card', hover && 'card-hover', className)}>
      {children}
    </div>
  )
}

