from pydantic import BaseModel, EmailStr, Field, field_validator
from typing import Optional
import re


class CandidateInfo(BaseModel):
    """
    Pydantic model for candidate information validation.
    """
    name: str = Field(..., min_length=2, max_length=100)
    email: EmailStr
    phone_number: str
    years_of_experience: int = Field(..., ge=0, le=50)
    desired_position: str = Field(..., min_length=2, max_length=100)
    current_location: str = Field(..., min_length=2, max_length=100)
    tech_stack: str = Field(..., min_length=1)
    
    @field_validator('phone_number')
    @classmethod
    def validate_phone(cls, v: str) -> str:
        """Validate phone number format.""" 
        # Regular expression to validate phone number picked from net.
        pattern = r'^[\+]?[(]?[0-9]{1,4}[)]?[-\s\.]?[(]?[0-9]{1,4}[)]?[-\s\.]?[0-9]{1,5}[-\s\.]?[0-9]{1,5}$'
        if not re.match(pattern, v):
            raise ValueError('Invalid phone number format')
        return v
    
    #Checking that tech stack is not empty if empty it will give error
    @field_validator('tech_stack')
    @classmethod
    def validate_tech_stack(cls, v: str) -> str:
        """Check if tech stack is not empty."""
        if not v or not v.strip():
            raise ValueError('Tech stack cannot be empty')
        return v.strip()


def format_candidate_info(candidate: CandidateInfo) -> str:
    """
    Format candidate information for display using streamlit
    Args:
        candidate: CandidateInfo object
    Returns:
        str: Formatted string of candidate details
    """
    return f"""
**Candidate Information:**
- Name: {candidate.name}
- Email: {candidate.email}
- Phone: {candidate.phone_number}
- Experience: {candidate.years_of_experience} years
- Position: {candidate.desired_position}
- Location: {candidate.current_location}
- Tech Stack: {candidate.tech_stack}
"""


def is_conversation_ending(message: str) -> bool:
    """
    Check if the message contains conversation-ending keywords.
    
    Args:
        message: User message
        
    Returns:
        bool: True if conversation should end
    """
    ending_keywords = ['bye', 'goodbye', 'exit', 'quit', 'end', 'stop', 'thank you', 'thanks']
    message_lower = message.lower()
    return any(keyword in message_lower for keyword in ending_keywords)