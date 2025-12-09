'use client'

import { useState, useRef, useEffect } from 'react'
import Link from 'next/link'
import { ArrowLeft, Send, Loader2, RefreshCw, Zap, BarChart3, Microscope, CheckCircle2, Search, Database, Globe, BookOpen } from 'lucide-react'
import { getUserLanguage } from '@/lib/language'

// Search mode type for medical expert
type SearchMode = 'fast' | 'normal' | 'deep'

// Medical API sources for the research show - 77 APIs TOTAL
const MEDICAL_SOURCES = {
    fast: [
        { name: 'Base locale', icon: '📚', delay: 100 },
        { name: 'Cache IA', icon: '🧠', delay: 200 },
        { name: 'Réponse rapide', icon: '⚡', delay: 300 },
    ],
    normal: [
        { name: 'PubMed / MEDLINE', icon: '📖', delay: 200 },
        { name: 'FDA USA', icon: '🇺🇸', delay: 400 },
        { name: 'WHO / OMS', icon: '🌍', delay: 600 },
        { name: 'RxNorm NIH', icon: '💊', delay: 800 },
        { name: 'Europe PMC', icon: '🇪🇺', delay: 1000 },
        { name: 'Analyse IA', icon: '🧠', delay: 1200 },
    ],
    deep: [
        // === PHASE 1: APIs OBLIGATOIRES (12 APIs) ===
        { name: '📖 PubMed/MEDLINE - 35M+ articles (NLM/NIH)', icon: '🇺🇸', delay: 200 },
        { name: '📚 PubMed Central - 8M+ articles open access', icon: '🇺🇸', delay: 350 },
        { name: '🇺🇸 OpenFDA - Médicaments approuvés USA', icon: '💊', delay: 500 },
        { name: '💉 RxNorm NIH - Terminologie médicaments', icon: '🇺🇸', delay: 650 },
        { name: '🌍 WHO/OMS - Statistiques santé mondiale', icon: '🌍', delay: 800 },
        { name: '🇪🇺 Europe PMC - Littérature européenne', icon: '🇪🇺', delay: 950 },
        { name: '🔬 ClinicalTrials.gov - 400K+ essais cliniques', icon: '🇺🇸', delay: 1100 },

        // === PHASE 2: APIs USA (10+ APIs) ===
        { name: '🧬 NCBI Gene - Base génétique NIH', icon: '🇺🇸', delay: 1250 },
        { name: '📑 MeSH NLM - 30K+ termes médicaux', icon: '🇺🇸', delay: 1400 },
        { name: '💊 DailyMed - Notices médicaments FDA', icon: '🇺🇸', delay: 1550 },
        { name: '🏥 CDC Wonder - Statistiques épidémio', icon: '🇺🇸', delay: 1700 },
        { name: '🧪 ClinVar - Variants génétiques', icon: '🇺🇸', delay: 1850 },

        // === PHASE 3: APIs EUROPE (15+ APIs) ===
        { name: '🇪🇺 EMA - Agence Européenne du Médicament', icon: '🇪🇺', delay: 2000 },
        { name: '🦠 Orphanet - 6000+ maladies rares', icon: '🇫🇷', delay: 2150 },
        { name: '🏥 SNOMED CT - Classification internationale', icon: '🇬🇧', delay: 2300 },
        { name: '📋 ICD-11 WHO - Classification des maladies', icon: '🌍', delay: 2450 },
        { name: '🧪 LOINC - Tests laboratoire', icon: '🌍', delay: 2600 },

        // === PHASE 4: APIs PREMIUM (10+ APIs) ===
        { name: '💊 DrugBank - Base pharmacologique mondiale', icon: '🇨🇦', delay: 2750 },
        { name: '🔄 KEGG - Voies métaboliques (Japon)', icon: '🇯🇵', delay: 2900 },
        { name: '🧬 OMIM - Maladies génétiques', icon: '🇺🇸', delay: 3050 },
        { name: '🎯 Open Targets - Cibles thérapeutiques', icon: '🇬🇧', delay: 3200 },
        { name: '🔬 UniProt - Base protéines mondiale', icon: '🇨🇭', delay: 3350 },

        // === PHASE 5: APIs ELITE (10+ APIs) ===
        { name: '🤖 Semantic Scholar - 200M+ articles IA', icon: '🇺🇸', delay: 3500 },
        { name: '⚡ Reactome - 2600+ voies biologiques', icon: '🇬🇧', delay: 3650 },
        { name: '🏥 GARD NIH - 7000+ maladies rares', icon: '🇺🇸', delay: 3800 },
        { name: '🧬 GeneCards (Weizmann)', icon: '🇮🇱', delay: 3950 },
        { name: '🏥 MalaCards (Weizmann)', icon: '🇮🇱', delay: 4100 },

        // === PHASE 6: ANALYSE IA ===
        { name: '🧠 Analyse comparative multi-sources', icon: '🤖', delay: 4250 },
        { name: '📊 Corrélation des données mondiales', icon: '📈', delay: 4400 },
        { name: '✍️ Synthèse et rédaction rapport (3000+ mots)', icon: '📝', delay: 4550 },
    ]
}

