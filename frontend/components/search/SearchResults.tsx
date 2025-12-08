'use client'

import ResultCard from './ResultCard'
import AISummary from './AISummary'
import ExportButton from '../ui/ExportButton'

interface SearchResultsProps {
  results: any
  query: string
}

export default function SearchResults({ results, query }: SearchResultsProps) {
  if (!results) return null

  return (
    <div className="space-y-6">
      {/* AI Summary if available */}
      {results.ai_summary && (
        <AISummary summary={results.ai_summary} />
      )}

      {/* Results in 3 columns */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Column 1: AI Synthesis */}
        <div className="lg:col-span-1">
          <h3 className="text-lg font-semibold text-white mb-4 flex items-center gap-2">
            <span className="w-2 h-2 rounded-full bg-indigo-400"></span>
            Synthèse IA
          </h3>
          {results.ai_results && results.ai_results.length > 0 ? (
            <div className="space-y-3">
              {results.ai_results.map((result: any, i: number) => (
                <ResultCard key={i} result={result} type="ai" />
              ))}
            </div>
          ) : (
            <div className="card text-center text-dark-400 py-8">
              <p>Aucun résultat IA</p>
            </div>
          )}
        </div>

        {/* Column 2: Web Results */}
        <div className="lg:col-span-1">
          <h3 className="text-lg font-semibold text-white mb-4 flex items-center gap-2">
            <span className="w-2 h-2 rounded-full bg-blue-400"></span>
            Résultats Web
          </h3>
          {results.web_results && results.web_results.length > 0 ? (
            <div className="space-y-3">
              {results.web_results.map((result: any, i: number) => (
                <ResultCard key={i} result={result} type="web" />
              ))}
            </div>
          ) : (
            <div className="card text-center text-dark-400 py-8">
              <p>Aucun résultat web</p>
            </div>
          )}
        </div>

        {/* Column 3: API Data */}
        <div className="lg:col-span-1">
          <h3 className="text-lg font-semibold text-white mb-4 flex items-center gap-2">
            <span className="w-2 h-2 rounded-full bg-purple-400"></span>
            Données APIs
          </h3>
          {results.api_results && results.api_results.length > 0 ? (
            <div className="space-y-3">
              {results.api_results.map((result: any, i: number) => (
                <ResultCard key={i} result={result} type="api" />
              ))}
            </div>
          ) : (
            <div className="card text-center text-dark-400 py-8">
              <p>Aucune donnée API</p>
            </div>
          )}
        </div>
      </div>

      {/* Export Button */}
      <div className="flex justify-end">
        <ExportButton data={results} filename={`search-${query}`} />
      </div>
    </div>
  )
}





