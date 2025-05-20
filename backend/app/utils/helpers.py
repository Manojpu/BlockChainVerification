"""
Helper utilities for the blockchain verification system.
"""
import json
import hashlib
from typing import Dict, Any, Optional
from datetime import datetime, timezone

def create_hash(data: Dict[str, Any]) -> str:
    """
    Create a deterministic hash from a dictionary.
    
    Args:
        data: Dictionary to hash
        
    Returns:
        Hex string of the hash
    """
    # Ensure consistent serialization by sorting keys
    serialized = json.dumps(data, sort_keys=True)
    # Create SHA-256 hash
    hash_obj = hashlib.sha256(serialized.encode())
    return "0x" + hash_obj.hexdigest()

def timestamp_to_datetime(timestamp: int) -> str:
    """
    Convert Unix timestamp to ISO datetime string.
    
    Args:
        timestamp: Unix timestamp
        
    Returns:
        ISO formatted datetime string
    """
    dt = datetime.fromtimestamp(timestamp, tz=timezone.utc)
    return dt.isoformat()

def format_blockchain_address(address: str) -> str:
    """
    Format blockchain address for display.
    
    Args:
        address: Ethereum address
        
    Returns:
        Formatted address (first 6 chars...last 4 chars)
    """
    if not address:
        return ""
        
    if address.startswith("0x"):
        return f"{address[:8]}...{address[-6:]}"
    else:
        return f"0x{address[:6]}...{address[-4:]}"
        
def format_verification_type(type_index: int) -> str:
    """
    Convert verification type index to human-readable string.
    
    Args:
        type_index: Verification type index from smart contract
        
    Returns:
        Human-readable verification type string
    """
    types = {
        0: "GPA Verification",
        1: "Employment Verification",
        2: "Degree Verification",
        3: "Certificate Verification"
    }
    
    return types.get(type_index, "Unknown Verification Type")

def format_verification_result(result: Dict[str, Any]) -> Dict[str, Any]:
    """
    Format verification result for human-readable display.
    
    Args:
        result: Verification result from blockchain
        
    Returns:
        Formatted verification result
    """
    formatted = result.copy()
    
    # Format timestamp
    if "timestamp" in formatted:
        formatted["formatted_time"] = timestamp_to_datetime(formatted["timestamp"])
    
    # Format oracle address
    if "oracle_address" in formatted:
        formatted["formatted_oracle"] = format_blockchain_address(formatted["oracle_address"])
    
    # Format verification type
    if "verification_type" in formatted and isinstance(formatted["verification_type"], int):
        formatted["verification_type"] = format_verification_type(formatted["verification_type"])
        
    return formatted

def convert_objectid(obj):
    """
    Convert MongoDB ObjectId to string in a document or list of documents.
    """
    from bson.objectid import ObjectId
    
    if isinstance(obj, dict):
        for key, value in list(obj.items()):
            if isinstance(value, ObjectId):
                obj[key] = str(value)
            elif isinstance(value, (dict, list)):
                convert_objectid(value)
    elif isinstance(obj, list):
        for i, value in enumerate(obj):
            if isinstance(value, ObjectId):
                obj[i] = str(value)
            elif isinstance(value, (dict, list)):
                convert_objectid(value)
    return obj

def extract_gpa(details: str) -> Optional[float]:
    """
    Extract GPA value from education details.
    
    Args:
        details: Education details string
        
    Returns:
        Extracted GPA as float or None if not found
    """
    if not details:
        return None
        
    # Common patterns for GPA
    gpa_patterns = [
        r'CGPA:\s*(\d+\.\d+)/4\.0', 
        r'C-GPA:\s*(\d+\.\d+)/4\.0',
        r'GPA:\s*(\d+\.\d+)/4\.0',
        r'CGPA\s*(\d+\.\d+)/4\.0',
        r'C-GPA\s*(\d+\.\d+)/4\.0',
        r'GPA\s*(\d+\.\d+)/4\.0',
        r'CGPA:?\s*(\d+\.\d+)',
        r'GPA:?\s*(\d+\.\d+)'
    ]
    import re
    for pattern in gpa_patterns:
        match = re.search(pattern, details)
        if match:
            try:
                return float(match.group(1))
            except (ValueError, IndexError):
                continue
    
    return None