'use client'

import { useState } from 'react'
import Link from 'next/link'
import MainLayout from '@/components/layouts/MainLayout'
import { useAuth } from '@/hooks/useAuth'
import { useRouter } from 'next/navigation'

export default function LoginPage() {
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState('')
  const { login } = useAuth()
  const router = useRouter()

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setError('')
    try {
      await login(email, password)
      router.push('/dashboard')
    } catch (err) {
      setError('Erreur de connexion')
    }
  }

  return (
    <MainLayout>
      <div className="max-w-md mx-auto px-6 py-16">
        <div className="text-center mb-8">
          <h1 className="text-4xl font-bold mb-4 gradient-text">Connexion</h1>
          <p className="text-dark-400">Connectez-vous à votre compte WikiAsk</p>
        </div>

        <form onSubmit={handleSubmit} className="card space-y-6">
          {error && (
            <div className="bg-red-500/10 border border-red-500/50 rounded-lg p-3 text-sm text-red-400">
              {error}
            </div>
          )}

          <div>
            <label className="block text-sm font-medium text-dark-300 mb-2">
              Email
            </label>
            <input
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
              className="input-dark w-full"
              placeholder="votre@email.com"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-dark-300 mb-2">
              Mot de passe
            </label>
            <input
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
              className="input-dark w-full"
              placeholder="••••••••"
            />
          </div>

          <button type="submit" className="btn-primary w-full">
            Se connecter
          </button>

          <div className="text-center text-sm text-dark-400">
            Pas encore de compte ?{' '}
            <Link href="/register" className="text-indigo-400 hover:text-indigo-300">
              S'inscrire
            </Link>
          </div>
        </form>
      </div>
    </MainLayout>
  )
}

