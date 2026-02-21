from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from career_graph import run_career_pipeline
from database import assessments_collection # Import your database connection
from datetime import datetime

app = FastAPI()

# Allow frontend to communicate with backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Define the structure of the data coming from the frontend
class AssessmentData(BaseModel):
    name: str
    stream: str
    education_level: str
    hobbies: str
    favorite_subject: str
    work_preference: str
    interest_answers: list[str] = []
    personality_answers: list[str] = []
    aptitude_score: int

@app.post("/analyze")
def analyze(data: AssessmentData):
    # 1. Generate the AI career recommendation first
    result = run_career_pipeline(data)
    
    # 2. Try to save the user's data and the AI's answer to MongoDB
    try:
        # Convert the incoming data to a Python dictionary
        db_record = data.model_dump() 
        
        # Add the AI's answer and the exact time they took the test
        db_record["ai_recommendation"] = result
        db_record["timestamp"] = datetime.now()
        
        # Insert it into the database
        assessments_collection.insert_one(db_record)
        print(f"✅ Successfully saved {data.name}'s assessment to MongoDB!")
        
    except Exception as e:
        # If MongoDB crashes or timeouts, it will print this error 
        # but it WON'T crash the app, preventing the frontend from freezing!
        print(f"⚠️ Warning: Database save failed. Error: {e}")
    
    # 3. Always return the AI result to the frontend no matter what
    return {"result": result}