# Backend – FastAPI + MongoDB + Web3

This is the backend service for the **Blockchain-Based Applicant Verification** system. It provides APIs to verify applicant GPA, work experience, and certificates. It also simulates Chainlink-like oracle interactions using `web3.py`.

---

## 📦 Tech Stack

- Python 3.10+
- FastAPI
- MongoDB (Atlas or local)
- Web3.py
- Pydantic
- Uvicorn

---

## 🚀 Getting Started

### 1. Create and activate virtual environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the FastAPI server

```bash
uvicorn app.main:app --reload
```

Visit: [http://localhost:8000/docs](http://localhost:8000/docs) for Swagger UI.

---

## 📂 Directory Structure

```
backend/
├── app/
│   ├── main.py                # FastAPI entrypoint
│   ├── routes/
│   │   └── verification.py    # GPA, experience, and certificate APIs
│   ├── services/
│   │   ├── mock_db.py         # MongoDB data access
│   │   ├── blockchain.py      # web3 interaction
│   │   └── oracle_simulator.py# Simulate oracle fulfillment
│   ├── models/
│   │   └── schemas.py         # Pydantic models
│   └── utils/
│       └── helpers.py         # Shared helper functions
├── data/
│   ├── university_records.json
│   └── company_records.json
├── tests/
│   └── test_verification.py   # Unit tests
├── requirements.txt
└── README.md
```

---

## 🔐 .env Example (Optional)

```env
MONGO_URI=mongodb+srv://<username>:<password>@cluster.mongodb.net/dbname
CONTRACT_ADDRESS=0x...
CHAIN_ID=1337
PRIVATE_KEY=0x...
```
