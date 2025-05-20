anojekanayaka / Documents / BlockChain / resume -
  verification -
  app / frontend / next.config.ts;
const path = require("path");

/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  images: {
    domains: [],
  },
  webpack(config) {
    config.resolve.alias = {
      ...config.resolve.alias,
      "@": path.resolve(__dirname, "src"),
    };

    return config;
  },
};

module.exports = nextConfig;