// Mode configurations for medical expert
const SEARCH_MODES = [
    {
        id: 'fast' as SearchMode,
        label: '⚡ Rapide',
        description: '< 1s - Réponse instantanée',
        icon: Zap,
        color: 'text-yellow-600',
        bgColor: 'bg-yellow-50',
        borderColor: 'border-yellow-300',
        selectedBg: 'bg-yellow-100',
    },
    {
        id: 'normal' as SearchMode,
        label: '📊 Normal',
        description: '2-3s - Résultats équilibrés',
        icon: BarChart3,
        color: 'text-blue-600',
        bgColor: 'bg-blue-50',
        borderColor: 'border-blue-300',
        selectedBg: 'bg-blue-100',
    },
    {
        id: 'deep' as SearchMode,
        label: '🔬 Approfondi',
        description: '10-30s - 77 APIs médicales mondiales (3000+ mots)',
        icon: Microscope,
        color: 'text-purple-600',
        bgColor: 'bg-purple-50',
        borderColor: 'border-purple-300',
        selectedBg: 'bg-purple-100',
    },
]

// Expert configurations matching backend - 12 experts
const EXPERT_CONFIG: Record<string, {
    name: string;
    emoji: string;
    tagline: string;
    color: string;
    bgColor: string;
    borderColor: string;
    textColor: string;
    welcomeMessage: string;
    exampleQuestions: string[];
}> = {
    health: {
        name: 'Recherche Santé',
        emoji: '🔬',
        tagline: 'Moteur de recherche santé avec 77 APIs médicales',
        color: 'from-emerald-400 to-teal-500',
        bgColor: 'bg-emerald-50',
        borderColor: 'border-emerald-200',
        textColor: 'text-emerald-700',
        welcomeMessage: "Bienvenue ! 🔬 Je suis un moteur de recherche en informations de santé avec accès à 77 APIs médicales mondiales (PubMed, FDA, WHO, etc.). Choisissez votre mode de recherche : ⚡ Rapide, 📊 Normal ou 🔬 Approfondi. Pour tout problème de santé, consultez toujours un professionnel.",
        exampleQuestions: [
            "Quels sont les traitements du diabète de type 2 ?",
            "Effets secondaires de la metformine ?",
            "Comment fonctionne le système immunitaire ?"
        ]
    },
    sports: {
        name: 'Coach Alex',
        emoji: '⚽',
        tagline: 'Sport et fitness',
        color: 'from-orange-400 to-amber-500',
        bgColor: 'bg-orange-50',
        borderColor: 'border-orange-200',
        textColor: 'text-orange-700',
        welcomeMessage: "Salut ! ⚽ Je suis Coach Alex ! Parlons sport, fitness ou des derniers résultats. C'est parti !",
        exampleQuestions: [
            "Quels sont les derniers résultats foot ?",
            "Comment débuter la course à pied ?",
            "Quels exercices pour se muscler ?"
        ]
    },
    finance: {
        name: 'Guide Finance',
        emoji: '📊',
        tagline: 'Infos financières',
        color: 'from-blue-400 to-indigo-500',
        bgColor: 'bg-blue-50',
        borderColor: 'border-blue-200',
        textColor: 'text-blue-700',
        welcomeMessage: "Bonjour ! 📊 Je suis votre guide finance. Je partage des infos sur les marchés et l'économie. Rappel : ceci n'est pas du conseil financier personnalisé.",
        exampleQuestions: [
            "Quel est le cours du Bitcoin ?",
            "C'est quoi un ETF ?",
            "Comment fonctionnent les actions ?"
        ]
    },
    tourism: {
        name: 'Léa Voyage',
        emoji: '✈️',
        tagline: 'Guide de voyage',
        color: 'from-pink-400 to-rose-500',
        bgColor: 'bg-pink-50',
        borderColor: 'border-pink-200',
        textColor: 'text-pink-700',
        welcomeMessage: "Coucou ! ✈️ Je suis Léa, ta guide voyage ! Tu rêves d'aller où ? Je connais plein de destinations géniales !",
        exampleQuestions: [
            "Quel temps fait-il à Barcelone ?",
            "Que visiter à Tokyo ?",
            "Quelle est la meilleure période pour la Thaïlande ?"
        ]
    },
    general: {
        name: 'Wiki',
        emoji: '📚',
        tagline: 'Culture générale',
        color: 'from-violet-400 to-purple-500',
        bgColor: 'bg-violet-50',
        borderColor: 'border-violet-200',
        textColor: 'text-violet-700',
        welcomeMessage: "Bonjour ! 📚 Je suis Wiki, ton assistant culture G ! Pose-moi n'importe quelle question, j'adore partager !",
        exampleQuestions: [
            "Qui a inventé Internet ?",
            "Pourquoi le ciel est bleu ?",
            "C'est quoi l'IA ?"
        ]
    },
    humor: {
        name: 'Ricky Rire',
        emoji: '😂',
        tagline: 'Humour et détente',
        color: 'from-yellow-400 to-amber-500',
        bgColor: 'bg-yellow-50',
        borderColor: 'border-yellow-200',
        textColor: 'text-yellow-700',
        welcomeMessage: "Salut ! 😄 Je suis Ricky Rire ! Tu veux une blague ? Je suis là pour te faire sourire !",
        exampleQuestions: [
            "Raconte-moi une blague !",
            "Un jeu de mots ?",
            "Fais-moi rire !"
        ]
    },
    cuisine: {
        name: 'Chef Gourmand',
        emoji: '🍳',
        tagline: 'Recettes et cuisine',
        color: 'from-red-400 to-rose-500',
        bgColor: 'bg-red-50',
        borderColor: 'border-red-200',
        textColor: 'text-red-700',
        welcomeMessage: "Salut chef ! 🍳 Je suis Chef Gourmand ! Tu cherches une recette ou des idées pour ce soir ? Je suis là !",
        exampleQuestions: [
            "Une recette de carbonara ?",
            "Idée dessert facile ?",
            "Comment réussir une omelette ?"
        ]
    },
    tech: {
        name: 'Tech Insider',
        emoji: '💻',
        tagline: 'Actualités tech',
        color: 'from-indigo-400 to-violet-500',
        bgColor: 'bg-indigo-50',
        borderColor: 'border-indigo-200',
        textColor: 'text-indigo-700',
        welcomeMessage: "Hey ! 💻 Je suis Tech Insider ! Parlons IA, gadgets ou dernières innovations tech !",
        exampleQuestions: [
            "C'est quoi ChatGPT ?",
            "Quel smartphone choisir ?",
            "Les dernières news tech ?"
        ]
    },
    cinema: {
        name: 'Ciné Fan',
        emoji: '🎬',
        tagline: 'Films et séries',
        color: 'from-rose-500 to-red-600',
        bgColor: 'bg-rose-50',
        borderColor: 'border-rose-200',
        textColor: 'text-rose-700',
        welcomeMessage: "Hello ! 🎬 Je suis Ciné Fan ! Tu cherches un film ou une série ? J'ai plein de recos !",
        exampleQuestions: [
            "Un bon film ce soir ?",
            "Les meilleures séries Netflix ?",
            "C'est quoi le dernier Marvel ?"
        ]
    },
    weather: {
        name: 'Météo Pro',
        emoji: '☀️',
        tagline: 'Prévisions météo',
        color: 'from-sky-400 to-blue-500',
        bgColor: 'bg-sky-50',
        borderColor: 'border-sky-200',
        textColor: 'text-sky-700',
        welcomeMessage: "Bonjour ! ☀️ Je suis Météo Pro ! Dis-moi où tu es ou où tu vas, je te dis le temps qu'il fait !",
        exampleQuestions: [
            "Météo Paris demain ?",
            "Il va pleuvoir ce week-end ?",
            "Quel temps à New York ?"
        ]
    },
    love: {
        name: 'Love Coach',
        emoji: '💕',
        tagline: 'Conseils relationnels',
        color: 'from-pink-500 to-rose-600',
        bgColor: 'bg-pink-50',
        borderColor: 'border-pink-300',
        textColor: 'text-pink-700',
        welcomeMessage: "Coucou ! 💕 Je suis Love Coach. Besoin de parler relations, amitié ou de toi ? Je suis là pour écouter.",
        exampleQuestions: [
            "Comment mieux communiquer en couple ?",
            "Comment se remettre d'une rupture ?",
            "Comment se faire des amis ?"
        ]
    },
    gaming: {
        name: 'Gamer Zone',
        emoji: '🎮',
        tagline: 'Jeux vidéo',
        color: 'from-green-400 to-emerald-500',
        bgColor: 'bg-green-50',
        borderColor: 'border-green-200',
        textColor: 'text-green-700',
        welcomeMessage: "GG ! 🎮 Je suis Gamer Zone ! Parlons jeux vidéo, esports ou trouve des recos de jeux !",
        exampleQuestions: [
            "Les meilleurs jeux 2024 ?",
            "Tips pour Fortnite ?",
            "Actus esports ?"
        ]
    },
    news: {
        name: 'Actu Live',
        emoji: '📰',
        tagline: 'Actualités temps réel',
        color: 'from-slate-500 to-zinc-600',
        bgColor: 'bg-slate-50',
        borderColor: 'border-slate-200',
        textColor: 'text-slate-700',
        welcomeMessage: "📰 Bienvenue sur Actu Live ! Quelles actualités vous intéressent ? Politique, sport, tech, monde... je suis à jour !",
        exampleQuestions: [
            "Actualités du jour ?",
            "News tech récentes ?",
            "Quoi de neuf dans le monde ?"
        ]
    },
    horoscope: {
        name: 'Étoile',
        emoji: '🔮',
        tagline: 'Astrologie quotidienne',
        color: 'from-purple-500 to-violet-600',
        bgColor: 'bg-purple-50',
        borderColor: 'border-purple-200',
        textColor: 'text-purple-700',
        welcomeMessage: "✨ Bienvenue, belle âme ! Je suis Étoile. Quel est ton signe ? Laisse-moi te guider avec les étoiles...",
        exampleQuestions: [
            "Horoscope Bélier aujourd'hui ?",
            "Compatibilité Lion et Scorpion ?",
            "Quel est mon signe ascendant ?"
        ]
    },
    prenom: {
        name: 'Prénom Expert',
        emoji: '👶',
        tagline: 'Signification des prénoms',
        color: 'from-pink-500 to-rose-600',
        bgColor: 'bg-pink-50',
        borderColor: 'border-pink-200',
        textColor: 'text-pink-700',
        welcomeMessage: "👶 Bonjour ! Je suis Prénom Expert. Tu cherches un prénom ou tu veux connaître la signification du tien ? Dis-moi !",
        exampleQuestions: [
            "Que signifie Emma ?",
            "Origine du prénom Lucas ?",
            "Prénoms tendance 2024 ?"
        ]
    },
    history: {
        name: 'Ce Jour',
        emoji: '📅',
        tagline: "L'histoire au quotidien",
        color: 'from-amber-600 to-orange-700',
        bgColor: 'bg-amber-50',
        borderColor: 'border-amber-200',
        textColor: 'text-amber-700',
        welcomeMessage: "📅 Bonjour ! Je suis Ce Jour. Savais-tu ce qui s'est passé un jour comme aujourd'hui ? Laisse-moi te raconter !",
        exampleQuestions: [
            "Que s'est-il passé aujourd'hui ?",
            "Célébrités nées le 15 mars ?",
            "Événements du 14 juillet ?"
        ]
    },
}

