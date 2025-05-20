"""
Common utilities and enums shared across verification services.
"""
from enum import Enum

class VerificationState(str, Enum):
    """Enum for verification states of individual items."""
    PENDING = "PENDING"
    BLOCKCHAIN_VERIFIED = "BLOCKCHAIN_VERIFIED"
    SUBMITTED = "SUBMITTED"
    VERIFIED = "VERIFIED"
    REJECTED = "REJECTED"