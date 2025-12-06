/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  // Images optimization
  images: {
    domains: ['api.wikiask.net', 'universal-api-hub.fly.dev'],
  },
  // Rewrites pour développement (production utilise netlify.toml)
  async rewrites() {
    // En développement, utiliser l'API locale ou distante
    const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'https://api.wikiask.net'
    return [
      {
        source: '/api/:path*',
        destination: `${apiUrl}/api/:path*`,
      },
    ]
  },
}

module.exports = nextConfig


