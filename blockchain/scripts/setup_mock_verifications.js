/**
 * Script to populate the deployed contract with mock verification data
 * This is useful for development and demonstration purposes
 */
const Web3 = require("web3");
const fs = require("fs");
const path = require("path");
const keccak256 = require("js-sha3").keccak256;

// Import contract ABI
let contractAddress;
try {
  // Try to read from deployed contract file
  const deployedInfo = JSON.parse(
    fs.readFileSync("./deployed_contract_address.json", "utf8")
  );
  contractAddress = deployedInfo.address;
} catch (error) {
  // If file doesn't exist, use hardcoded address (change this as needed)
  contractAddress = "0x5b1869D9A4C187F2EAa108f3062412ecf0526b24"; // Replace with actual address
  console.warn(
    "Could not find deployed contract address file. Please update the contract address manually."
  );
}

// University and company mock data
const mockUniversityData = [
  {
    name: "Kalana De Alwis",
    university: "NSBM Green University",
    degree: "BSc in Software Engineering",
    gpa: 3.73,
  },
  {
    name: "Shehani Jayawardena",
    university: "University of Colombo",
    degree: "BSc in Computer Science",
    gpa: 3.9,
  },
];

const mockCompanyData = [
  {
    name: "Shehani Jayawardena",
    company: "99X Technology",
    job_title: "ML Engineer",
    job_category: "Machine Learning",
  },
  {
    name: "Kalana De Alwis",
    company: "WSO2",
    job_title: "Software Engineer",
    job_category: "Software Development",
  },
];

// Function to create hash from data
function createDataHash(data) {
  // Convert data to string and create keccak256 hash
  const dataString = JSON.stringify(data);
  const hash = "0x" + keccak256(dataString);
  return hash;
}

async function setupMockVerifications() {
  try {
    // Read contract ABI
    const contractJson = JSON.parse(
      fs.readFileSync("./build/contracts/Verification.json", "utf8")
    );
    const abi = contractJson.abi;

    // Setup web3
    const web3 = new Web3("http://localhost:7545");
    const accounts = await web3.eth.getAccounts();

    // Create contract instance
    const verificationContract = new web3.eth.Contract(abi, contractAddress);

    console.log(`Connected to contract at: ${contractAddress}`);
    console.log("Setting up mock verifications...");

    // Add GPA verifications
    for (const student of mockUniversityData) {
      // Create data for GPA verification
      const gpaData = {
        name: student.name,
        university: student.university,
        gpa: student.gpa,
      };

      // Create hash
      const dataHash = web3.utils.sha3(JSON.stringify(gpaData));

      // Store verification (GPA = enum value 0)
      await verificationContract.methods
        .storeVerificationResult(
          dataHash,
          true, // isVerified
          0, // VerificationType.GPA
          `Verified ${student.name}'s GPA of ${student.gpa} at ${student.university}`
        )
        .send({
          from: accounts[0],
          gas: 200000,
        });

      console.log(`Added GPA verification for ${student.name}`);

      // Create data for Degree verification
      const degreeData = {
        name: student.name,
        university: student.university,
        degree: student.degree,
      };

      // Create hash
      const degreeHash = web3.utils.sha3(JSON.stringify(degreeData));

      // Store verification (Degree = enum value 2)
      await verificationContract.methods
        .storeVerificationResult(
          degreeHash,
          true, // isVerified
          2, // VerificationType.Degree
          `Verified ${student.name}'s ${student.degree} degree from ${student.university}`
        )
        .send({
          from: accounts[0],
          gas: 200000,
        });

      console.log(`Added Degree verification for ${student.name}`);
    }

    // Add Employment verifications
    for (const employee of mockCompanyData) {
      // Create data for Employment verification
      const employmentData = {
        name: employee.name,
        company: employee.company,
        job_title: employee.job_title,
      };

      // Create hash
      const dataHash = web3.utils.sha3(JSON.stringify(employmentData));

      // Store verification (Employment = enum value 1)
      await verificationContract.methods
        .storeVerificationResult(
          dataHash,
          true, // isVerified
          1, // VerificationType.Employment
          `Verified ${employee.name} worked at ${employee.company} as ${employee.job_title}`
        )
        .send({
          from: accounts[0],
          gas: 200000,
        });

      console.log(
        `Added Employment verification for ${employee.name} at ${employee.company}`
      );
    }

    // Get verification count to confirm success
    const count = await verificationContract.methods
      .getVerificationCount()
      .call();
    console.log(
      `Successfully added ${count} mock verifications to the contract`
    );
  } catch (error) {
    console.error("Error setting up mock verifications:", error);
  }
}

// Only run if script is run directly
if (require.main === module) {
  setupMockVerifications()
    .then(() => process.exit(0))
    .catch((error) => {
      console.error(error);
      process.exit(1);
    });
}

module.exports = setupMockVerifications;
