from llm import generate_career_recommendation

def run_career_pipeline(data):

    # Simple intelligence logic before LLM
    level_modifier = ""

    if data.education_level == "10th":
        level_modifier = "Beginner level careers"
    elif data.education_level == "12th":
        level_modifier = "Intermediate academic careers"
    elif data.education_level == "undergraduate":
        level_modifier = "Professional degree level careers"
    elif data.education_level == "postgraduate":
        level_modifier = "Advanced expert-level careers"

    processed_data = {
        "name": data.name,
        "stream": data.stream,
        "education_level": data.education_level,
        "level_modifier": level_modifier,
        "hobbies": data.hobbies,
        "favorite_subject": data.favorite_subject,
        "work_preference": data.work_preference,
        "interest_answers": data.interest_answers,
        "personality_answers": data.personality_answers,
        "aptitude_score": data.aptitude_score
    }

    return generate_career_recommendation(processed_data)