// Blog article data - shared between pages
export interface ArticleContent {
    title: string;
    categoryName: string;
    excerpt: string;
    content: string;
    cta: string;
}

export interface Article {
    fr: ArticleContent;
    en: ArticleContent;
    category: string;
    emoji: string;
    expertId: string;
    date: string;
    readTime: number;
    keywords: string[];
}

export const ARTICLES: Record<string, Article> = {
    'pubmed-recherche-medicale-ia': {
        category: 'health',
        emoji: '🔬',
        expertId: 'health',
        date: '2024-12-06',
        readTime: 5,
        keywords: ['pubmed', 'recherche médicale', 'IA santé', 'medline', 'articles scientifiques'],
        fr: {
            title: 'Comment PubMed et l\'IA révolutionnent la recherche santé',
            categoryName: 'Recherche Santé',
            excerpt: 'Découvrez comment nous utilisons PubMed pour vous fournir des informations de santé fiables.',
            content: `
## Pourquoi PubMed ?

PubMed est la plus grande base de données médicales au monde, gérée par le National Institutes of Health (NIH) américain. Elle contient plus de **35 millions d'articles scientifiques** issus de revues médicales évaluées par des pairs.

## Comment WikiAsk utilise PubMed

Notre système fonctionne en 3 étapes :

1. **Recherche sémantique** — Quand vous posez une question, notre IA identifie les termes médicaux pertinents
2. **Extraction de données** — Nous interrogeons PubMed pour récupérer les études les plus récentes
3. **Synthèse intelligente** — L'IA analyse et résume les informations en langage simple

## Pourquoi c'est plus fiable

Contrairement à une recherche Google classique qui peut afficher des blogs non vérifiés, WikiAsk s'appuie sur :
- Des études scientifiques publiées
- Des revues médicales reconnues
- Des données actualisées

## Important

⚠️ WikiAsk fournit des informations générales à but éducatif. Consultez toujours un professionnel de santé pour un avis médical personnalisé.
      `,
            cta: 'Poser une question à Recherche Santé'
        },
        en: {
            title: 'How PubMed and AI are Revolutionizing Health Research',
            categoryName: 'Health Search',
            excerpt: 'Discover how we use PubMed to provide you with reliable health information.',
            content: `
## Why PubMed?

PubMed is the world's largest medical database, managed by the US National Institutes of Health (NIH). It contains over **35 million scientific articles** from peer-reviewed medical journals.

## How WikiAsk Uses PubMed

Our system works in 3 steps:

1. **Semantic search** — When you ask a question, our AI identifies relevant medical terms
2. **Data extraction** — We query PubMed to retrieve the most recent studies
3. **Intelligent synthesis** — AI analyzes and summarizes information in simple language

## Why It's More Reliable

Unlike a classic Google search that may display unverified blogs, WikiAsk relies on:
- Published scientific studies
- Recognized medical journals
- Up-to-date data

## Important

⚠️ WikiAsk provides general educational information. Always consult a healthcare professional for personalized medical advice.
      `,
            cta: 'Ask Health Search a question'
        }
    },
    'bitcoin-debutant-guide-complet': {
        category: 'finance',
        emoji: '📊',
        expertId: 'finance',
        date: '2024-12-05',
        readTime: 7,
        keywords: ['bitcoin', 'crypto', 'débutant', 'coingecko', 'cryptomonnaie', 'BTC'],
        fr: {
            title: 'Comprendre le Bitcoin : Guide complet pour débutants 2024',
            categoryName: 'Guide Finance',
            excerpt: 'Le Bitcoin expliqué simplement avec des données CoinGecko en temps réel.',
            content: `
## Qu'est-ce que le Bitcoin ?

Le Bitcoin (BTC) est la première cryptomonnaie, créée en 2009 par Satoshi Nakamoto. C'est une monnaie numérique décentralisée qui fonctionne sans banque centrale.

## D'où viennent nos données ?

WikiAsk utilise **CoinGecko**, une des sources les plus fiables pour les données crypto :
- Cours en temps réel
- Capitalisation boursière
- Volume d'échanges 24h
- Historique des prix

## Les bases à connaître

### Pourquoi le Bitcoin a de la valeur
- **Offre limitée** : Maximum 21 millions de BTC
- **Décentralisation** : Aucune autorité centrale
- **Sécurité** : Blockchain immuable

### Risques à considérer
- Volatilité importante
- Pas de garantie de capital
- Risques de piratage (wallets)

## Disclaimer

⚠️ Ceci n'est pas un conseil financier. Les cryptomonnaies sont des actifs volatils. N'investissez que ce que vous pouvez vous permettre de perdre.
      `,
            cta: 'Poser une question à Guide Finance'
        },
        en: {
            title: 'Understanding Bitcoin: Complete Guide for Beginners 2024',
            categoryName: 'Finance Guide',
            excerpt: 'Bitcoin explained simply with real-time CoinGecko data.',
            content: `
## What is Bitcoin?

Bitcoin (BTC) is the first cryptocurrency, created in 2009 by Satoshi Nakamoto. It's a decentralized digital currency that operates without a central bank.

## Where Does Our Data Come From?

WikiAsk uses **CoinGecko**, one of the most reliable sources for crypto data:
- Real-time prices
- Market capitalization
- 24h trading volume
- Price history

## The Basics You Need to Know

### Why Bitcoin Has Value
- **Limited supply**: Maximum 21 million BTC
- **Decentralization**: No central authority
- **Security**: Immutable blockchain

### Risks to Consider
- Significant volatility
- No capital guarantee
- Hacking risks (wallets)

## Disclaimer

⚠️ This is not financial advice. Cryptocurrencies are volatile assets. Only invest what you can afford to lose.
      `,
            cta: 'Ask Finance Guide a question'
        }
    },
    'horoscope-belier-2024-complet': {
        category: 'horoscope',
        emoji: '🔮',
        expertId: 'horoscope',
        date: '2024-12-04',
        readTime: 6,
        keywords: ['horoscope', 'bélier', '2024', 'astrologie', 'signe zodiaque', 'prédictions'],
        fr: {
            title: 'Horoscope Bélier 2024 : Prédictions Amour, Travail, Santé',
            categoryName: 'Étoile',
            excerpt: 'Prédictions complètes pour le Bélier en 2024. Notre IA analyse les transits planétaires.',
            content: `
## Vue d'ensemble 2024 pour le Bélier

L'année 2024 s'annonce comme une période de **transformation majeure** pour les natifs du Bélier (21 mars - 19 avril). Jupiter en transit favorable apporte des opportunités d'expansion.

## Comment WikiAsk analyse votre horoscope

Notre système combine plusieurs sources :
- **Éphémérides astronomiques** précises
- **Transits planétaires** en temps réel
- **Analyse IA** des configurations astrales

## Prédictions par domaine

### Amour et Relations ❤️
- Premier trimestre : Vénus favorise les nouvelles rencontres
- Été : Période propice aux engagements
- Automne : Consolidation des liens existants

### Carrière et Finances 💼
- Mars amplifie votre ambition professionnelle
- Opportunités de promotion au printemps
- Prudence financière recommandée en août

### Santé et Bien-être 🌿
- Énergie débordante au premier semestre
- Attention au surmenage en période Mars rétrograde
- Sport et activité physique favorisés

## Dates clés à retenir

- **Mars 2024** : Nouvelle Lune bénéfique
- **Juin 2024** : Solstice porteur
- **Octobre 2024** : Éclipse transformatrice

## Note importante

⚠️ L'astrologie est un art divinatoire à but ludique. Les prédictions ne constituent pas des conseils de vie.
      `,
            cta: 'Poser une question à Étoile'
        },
        en: {
            title: 'Aries Horoscope 2024: Love, Career, Health Predictions',
            categoryName: 'Star',
            excerpt: 'Complete predictions for Aries in 2024. Our AI analyzes planetary transits.',
            content: `
## 2024 Overview for Aries

2024 promises to be a period of **major transformation** for Aries natives (March 21 - April 19). Jupiter in favorable transit brings opportunities for expansion.

## How WikiAsk Analyzes Your Horoscope

Our system combines multiple sources:
- **Precise astronomical ephemeris**
- **Real-time planetary transits**
- **AI analysis** of astral configurations

## Predictions by Area

### Love and Relationships ❤️
- First quarter: Venus favors new encounters
- Summer: Favorable period for commitments
- Autumn: Consolidation of existing bonds

### Career and Finances 💼
- Mars amplifies your professional ambition
- Promotion opportunities in spring
- Financial caution recommended in August

### Health and Wellness 🌿
- Overflowing energy in the first half
- Watch for overwork during Mars retrograde
- Sports and physical activity favored

## Key Dates to Remember

- **March 2024**: Beneficial New Moon
- **June 2024**: Promising Solstice
- **October 2024**: Transformative Eclipse

## Important Note

⚠️ Astrology is a divinatory art for entertainment purposes. Predictions do not constitute life advice.
      `,
            cta: 'Ask Star a question'
        }
    },
    'signification-prenom-emma': {
        category: 'prenom',
        emoji: '👶',
        expertId: 'prenom',
        date: '2024-12-03',
        readTime: 4,
        keywords: ['prénom', 'emma', 'signification', 'origine', 'bébé', 'personnalité'],
        fr: {
            title: 'Prénom Emma : Signification, Origine et Personnalité',
            categoryName: 'Prénom Expert',
            excerpt: 'Tout savoir sur le prénom Emma : étymologie, histoire, popularité et personnalité.',
            content: `
## Origine et étymologie

**Emma** est un prénom d'origine germanique, dérivé du terme "ermen" signifiant **"toute", "universelle"** ou "grande". C'est l'un des prénoms les plus anciens encore utilisés aujourd'hui.

## D'où viennent nos informations ?

WikiAsk compile des données de :
- **État civil français** (statistiques officielles)
- **Bases de données historiques** des prénoms
- **Études onomastiques** (science des noms)

## Histoire du prénom

### Époque médiévale
Emma était déjà populaire au Moyen Âge. La reine Emma de Normandie (985-1052) a contribué à sa diffusion.

### Évolution moderne
- **Années 1900** : Prénom démodé
- **Années 2000** : Renaissance spectaculaire
- **2005-2020** : N°1 en France pendant 15 ans

## Personnalité associée

Les Emma sont souvent décrites comme :
- **Déterminées** et volontaires
- **Sensibles** et empathiques
- **Créatives** avec un sens artistique
- **Sociables** mais indépendantes

## Statistiques France

- **Popularité actuelle** : Top 5
- **Emma célèbres** : Emma Watson, Emma Stone
- **Variantes** : Emmanuella, Ema, Emmy

## Fête

📅 La Sainte Emma se fête le **19 avril** (en l'honneur de Sainte Emma de Sangau).
      `,
            cta: 'Poser une question à Prénom Expert'
        },
        en: {
            title: 'Name Emma: Meaning, Origin and Personality',
            categoryName: 'Name Expert',
            excerpt: 'Everything about the name Emma: etymology, history, popularity and personality.',
            content: `
## Origin and Etymology

**Emma** is a name of Germanic origin, derived from the term "ermen" meaning **"whole", "universal"** or "great". It's one of the oldest names still in use today.

## Where Does Our Information Come From?

WikiAsk compiles data from:
- **Official civil registry** (official statistics)
- **Historical name databases**
- **Onomastic studies** (science of names)

## History of the Name

### Medieval Era
Emma was already popular in the Middle Ages. Queen Emma of Normandy (985-1052) contributed to its spread.

### Modern Evolution
- **1900s**: Old-fashioned name
- **2000s**: Spectacular renaissance
- **2005-2020**: #1 in France for 15 years

## Associated Personality

Emmas are often described as:
- **Determined** and strong-willed
- **Sensitive** and empathetic
- **Creative** with artistic sense
- **Sociable** but independent

## France Statistics

- **Current popularity**: Top 5
- **Famous Emmas**: Emma Watson, Emma Stone
- **Variants**: Emmanuella, Ema, Emmy

## Name Day

📅 Saint Emma's day is celebrated on **April 19th** (in honor of Saint Emma of Sangau).
      `,
            cta: 'Ask Name Expert a question'
        }
    },
    '14-juillet-histoire-evenements': {
        category: 'history',
        emoji: '📅',
        expertId: 'history',
        date: '2024-12-02',
        readTime: 5,
        keywords: ['14 juillet', 'histoire', 'bastille', 'révolution française', 'fête nationale'],
        fr: {
            title: '14 Juillet : Les événements historiques marquants',
            categoryName: 'Ce Jour',
            excerpt: 'Découvrez ce qui s\'est passé un 14 juillet à travers l\'histoire mondiale.',
            content: `
## L'événement majeur : La prise de la Bastille (1789)

Le **14 juillet 1789** marque un tournant dans l'histoire de France. La prise de la forteresse de la Bastille symbolise la fin de l'Ancien Régime et le début de la Révolution française.

## Comment WikiAsk explore l'histoire

Notre IA consulte :
- **Archives historiques** numérisées
- **Encyclopédies** de référence
- **Sources académiques** vérifiées

## Autres événements un 14 juillet

### Naissances célèbres
- **1862** : Gustav Klimt (peintre autrichien)
- **1913** : Gerald Ford (38e président américain)
- **1918** : Ingmar Bergman (réalisateur suédois)

### Événements historiques
- **1223** : Louis VIII devient roi de France
- **1865** : Première ascension du Cervin
- **1958** : Révolution en Irak

### Culture et sport
- **1998** : La France remporte sa première Coupe du Monde de football
- **2019** : Record de température en France (46°C)

## Pourquoi le 14 juillet est férié

Depuis **1880**, le 14 juillet est la fête nationale française. Elle commémore :
- La prise de la Bastille (1789)
- La Fête de la Fédération (1790)

## Le saviez-vous ?

🎆 Le feu d'artifice du 14 juillet à Paris attire plus de **500 000 spectateurs** chaque année !
      `,
            cta: 'Poser une question à Ce Jour'
        },
        en: {
            title: 'July 14th: Major Historical Events',
            categoryName: 'On This Day',
            excerpt: 'Discover what happened on July 14th throughout world history.',
            content: `
## The Major Event: The Storming of the Bastille (1789)

**July 14, 1789** marks a turning point in French history. The capture of the Bastille fortress symbolizes the end of the Ancien Régime and the beginning of the French Revolution.

## How WikiAsk Explores History

Our AI consults:
- **Digitized historical archives**
- **Reference encyclopedias**
- **Verified academic sources**

## Other Events on July 14th

### Famous Births
- **1862**: Gustav Klimt (Austrian painter)
- **1913**: Gerald Ford (38th US President)
- **1918**: Ingmar Bergman (Swedish director)

### Historical Events
- **1223**: Louis VIII becomes King of France
- **1865**: First ascent of the Matterhorn
- **1958**: Revolution in Iraq

### Culture and Sports
- **1998**: France wins its first FIFA World Cup
- **2019**: Temperature record in France (46°C)

## Why July 14th is a Holiday

Since **1880**, July 14th has been the French national holiday. It commemorates:
- The Storming of the Bastille (1789)
- The Fête de la Fédération (1790)

## Did You Know?

🎆 The July 14th fireworks in Paris attract more than **500,000 spectators** every year!
      `,
            cta: 'Ask On This Day a question'
        }
    },
    // ===== NEW SEO ARTICLES =====
    'effets-secondaires-doliprane': {
        category: 'health',
        emoji: '🔬',
        expertId: 'health',
        date: '2024-12-06',
        readTime: 5,
        keywords: ['doliprane', 'paracétamol', 'effets secondaires', 'médicament', 'douleur'],
        fr: {
            title: 'Effets secondaires du Doliprane : Ce que dit la science',
            categoryName: 'Recherche Santé',
            excerpt: 'Tout savoir sur les effets secondaires du paracétamol (Doliprane). WikiAsk consulte les bases officielles ANSM et FDA en temps réel.',
            content: `
## Le Doliprane, c'est quoi exactement ?

Le **Doliprane** (paracétamol) est l'antidouleur le plus utilisé en France. Mais comme tout médicament, il peut avoir des effets secondaires.

## Comment WikiAsk vous informe

Notre expert **Recherche Santé** consulte en temps réel :
- 📊 **ANSM** (Agence Nationale du Médicament)
- 🇺🇸 **OpenFDA** (données américaines)
- 📚 **PubMed** (études scientifiques)

## Effets secondaires fréquents

Selon les bases de données officielles :
- Réactions allergiques (rares)
- Problèmes hépatiques en cas de surdosage
- Nausées légères

## Posologie recommandée

⚠️ Ne jamais dépasser **3g/jour** chez l'adulte (4g max sur avis médical).

## Interactions médicamenteuses

Notre IA peut vérifier les interactions avec vos autres médicaments. Posez votre question !
            `,
            cta: 'Vérifier avec Recherche Santé'
        },
        en: {
            title: 'Doliprane Side Effects: What Science Says',
            categoryName: 'Health Search',
            excerpt: 'Everything about paracetamol (Doliprane) side effects. WikiAsk queries official ANSM and FDA databases in real-time.',
            content: `
## What is Doliprane exactly?

**Doliprane** (paracetamol/acetaminophen) is the most commonly used painkiller in France. But like any medication, it can have side effects.

## How WikiAsk informs you

Our **Health Search** expert queries in real-time:
- 📊 **ANSM** (French Drug Agency)
- 🇺🇸 **OpenFDA** (American data)
- 📚 **PubMed** (scientific studies)

## Common side effects

According to official databases:
- Allergic reactions (rare)
- Liver problems in case of overdose
- Mild nausea

## Recommended dosage

⚠️ Never exceed **3g/day** in adults (4g max on medical advice).

## Drug interactions

Our AI can check interactions with your other medications. Ask your question!
            `,
            cta: 'Check with Health Search'
        }
    },
    'chatgpt-vs-claude-comparaison': {
        category: 'tech',
        emoji: '💻',
        expertId: 'tech',
        date: '2024-12-06',
        readTime: 6,
        keywords: ['ChatGPT', 'Claude', 'comparaison', 'IA', 'intelligence artificielle', 'meilleur'],
        fr: {
            title: 'ChatGPT vs Claude : Quelle IA choisir en 2024 ?',
            categoryName: 'Tech Insider',
            excerpt: 'Comparaison détaillée entre ChatGPT et Claude. Notre expert Tech analyse les forces de chaque IA.',
            content: `
## Le match des géants de l'IA

**ChatGPT** (OpenAI) et **Claude** (Anthropic) dominent le marché. Mais lequel choisir ?

## Comparaison objective

| Critère | ChatGPT | Claude |
|---------|---------|--------|
| Vitesse | ⚡ Rapide | ⚡ Rapide |
| Contexte | 128K tokens | 200K tokens |
| Code | ✅ Excellent | ✅ Excellent |
| Prix | $20/mois | $20/mois |

## Comment WikiAsk vous aide

**Tech Insider** suit l'actualité IA quotidiennement via :
- 📰 HackerNews
- 🔬 Benchmarks publics
- 📊 Retours utilisateurs

## Notre avis

Les deux sont excellents ! Le choix dépend de votre usage :
- **ChatGPT** : Plugins, DALL-E, GPTs personnalisés
- **Claude** : Contexte long, écriture, analyse documents
            `,
            cta: 'Demander à Tech Insider'
        },
        en: {
            title: 'ChatGPT vs Claude: Which AI to Choose in 2024?',
            categoryName: 'Tech Insider',
            excerpt: 'Detailed comparison between ChatGPT and Claude. Our Tech expert analyzes the strengths of each AI.',
            content: `
## The battle of AI giants

**ChatGPT** (OpenAI) and **Claude** (Anthropic) dominate the market. But which one to choose?

## Objective comparison

| Criteria | ChatGPT | Claude |
|----------|---------|--------|
| Speed | ⚡ Fast | ⚡ Fast |
| Context | 128K tokens | 200K tokens |
| Code | ✅ Excellent | ✅ Excellent |
| Price | $20/month | $20/month |

## How WikiAsk helps you

**Tech Insider** follows AI news daily via:
- 📰 HackerNews
- 🔬 Public benchmarks
- 📊 User feedback

## Our opinion

Both are excellent! The choice depends on your use:
- **ChatGPT**: Plugins, DALL-E, custom GPTs
- **Claude**: Long context, writing, document analysis
            `,
            cta: 'Ask Tech Insider'
        }
    },
    'meilleurs-films-2024-voir': {
        category: 'cinema',
        emoji: '🎬',
        expertId: 'cinema',
        date: '2024-12-06',
        readTime: 5,
        keywords: ['films', '2024', 'meilleur', 'voir', 'cinéma', 'recommandation', 'Netflix'],
        fr: {
            title: 'Meilleurs Films 2024 : Notre Sélection à Voir Absolument',
            categoryName: 'Ciné Fan',
            excerpt: 'Découvrez les films incontournables de 2024 avec notre expert Ciné Fan. Données TMDB en temps réel.',
            content: `
## Les must-see de 2024

Notre expert **Ciné Fan** analyse les sorties et critiques quotidiennement.

## D'où viennent nos recommandations ?

Nous utilisons **TMDB** (The Movie Database) :
- ⭐ Notes du public
- 🎬 Critiques presse
- 📊 Box-office mondial

## Top Films 2024

1. **Dune 2** - Science-fiction épique
2. **Oppenheimer** - Biopic historique
3. **Barbie** - Comédie phénomène

## Comment WikiAsk vous aide

Posez des questions personnalisées :
- "Films comme Inception"
- "Quoi regarder ce soir ?"
- "Meilleur film horreur récent"
            `,
            cta: 'Demander à Ciné Fan'
        },
        en: {
            title: 'Best Movies 2024: Our Must-Watch Selection',
            categoryName: 'Ciné Fan',
            excerpt: 'Discover the must-see movies of 2024 with our Ciné Fan expert. Real-time TMDB data.',
            content: `
## The must-sees of 2024

Our **Ciné Fan** expert analyzes releases and reviews daily.

## Where do our recommendations come from?

We use **TMDB** (The Movie Database):
- ⭐ Audience ratings
- 🎬 Press reviews
- 📊 Worldwide box office

## Top Films 2024

1. **Dune 2** - Epic sci-fi
2. **Oppenheimer** - Historical biopic
3. **Barbie** - Phenomenon comedy

## How WikiAsk helps you

Ask personalized questions:
- "Movies like Inception"
- "What to watch tonight?"
- "Best recent horror movie"
            `,
            cta: 'Ask Ciné Fan'
        }
    },
    'recette-ingredients-maison': {
        category: 'cuisine',
        emoji: '🍳',
        expertId: 'cuisine',
        date: '2024-12-06',
        readTime: 4,
        keywords: ['recette', 'ingrédients', 'frigo', 'cuisine', 'facile', 'rapide'],
        fr: {
            title: 'Recettes avec ce que j\'ai : L\'IA qui cuisine pour vous',
            categoryName: 'Chef Gourmand',
            excerpt: 'Trouvez des recettes avec les ingrédients de votre frigo. Notre Chef Gourmand analyse et propose.',
            content: `
## Plus jamais "Je sais pas quoi faire"

**Chef Gourmand** utilise vos ingrédients pour suggérer des recettes.

## Comment ça marche ?

1. 📝 Listez vos ingrédients
2. 🤖 L'IA cherche dans **Spoonacular** (500K+ recettes)
3. 🍳 Recevez des suggestions adaptées

## Exemple

> "J'ai des tomates, des œufs et du fromage"
> → Omelette tomate-fromage, Shakshuka, Quiche express...

## Avantages WikiAsk

- **Temps réel** : Pas de pages à scroller
- **Personnalisé** : Régimes, allergies pris en compte
- **Interactif** : Posez des questions de suivi
            `,
            cta: 'Cuisiner avec Chef Gourmand'
        },
        en: {
            title: 'Recipes with What I Have: AI That Cooks for You',
            categoryName: 'Chef Gourmand',
            excerpt: 'Find recipes with ingredients from your fridge. Our Chef Gourmand analyzes and suggests.',
            content: `
## Never again "I don't know what to make"

**Chef Gourmand** uses your ingredients to suggest recipes.

## How does it work?

1. 📝 List your ingredients
2. 🤖 AI searches in **Spoonacular** (500K+ recipes)
3. 🍳 Receive adapted suggestions

## Example

> "I have tomatoes, eggs and cheese"
> → Tomato-cheese omelette, Shakshuka, Express quiche...

## WikiAsk advantages

- **Real-time**: No pages to scroll
- **Personalized**: Diets, allergies taken into account
- **Interactive**: Ask follow-up questions
            `,
            cta: 'Cook with Chef Gourmand'
        }
    },
    'meteo-paris-15-jours-fiable': {
        category: 'weather',
        emoji: '☀️',
        expertId: 'weather',
        date: '2024-12-06',
        readTime: 3,
        keywords: ['météo', 'Paris', '15 jours', 'prévision', 'fiable', 'temps'],
        fr: {
            title: 'Météo Paris 15 Jours : Prévisions Fiables en Temps Réel',
            categoryName: 'Météo Pro',
            excerpt: 'Consultez la météo de Paris sur 15 jours avec des données OpenWeatherMap actualisées.',
            content: `
## La météo parisienne en temps réel

**Météo Pro** utilise **OpenWeatherMap** pour des prévisions précises.

## Ce que vous obtenez

- 🌡️ Température min/max
- 🌧️ Probabilité de pluie
- 💨 Vitesse du vent
- ☀️ Lever/coucher du soleil

## Pourquoi WikiAsk ?

Notre IA ne se contente pas d'afficher les données :
1. **Interprète** les prévisions
2. **Conseille** (parapluie, crème solaire...)
3. **Répond** à vos questions spécifiques

## Questions exemples

- "Va-t-il pleuvoir demain à Paris ?"
- "Quel temps ce week-end ?"
- "Dois-je prendre un parapluie ?"
            `,
            cta: 'Demander à Météo Pro'
        },
        en: {
            title: 'Paris Weather 15 Days: Reliable Real-Time Forecast',
            categoryName: 'Weather Pro',
            excerpt: 'Check Paris weather for 15 days with updated OpenWeatherMap data.',
            content: `
## Paris weather in real-time

**Weather Pro** uses **OpenWeatherMap** for accurate forecasts.

## What you get

- 🌡️ Min/max temperature
- 🌧️ Rain probability
- 💨 Wind speed
- ☀️ Sunrise/sunset

## Why WikiAsk?

Our AI doesn't just display data:
1. **Interprets** forecasts
2. **Advises** (umbrella, sunscreen...)
3. **Answers** your specific questions

## Example questions

- "Will it rain tomorrow in Paris?"
- "What's the weather this weekend?"
- "Should I take an umbrella?"
            `,
            cta: 'Ask Weather Pro'
        }
    },
    'actualites-ia-intelligence-artificielle': {
        category: 'news',
        emoji: '📰',
        expertId: 'news',
        date: '2024-12-06',
        readTime: 4,
        keywords: ['actualités', 'IA', 'intelligence artificielle', 'news', 'tech', 'AI'],
        fr: {
            title: 'Actualités IA : Suivez l\'Intelligence Artificielle en Temps Réel',
            categoryName: 'Actu Live',
            excerpt: 'Toutes les actualités de l\'intelligence artificielle résumées par notre IA. Sources fiables et synthèse claire.',
            content: `
## L'IA expliquée par l'IA

**Actu Live** agrège les principales sources d'information sur l'IA.

## Nos sources

- 📰 **NewsAPI** : Grands médias tech
- 🔬 **HackerNews** : Communauté tech
- 🎓 **ArXiv** : Publications scientifiques

## Pourquoi suivre l'actu IA ?

L'IA évolue chaque jour :
- Nouveaux modèles (GPT, Claude, Gemini...)
- Réglementations (EU AI Act...)
- Applications pratiques

## Comment WikiAsk vous aide

1. **Agrège** les meilleures sources
2. **Filtre** le bruit médiatique
3. **Synthétise** l'essentiel
4. **Explique** en langage simple

## Posez vos questions !

- "Quoi de neuf en IA cette semaine ?"
- "C'est quoi GPT-5 ?"
- "L'IA va-t-elle remplacer mon métier ?"
            `,
            cta: 'Consulter Actu Live'
        },
        en: {
            title: 'AI News: Follow Artificial Intelligence in Real-Time',
            categoryName: 'News Live',
            excerpt: 'All artificial intelligence news summarized by our AI. Reliable sources and clear synthesis.',
            content: `
## AI explained by AI

**News Live** aggregates major information sources on AI.

## Our sources

- 📰 **NewsAPI**: Major tech media
- 🔬 **HackerNews**: Tech community
- 🎓 **ArXiv**: Scientific publications

## Why follow AI news?

AI evolves every day:
- New models (GPT, Claude, Gemini...)
- Regulations (EU AI Act...)
- Practical applications

## How WikiAsk helps you

1. **Aggregates** the best sources
2. **Filters** media noise
3. **Synthesizes** the essentials
4. **Explains** in simple language

## Ask your questions!

- "What's new in AI this week?"
- "What is GPT-5?"
- "Will AI replace my job?"
            `,
            cta: 'Check News Live'
        }
    },
}

