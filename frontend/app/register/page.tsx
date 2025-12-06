'use client'

import { useState } from 'react'
import Link from 'next/link'
import MainLayout from '@/components/layouts/MainLayout'
import { useRouter } from 'next/navigation'

export default function RegisterPage() {
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [confirmPassword, setConfirmPassword] = useState('')
  const [error, setError] = useState('')
  const router = useRouter()

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setError('')

    if (password !== confirmPassword) {
      setError('Les mots de passe ne correspondent pas')
      return
    }

    // TODO: Implement registration API call
    try {
      // Mock registration
      router.push('/login')
    } catch (err) {
      setError('Erreur lors de l\'inscription')
    }
  }

  return (
    <MainLayout>
      <div className="max-w-md mx-auto px-6 py-16">
        <div className="text-center mb-8">
          <h1 className="text-4xl font-bold mb-4 gradient-text">Inscription</h1>
          <p className="text-dark-400">Créez votre compte WikiAsk</p>
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

          <div>
            <label className="block text-sm font-medium text-dark-300 mb-2">
              Confirmer le mot de passe
            </label>
            <input
              type="password"
              value={confirmPassword}
              onChange={(e) => setConfirmPassword(e.target.value)}
              required
              className="input-dark w-full"
              placeholder="••••••••"
            />
          </div>

          <button type="submit" className="btn-primary w-full">
            S'inscrire
          </button>

          <div className="text-center text-sm text-dark-400">
            Déjà un compte ?{' '}
            <Link href="/login" className="text-indigo-400 hover:text-indigo-300">
              Se connecter
            </Link>
          </div>
        </form>
      </div>
    </MainLayout>
  )
}

