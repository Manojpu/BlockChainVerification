from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging

from app.routes import verification
from app.routes import resume_verification  # Add this import

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Blockchain-Based Applicant Verification API",
    description="API for verifying resume information using blockchain and oracle simulations",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Update with specific origins in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(verification.router, prefix="/verification")
app.include_router(resume_verification.router)  # Add this line

@app.get("/")
async def root():
    return {
        "name": "Blockchain-Based Applicant Verification API",
        "version": "1.0.0",
        "status": "online"
    }

@app.get("/health")
async def health():
    return {"status": "healthy"}