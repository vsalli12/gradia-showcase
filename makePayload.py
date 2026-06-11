import pandas as pd
import numpy as np
import json



def load_data(path: str) -> pd.DataFrame:
    """
    Loads the data from the given path and performs two operations:
    Counts the total number of theses by summing the "hankkeistetutOpinnaytetyot" and "opinnaytetyotEiHankkeistetut" columns.
    Creates a new "field" column based on the "koulutusala02" column, and if that is missing or marked as "Tieto puuttuu", it uses the "okmOhjauksenAla" column instead.
    If the field is still missing, it is filtered out.
    A copy of the nonfiltered dataframe 'dfRaw' is returned for university-level analysis.
    """
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

def build_university_table(df):
    uni = (
        df.groupby(["tilastovuosi", "ammattikorkeakoulu"])["total"]
        .sum()
        .reset_index()
    )

    uni["year_total"] = uni.groupby("tilastovuosi")["total"].transform("sum")
    uni["share"] = uni["total"] / uni["year_total"]

    return uni

def build_field_table(df):
    fld = (
        df.groupby(["tilastovuosi", "field"])["total"]
        .sum()
        .reset_index()
    )

    fld["year_total"] = fld.groupby("tilastovuosi")["total"].transform("sum")
    fld["share"] = fld["total"] / fld["year_total"]

    return fld

def pivot_university(uni):
    pivot = uni.pivot(
        index="ammattikorkeakoulu",
        columns="tilastovuosi",
        values="total"
    ).fillna(0)

    return pivot

def pivot_field(fld):
    pivot = fld.pivot(
        index="field",
        columns="tilastovuosi",
        values="total"
    ).fillna(0)

    return pivot

def add_deltas(pivot: pd.DataFrame):
    years = sorted(pivot.columns)

    for i in range(1, len(years)):
        y0, y1 = years[i - 1], years[i]

        pivot["delta"] = (
            (pivot[y1] - pivot[y0])
            / pivot[y0].replace(0, np.nan)
        ) * 100

    return pivot

def build_payload(table, year, top_n=10):
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
    df, dfRaw = load_data(PATH_DATA)

    uni = build_university_table(dfRaw)
    fld = build_field_table(df)

    #uni_pivot = add_deltas(pivot_university(uni))
    #fld_pivot = add_deltas(pivot_field(fld))

    payloads = {}
    finalPayload = ""
    totalTheses = {}
    for year in df["tilastovuosi"].unique():
        totalTheses[int(year)] = {
            "total": int(df[df["tilastovuosi"] == year]["total"].sum()),
            "unis": build_payload(uni, year),
            "fields": build_payload(fld, year)
        }


        payload = "UNIVERSITIES\n" + constructLines(build_payload(uni, year)) + "\nFIELDS\n" + constructLines(build_payload(fld, year))
        finalPayload += str(year) + "\n" + payload
        payloads[int(year)] = payload

    if asDict:
        return payloads, totalTheses
    return finalPayload, totalTheses







if __name__ == "__main__":
    makePayload()