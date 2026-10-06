import type { NextConfig } from "next";

const configuredBackendUrl =
  process.env.BACKEND_API_URL || process.env.NEXT_PUBLIC_API_URL || "";

const backendUrl = configuredBackendUrl.replace(/\/api\/v1\/?$/, "");

const nextConfig: NextConfig = {
  reactStrictMode: true,
  async rewrites() {
    if (!backendUrl) return [];
    return [
      {
        source: "/api/backend/:path*",
        destination: `${backendUrl}/:path*`,
      },
    ];
  },
};

export default nextConfig;
