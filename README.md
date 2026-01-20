 # FinTrust – Distributed Financial System

FinTrust is a distributed financial management system built using a microservices architecture.  
The project is divided into two main components:

- Backend (API Gateway + gRPC Microservices)
- Frontend (Web Client)

## Project Structure

FinTrust-System/
├── backend/       # API Gateway and microservices
├── frontend/      # Web application (Vite + React)
├── README.md
└── .gitignore

## Technologies Used

### Backend
- Python
- FastAPI / Uvicorn
- gRPC
- Microservices architecture

### Frontend
- React + Vite
- JavaScript / TypeScript
- REST communication with API Gateway

## How to Run the Project

### 1. Backend

Navigate to backend directory:

cd backend

Install dependencies:

pip install -r requirements.txt

Run the gateway:

python gateway.py

Make sure the following services are running:

- AUTH service → port 50051  
- ACCOUNT service → port 50052  
- TRANSFER service → port 50053  
- API Gateway → port 8080  

### 2. Frontend

Navigate to frontend directory:

cd frontend

Install dependencies:

npm install

Run development server:

npm run dev

Access the application at:

http://localhost:5173

## Environment Variables

Create a `.env` file inside the frontend folder with:

VITE_API_URL=http://localhost:8080

## Notes

- Make sure Apache or any service using port 8080 is disabled before running the gateway.
- All backend services must be running before starting the frontend.

## Authors

Developed as part of the Distributed Systems course project.

