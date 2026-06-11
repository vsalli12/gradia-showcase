import json

from fetchdata import fetchData
from makePayload import makePayload
import os
from google import genai
from gemini import generateDatapoints, fallBackToCache
def generateInfo():

    PATH_DATA = "cache/data.csv"
    PATH_MODEL_RESPONSE = "cache/modelResponse.txt"

    USE_FETCH = True
    if USE_FETCH:
        fetchData(PATH_DATA)
        print("Data fetched, now processing...")
    else:
        print("Skipping fetch.")
    
    payload, totalTheses = makePayload(PATH_DATA, asDict=False)
    
    GENAI = True
    if GENAI:
        DP_DICT = generateDatapoints(payload, PATH_MODEL_RESPONSE)
    else:
        DP_DICT = fallBackToCache(PATH_MODEL_RESPONSE)

    jsonLike = {}
    for key in totalTheses:
        jsonLike[key] = {
            "theses": totalTheses[key].get("total", 0),
            "insight": DP_DICT.get(key, []),
            "universities": totalTheses[key].get("unis", []),
            "fields": totalTheses[key].get("fields", [])
        }
    print("Json fetched!")
    return jsonLike



if __name__ == "__main__":
    jsonLike = generateInfo()
    print(jsonLike)