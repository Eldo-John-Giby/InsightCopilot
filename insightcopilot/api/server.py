import os
import shutil
from fastapi import FastAPI, File, UploadFile, HTTPException
from pydantic import BaseModel
from agents.faq_agent import FAQAgent
from agents.research_agent import ResearchAgent
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = FastAPI(
    title="InsightCopilot API",
    description="GenAI Research & Reporting Agent",
    version="1.0.0"
)

# --- Pydantic Models ---
class FAQRequest(BaseModel):
    query: str

class FAQResponse(BaseModel):
    answer: str

class ResearchResponse(BaseModel):
    analysis: str

# --- Agent Initialization ---
try:
    faq_agent = FAQAgent(model_name="openai")
    research_agent = ResearchAgent(model_name="openai")
except ValueError as e:
    # This will catch missing API key errors on startup
    raise RuntimeError(f"Failed to initialize agents: {e}")


# --- API Endpoints ---

@app.get("/", summary="Root endpoint", description="A simple hello world endpoint to check if the server is running.")
async def root():
    return {"message": "Welcome to InsightCopilot API"}

@app.post("/faq", response_model=FAQResponse, summary="Get answers to business questions", tags=["FAQ Agent"])
async def get_faq_answer(request: FAQRequest):
    """
    Accepts a business-related question and returns a step-by-step answer.
    """
    try:
        answer = faq_agent.get_answer(request.query)
        return FAQResponse(answer=answer)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/research", response_model=ResearchResponse, summary="Analyze a PDF document", tags=["Research Agent"])
async def analyze_document(file: UploadFile = File(...)):
    """
    Upload a PDF report (e.g., annual report) to extract structured insights.
    """
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Invalid file type. Please upload a PDF.")

    # Create a temporary directory to store the uploaded file
    temp_dir = "temp_uploads"
    os.makedirs(temp_dir, exist_ok=True)
    temp_file_path = os.path.join(temp_dir, file.filename)

    try:
        # Save the uploaded file temporarily
        with open(temp_file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # Analyze the document
        analysis = research_agent.analyze_document(temp_file_path)
        
        if "Error:" in analysis:
             raise HTTPException(status_code=500, detail=analysis)

        return ResearchResponse(analysis=analysis)

    except HTTPException as e:
        # Re-raise HTTP exceptions to let FastAPI handle them
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")
    finally:
        # Clean up the temporary file and directory
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)
        if os.path.exists(temp_dir) and not os.listdir(temp_dir):
            os.rmdir(temp_dir)

# To run this server:
# uvicorn api.server:app --reload
