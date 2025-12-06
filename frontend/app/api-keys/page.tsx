'use client'

import { useState } from 'react'
import MainLayout from '@/components/layouts/MainLayout'
import { Key, Plus, Copy, Trash2, Eye, EyeOff } from 'lucide-react'

interface APIKey {
  id: string
  name: string
  key: string
  created: string
  lastUsed?: string
}

export default function APIKeysPage() {
  const [keys, setKeys] = useState<APIKey[]>([])
  const [showKey, setShowKey] = useState<Record<string, boolean>>({})
  const [showCreateModal, setShowCreateModal] = useState(false)
  const [newKeyName, setNewKeyName] = useState('')

  const generateKey = () => {
    return `aska_${Math.random().toString(36).substring(2, 15)}${Math.random().toString(36).substring(2, 15)}`
  }

  const handleCreate = () => {
    if (!newKeyName.trim()) return

    const newKey: APIKey = {
      id: Date.now().toString(),
      name: newKeyName,
      key: generateKey(),
      created: new Date().toISOString(),
    }

    setKeys(prev => [...prev, newKey])
    setNewKeyName('')
    setShowCreateModal(false)
  }

  const handleCopy = (key: string) => {
    navigator.clipboard.writeText(key)
  }

  const handleDelete = (id: string) => {
    setKeys(prev => prev.filter(k => k.id !== id))
  }

  return (
    <MainLayout>
      <div className="max-w-4xl mx-auto px-6 py-8">
        <div className="mb-8 flex items-center justify-between">
          <div>
            <h1 className="text-4xl font-bold mb-4 gradient-text">Clés API</h1>
            <p className="text-dark-400">Gérez vos clés API pour accéder à WikiAsk</p>
          </div>
          <button
            onClick={() => setShowCreateModal(true)}
            className="btn-primary flex items-center gap-2"
          >
            <Plus className="w-5 h-5" />
            Créer une clé
          </button>
        </div>

        {keys.length === 0 ? (
          <div className="card text-center py-12">
            <Key className="w-16 h-16 mx-auto mb-4 opacity-50 text-dark-400" />
            <p className="text-dark-400 mb-4">Aucune clé API</p>
            <button onClick={() => setShowCreateModal(true)} className="btn-primary">
              Créer votre première clé
            </button>
          </div>
        ) : (
          <div className="space-y-4">
            {keys.map((key) => (
              <div key={key.id} className="card">
                <div className="flex items-start justify-between">
                  <div className="flex-1">
                    <h3 className="font-semibold text-white mb-2">{key.name}</h3>
                    <div className="flex items-center gap-2 mb-2">
                      <code className="text-sm text-dark-300 bg-dark-800 px-3 py-1 rounded">
                        {showKey[key.id] ? key.key : '••••••••••••••••••••••••'}
                      </code>
                      <button
                        onClick={() => setShowKey(prev => ({ ...prev, [key.id]: !prev[key.id] }))}
                        className="text-dark-400 hover:text-white transition"
                      >
                        {showKey[key.id] ? <EyeOff className="w-4 h-4" /> : <Eye className="w-4 h-4" />}
                      </button>
                      <button
                        onClick={() => handleCopy(key.key)}
                        className="text-dark-400 hover:text-white transition"
                        title="Copier"
                      >
                        <Copy className="w-4 h-4" />
                      </button>
                    </div>
                    <p className="text-xs text-dark-400">
                      Créée le {new Date(key.created).toLocaleDateString('fr-FR')}
                    </p>
                  </div>
                  <button
                    onClick={() => handleDelete(key.id)}
                    className="text-dark-400 hover:text-red-400 transition"
                  >
                    <Trash2 className="w-5 h-5" />
                  </button>
                </div>
              </div>
            ))}
          </div>
        )}

        {/* Create Modal */}
        {showCreateModal && (
          <div className="fixed inset-0 z-50 flex items-center justify-center p-4">
            <div
              className="absolute inset-0 bg-black/50 backdrop-blur-sm"
              onClick={() => setShowCreateModal(false)}
            />
            <div className="relative glass rounded-2xl p-6 max-w-md w-full">
              <h2 className="text-2xl font-bold mb-4 text-white">Créer une clé API</h2>
              <div className="space-y-4">
                <div>
                  <label className="block text-sm font-medium text-dark-300 mb-2">
                    Nom de la clé
                  </label>
                  <input
                    type="text"
                    value={newKeyName}
                    onChange={(e) => setNewKeyName(e.target.value)}
                    placeholder="Ma clé API"
                    className="input-dark w-full"
                    autoFocus
                  />
                </div>
                <div className="flex gap-3">
                  <button
                    onClick={handleCreate}
                    className="btn-primary flex-1"
                  >
                    Créer
                  </button>
                  <button
                    onClick={() => setShowCreateModal(false)}
                    className="btn-secondary"
                  >
                    Annuler
                  </button>
                </div>
              </div>
            </div>
          </div>
        )}
      </div>
    </MainLayout>
  )
}

