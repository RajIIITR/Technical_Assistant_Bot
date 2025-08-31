# Hiring Assistant Bot

## Project Overview

The Hiring Assistant is an intelligent conversational AI system designed to streamline the recruitment process by automating initial candidate screening, information gathering, and technical assessment. Built with advanced natural language processing capabilities using Groq's Llama3-70B model, this chatbot serves as a virtual technical interviewer that can engage candidates in meaningful conversations, extract relevant professional information, and generate tailored technical questions based on job requirements.

### Key Capabilities

- **Intelligent Question Generation**: Creates 3-6 relevant technical questions based on candidate's tech stack and experience level
- **Data Validation**: Robust input validation using Pydantic models for candidate information
- **Dual Interface**: Both REST API (FastAPI) and interactive web interface (Streamlit)
- **MongoDB Integration**: Persistent storage of candidate information and interview data
- **Experience-Based Filtering**: Tailors question difficulty to candidate's years of experience
- **Real-time Processing**: Instant question generation and candidate information storage

## Installation Instructions

### Prerequisites

- Python 3.10
- Groq API key
- MongoDB Atlas account and cluster key

### Step 1: Clone the Repository

```bash
git clone https://github.com/your-org/hiring-assistant-chatbot.git
cd hiring-assistant-chatbot
```

### Step 2: Set Up Virtual Environment

```bash
# Create virtual environment
conda create -p PG_AGI python==3.10 -y

# Activate virtual environment
# On Windows:
conda activate PG_AGI/
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Environment Configuration

Create a `.env` file in the root directory:

```env
GROQ_API_KEY=your_groq_api_key_here
CLUSTER_KEY=mongodb+srv://username:password%40cluster.mongodb.net/
```

**Important Notes:**
- Get your Groq API key from [https://console.groq.com](https://console.groq.com)
- For MongoDB Atlas, ensure '@' in password is URL-encoded as '%40'
- The MongoDB connection creates a database named `hiring_assistant` with collection `candidate_info`

### Step 5: Run the Application

#### Option 1: Run Both Services (Recommended)

```bash
python main.py
```

This will start:
- FastAPI server on `http://localhost:8000`
- Streamlit frontend on `http://localhost:8501`

#### Option 2: Run Services Separately

**Terminal 1 - FastAPI API:**
```bash
uvicorn app:app --reload --port 8000
```

**Terminal 2 - To run main.py**
```bash
python main.py
```

## Usage Guide

### For Candidates (Streamlit Interface)

1. **Access the Application**: Navigate to `http://localhost:8501`
2. **Fill Candidate Information**:
   - Full Name (2-100 characters)
   - Email Address (validated format)
   - Phone Number (international format supported)
   - Years of Experience (0-50 years)
   - Desired Position
   - Current Location
   - Tech Stack (comma-separated technologies)
3. **Generate Questions**: Click "Generate Interview Questions"
4. **Review Questions**: View personalized technical questions
5. **Start New Session**: Use "Start New Interview" for another candidate

### For Recruiters/HR Managers (API Interface)

#### Generate Interview Questions
```bash
POST http://localhost:8000/generate-interview
Content-Type: application/json

{
    "name": "John Doe",
    "email": "john@example.com",
    "phone_number": "+91-1234567890",
    "years_of_experience": 5,
    "desired_position": "Backend Developer",
    "current_location": "Delhi, India",
    "tech_stack": "Python, Django, PostgreSQL, Docker"
}
```

### API Documentation

Access interactive API documentation at `http://localhost:8000/docs` when FastAPI is running.

## Technical Details


### Core Libraries and Technologies

- **FastAPI**: High-performance REST API framework known for ASGI.
- **Streamlit**: Interactive web application framework for the candidate interface
- **LangChain**: Framework for LLM application development with prompt templating
- **Groq API**: High-speed inference platform running Llama3-70B-8192 model
- **Pydantic**: Data validation using Python type annotations
- **PyMongo**: To use MongoDB Database
- **Threading**: Concurrent execution of FastAPI and Streamlit servers

### Model Configuration

```python
llm = ChatGroq(
    model="llama3-70b-8192",
    temperature=0.2,  # Low temperature for consistent, focused responses
)
```

### Data Models

#### CandidateInfo (Pydantic)
```python
class CandidateInfo(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    email: EmailStr
    phone_number: str  # Validated with regex pattern
    years_of_experience: int = Field(..., ge=0, le=50)
    desired_position: str = Field(..., min_length=2, max_length=100)
    current_location: str = Field(..., min_length=2, max_length=100)
    tech_stack: str = Field(..., min_length=1)
```

### Database Schema

#### MongoDB Collection: `candidate_info`
```json
{
    "_id": "ObjectId",
    "name": "string",
    "email": "string",
    "phone_number": "string",
    "years_of_experience": "integer",
    "desired_position": "string",
    "current_location": "string",
    "tech_stack": ["array", "of", "technologies"]
}
```

## Prompt Design

### Core Interview Prompt Strategy

The system uses a sophisticated prompt engineering approach to generate relevant technical questions:

```python
INTERVIEW_PROMPT = """
You are a senior technical interviewer with 15 years of experience in {tech_stack}. 
You are the tech lead of the company.

Your task is to ask the candidate 3-6 **relevant and non-repetitive** technical questions 
based on their provided tech stack, years of experience, and the {desired_position} role.

- Cover programming languages, frameworks, databases, and tools from their {tech_stack}.
- Tailor questions to their {years_of_experience} years of experience level.
- If a listed tech stack is irrelevant to the {desired_position}, do not ask questions about it. 
  Instead, politely inform the candidate that those skills are not relevant for this role.
"""
```

## Challenges & Solutions

### Challenge 1: Input Validation and Data Quality
**Problem**: Handling invalid or malformed candidate information.
**Solution**: 
- Implemented comprehensive Pydantic models with field validators

### Challenge 2: Database Connection Management
**Problem**: MongoDB Atlas connection issues with special characters in passwords.
**Solution**: 
- URL-encoded special characters (@ → %40) in connection strings

### Challenge 3: Tech Stack Relevance Filtering
**Problem**: Candidates might list technologies irrelevant to their desired position.
**Solution**: 
- Enhanced prompt engineering to include relevance checking logic


## Project Structure
```
hiring-assistant-chatbot/
├── app.py                 # FastAPI application
├── frontend.py           # Streamlit interface
├── main.py              # Application launcher
├── requirements.txt     # Dependencies
├── .env                 # Environment variables
└── src/
    ├── helper.py        # Pydantic models and utilities
    ├── prompt.py        # Prompt templates
    └── store.py         # MongoDB operations
```