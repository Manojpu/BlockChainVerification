// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract ResumeVerifier {
    struct Resume {
        string name;
        string email;
        string[] skills;
        string ipfsHash;
        bool verified;
    }

    mapping(address => Resume) public resumes;
    mapping(address => bool) public hasResume;

    event ResumeUploaded(address indexed user, string ipfsHash);
    event ResumeVerified(address indexed user);

    function uploadResume(string memory _name, string memory _email, string[] memory _skills, string memory _ipfsHash) public {
        require(!hasResume[msg.sender], "Resume already uploaded");

        resumes[msg.sender] = Resume({
            name: _name,
            email: _email,
            skills: _skills,
            ipfsHash: _ipfsHash,
            verified: false
        });

        hasResume[msg.sender] = true;
        emit ResumeUploaded(msg.sender, _ipfsHash);
    }

    function verifyResume(address _user) public {
        require(hasResume[_user], "No resume uploaded");
        require(!resumes[_user].verified, "Resume already verified");

        resumes[_user].verified = true;
        emit ResumeVerified(_user);
    }

    function getResume(address _user) public view returns (string memory, string memory, string[] memory, string memory, bool) {
        require(hasResume[_user], "No resume uploaded");
        Resume memory resume = resumes[_user];
        return (resume.name, resume.email, resume.skills, resume.ipfsHash, resume.verified);
    }
}