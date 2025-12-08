'use client'

import { use } from 'react'
import MainLayout from '@/components/layouts/MainLayout'
import APITester from '@/components/explore/APITester'
import APIStats from '@/components/explore/APIStats'
import { ArrowLeft, BookOpen, Code } from 'lucide-react'
import Link from 'next/link'

interface PageProps {
  params: Promise<{ api: string }>
}

export default function APIDetailPage({ params }: PageProps) {
  const { api } = use(params)

  return (
    <MainLayout>
      <div className="max-w-7xl mx-auto px-6 py-8">
        <Link
          href="/explore"
          className="inline-flex items-center gap-2 text-dark-400 hover:text-white transition mb-6"
        >
          <ArrowLeft className="w-4 h-4" />
          Retour à l'explorateur
        </Link>

        <div className="mb-8">
          <h1 className="text-4xl font-bold mb-4 gradient-text capitalize">{api}</h1>
          <p className="text-dark-400">Détails et test de l'API {api}</p>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          <div className="lg:col-span-2 space-y-6">
            <div className="card">
              <h2 className="text-2xl font-semibold mb-4 flex items-center gap-2">
                <Code className="w-6 h-6 text-indigo-400" />
                Tester l'API
              </h2>
              <APITester apiId={api} />
            </div>

            <div className="card">
              <h2 className="text-2xl font-semibold mb-4 flex items-center gap-2">
                <BookOpen className="w-6 h-6 text-indigo-400" />
                Documentation
              </h2>
              <p className="text-dark-400 mb-4">
                Endpoint: <code className="text-indigo-400">/api/{api}</code>
              </p>
              <p className="text-dark-300">
                Documentation complète disponible dans la section Docs.
              </p>
            </div>
          </div>

          <div className="lg:col-span-1">
            <APIStats apiId={api} />
          </div>
        </div>
      </div>
    </MainLayout>
  )
}





