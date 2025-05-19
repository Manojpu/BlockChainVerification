const withImages = require('next-images');

module.exports = withImages({
  reactStrictMode: true,
  env: {
    API_URL: process.env.API_URL,
    BLOCKCHAIN_URL: process.env.BLOCKCHAIN_URL,
  },
  webpack: (config) => {
    config.resolve.alias['@'] = path.resolve(__dirname, 'src');
    return config;
  },
});