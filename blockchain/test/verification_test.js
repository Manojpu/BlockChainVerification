const Verification = artifacts.require("Verification");
const { assert } = require("chai");

contract("Verification", (accounts) => {
  const owner = accounts[0];
  const oracle = accounts[1];
  const nonOracle = accounts[2];

  // Test data
  const testDataHash = web3.utils.sha3("Test data");
  const testDetails = "Test verification details";

  let verificationContract;

  // Set up before tests
  beforeEach(async () => {
    // Deploy a new contract for each test
    verificationContract = await Verification.new({ from: owner });
  });

  describe("Deployment", () => {
    it("should set the deployer as owner", async () => {
      const contractOwner = await verificationContract.owner();
      assert.equal(contractOwner, owner, "The deployer should be the owner");
    });

    it("should set the deployer as an authorized oracle", async () => {
      const isOracle = await verificationContract.authorizedOracles(owner);
      assert.equal(
        isOracle,
        true,
        "The deployer should be an authorized oracle"
      );
    });
  });

  describe("Oracle management", () => {
    it("should allow the owner to authorize a new oracle", async () => {
      await verificationContract.authorizeOracle(oracle, { from: owner });
      const isOracle = await verificationContract.authorizedOracles(oracle);
      assert.equal(
        isOracle,
        true,
        "The account should be authorized as an oracle"
      );
    });

    it("should allow the owner to deauthorize an oracle", async () => {
      // First authorize
      await verificationContract.authorizeOracle(oracle, { from: owner });

      // Then deauthorize
      await verificationContract.deauthorizeOracle(oracle, { from: owner });

      const isOracle = await verificationContract.authorizedOracles(oracle);
      assert.equal(
        isOracle,
        false,
        "The account should no longer be an oracle"
      );
    });

    it("should prevent non-owners from authorizing oracles", async () => {
      try {
        await verificationContract.authorizeOracle(oracle, { from: nonOracle });
        assert.fail("The transaction should have reverted");
      } catch (error) {
        assert(
          error.message.includes("Only the owner"),
          "Expected 'Only the owner' error message"
        );
      }
    });
  });

  describe("Verification operations", () => {
    it("should emit an event when requesting verification", async () => {
      const tx = await verificationContract.requestVerification(
        testDataHash,
        0,
        { from: owner }
      );

      // Check for the event
      assert.equal(tx.logs.length, 1, "One event should have been emitted");
      assert.equal(
        tx.logs[0].event,
        "VerificationRequested",
        "VerificationRequested event should be emitted"
      );
      assert.equal(
        tx.logs[0].args.dataHash,
        testDataHash,
        "Data hash should match"
      );
      assert.equal(
        tx.logs[0].args.verificationType,
        0,
        "Verification type should match"
      );
    });

    it("should allow an authorized oracle to store verification results", async () => {
      // First authorize an oracle
      await verificationContract.authorizeOracle(oracle, { from: owner });

      // Store verification result
      const tx = await verificationContract.storeVerificationResult(
        testDataHash,
        true,
        0,
        testDetails,
        { from: oracle }
      );

      // Check for the event
      assert.equal(tx.logs.length, 1, "One event should have been emitted");
      assert.equal(
        tx.logs[0].event,
        "VerificationCompleted",
        "VerificationCompleted event should be emitted"
      );

      // Check the stored verification
      const result = await verificationContract.getVerificationStatus(
        testDataHash
      );
      assert.equal(
        result.isVerified,
        true,
        "Verification result should be true"
      );
      assert.equal(
        result.verificationType,
        0,
        "Verification type should be 0 (GPA)"
      );
      assert.equal(result.oracleAddress, oracle, "Oracle address should match");
      assert.equal(result.details, testDetails, "Details should match");
    });

    it("should prevent unauthorized accounts from storing verification results", async () => {
      try {
        await verificationContract.storeVerificationResult(
          testDataHash,
          true,
          0,
          testDetails,
          { from: nonOracle }
        );
        assert.fail("The transaction should have reverted");
      } catch (error) {
        assert(
          error.message.includes("Only authorized oracles"),
          "Expected 'Only authorized oracles' error message"
        );
      }
    });

    it("should correctly report if a verification exists", async () => {
      // Initially, verification should not exist
      let exists = await verificationContract.verificationExists(testDataHash);
      assert.equal(exists, false, "Verification should not exist yet");

      // Store a verification
      await verificationContract.storeVerificationResult(
        testDataHash,
        true,
        0,
        testDetails,
        { from: owner }
      );

      // Now verification should exist
      exists = await verificationContract.verificationExists(testDataHash);
      assert.equal(exists, true, "Verification should now exist");
    });

    it("should track verification hashes correctly", async () => {
      // Store two different verifications
      const dataHash1 = web3.utils.sha3("Data 1");
      const dataHash2 = web3.utils.sha3("Data 2");

      await verificationContract.storeVerificationResult(
        dataHash1,
        true,
        0,
        "Details 1",
        { from: owner }
      );
      await verificationContract.storeVerificationResult(
        dataHash2,
        false,
        1,
        "Details 2",
        { from: owner }
      );

      // Check count
      const count = await verificationContract.getVerificationCount();
      assert.equal(count, 2, "There should be 2 verifications");

      // Check hashes by index
      const hash1 = await verificationContract.getVerificationHashAtIndex(0);
      const hash2 = await verificationContract.getVerificationHashAtIndex(1);

      assert.equal(hash1, dataHash1, "First hash should match");
      assert.equal(hash2, dataHash2, "Second hash should match");
    });

    it("should revert when trying to get a non-existent verification", async () => {
      try {
        await verificationContract.getVerificationStatus(
          web3.utils.sha3("Non-existent")
        );
        assert.fail("The transaction should have reverted");
      } catch (error) {
        assert(
          error.message.includes("No verification record found"),
          "Expected 'No verification record found' error message"
        );
      }
    });
  });
});
