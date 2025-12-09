'use client';

import { useState, useRef, useEffect } from 'react';
import ReactMarkdown from 'react-markdown';

// --- TYPES ---
type Domain = 'medical' | 'finance' | 'weather' | 'news' | 'general';
type Mode = 'normal' | 'thinking';

interface SearchState {
  status: 'idle' | 'loading' | 'success' | 'error';
  result: string;
  sources: string[];
  error?: string;
  wordCount?: number;
}

// --- CONFIG ---
const DOMAINS: { id: Domain; label: string; icon: string; expertId: string }[] = [
  { id: 'medical', label: 'Médical', icon: '🔬', expertId: 'health' },
  { id: 'finance', label: 'Finance', icon: '💰', expertId: 'finance' },
  { id: 'weather', label: 'Météo', icon: '☀️', expertId: 'weather' },
  { id: 'news', label: 'Actualités', icon: '📰', expertId: 'news' },
  { id: 'general', label: 'Général', icon: '🧠', expertId: 'general' },
];

const API_Base_URL = process.env.NEXT_PUBLIC_API_URL || '';

export default function Home() {
  // State
  const [domain, setDomain] = useState<Domain>('medical');
  const [mode, setMode] = useState<Mode>('normal');
  const [query, setQuery] = useState('');
  const [state, setState] = useState<SearchState>({ status: 'idle', result: '', sources: [] });

  // Refs
  const resultRef = useRef<HTMLDivElement>(null);

  // Scroll to result on success
  useEffect(() => {
    if (state.status === 'success' && resultRef.current) {
      resultRef.current.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }
  }, [state.status]);

  // Handlers
  const handleSearch = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!query.trim() || state.status === 'loading') return;

    setState({ status: 'loading', result: '', sources: [] });

    // Determine endpoint and payload
    const selectedDomain = DOMAINS.find(d => d.id === domain)!;
    const isThinkingMode = domain === 'medical' && mode === 'thinking';
    const payload = {
      message: query,
      language: 'fr',
      search_mode: isThinkingMode ? 'deep' : 'normal'
    };

    try {
      const res = await fetch(`${API_Base_URL}/api/expert/${selectedDomain.expertId}/chat`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(payload)
      });

      if (!res.ok) throw new Error('Erreur réseau');

      const data = await res.json();

      if (data.error) throw new Error(data.error);

      // Extract sources if available (often in data.sources or embedded in text)
      // The backend response format: { expert_id, expert_name, response, session_id }
      // Thinking mode might embed sources in text or return them separately depending on implementation.
      // Based on previous code, health expert returns sources in markdown or data.sources.

      let finalResult = data.response;
      // Add word count info for thinking mode if available
      if (isThinkingMode && data.word_count) {
        finalResult = `📊 **Rapport approfondi généré** (${data.word_count} mots)\n\n${finalResult}`;
      }

      setState({
        status: 'success',
        result: finalResult,
        sources: data.sources || [],
        wordCount: data.word_count
      });

    } catch (err: any) {
      setState({
        status: 'error',
        result: '',
        sources: [],
        error: err.message || "Une erreur est survenue. Veuillez réessayer."
      });
    }
  };

  return (
    <div className="max-w-4xl mx-auto px-4 py-8 md:py-16 min-h-screen flex flex-col items-center justify-center">

      {/* HEADER */}
      <header className="text-center mb-12 w-full animate-fade-in">
        <div className="inline-flex items-center justify-center w-16 h-16 rounded-2xl bg-indigo-500/10 mb-6 border border-indigo-500/20 shadow-[0_0_15px_rgba(99,102,241,0.3)]">
          <span className="text-4xl">🎯</span>
        </div>
        <h1 className="text-4xl md:text-6xl font-bold bg-gradient-to-r from-white via-indigo-200 to-indigo-400 bg-clip-text text-transparent mb-4">
          WikiAsk
        </h1>
        <p className="text-slate-400 text-lg md:text-xl font-light">
          Moteur de recherche IA intelligent
        </p>
      </header>

      {/* SEARCH CARD */}
      <div className="w-full glass-panel rounded-3xl p-6 md:p-8 shadow-2xl animate-fade-in" style={{ animationDelay: '0.1s' }}>
        <form onSubmit={handleSearch} className="space-y-8">

          {/* DOMAINE SELECTOR */}
          <div className="space-y-3">
            <label className="text-sm font-medium text-slate-400 uppercase tracking-wider pl-1">Domaine</label>
            <div className="relative">
              <select
                value={domain}
                onChange={(e) => {
                  const newDomain = e.target.value as Domain;
                  setDomain(newDomain);
                  if (newDomain !== 'medical') setMode('normal');
                }}
                className="w-full appearance-none bg-slate-900/50 border border-slate-700 rounded-xl px-5 py-4 text-white text-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent outline-none transition-all cursor-pointer hover:border-slate-600"
              >
                {DOMAINS.map(d => (
                  <option key={d.id} value={d.id}>
                    {d.icon} {d.label}
                  </option>
                ))}
              </select>
              <div className="absolute right-5 top-1/2 -translate-y-1/2 pointer-events-none text-slate-400">
                ▼
              </div>
            </div>
            {/* Quick Pills */}
            <div className="flex flex-wrap gap-2 pt-1">
              {DOMAINS.map(d => (
                <button
                  key={d.id}
                  type="button"
                  onClick={() => {
                    setDomain(d.id);
                    if (d.id !== 'medical') setMode('normal');
                  }}
                  className={`px-3 py-1.5 rounded-lg text-sm transition-all ${domain === d.id ? 'bg-indigo-600/30 text-indigo-300 border border-indigo-500/30' : 'bg-slate-800/50 text-slate-400 hover:bg-slate-800 border border-transparent'}`}
                >
                  {d.icon} {d.label}
                </button>
              ))}
            </div>
          </div>

          {/* MODE SELECTOR */}
          <div className="space-y-3">
            <label className="text-sm font-medium text-slate-400 uppercase tracking-wider pl-1">Mode d'analyse</label>
            <div className="grid grid-cols-2 gap-4">
              {/* NORMAL MODE */}
              <label className={`
                relative cursor-pointer rounded-xl p-4 border transition-all duration-200
                ${mode === 'normal'
                  ? 'bg-indigo-600/20 border-indigo-500 shadow-[0_0_15px_rgba(99,102,241,0.15)]'
                  : 'bg-slate-900/30 border-slate-800 hover:border-slate-700'}
              `}>
                <input
                  type="radio"
                  name="mode"
                  value="normal"
                  checked={mode === 'normal'}
                  onChange={() => setMode('normal')}
                  className="sr-only"
                />
                <div className="flex items-center gap-3">
                  <div className={`w-5 h-5 rounded-full border-2 flex items-center justify-center ${mode === 'normal' ? 'border-indigo-400' : 'border-slate-600'}`}>
                    {mode === 'normal' && <div className="w-2.5 h-2.5 rounded-full bg-indigo-400" />}
                  </div>
                  <div>
                    <div className="font-semibold text-white">Normal</div>
                    <div className="text-xs text-slate-400 mt-1">Réponse rapide ~2s</div>
                  </div>
                </div>
              </label>

              {/* THINKING MODE */}
              <label className={`
                relative rounded-xl p-4 border transition-all duration-200
                ${domain !== 'medical' ? 'opacity-50 cursor-not-allowed bg-slate-900/30 border-slate-800' : 'cursor-pointer'}
                ${mode === 'thinking' && domain === 'medical'
                  ? 'bg-purple-600/20 border-purple-500 shadow-[0_0_15px_rgba(168,85,247,0.15)]'
                  : domain === 'medical' ? 'bg-slate-900/30 border-slate-800 hover:border-purple-500/50' : ''}
              `}>
                <input
                  type="radio"
                  name="mode"
                  value="thinking"
                  checked={mode === 'thinking'}
                  onChange={() => setMode('thinking')}
                  disabled={domain !== 'medical'}
                  className="sr-only"
                />
                <div className="flex items-center gap-3">
                  <div className={`w-5 h-5 rounded-full border-2 flex items-center justify-center ${mode === 'thinking' ? 'border-purple-400' : 'border-slate-600'}`}>
                    {mode === 'thinking' && <div className="w-2.5 h-2.5 rounded-full bg-purple-400" />}
                  </div>
                  <div>
                    <div className="font-semibold text-white flex items-center gap-2">
                      Thinking <span className="text-lg">🧠</span>
                    </div>
                    <div className="text-xs text-slate-400 mt-1">Analyse profonde ~20s</div>
                  </div>
                </div>
                {domain !== 'medical' && (
                  <div className="absolute top-2 right-2 text-xs text-slate-500 bg-slate-900 px-2 py-1 rounded">
                    Médical uniquement
                  </div>
                )}
              </label>
            </div>
          </div>

          {/* INPUT AREA */}
          <div className="space-y-3">
            <label className="text-sm font-medium text-slate-400 uppercase tracking-wider pl-1">Votre question</label>
            <div className="relative">
              <textarea
                value={query}
                onChange={(e) => setQuery(e.target.value)}
                onKeyDown={(e) => {
                  if (e.key === 'Enter' && !e.shiftKey) {
                    e.preventDefault();
                    handleSearch(e);
                  }
                }}
                placeholder={
                  domain === 'medical' ? "Quels sont les traitements pour..." :
                    domain === 'finance' ? "Prix du Bitcoin..." :
                      domain === 'weather' ? "Météo à Paris..." :
                        "Posez votre question..."
                }
                className="w-full h-32 bg-slate-900/50 border border-slate-700 rounded-xl p-5 text-white text-lg placeholder-slate-600 focus:ring-2 focus:ring-indigo-500 focus:border-transparent outline-none transition-all resize-none"
              />
            </div>
          </div>

          {/* SUBMIT BUTTON */}
          <button
            type="submit"
            disabled={!query.trim() || state.status === 'loading'}
            className={`
              w-full py-4 rounded-xl font-bold text-lg text-white shadow-lg transition-all transform hover:-translate-y-0.5
              flex items-center justify-center gap-3
              ${!query.trim() || state.status === 'loading'
                ? 'bg-slate-800 text-slate-500 cursor-not-allowed shadow-none'
                : 'bg-gradient-to-r from-indigo-600 to-purple-600 hover:shadow-indigo-500/25'}
            `}
          >
            {state.status === 'loading' ? (
              <>
                <svg className="animate-spin h-6 w-6 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                  <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                  <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                </svg>
                <span>{domain === 'medical' && mode === 'thinking' ? "Analyse approfondie en cours..." : "Recherche en cours..."}</span>
              </>
            ) : (
              <>
                <span>🚀</span>
                <span>Lancer la recherche</span>
              </>
            )}
          </button>

          {/* Info text */}
          <p className="text-center text-xs text-slate-500">
            {domain === 'medical' && mode === 'thinking'
              ? "Le mode Thinking analyse jusqu'à 77 sources médicales. Cela prend jusqu'à 30 secondes."
              : "Le mode Normal fournit une réponse rapide basée sur nos connaissances."}
          </p>

        </form>
      </div>

      {/* RESULTS AREA */}
      {(state.status === 'success' || state.status === 'error') && (
        <div ref={resultRef} className="w-full mt-8 animate-fade-in">
          {state.status === 'error' ? (
            <div className="bg-red-500/10 border border-red-500/20 p-6 rounded-2xl text-red-200 text-center">
              <div className="text-3xl mb-2">⚠️</div>
              <p>{state.error}</p>
            </div>
          ) : (
            <div className="glass-panel p-8 rounded-3xl border border-white/10 shadow-2xl">
              <div className="prose prose-invert max-w-none">
                <ReactMarkdown>{state.result}</ReactMarkdown>
              </div>

              {/* Sources (if separate) */}
              {state.sources.length > 0 && (
                <div className="mt-8 pt-8 border-t border-slate-700/50">
                  <h3 className="text-sm font-bold text-slate-400 uppercase tracking-wider mb-4 flex items-center gap-2">
                    📚 Sources consultées
                  </h3>
                  <div className="flex flex-wrap gap-2">
                    {state.sources.map((source, i) => (
                      <span key={i} className="px-3 py-1 bg-slate-800 rounded-full text-xs text-slate-300 border border-slate-700">
                        {source}
                      </span>
                    ))}
                  </div>
                </div>
              )}

              <div className="mt-12 p-4 bg-yellow-500/5 border border-yellow-500/10 rounded-xl text-yellow-200/60 text-xs text-center">
                ⚠️ INFORMATION ÉDUCATIVE UNIQUEMENT. NE REMPLACE PAS UN AVIS MÉDICAL.
              </div>
            </div>
          )}
        </div>
      )}

      {/* FOOTER */}
      <footer className="mt-20 text-center space-y-2 opacity-60 hover:opacity-100 transition-opacity">
        <p className="text-slate-500 text-sm font-medium">⚠️ Version Beta — En cours de développement</p>
        <p className="text-slate-600 text-xs">© 2024 ECOFUN DRIVE (SASU) — France</p>
      </footer>

    </div>
  );
}
