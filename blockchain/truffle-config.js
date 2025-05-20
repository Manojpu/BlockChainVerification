/**
 * Truffle configuration for Resume Verification project
 * Use this to configure connection to Ganache and other networks
 */
module.exports = {
  networks: {
    development: {
      host: "127.0.0.1", // Local Ganache instance
      port: 7545, // Default Ganache port
      network_id: "*", // Match any network id
      gas: 6721975, // Gas limit
      gasPrice: 20000000000, // 20 gwei
    },
    // For when ready to deploy to a testnet like Sepolia
    // sepolia: {
    //   provider: () => new HDWalletProvider(
    //     process.env.MNEMONIC,
    //     `https://sepolia.infura.io/v3/${process.env.INFURA_KEY}`
    //   ),
    //   network_id: 11155111,   // Sepolia's id
    //   gas: 5500000,
    //   confirmations: 2,       // # of confirmations to wait
    //   timeoutBlocks: 200,     // # of blocks before a deployment times out
    //   skipDryRun: true        // Skip dry run before migrations
    // }
  },

  // Configure compilers
  compilers: {
    solc: {
      version: "0.8.17", // Match the version in contract
      settings: {
        optimizer: {
          enabled: true,
          runs: 200,
        },
      },
    },
  },

  // Deployment plugin options
  plugins: [
    "truffle-plugin-verify", // For etherscan verification when needed
  ],

  // Configure path for contracts, migrations, and build artifacts
  contracts_directory: "./contracts/",
  contracts_build_directory: "./build/contracts/",
  migrations_directory: "./migrations/",

  // Configure Mocha test framework
  mocha: {
    timeout: 100000,
    reporter: "spec",
  },
};
