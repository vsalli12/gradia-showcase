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
    - Translate field and university names to English, but keep them concise

    DATA:
    {payload}
    """
    KEY = os.getenv("GENAI_API_KEY")
    if not KEY:
        print("No API key. Using a pregenerated response.")
        return fallBackToCache(PATH_MODEL_RESPONSE)

    try:
        client = genai.Client(
            api_key=KEY
        )
    except ValueError:
        print("Invalid API key. Using a pregenerated response.")
        return fallBackToCache(PATH_MODEL_RESPONSE)

    print("Awaiting Gemini response...")
    response = client.models.generate_content(
        model="gemini-3.1-flash-lite",
        contents=prompt
    )
    print("Done!")

    DP_DICT = parseGeminiResponse(response.text)
    if DP_DICT is None:
        print("Falling back to cached response due to parsing error.")
        DP_DICT = fallBackToCache(PATH_MODEL_RESPONSE)


    
    print("Parsing done!")

    with open(PATH_MODEL_RESPONSE, "w", encoding="utf-8") as f:
        f.write(response.text)

    return DP_DICT

def parseGeminiResponse(response):
    DATAPOINTS = response.split("&")
    DP_DICT = {}
    try:
        for i, dp in enumerate(DATAPOINTS):
            if dp.strip():
                lines = dp.strip().split("\n")
                year = int(lines[0].strip())
                bullets = [line.strip() for line in lines[1:] if line.strip()]
                DP_DICT[year] = bullets
        return DP_DICT
    except Exception as e:
        print(f"Error parsing Gemini response: {e}")
        return None

def fallBackToCache(PATH_MODEL_RESPONSE):
    with open(PATH_MODEL_RESPONSE, "r", encoding="utf-8") as f:
        return parseGeminiResponse(f.read())