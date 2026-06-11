import pandas as pd
import numpy as np

def loadData(path: str) -> pd.DataFrame:
    df = pd.read_csv(path)

    

    df["total"] = (
        df["hankkeistetutOpinnaytetyot"]
        + df["opinnaytetyotEiHankkeistetut"]
    )

    dfRaw = df.copy()

    df["field"] = df["koulutusala02"]
    mask = (
        df["field"].isna()
        | (df["field"] == "Tieto puuttuu")
    )
    df.loc[mask, "field"] = df.loc[mask, "okmOhjauksenAla"]

    df = df[
        (df["field"].notna())
        & (df["field"] != "Tieto puuttuu")
        & (df["ammattikorkeakoulu"].notna())
        & (df["ammattikorkeakoulu"] != "Tieto puuttuu")
    ]

    return df, dfRaw

def buildUniversityTable(df):
    uni = (
        df.groupby(["tilastovuosi", "ammattikorkeakoulu"])["total"]
        .sum()
        .reset_index()
    )

    uni["year_total"] = uni.groupby("tilastovuosi")["total"].transform("sum")
    uni["share"] = uni["total"] / uni["year_total"]

    return uni

def buildFieldTable(df):
    fld = (
        df.groupby(["tilastovuosi", "field"])["total"]
        .sum()
        .reset_index()
    )

    fld["year_total"] = fld.groupby("tilastovuosi")["total"].transform("sum")
    fld["share"] = fld["total"] / fld["year_total"]

    return fld

def pivotUniversity(uni):
    pivot = uni.pivot(
        index="ammattikorkeakoulu",
        columns="tilastovuosi",
        values="total"
    ).fillna(0)

    return pivot

def pivotField(fld):
    pivot = fld.pivot(
        index="field",
        columns="tilastovuosi",
        values="total"
    ).fillna(0)

    return pivot

def addDeltas(pivot: pd.DataFrame):
    years = sorted(pivot.columns)

    for i in range(1, len(years)):
        y0, y1 = years[i - 1], years[i]

        pivot["delta"] = (
            (pivot[y1] - pivot[y0])
            / pivot[y0].replace(0, np.nan)
        ) * 100

    return pivot

def buildPayload(table, year, top_n=10):
    data = table[table["tilastovuosi"] == year].copy()

    data = data.sort_values("total", ascending=False).head(top_n)

    return [
        {
            "name": r.iloc[1],
            "value": float(r["total"]),
            "share": float(r["share"])
        }
        for _, r in data.iterrows()
    ]

def constructLines(payload):
    totalLine = ""
    for item in payload:

        if "delta" in item:
            line = f"{item['name']} ({item['value']:.0f} theses ({item['delta']:+.1f}%), {item['share']:.1%} share)"
        else:
            line = f"{item['name']} ({item['value']:.0f} theses, {item['share']:.1%} share)"
        totalLine += line + "\n"
    return totalLine

def makePayload(PATH_DATA, asDict = False):
    df, dfRaw = loadData(PATH_DATA)

    uni = buildUniversityTable(dfRaw)
    fld = buildFieldTable(df)

    # Unused pivot tables with deltas, which was used for yearly difference in theses counts.
    #uni_pivot = addDeltas(pivotUniversity(uni))
    #fld_pivot = addDeltas(pivotField(fld))

    payloads = {}
    finalPayload = ""
    totalTheses = {}
    for year in df["tilastovuosi"].unique():
        totalTheses[int(year)] = {
            "total": int(df[df["tilastovuosi"] == year]["total"].sum()),
            "unis": buildPayload(uni, year),
            "fields": buildPayload(fld, year)
        }


        payload = "UNIVERSITIES\n" + constructLines(buildPayload(uni, year)) + "\nFIELDS\n" + constructLines(buildPayload(fld, year))
        finalPayload += str(year) + "\n" + payload
        payloads[int(year)] = payload

    if asDict:
        return payloads, totalTheses
    return finalPayload, totalTheses


if __name__ == "__main__":
    makePayload()