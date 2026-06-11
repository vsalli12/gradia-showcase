import json

from fetchdata import fetchData
from makePayload import makePayload
import os
from google import genai
from gemini import generateDatapoints
def generateInfo():

    PATH_DATA = "cache/data.csv"
    PATH_MODEL_RESPONSE = "cache/modelResponse.txt"

    USE_FETCH = not os.path.exists(PATH_DATA)
    if USE_FETCH:
        fetchData(PATH_DATA)
        print("Data fetched, now processing...")
    else:
        print("Data file already exists, skipping fetch.")
    
    payload, totalTheses = makePayload(PATH_DATA, asDict=False)
    
    GENAI = True
    if GENAI:
        DATAPOINTS = generateDatapoints(payload, PATH_MODEL_RESPONSE)

    else:
        with open(PATH_MODEL_RESPONSE, "r", encoding="utf-8") as f:
            DATAPOINTS = f.read()

    DATAPOINTS = DATAPOINTS.split("&")
    DP_DICT = {}
    for i, dp in enumerate(DATAPOINTS):
        if dp.strip():
            lines = dp.strip().split("\n")
            year = int(lines[0].strip())
            bullets = [line.strip() for line in lines[1:] if line.strip()]
            DP_DICT[year] = bullets

    jsonLike = {}
    for key in totalTheses:
        jsonLike[key] = {
            "theses": totalTheses[key].get("total", 0),
            "insight": DP_DICT.get(key, []),
            "universities": totalTheses[key].get("unis", []),
            "fields": totalTheses[key].get("fields", [])
        }
    print("Json fetched!")
    #print(jsonLike)
    return jsonLike
    #with open("insights.json", "w", encoding="utf-8") as f:
    #    json.dump(jsonLike, f, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    generateInfo()