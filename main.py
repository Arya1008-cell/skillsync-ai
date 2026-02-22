from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
from langchain_google_genai import ChatGoogleGenerativeAI

# This imports your existing career AI logic
from career_graph import run_career_pipeline 

app = FastAPI()

# --- 1. CORS Setup (Crucial for Vercel to talk to Render) ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows any frontend website to connect
    allow_credentials=True,
    allow_methods=["*"],  # Allows POST, GET, etc.
    allow_headers=["*"],
)

# --- 2. Data Models ---
class AssessmentData(BaseModel):
    name: str
    stream: str
    education_level: str
    hobbies: str
    favorite_subject: str
    work_preference: str
    interest_answers: list = []
    personality_answers: list = []
    aptitude_score: int

class ChatRequest(BaseModel):
    message: str

# --- 3. Routes ---

# Your main career assessment route
@app.post("/analyze")
async def analyze_career(data: AssessmentData):
    try:
        # Calls your existing AI generation logic
        result = run_career_pipeline(data.dict())
        return {"result": result}
    except Exception as e:
        print(f"Error in /analyze: {e}")
        raise HTTPException(status_code=500, detail="Error generating career roadmap")

# Your new SkillSync Chatbot route
@app.post("/chat")
async def chat_with_bot(req: ChatRequest):
    try:
        # Initialize Gemini using LangChain
        llm = ChatGoogleGenerativeAI(
            model="gemini-1.5-pro", 
            google_api_key=os.getenv("GOOGLE_API_KEY")
        )
        
        # Give the bot a personality
        prompt = f"""
        You are 'SkillSync AI', a friendly and highly encouraging career guidance counselor. 
        A student asks you: "{req.message}"
        Answer them directly, helpfully, and keep your response under 3 sentences so it fits in a chat window.
        """
        
        response = llm.invoke(prompt)
        return {"reply": response.content}
        
    except Exception as e:
        print(f"Chat Error: {e}")
        raise HTTPException(status_code=500, detail="Could not connect to AI.")