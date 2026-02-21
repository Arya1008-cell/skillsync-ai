from langchain_google_genai import ChatGoogleGenerativeAI
import os
from dotenv import load_dotenv

load_dotenv()

# Fixed the trailing space in the model name
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash", 
    google_api_key=os.getenv("GOOGLE_API_KEY")
)

def generate_career_recommendation(data):

   prompt = f"""
You are an expert AI Career Counselor.

Student Information:
Name: {data['name']}
Stream: {data['stream']}
Education Level: {data['education_level']}
Career Category: {data['level_modifier']}
Hobbies: {data['hobbies']}
Favorite Subject: {data['favorite_subject']}
Work Preference: {data['work_preference']}
Interests: {data['interest_answers']}
Personality: {data['personality_answers']}
Aptitude Score: {data['aptitude_score']} out of 5

Instructions:
- NO conversational greetings or intro paragraphs. Start immediately with the careers.
- Output the response in clean, structured Markdown format.
- Keep descriptions extremely brief and to the point.

Format each of the 3 careers EXACTLY like this template:

### 1. [Insert Career Name]
* **Why Suitable:** [Exactly 1 crisp sentence explaining the match]
* **Required Skills:** [Comma-separated list of 3-4 key skills]
* **Roadmap:** [Exactly 1 brief sentence on the next step to take]
* **Future Scope:** [Exactly 1 brief sentence on industry demand]
"""
   response = llm.invoke(prompt)
   return response.content