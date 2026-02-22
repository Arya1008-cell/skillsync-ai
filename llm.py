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
Hobbies: {data['hobbies']}
Favorite Subject: {data['favorite_subject']}
Work Preference: {data['work_preference']}
Aptitude Score: {data['aptitude_score']} out of 5

Instructions:
- NO conversational greetings or intro paragraphs. Start immediately with the careers.
- Output the response in clean, structured Markdown format.
- Keep descriptions extremely brief and to the point.
- For the 'Resources' section, generate real, clickable Markdown search links for Coursera and YouTube using the career name as the search query. Format them EXACTLY as shown in the template.

Format each of the 3 careers EXACTLY like this template:

### 1. [Insert Career Name]
* **Why Suitable:** [Exactly 1 crisp sentence explaining the match]
* **Required Skills:** [Comma-separated list of 3-4 key skills]
* **Roadmap:** [Exactly 1 brief sentence on the next step to take]
* **Future Scope:** [Exactly 1 brief sentence on industry demand]
* **Resources:** 📚 [Find Courses on Coursera](https://www.coursera.org/search?query=[Insert+Career+Name]) | 🎥 [Watch Tutorials on YouTube](https://www.youtube.com/results?search_query=[Insert+Career+Name])
"""
 response = llm.invoke(prompt)
 return response.content