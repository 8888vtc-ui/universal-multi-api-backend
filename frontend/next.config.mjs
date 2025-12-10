/** @type {import('next').NextConfig} */
// Deploy Trigger: Sync with Backend (Health Category Update)
const nextConfig = {
    reactStrictMode: true,
    typescript: {
        ignoreBuildErrors: true,
    },
    eslint: {
        ignoreDuringBuilds: true,
    }
};

export default nextConfig;
