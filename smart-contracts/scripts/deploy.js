const hre = require("hardhat");

async function main() {
    // We get the contract to deploy
    const ResumeVerifier = await hre.ethers.getContractFactory("ResumeVerifier");
    const resumeVerifier = await ResumeVerifier.deploy();

    await resumeVerifier.deployed();

    console.log("ResumeVerifier deployed to:", resumeVerifier.address);
}

// We recommend this pattern to be able to use async/await everywhere
// and properly handle errors.
main()
    .then(() => process.exit(0))
    .catch((error) => {
        console.error(error);
        process.exit(1);
    });