import os
from google import genai

def generateDatapoints(payload, PATH_MODEL_RESPONSE):
    prompt = f"""
        You are generating UI tooltips for each year of the following data.

        Return ONLY 5 short bullet points PER YEAR.

        Each bullet must be:
        - max 18 words
        - factual or clearly inferential
        - no preamble, no summary, no explanation sections

        Focus:
        - dominant structure
        - biggest change signals
        - key imbalance
        
        Do not focus on a single university or field, but rather the overall structure and changes in the data.

        Construct your answer based on the following example. Do not format the bullet points to have either -, * or similar.
        &2015
        Bullet 1
        Bullet 2
        Bullet 3
        Bullet 4
        Bullet 5
        &2016
        Bullet 1
        Bullet 2
        Bullet 3
        Bullet 4
        Bullet 5
        ...

        DATA:
        {payload}
    """
    KEY = os.getenv("GENAI_API_KEY")
    print(KEY)
    
    client = genai.Client(
        api_key=KEY
    )
    print("Awaiting Gemini response...")
    response = client.models.generate_content(
        model="gemini-3.1-flash-lite",
        contents=prompt
    )
    print("Done!")
    with open(PATH_MODEL_RESPONSE, "w", encoding="utf-8") as f:
        f.write(response.text)

    return response.text