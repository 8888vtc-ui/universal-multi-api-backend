'use client'

import { useState } from 'react'
import { Play, Loader2 } from 'lucide-react'

interface APITesterProps {
  apiId: string
}

export default function APITester({ apiId }: APITesterProps) {
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState<any>(null)
  const [error, setError] = useState<string | null>(null)

  const handleTest = async () => {
    setLoading(true)
    setError(null)
    setResult(null)

    try {
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL || ''}/api/${apiId}`)
      const data = await response.json()
      setResult(data)
    } catch (err) {
      setError('Erreur lors du test')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div>
      <button
        onClick={handleTest}
        disabled={loading}
        className="w-full btn-secondary flex items-center justify-center gap-2 text-sm mb-3"
      >
        {loading ? (
          <>
            <Loader2 className="w-4 h-4 animate-spin" />
            Test en cours...
          </>
        ) : (
          <>
            <Play className="w-4 h-4" />
            Exécuter le test
          </>
        )}
      </button>

      {error && (
        <div className="bg-red-500/10 border border-red-500/50 rounded-lg p-3 text-sm text-red-400">
          {error}
        </div>
      )}

      {result && (
        <div className="bg-dark-800 rounded-lg p-3 max-h-48 overflow-auto">
          <pre className="text-xs text-dark-200 font-mono">
            {JSON.stringify(result, null, 2)}
          </pre>
        </div>
      )}
    </div>
  )
}




import { useState } from 'react'
import { Play, Loader2 } from 'lucide-react'

interface APITesterProps {
  apiId: string
}

export default function APITester({ apiId }: APITesterProps) {
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState<any>(null)
  const [error, setError] = useState<string | null>(null)

  const handleTest = async () => {
    setLoading(true)
    setError(null)
    setResult(null)

    try {
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL || ''}/api/${apiId}`)
      const data = await response.json()
      setResult(data)
    } catch (err) {
      setError('Erreur lors du test')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div>
      <button
        onClick={handleTest}
        disabled={loading}
        className="w-full btn-secondary flex items-center justify-center gap-2 text-sm mb-3"
      >
        {loading ? (
          <>
            <Loader2 className="w-4 h-4 animate-spin" />
            Test en cours...
          </>
        ) : (
          <>
            <Play className="w-4 h-4" />
            Exécuter le test
          </>
        )}
      </button>

      {error && (
        <div className="bg-red-500/10 border border-red-500/50 rounded-lg p-3 text-sm text-red-400">
          {error}
        </div>
      )}

      {result && (
        <div className="bg-dark-800 rounded-lg p-3 max-h-48 overflow-auto">
          <pre className="text-xs text-dark-200 font-mono">
            {JSON.stringify(result, null, 2)}
          </pre>
        </div>
      )}
    </div>
  )
}