export const CATEGORIES = [
    { id: 'all', name: 'Tous', nameEn: 'All', emoji: '📚' },
    { id: 'health', name: 'Santé', nameEn: 'Health', emoji: '🔬' },
    { id: 'finance', name: 'Finance', nameEn: 'Finance', emoji: '📊' },
    { id: 'horoscope', name: 'Horoscope', nameEn: 'Horoscope', emoji: '🔮' },
    { id: 'prenom', name: 'Prénoms', nameEn: 'Names', emoji: '👶' },
    { id: 'history', name: 'Histoire', nameEn: 'History', emoji: '📅' },
    { id: 'tech', name: 'Tech', nameEn: 'Tech', emoji: '💻' },
    { id: 'cinema', name: 'Cinéma', nameEn: 'Movies', emoji: '🎬' },
    { id: 'cuisine', name: 'Cuisine', nameEn: 'Cooking', emoji: '🍳' },
    { id: 'weather', name: 'Météo', nameEn: 'Weather', emoji: '☀️' },
    { id: 'news', name: 'Actualités', nameEn: 'News', emoji: '📰' },
]

export function getArticleSlugs(): string[] {
    return Object.keys(ARTICLES)
}

export function getArticle(slug: string): Article | undefined {
    return ARTICLES[slug]
}
