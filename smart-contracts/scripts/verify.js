const hre = require("hardhat");

async function main() {
    const ResumeVerifier = await hre.ethers.getContractFactory("ResumeVerifier");
    const resumeVerifier = await ResumeVerifier.attach("YOUR_CONTRACT_ADDRESS");

    const resumeId = "YOUR_RESUME_ID"; // Replace with the actual resume ID you want to verify
    const verificationResult = await resumeVerifier.verifyResume(resumeId);

    console.log(`Verification result for resume ID ${resumeId}:`, verificationResult);
}

main()
    .then(() => process.exit(0))
    .catch((error) => {
        console.error(error);
        process.exit(1);
    });