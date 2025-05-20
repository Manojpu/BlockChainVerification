# Blockchain – Solidity + Truffle + Ganache

This folder contains smart contracts and local blockchain simulation tools for the **Blockchain-Based Applicant Verification** system.

---

## ⚙️ Tech Stack

- Solidity
- Truffle
- Ganache CLI / Ganache GUI
- Web3.js

---

## 🚀 Getting Started

### 1. Install Truffle globally

```bash
npm install -g truffle
```

### 2. Start local blockchain (Ganache)

```bash
ganache-cli --port 7545
```

Alternatively, open Ganache GUI and select port `7545`.

### 3. Compile and deploy smart contracts

```bash
truffle compile
truffle migrate --network development
```

---

## 📂 Folder Structure

```
blockchain/
├── contracts/
│   └── Verification.sol         # Solidity contract
├── migrations/
│   └── 1_deploy_contracts.js    # Truffle deployment script
├── scripts/
│   ├── deploy.js                # Web3-based deploy script
│   └── setup_mock_verifications.js # Populate contract with test data
├── test/
│   └── verification_test.js     # Contract test cases
├── truffle-config.js            # Network config
└── README.md
```

---

## 🌐 `truffle-config.js` Sample

```javascript
module.exports = {
  networks: {
    development: {
      host: "127.0.0.1",
      port: 7545,
      network_id: "*", // Match Ganache network
    },
  },
  compilers: {
    solc: {
      version: "0.8.21",
    },
  },
};
```

---

## 🔗 After Deployment

- Copy the contract address and ABI.
- Update:
  - `backend/services/blockchain.py`
  - `frontend/src/services/web3.js`

You’re now ready to simulate Chainlink verification on your local Ethereum blockchain!
