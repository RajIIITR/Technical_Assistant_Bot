from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict
from dotenv import load_dotenv
import os

load_dotenv()

from langchain_groq import ChatGroq
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

from src.helper import CandidateInfo
from src.prompt import INTERVIEW_PROMPT
from src.store import save_candidate, get_all_candidates

# Initialize FastAPI app
app = FastAPI(title="Hiring Assistant API", version="1.0.0")

# Initialize LLM - using your exact code
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

llm = ChatGroq(
    model="llama3-70b-8192",
    temperature=0.2,
)


class GenerateQuestionsRequest(BaseModel):
    """Request model for generating interview questions."""
    name: str
    email: str
    phone_number: str
    years_of_experience: int
    desired_position: str
    current_location: str
    tech_stack: str


@app.get("/")
async def root():
    """Root endpoint."""
    return {"message": "Hiring Assistant API is running!"}


@app.post("/generate-interview")
async def generate_interview(candidate: GenerateQuestionsRequest):
    """
    Generate interview questions and save candidate - main endpoint.
    This takes user input and returns the generated questions.
    """
    try:
        # Using your exact prompt and chain code
        prompt_template = PromptTemplate(
            template=INTERVIEW_PROMPT,
            input_variables=["tech_stack", "years_of_experience", "desired_position", "name"],
        )
        
        chain = LLMChain(prompt=prompt_template, llm=llm)
        
        # Run the chain with candidate details - using your exact code
        response = chain.run({
            "tech_stack": candidate.tech_stack,
            "years_of_experience": candidate.years_of_experience,
            "desired_position": candidate.desired_position,
            "name": candidate.name
        })
        
        # Save candidate to MongoDB using your code structure
        candidate_dict = {
            "name": candidate.name,
            "email": candidate.email,
            "phone_number": candidate.phone_number,
            "years_of_experience": candidate.years_of_experience,
            "desired_position": candidate.desired_position,
            "current_location": candidate.current_location,
            "tech_stack": candidate.tech_stack.split(",")  # Convert to list for storage
        }
        
        save_candidate(candidate_dict)
        
        # Return the generated questions
        return {
            "candidate_name": candidate.name,
            "interview_questions": response
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/candidates")
async def get_candidates():
    """
    Get all candidates from database.
    """
    try:
        candidates = get_all_candidates()
        # Convert ObjectId to string for JSON serialization
        for candidate in candidates:
            candidate["_id"] = str(candidate["_id"])
        return {"candidates": candidates}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))