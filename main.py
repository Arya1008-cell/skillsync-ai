from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from career_graph import run_career_pipeline
from database import assessments_collection
from datetime import datetime



app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


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
   
    result = run_career_pipeline(data)
    
    try:
        
        db_record = data.model_dump() 
        
       
        db_record["ai_recommendation"] = result
        db_record["timestamp"] = datetime.now()
        
      
        assessments_collection.insert_one(db_record)
        print(f"✅ Successfully saved {data.name}'s assessment to MongoDB!")
        
    except Exception as e:
       
        print(f"⚠️ Warning: Database save failed. Error: {e}")
    
  
    return {"result": result}