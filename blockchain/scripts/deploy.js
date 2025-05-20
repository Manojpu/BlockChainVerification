/**
 * Alternative deployment script using web3.js
 * Can be used instead of Truffle migrations
 */
const fs = require("fs");
const Web3 = require("web3");

async function deployContract() {
  try {
    // Read contract details
    const contractJson = JSON.parse(
      fs.readFileSync("./build/contracts/Verification.json", "utf8")
    );
    const abi = contractJson.abi;
    const bytecode = contractJson.bytecode;

    // Configure web3 provider (Ganache by default)
    const web3 = new Web3("http://localhost:7545");

    // Get accounts
    const accounts = await web3.eth.getAccounts();
    const deployerAccount = accounts[0];

    console.log(`Deploying from account: ${deployerAccount}`);

    // Create contract instance
    const VerificationContract = new web3.eth.Contract(abi);

    // Deploy contract
    console.log("Deploying contract...");
    const deployTx = VerificationContract.deploy({
      data: bytecode,
      arguments: [], // Constructor arguments if any
    });

    // Estimate gas
    const gas = await deployTx.estimateGas();

    // Send transaction
    const deployedContract = await deployTx.send({
      from: deployerAccount,
      gas,
      gasPrice: web3.utils.toWei("20", "gwei"),
    });

    console.log(
      `Contract deployed at address: ${deployedContract.options.address}`
    );

    // Save contract address to file for easy reference
    fs.writeFileSync(
      "./deployed_contract_address.json",
      JSON.stringify({ address: deployedContract.options.address }, null, 2)
    );

    return deployedContract;
  } catch (error) {
    console.error("Error deploying contract:", error);
    throw error;
  }
}

// Only run if script is run directly
if (require.main === module) {
  deployContract()
    .then(() => process.exit(0))
    .catch((error) => {
      console.error(error);
      process.exit(1);
    });
}

module.exports = deployContract;