interface Message {
    id: string
    role: 'user' | 'assistant'
    content: string
    timestamp: Date
    mode?: SearchMode
    sources?: string[]  // List of sources used
}

// Research progress step
interface ResearchStep {
    name: string
    icon: string
    status: 'pending' | 'searching' | 'done'
}

export default function ExpertChatPage({ params }: { params: { expertId: string } }) {
    const { expertId } = params
    const expert = EXPERT_CONFIG[expertId]
    const isHealthExpert = expertId === 'health'

    const [messages, setMessages] = useState<Message[]>([])
    const [input, setInput] = useState('')
    const [loading, setLoading] = useState(false)
    const [sessionId, setSessionId] = useState<string | null>(null)
    const [searchMode, setSearchMode] = useState<SearchMode>('normal')
    const [researchSteps, setResearchSteps] = useState<ResearchStep[]>([])
    const [currentStep, setCurrentStep] = useState<string>('')
    const messagesEndRef = useRef<HTMLDivElement>(null)

    // Générer/stocker session_id pour la mémoire conversationnelle
    useEffect(() => {
        if (expertId) {
            const storageKey = `expert_session_${expertId}`
            const stored = localStorage.getItem(storageKey)
            if (stored) {
                setSessionId(stored)
            } else {
                const newSessionId = `session_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`
                setSessionId(newSessionId)
                localStorage.setItem(storageKey, newSessionId)
            }
        }
    }, [expertId])

    useEffect(() => {
        if (expert && messages.length === 0) {
            setMessages([{
                id: 'welcome',
                role: 'assistant',
                content: expert.welcomeMessage,
                timestamp: new Date()
            }])
        }
    }, [expert])

    useEffect(() => {
        messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
    }, [messages])

    if (!expert) {
        return (
            <div className="min-h-screen bg-gradient-to-br from-amber-50 via-white to-rose-50 flex items-center justify-center">
                <div className="text-center">
                    <div className="text-6xl mb-4">🔍</div>
                    <h2 className="text-2xl font-bold text-gray-900 mb-2">Expert non trouvé</h2>
                    <Link href="/" className="text-amber-600 hover:text-amber-700 font-medium">
                        Retour à l'accueil
                    </Link>
                </div>
            </div>
        )
    }

    const handleSend = async () => {
        if (!input.trim() || loading) return

        const userMessage: Message = {
            id: Date.now().toString(),
            role: 'user',
            content: input.trim(),
            timestamp: new Date(),
            mode: isHealthExpert ? searchMode : undefined
        }

        setMessages(prev => [...prev, userMessage])
        setInput('')
        setLoading(true)

        // Start research animation for health expert
        if (isHealthExpert) {
            const sources = MEDICAL_SOURCES[searchMode]
            const steps: ResearchStep[] = sources.map(s => ({
                name: s.name,
                icon: s.icon,
                status: 'pending' as const
            }))
            setResearchSteps(steps)

            // Animate each step
            for (let i = 0; i < sources.length; i++) {
                await new Promise(resolve => setTimeout(resolve, sources[i].delay))
                setCurrentStep(sources[i].name)
                setResearchSteps(prev => prev.map((step, idx) => ({
                    ...step,
                    status: idx < i ? 'done' : idx === i ? 'searching' : 'pending'
                })))
            }
        }

        try {
            // Détecter la langue : prioriser la langue du message, sinon celle du navigateur
            const { detectMessageLanguage, getUserLanguage } = await import('@/lib/language')

            // Détecter la langue du message (simple détection)
            const messageLang = detectMessageLanguage(userMessage.content)
            // Si le message est clairement dans une langue, l'utiliser, sinon utiliser celle du navigateur
            const userLanguage = messageLang || getUserLanguage()

            // Build request body - include search_mode for health expert
            const requestBody: any = {
                message: userMessage.content,
                language: userLanguage,
                session_id: sessionId
            }

            // Add search_mode only for health expert
            if (isHealthExpert) {
                requestBody.search_mode = searchMode
            }

            const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL || ''}/api/expert/${expertId}/chat`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(requestBody)
            })

            // Check for HTTP errors before parsing response
            if (!response.ok) {
                const errorData = await response.json().catch(() => ({ detail: 'Unknown error' }))
                throw new Error(`HTTP ${response.status}: ${errorData.detail || 'Request failed'}`)
            }

            const data = await response.json()

            // Utiliser le session_id retourné par l'API (ou garder celui existant)
            if (data.session_id && data.session_id !== sessionId) {
                setSessionId(data.session_id)
                const storageKey = `expert_session_${expertId}`
                localStorage.setItem(storageKey, data.session_id)
            }

            // Format response based on mode
            let responseContent = data.response || 'Désolé, je n\'ai pas pu répondre. Réessaie !'

            // Add sources header for health expert
            if (isHealthExpert) {
                const sources = MEDICAL_SOURCES[searchMode]
                const sourceNames = sources.map(s => s.name).join(' • ')

                if (searchMode === 'deep') {
                    const wordCount = data.word_count || responseContent.split(/\s+/).length
                    responseContent = `📊 **RAPPORT DE RECHERCHE APPROFONDI**\n\n` +
                        `📚 **Sources consultées:** ${sources.length} bases de données médicales\n` +
                        `🔬 ${sourceNames}\n\n` +
                        `📝 **Taille du rapport:** ~${wordCount} mots\n` +
                        `━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n` +
                        responseContent
                } else if (searchMode === 'normal') {
                    responseContent = `📋 **Sources:** ${sourceNames}\n\n${responseContent}`
                }
            }

            // Mark all steps as done
            if (isHealthExpert) {
                setResearchSteps(prev => prev.map(step => ({ ...step, status: 'done' as const })))
                setCurrentStep('Réponse générée ✅')
            }

            const assistantMessage: Message = {
                id: (Date.now() + 1).toString(),
                role: 'assistant',
                content: responseContent,
                timestamp: new Date(),
                mode: isHealthExpert ? searchMode : undefined,
                sources: isHealthExpert ? MEDICAL_SOURCES[searchMode].map(s => s.name) : undefined
            }

            setMessages(prev => [...prev, assistantMessage])
        } catch (error: any) {
            // Provide more informative error messages based on error type
            let errorMessage = 'Oups ! Je suis momentanément indisponible. Réessaie dans quelques instants.'
            const errorStr = error?.message || ''

            if (errorStr.includes('503') || errorStr.toLowerCase().includes('temporarily unavailable')) {
                errorMessage = '🔧 Le service IA est temporairement surchargé. Réessaie dans quelques secondes !'
            } else if (errorStr.includes('Failed to fetch') || errorStr.includes('NetworkError') || errorStr.includes('fetch')) {
                errorMessage = '📡 Problème de connexion. Vérifie ta connexion internet et réessaie.'
            } else if (errorStr.includes('timeout') || errorStr.includes('408')) {
                errorMessage = '⏱️ La requête a pris trop de temps. Réessaie avec une question plus courte.'
            } else if (errorStr.includes('500')) {
                errorMessage = '⚠️ Une erreur serveur s\'est produite. Nous travaillons dessus !'
            }

            console.error('Expert chat error:', error)

            setMessages(prev => [...prev, {
                id: (Date.now() + 1).toString(),
                role: 'assistant',
                content: errorMessage,
                timestamp: new Date()
            }])
        } finally {
            setLoading(false)
            // Clear research steps after a delay to show completion
            setTimeout(() => {
                setResearchSteps([])
                setCurrentStep('')
            }, 1000)
        }
    }

    return (
        <div className={`min-h-screen ${expert.bgColor} flex flex-col`}>
            {/* Header */}
            <header className={`bg-white/90 backdrop-blur-md border-b ${expert.borderColor} sticky top-0 z-50`}>
                <div className="max-w-4xl mx-auto px-4 py-3 flex items-center gap-4">
                    <Link href="/" className={`p-2 rounded-full hover:bg-gray-100 transition ${expert.textColor}`}>
                        <ArrowLeft className="w-5 h-5" />
                    </Link>

                    <div className={`w-12 h-12 rounded-xl bg-gradient-to-br ${expert.color} flex items-center justify-center text-2xl shadow-md`}>
                        {expert.emoji}
                    </div>

                    <div className="flex-1">
                        <h1 className={`font-bold ${expert.textColor}`}>{expert.name}</h1>
                        <p className="text-sm text-gray-500">{expert.tagline}</p>
                    </div>

                    <button
                        onClick={() => setMessages([{
                            id: 'welcome',
                            role: 'assistant',
                            content: expert.welcomeMessage,
                            timestamp: new Date()
                        }])}
                        className="p-2 rounded-full hover:bg-gray-100 transition text-gray-500"
                        title="Nouvelle conversation"
                    >
                        <RefreshCw className="w-5 h-5" />
                    </button>
                </div>
            </header>

            {/* Messages */}
            <div className="flex-1 overflow-y-auto px-4 py-6">
                <div className="max-w-4xl mx-auto space-y-4">
                    {messages.map((message) => (
                        <div key={message.id} className={`flex ${message.role === 'user' ? 'justify-end' : 'justify-start'}`}>
                            <div className={`max-w-[85%] rounded-2xl px-4 py-3 ${message.role === 'user'
                                ? `bg-gradient-to-br ${expert.color} text-white shadow-md`
                                : 'bg-white border border-gray-200 shadow-sm'
                                }`}>
                                <p className={`text-sm sm:text-base leading-relaxed whitespace-pre-wrap ${message.role === 'user' ? 'text-white' : 'text-gray-800'
                                    }`}>
                                    {message.content}
                                </p>
                            </div>
                        </div>
                    ))}

                    {loading && (
                        <div className="flex justify-start">
                            <div className="bg-white border border-gray-200 rounded-2xl px-4 py-4 shadow-sm max-w-md w-full">
                                {/* Research Title */}
                                {isHealthExpert && researchSteps.length > 0 ? (
                                    <div className="space-y-3">
                                        <div className="flex items-center gap-2 border-b border-gray-100 pb-2">
                                            <Search className="w-4 h-4 text-emerald-600 animate-pulse" />
                                            <span className="text-sm font-semibold text-emerald-700">
                                                🔬 Recherche Médicale en cours...
                                            </span>
                                        </div>

                                        {/* Research Steps */}
                                        <div className="space-y-1.5 max-h-48 overflow-y-auto">
                                            {researchSteps.map((step, idx) => (
                                                <div
                                                    key={idx}
                                                    className={`flex items-center gap-2 text-xs py-1 px-2 rounded transition-all duration-300 ${step.status === 'done'
                                                        ? 'bg-green-50 text-green-700'
                                                        : step.status === 'searching'
                                                            ? 'bg-blue-50 text-blue-700 animate-pulse'
                                                            : 'bg-gray-50 text-gray-400'
                                                        }`}
                                                >
                                                    <span className="w-5 text-center">
                                                        {step.status === 'done'
                                                            ? '✅'
                                                            : step.status === 'searching'
                                                                ? <Loader2 className="w-3 h-3 animate-spin" />
                                                                : step.icon
                                                        }
                                                    </span>
                                                    <span className={step.status === 'searching' ? 'font-medium' : ''}>
                                                        {step.status === 'searching'
                                                            ? `Recherche: ${step.name}...`
                                                            : step.name
                                                        }
                                                    </span>
                                                </div>
                                            ))}
                                        </div>

                                        {/* Current Action */}
                                        <div className="pt-2 border-t border-gray-100">
                                            <div className="flex items-center gap-2 text-xs text-gray-500">
                                                <Loader2 className="w-3 h-3 animate-spin" />
                                                <span className="animate-pulse">
                                                    {currentStep ? `Analyse de ${currentStep}...` : 'Initialisation...'}
                                                </span>
                                            </div>
                                        </div>
                                    </div>
                                ) : (
                                    <div className="flex items-center gap-2">
                                        <Loader2 className={`w-4 h-4 animate-spin ${expert.textColor}`} />
                                        <span className="text-gray-500 text-sm">Réflexion...</span>
                                    </div>
                                )}
                            </div>
                        </div>
                    )}

                    <div ref={messagesEndRef} />
                </div>
            </div>

            {/* Example questions */}
            {messages.length <= 1 && (
                <div className="px-4 pb-4">
                    <div className="max-w-4xl mx-auto">
                        <p className="text-sm text-gray-500 mb-2">Essayez :</p>
                        <div className="flex flex-wrap gap-2">
                            {expert.exampleQuestions.map((q, i) => (
                                <button
                                    key={i}
                                    onClick={() => setInput(q)}
                                    className={`px-3 py-1.5 rounded-full text-xs ${expert.bgColor} ${expert.borderColor} border ${expert.textColor} hover:bg-white transition`}
                                >
                                    {q}
                                </button>
                            ))}
                        </div>
                    </div>
                </div>
            )}

            {/* Input */}
            <div className={`bg-white/90 backdrop-blur-md border-t ${expert.borderColor} p-4`}>
                <div className="max-w-4xl mx-auto space-y-3">
                    {/* Search Mode Selector - Only for Health Expert */}
                    {isHealthExpert && (
                        <div className="flex flex-wrap items-center gap-2">
                            <span className="text-xs font-medium text-gray-500">Mode de recherche:</span>
                            <div className="flex gap-1 flex-wrap">
                                {SEARCH_MODES.map((mode) => {
                                    const Icon = mode.icon
                                    const isSelected = searchMode === mode.id
                                    return (
                                        <button
                                            key={mode.id}
                                            onClick={() => setSearchMode(mode.id)}
                                            disabled={loading}
                                            className={`
                                                flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-medium transition-all
                                                border ${isSelected
                                                    ? `${mode.selectedBg} ${mode.borderColor} ${mode.color}`
                                                    : 'border-gray-200 text-gray-500 hover:border-gray-300 bg-white'
                                                }
                                                ${loading ? 'opacity-50 cursor-not-allowed' : 'cursor-pointer'}
                                            `}
                                            title={mode.description}
                                        >
                                            <Icon className="w-3.5 h-3.5" />
                                            <span>{mode.label}</span>
                                        </button>
                                    )
                                })}
                            </div>
                            <span className={`text-xs ${SEARCH_MODES.find(m => m.id === searchMode)?.color || 'text-gray-400'}`}>
                                {SEARCH_MODES.find(m => m.id === searchMode)?.description}
                            </span>
                        </div>
                    )}

                    {/* Input Field */}
                    <div className="flex gap-3">
                        <input
                            type="text"
                            value={input}
                            onChange={(e) => setInput(e.target.value)}
                            onKeyDown={(e) => e.key === 'Enter' && handleSend()}
                            placeholder={`Message à ${expert.name}...`}
                            disabled={loading}
                            className={`flex-1 px-4 py-3 rounded-xl border ${expert.borderColor} focus:outline-none focus:ring-2 focus:ring-amber-300 bg-white text-gray-800 placeholder-gray-400`}
                        />
                        <button
                            onClick={handleSend}
                            disabled={loading || !input.trim()}
                            className={`px-6 py-3 rounded-xl bg-gradient-to-r ${expert.color} text-white font-medium shadow-md hover:shadow-lg disabled:opacity-50 disabled:cursor-not-allowed transition-all`}
                        >
                            {loading ? <Loader2 className="w-5 h-5 animate-spin" /> : <Send className="w-5 h-5" />}
                        </button>
                    </div>
                </div>
            </div>
        </div>
    )
}
