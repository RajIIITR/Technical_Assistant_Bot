import subprocess
import threading
import time
import os
from dotenv import load_dotenv

load_dotenv()


def run_fastapi():
    """Run FastAPI server."""
    subprocess.run(["uvicorn", "app:app", "--reload", "--port", "8000"])


def run_streamlit():
    """Run Streamlit frontend."""
    time.sleep(2)  # Wait for FastAPI to start
    subprocess.run(["streamlit", "run", "frontend.py"])


def main():
    """
    Main function to run both FastAPI and Streamlit.
    """
    print(" Starting Hiring Assistant Application...")
    
    # Check for required environment variables
    if not os.getenv("GROQ_API_KEY"):
        print(" Error: GROQ_API_KEY not found!")
        return
    
    # Create threads for both servers
    fastapi_thread = threading.Thread(target=run_fastapi, daemon=True)
    streamlit_thread = threading.Thread(target=run_streamlit, daemon=True)
    
    # Start both servers
    print(" Starting FastAPI server on http://localhost:8000/docs")
    fastapi_thread.start()
    
    print(" Starting Streamlit frontend on http://localhost:8501")
    streamlit_thread.start()
    
    print(" Application is running!")
    print("Press Ctrl+C to stop")
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n Shutting down...")


if __name__ == "__main__":
    main()