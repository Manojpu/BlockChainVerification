// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

/**
 * @title Verification
 * @dev Contract for blockchain-based resume verification
 */
contract Verification {
    // Define verification types
    enum VerificationType { GPA, Employment, Degree, Certificate }
    
    // Structure to store verification data
    struct VerificationRecord {
        bytes32 dataHash;      // Hash of the data being verified
        bool isVerified;       // Verification result
        VerificationType verificationType;  // Type of verification
        uint256 timestamp;     // When verification occurred
        address oracleAddress; // Address of oracle that performed verification
        string details;        // Additional details (optional)
    }
    
    // Mapping from data hash to verification record
    mapping(bytes32 => VerificationRecord) public verifications;
    
    // Array to store all verification hashes for lookup
    bytes32[] public verificationHashes;
    
    // Owner of the contract
    address public owner;
    
    // Authorized oracles that can submit verifications
    mapping(address => bool) public authorizedOracles;
    
    // Events
    event VerificationRequested(bytes32 dataHash, VerificationType verificationType);
    event VerificationCompleted(bytes32 dataHash, bool result, VerificationType verificationType);
    event OracleAuthorized(address oracleAddress);
    event OracleDeauthorized(address oracleAddress);
    
    // Modifiers
    modifier onlyOwner() {
        require(msg.sender == owner, "Only the owner can call this function");
        _;
    }
    
    modifier onlyAuthorizedOracle() {
        require(authorizedOracles[msg.sender], "Only authorized oracles can call this function");
        _;
    }
    
    /**
     * @dev Constructor
     */
    constructor() {
        owner = msg.sender;
        // Authorize the contract deployer as the first oracle
        authorizedOracles[msg.sender] = true;
        emit OracleAuthorized(msg.sender);
    }
    
    /**
     * @dev Authorize a new oracle
     * @param _oracleAddress Address of the oracle to authorize
     */
    function authorizeOracle(address _oracleAddress) external onlyOwner {
        authorizedOracles[_oracleAddress] = true;
        emit OracleAuthorized(_oracleAddress);
    }
    
    /**
     * @dev Remove an oracle's authorization
     * @param _oracleAddress Address of the oracle to deauthorize
     */
    function deauthorizeOracle(address _oracleAddress) external onlyOwner {
        authorizedOracles[_oracleAddress] = false;
        emit OracleDeauthorized(_oracleAddress);
    }
    
    /**
     * @dev Request verification for data
     * @param _dataHash Hash of the data to verify
     * @param _verificationType Type of verification to perform
     */
    function requestVerification(bytes32 _dataHash, VerificationType _verificationType) external {
        emit VerificationRequested(_dataHash, _verificationType);
    }
    
    /**
     * @dev Store verification result
     * @param _dataHash Hash of the verified data
     * @param _isVerified Verification result
     * @param _verificationType Type of verification performed
     * @param _details Additional details about the verification
     */
    function storeVerificationResult(
        bytes32 _dataHash, 
        bool _isVerified, 
        VerificationType _verificationType,
        string memory _details
    ) external onlyAuthorizedOracle {
        // Store verification
        verifications[_dataHash] = VerificationRecord({
            dataHash: _dataHash,
            isVerified: _isVerified,
            verificationType: _verificationType,
            timestamp: block.timestamp,
            oracleAddress: msg.sender,
            details: _details
        });
        
        // Add hash to array if it's new
        bool hashExists = false;
        for (uint i = 0; i < verificationHashes.length; i++) {
            if (verificationHashes[i] == _dataHash) {
                hashExists = true;
                break;
            }
        }
        
        if (!hashExists) {
            verificationHashes.push(_dataHash);
        }
        
        emit VerificationCompleted(_dataHash, _isVerified, _verificationType);
    }
    
    /**
     * @dev Get verification status for a data hash
     * @param _dataHash Hash of the data to check
     * @return isVerified Verification result
     * @return verificationType Type of verification
     * @return timestamp When verification occurred
     * @return oracleAddress Address of oracle that performed verification
     * @return details Additional verification details
     */
    function getVerificationStatus(bytes32 _dataHash) external view returns (
        bool isVerified,
        VerificationType verificationType,
        uint256 timestamp,
        address oracleAddress,
        string memory details
    ) {
        VerificationRecord memory record = verifications[_dataHash];
        
        require(record.timestamp > 0, "No verification record found");
        
        return (
            record.isVerified,
            record.verificationType,
            record.timestamp,
            record.oracleAddress,
            record.details
        );
    }
    
    /**
     * @dev Check if verification exists
     * @param _dataHash Hash to check
     * @return exists True if verification exists
     */
    function verificationExists(bytes32 _dataHash) external view returns (bool) {
        return verifications[_dataHash].timestamp > 0;
    }
    
    /**
     * @dev Get verification count
     * @return count Total number of verifications
     */
    function getVerificationCount() external view returns (uint256) {
        return verificationHashes.length;
    }
    
    /**
     * @dev Get verification hash by index
     * @param _index Index in the array
     * @return dataHash Hash at the specified index
     */
    function getVerificationHashAtIndex(uint256 _index) external view returns (bytes32) {
        require(_index < verificationHashes.length, "Index out of bounds");
        return verificationHashes[_index];
    }
}