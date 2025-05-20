const Verification = artifacts.require("Verification");

module.exports = async function (deployer, network, accounts) {
  console.log("Deploying Verification contract...");
  console.log("Deployment account:", accounts[0]);

  // Deploy the Verification contract
  await deployer.deploy(Verification);

  // Get the deployed contract instance
  const verificationContract = await Verification.deployed();

  console.log("Contract deployed successfully!");
  console.log("Contract address:", verificationContract.address);

  // If not on development network, we might want to do additional setup
  if (network !== "development") {
    console.log("Setting up oracles for non-development network...");

    // Here you would set up oracles for production deployments
    // This is just an example - you'd likely handle this differently in production
    if (accounts.length > 1) {
      // Authorize a second account as an oracle
      await verificationContract.authorizeOracle(accounts[1], {
        from: accounts[0],
      });
      console.log("Authorized oracle:", accounts[1]);
    }
  }
};
