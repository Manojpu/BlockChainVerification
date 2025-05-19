# Resume Verification App

This project is a Resume Verification Application that allows users to upload, manage, and verify resumes using blockchain technology. The application is structured into three main parts: frontend, backend, and smart contracts.

## Project Structure

```
resume-verification-app/
├── frontend/          # Contains the React frontend application
│   ├── public/        # Static assets (images, fonts, etc.)
│   ├── src/           # Source code for the frontend
│   ├── .env.local     # Environment variables for frontend
│   ├── next.config.js # Next.js configuration
│   ├── package.json    # Frontend dependencies and scripts
│   └── tailwind.config.js # Tailwind CSS configuration
├── backend/           # Contains the Python backend application
│   ├── app/           # Main application code
│   ├── main.py        # Entry point for the backend
│   ├── requirements.txt # Backend dependencies
│   └── .env           # Environment variables for backend
├── smart-contracts/    # Contains the smart contracts
│   ├── contracts/     # Solidity smart contracts
│   ├── scripts/       # Scripts for deploying and verifying contracts
│   ├── test/          # Tests for smart contracts
│   ├── hardhat.config.js # Hardhat configuration
│   └── package.json    # Smart contract dependencies
├── README.md          # Project documentation
└── docker-compose.yml  # Docker configuration for the application
```

## Features

- **User Authentication**: Users can register and log in to manage their resumes.
- **Resume Management**: Users can upload, view, and verify their resumes.
- **Blockchain Integration**: Resumes are verified using smart contracts on the Ethereum blockchain.
- **Responsive Design**: The frontend is built with React and styled using Tailwind CSS for a modern user experience.

## Getting Started

### Prerequisites

- Node.js and npm for the frontend
- Python and pip for the backend
- Hardhat for smart contract development

### Installation

1. Clone the repository:
   ```
   git clone <repository-url>
   cd resume-verification-app
   ```

2. Set up the frontend:
   ```
   cd frontend
   npm install
   ```

3. Set up the backend:
   ```
   cd backend
   pip install -r requirements.txt
   ```

4. Set up the smart contracts:
   ```
   cd smart-contracts
   npm install
   ```

### Running the Application

- Start the backend server:
  ```
  cd backend
  python main.py
  ```

- Start the frontend application:
  ```
  cd frontend
  npm run dev
  ```

- Deploy the smart contracts:
  ```
  cd smart-contracts
  npx hardhat run scripts/deploy.js
  ```

### Docker

To run the application using Docker, use the following command:
```
docker-compose up
```

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.