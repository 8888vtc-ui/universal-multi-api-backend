'use client'

import { useState, useRef, useEffect } from 'react'
import Link from 'next/link'
import { ArrowLeft, Send, Loader2, RefreshCw } from 'lucide-react'

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
        tagline: 'Moteur de recherche santé',
        color: 'from-emerald-400 to-teal-500',
        bgColor: 'bg-emerald-50',
        borderColor: 'border-emerald-200',
        textColor: 'text-emerald-700',
        welcomeMessage: "Bienvenue ! 🔬 Je suis un moteur de recherche en informations de santé. Je peux vous aider à trouver des informations générales. Pour tout problème de santé, consultez toujours un professionnel.",
        exampleQuestions: [
            "Quels sont les bienfaits du sommeil ?",
            "C'est quoi une alimentation équilibrée ?",
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
    // 4 New high-traffic experts
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
}

export default function ExpertChatPage({ params }: { params: { expertId: string } }) {
    const { expertId } = params
    const expert = EXPERT_CONFIG[expertId]

    const [messages, setMessages] = useState<Message[]>([])
    const [input, setInput] = useState('')
    const [loading, setLoading] = useState(false)
    const messagesEndRef = useRef<HTMLDivElement>(null)

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
            timestamp: new Date()
        }

        setMessages(prev => [...prev, userMessage])
        setInput('')
        setLoading(true)

        try {
            const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL || ''}/api/expert/${expertId}/chat`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ message: userMessage.content, language: 'fr' })
            })

            const data = await response.json()

            const assistantMessage: Message = {
                id: (Date.now() + 1).toString(),
                role: 'assistant',
                content: data.response || 'Désolé, je n\'ai pas pu répondre. Réessaie !',
                timestamp: new Date()
            }

            setMessages(prev => [...prev, assistantMessage])
        } catch (error) {
            setMessages(prev => [...prev, {
                id: (Date.now() + 1).toString(),
                role: 'assistant',
                content: 'Oups ! Je suis momentanément indisponible. Réessaie dans quelques instants.',
                timestamp: new Date()
            }])
        } finally {
            setLoading(false)
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
                            <div className="bg-white border border-gray-200 rounded-2xl px-4 py-3 shadow-sm">
                                <div className="flex items-center gap-2">
                                    <Loader2 className={`w-4 h-4 animate-spin ${expert.textColor}`} />
                                    <span className="text-gray-500 text-sm">Réflexion...</span>
                                </div>
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
                <div className="max-w-4xl mx-auto flex gap-3">
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
    )
}
