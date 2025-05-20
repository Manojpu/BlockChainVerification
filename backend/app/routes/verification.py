"""
API routes for blockchain-based verification services.
"""
from fastapi import APIRouter, HTTPException, Depends 
from typing import List, Dict, Any

from ..services.mock_db import MockDatabase
from ..services.blockchain import BlockchainClient, VerificationType
from ..services.oracle_simulator import OracleSimulator
from ..models.schemas import (
    GPAVerificationRequest,
    DegreeVerificationRequest,
    EmploymentVerificationRequest,
    VerificationResponse,
    BlockchainStatus,
    VerificationListResponse
)

# Create router
router = APIRouter(
    prefix="/verification",
    tags=["verification"],
    responses={404: {"description": "Not found"}},
)

# Service dependencies
def get_db():
    db = MockDatabase()
    try:
        yield db
    finally:
        db.close()

def get_blockchain():
    blockchain = BlockchainClient()
    try:
        yield blockchain
    finally:
        pass  # No cleanup needed for blockchain client

def get_oracle():
    oracle = OracleSimulator()
    try:
        yield oracle
    finally:
        oracle.close()

# Routes
@router.post("/gpa", response_model=VerificationResponse)
async def verify_gpa(
    request: GPAVerificationRequest,
    oracle: OracleSimulator = Depends(get_oracle)
):
    """
    Verify GPA information against blockchain and university records.
    """
    try:
        result = oracle.verify_and_store_on_blockchain(
            data=request.dict(),
            verification_type=VerificationType.GPA
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error verifying GPA: {str(e)}")

@router.post("/degree", response_model=VerificationResponse)
async def verify_degree(
    request: DegreeVerificationRequest,
    oracle: OracleSimulator = Depends(get_oracle)
):
    """
    Verify degree information against blockchain and university records.
    """
    try:
        result = oracle.verify_and_store_on_blockchain(
            data=request.dict(),
            verification_type=VerificationType.DEGREE
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error verifying degree: {str(e)}")

@router.post("/employment", response_model=VerificationResponse)
async def verify_employment(
    request: EmploymentVerificationRequest,
    oracle: OracleSimulator = Depends(get_oracle)
):
    """
    Verify employment information against blockchain and company records.
    """
    try:
        result = oracle.verify_and_store_on_blockchain(
            data=request.dict(),
            verification_type=VerificationType.EMPLOYMENT
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error verifying employment: {str(e)}")

@router.get("/status", response_model=BlockchainStatus)
async def get_blockchain_status(
    blockchain: BlockchainClient = Depends(get_blockchain)
):
    """
    Get the current blockchain status and verification contract info.
    """
    try:
        block_number = blockchain.w3.eth.block_number
        verification_count = blockchain.get_verification_count()
        
        return {
            "provider": blockchain.w3.provider.endpoint_uri,
            "contract_address": blockchain.contract_address,
            "block_number": block_number,
            "verification_count": verification_count
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting blockchain status: {str(e)}")

@router.get("/list", response_model=VerificationListResponse)
async def list_verifications(
    blockchain: BlockchainClient = Depends(get_blockchain)
):
    """
    Get a list of all verifications stored on the blockchain.
    """
    try:
        verifications = blockchain.get_all_verifications()
        
        return {
            "verifications": verifications,
            "total": len(verifications)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error listing verifications: {str(e)}")

@router.get("/{data_hash}", response_model=Dict[str, Any])
async def get_verification(
    data_hash: str,
    blockchain: BlockchainClient = Depends(get_blockchain)
):
    """
    Get verification details by data hash.
    """
    try:
        if not blockchain.verification_exists(data_hash):
            raise HTTPException(status_code=404, detail="Verification not found")
            
        verification = blockchain.get_verification_status(data_hash)
        verification["data_hash"] = data_hash
        
        return verification
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting verification: {str(e)}")

@router.get("/mock/university/{name}")
async def get_university_record(
    name: str,
    db: MockDatabase = Depends(get_db)
):
    """
    Get university record for a student (for debugging/demo purposes).
    """
    try:
        record = db.get_university_record_by_name(name)
        if not record:
            raise HTTPException(status_code=404, detail=f"No university record found for {name}")
        
        # Remove MongoDB _id
        if "_id" in record:
            del record["_id"]
            
        return record
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting university record: {str(e)}")

@router.get("/mock/employment/{name}")
async def get_employment_records(
    name: str,
    db: MockDatabase = Depends(get_db)
):
    """
    Get employment records for an employee (for debugging/demo purposes).
    """
    try:
        records = db.get_employment_record_by_name(name)
        if not records:
            raise HTTPException(status_code=404, detail=f"No employment records found for {name}")
        
        # Remove MongoDB _id
        for record in records:
            if "_id" in record:
                del record["_id"]
            
        return records
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting employment records: {str(e)}")