import os
from google import genai

def generateDatapoints(payload, PATH_MODEL_RESPONSE):
    prompt = f"""
    You are generating structured UI tooltip data.

    STRICT OUTPUT RULES (must be followed exactly):
    - Output MUST start with &2010 (or first year in dataset)
    - Output MUST contain ONLY year blocks in format specified below
    - NO text before first year block
    - NO text after last year block
    - NO headings, no explanations, no summaries
    - NO additional formatting or characters outside defined structure
    - Any violation makes output invalid

    Each year block must follow EXACT format:

    &YEAR
    Bullet 1
    Bullet 2
    Bullet 3
    Bullet 4
    Bullet 5

    Rules for bullets:
    - max 18 words
    - no prefixes (-, *, numbers)
    - no empty lines
    - no extra formatting
    - focus on trends and structural changes across years

    DATA:
    {payload}
    """
    KEY = os.getenv("GENAI_API_KEY")
    if not KEY:
        print("No API key. Using a pregenerated response.")
        with open(PATH_MODEL_RESPONSE, "r", encoding="utf-8") as f:
            return f.read()

    
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