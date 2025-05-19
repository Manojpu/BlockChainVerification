import { expect } from "chai";
import { ethers } from "hardhat";

describe("ResumeVerifier", function () {
    let ResumeVerifier;
    let resumeVerifier;
    let owner;
    let addr1;

    beforeEach(async function () {
        ResumeVerifier = await ethers.getContractFactory("ResumeVerifier");
        [owner, addr1] = await ethers.getSigners();
        resumeVerifier = await ResumeVerifier.deploy();
        await resumeVerifier.deployed();
    });

    describe("Deployment", function () {
        it("Should set the right owner", async function () {
            expect(await resumeVerifier.owner()).to.equal(owner.address);
        });
    });

    describe("Verification", function () {
        it("Should allow a resume to be verified", async function () {
            const resumeHash = ethers.utils.keccak256("Sample Resume Data");
            await resumeVerifier.verifyResume(resumeHash);
            expect(await resumeVerifier.isVerified(resumeHash)).to.be.true;
        });

        it("Should not allow the same resume to be verified twice", async function () {
            const resumeHash = ethers.utils.keccak256("Sample Resume Data");
            await resumeVerifier.verifyResume(resumeHash);
            await expect(resumeVerifier.verifyResume(resumeHash)).to.be.revertedWith("Resume already verified");
        });
    });

    describe("Events", function () {
        it("Should emit a Verified event on successful verification", async function () {
            const resumeHash = ethers.utils.keccak256("Sample Resume Data");
            await expect(resumeVerifier.verifyResume(resumeHash))
                .to.emit(resumeVerifier, "Verified")
                .withArgs(resumeHash);
        });
    });
});