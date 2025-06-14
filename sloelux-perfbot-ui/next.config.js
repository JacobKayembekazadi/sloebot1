/** @type {import('next').NextConfig} */
const nextConfig = {
  output: 'standalone',
  async rewrites() {
    return [
      {
        source: '/grafana/:path*',
        destination: 'http://grafana:3000/:path*',
      },
    ]
  },
}

module.exports = nextConfig 