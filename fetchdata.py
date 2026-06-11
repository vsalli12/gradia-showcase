import traceback
import requests
import time
import sys
import pandas as pd

def fetchData(PATH_DATA):

    limit = 5000

    datagroup = "opinnaytetyot"
    requestTries = 3

    url = f"https://api.vipunen.fi/api/resources/{datagroup}/data?limit={limit}&offset="
    lineCountURL = f"https://api.vipunen.fi/api/resources/{datagroup}/data/count"

    filePath = PATH_DATA

    HEADERS = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        #"Caller-Id": "viliam sälli"
    }
    maxLineCount = requests.get(lineCountURL, headers=HEADERS).json()

    counter = 0

    allData = []

    for _ in range(0, maxLineCount, limit):

        urlTemp = f"{url}{counter}"

        response = None

        for tryIndex in range(1, requestTries + 1):
            try:
                response = requests.get(urlTemp, headers=HEADERS).json()
                break

            except ValueError:
                traceback.print_exc()
                print(f"{tryIndex}. retry")
                time.sleep(1)

        if response is None:
            print(f"Request failed after {requestTries} attempts. Exiting.")
            sys.exit(0)

        allData.extend(response)

        counter += limit

        print(min(counter, maxLineCount))

    df = pd.DataFrame(allData)

    df.to_csv(filePath, index=False)

    print(f"Ready, {len(df)} rows fetched")
    return df