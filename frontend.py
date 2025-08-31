import streamlit as st
from dotenv import load_dotenv
import os

load_dotenv()

from langchain_groq import ChatGroq
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

from src.helper import CandidateInfo
from src.prompt import INTERVIEW_PROMPT, GREETING_MESSAGE, INFORMATION_PROMPTS
from src.store import save_candidate

# Page config
st.set_page_config(
    page_title="AI Hiring Assistant",
    page_icon="🤖",
    layout="centered"
)

# Initialize LLM - using your exact code
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

llm = ChatGroq(
    model="llama3-70b-8192",
    temperature=0.2,
)

# Title
st.title("AI Hiring Assistant")
st.markdown("---")

# Initialize session state
if 'candidate_data' not in st.session_state:
    st.session_state.candidate_data = {}
    st.session_state.questions_generated = False

# Display greeting
st.info(GREETING_MESSAGE)

# Input form
with st.form("candidate_form"):
    st.subheader("Candidate Information")
    
    name = st.text_input("Full Name", placeholder="John Doe")
    email = st.text_input("Email", placeholder="john@example.com")
    phone_number = st.text_input("Phone Number", placeholder="+91-1234567890")
    years_of_experience = st.number_input("Years of Experience", min_value=0, max_value=50, value=0)
    desired_position = st.text_input("Desired Position", placeholder="Backend Developer")
    current_location = st.text_input("Current Location", placeholder="Delhi, India")
    tech_stack = st.text_area("Tech Stack", placeholder="Python, Django, PostgreSQL, Docker", 
                              help="Enter technologies separated by commas")
    
    submit_button = st.form_submit_button("Generate Interview Questions")

# Process form submission
if submit_button:
    if not all([name, email, phone_number, desired_position, current_location, tech_stack]):
        st.error("Please fill in all fields!")
    else:
        try:
            # Validate using Pydantic
            candidate = CandidateInfo(
                name=name,
                email=email,
                phone_number=phone_number,
                years_of_experience=years_of_experience,
                desired_position=desired_position,
                current_location=current_location,
                tech_stack=tech_stack
            )
            
            # Store candidate data
            st.session_state.candidate_data = candidate.model_dump()
            
            with st.spinner("Generating technical questions..."):
                # Using your exact prompt and chain code
                prompt_template = PromptTemplate(
                    template=INTERVIEW_PROMPT,
                    input_variables=["tech_stack", "years_of_experience", "desired_position", "name"],
                )
                
                chain = LLMChain(prompt=prompt_template, llm=llm)
                
                # Run the chain with candidate details
                response = chain.run({
                    "tech_stack": tech_stack,
                    "years_of_experience": years_of_experience,
                    "desired_position": desired_position,
                    "name": name
                })
                
                # Save to MongoDB
                candidate_dict = {
                    "name": name,
                    "email": email,
                    "phone_number": phone_number,
                    "years_of_experience": years_of_experience,
                    "desired_position": desired_position,
                    "current_location": current_location,
                    "tech_stack": tech_stack.split(",")
                }
                
                save_candidate(candidate_dict)
                
                # Display the generated questions
                st.success(" Interview questions generated successfully!")
                st.markdown("---")
                st.subheader("Technical Interview Questions")
                st.text(response)
                
                st.session_state.questions_generated = True
                
        except Exception as e:
            st.error(f"Error: {str(e)}")

# Clear button
if st.session_state.questions_generated:
    if st.button("Start New Interview"):
        st.session_state.candidate_data = {}
        st.session_state.questions_generated = False
        st.rerun()