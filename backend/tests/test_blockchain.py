import pytest
import time
import os
import json
from unittest.mock import patch, MagicMock
from web3 import Web3

# Import the module to test
from app.services.blockchain import BlockchainService, get_blockchain_service, VerificationType

# Test data
TEST_DATA_HASH = "0x1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef"
TEST_DETAILS = "Test verification details"

class TestBlockchainService:
    """Test class for the BlockchainService"""

    @pytest.fixture
    def mock_web3(self):
        """Create a mock Web3 instance"""
        with patch('app.services.blockchain.Web3') as mock_web3_class:
            mock_web3_instance = MagicMock()
            mock_web3_class.HTTPProvider.return_value = MagicMock()
            mock_web3_class.return_value = mock_web3_instance

            # Basic web3 behaviors
            mock_web3_instance.is_connected.return_value = True
            mock_web3_instance.to_checksum_address.side_effect = lambda x: x
            mock_web3_instance.to_hex.side_effect = lambda x: x if isinstance(x, str) else f"0x{x.hex()}"
            mock_web3_instance.eth.accounts = ["0x0000000000000000000000000000000000000001"]
            mock_web3_instance.eth.gas_price = 20000000000  # 20 Gwei
            mock_web3_instance.eth.get_transaction_count.return_value = 1

            # Mock contract
            mock_contract = MagicMock()
            mock_web3_instance.eth.contract.return_value = mock_contract

            yield mock_web3_instance

    @pytest.fixture
    def blockchain_service(self, mock_web3):
        """Create a BlockchainService instance with mocked dependencies"""
        with patch('builtins.open', create=True), patch('json.load', return_value={"abi": [{"name": "testFunction", "type": "function"}]}):
            service = BlockchainService("0xTestContractAddress")
            service.contract = mock_web3.eth.contract.return_value
            return service

    def test_singleton_pattern(self):
        """Test singleton pattern"""
        service1 = BlockchainService()
        service2 = BlockchainService()
        assert service1 is service2

    def test_initialization(self, blockchain_service, mock_web3):
        """Test initialization success"""
        assert blockchain_service.is_available
        assert blockchain_service.web3 is mock_web3

    def test_check_verification_exists(self, blockchain_service):
        """Test check_verification_exists method"""
        mock_call = MagicMock(return_value=True)
        blockchain_service.contract.functions.verificationExists.return_value.call.return_value = True

        result = blockchain_service.check_verification_exists(TEST_DATA_HASH)
        assert result is True
        blockchain_service.contract.functions.verificationExists.assert_called_once()

    def test_get_verification_details(self, blockchain_service):
        """Test get_verification_details method"""
        blockchain_service.contract.functions.verificationExists.return_value.call.return_value = True
        blockchain_service.contract.functions.getVerificationStatus.return_value.call.return_value = (
            True, 0, 123456789, "0xOracleAddress", "Test details"
        )

        result = blockchain_service.get_verification_details(TEST_DATA_HASH)

        assert result["is_verified"] is True
        assert result["verification_type_str"] == "GPA"
        assert result["oracle_address"] == "0xOracleAddress"

    def test_store_verification_result_with_private_key(self, blockchain_service, mock_web3):
        """Test store_verification_result with private key"""
        blockchain_service.contract.functions.storeVerificationResult.return_value.build_transaction.return_value = {"some": "txdata"}

        mock_signed_tx = MagicMock()
        mock_signed_tx.rawTransaction = b"rawtx"
        mock_web3.eth.account.sign_transaction.return_value = mock_signed_tx
        mock_web3.eth.send_raw_transaction.return_value = b"txhash"

        mock_web3.eth.wait_for_transaction_receipt.return_value = {"status": 1}

        result = blockchain_service.store_verification_result(
            data_hash=TEST_DATA_HASH,
            is_verified=True,
            verification_type=VerificationType.GPA,
            details=TEST_DETAILS,
            account_address="0x0000000000000000000000000000000000000001",
            private_key="dummy_private_key"
        )

        assert result.startswith("0x")

    def test_store_verification_result_without_private_key(self, blockchain_service, mock_web3):
        """Test store_verification_result without private key"""
        blockchain_service.contract.functions.storeVerificationResult.return_value.build_transaction.return_value = {"some": "txdata"}

        mock_web3.eth.send_transaction.return_value = b"txhash"
        mock_web3.eth.wait_for_transaction_receipt.return_value = {"status": 1}

        result = blockchain_service.store_verification_result(
            data_hash=TEST_DATA_HASH,
            is_verified=True,
            verification_type=VerificationType.GPA,
            details=TEST_DETAILS,
            account_address="0x0000000000000000000000000000000000000001"
        )

        assert result.startswith("0x")

    def test_fallback_to_simulation(self, blockchain_service):
        """Test fallback to simulation when blockchain unavailable"""
        blockchain_service.is_available = False

        result = blockchain_service.store_verification_result(
            TEST_DATA_HASH, True, VerificationType.GPA, TEST_DETAILS
        )
        assert result.startswith("0xsimulated")

    def test_get_blockchain_service_function(self):
        """Test get_blockchain_service"""
        service1 = get_blockchain_service()
        service2 = get_blockchain_service()
        assert service1 is service2  # Should be same (singleton)

if __name__ == "__main__":
    pytest.main(["-xvs", __file__])
