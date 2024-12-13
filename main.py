import os
import xarray as xr
from datetime import datetime as dt
from datetime import UTC
import numpy as np
import pandas as pd

path: str = f"{os.path.dirname(__file__)}/test_data/20230901_MFS_CTD1432.txt"

time_now = dt.now(UTC).strftime("%Y-%m-%dT%H:%M:%SZ")

df = pd.read_csv(path, sep='\t', header=3, encoding="unicode_escape")

# Converts date format
df["Date"] = pd.to_datetime(df["Date"]).dt.strftime("%Y-%m-%d")
df["Event_Date"] = df["Date"] + "T" + df["Time"] + "Z"

xrds = xr.Dataset(
    coords={
        "Pressure": df["Press"],
        "Date": df["Event_Date"],
        "Time": df["Time"],
    },
    data_vars={
        "Temperature": ("", df["Temp"]),
        "Salinity": ("", df["Sal."]),
        "Conductivity": ("", df["Cond."]),
    }
)

# CF Compliance
xrds["Temperature"].attrs = {
    "standard_name": "sea_water_temperature",
    "long_name": "Temperature of sea water",
    "units": "degrees_Celsius",
    "coverage_content_type": "physicalMeasurement"
}
xrds["Salinity"].attrs = {
    "standard_name": "sea_water_salinity",
    "long_name": "Salinity of sea water",
    "units": "PSU",
    "coverage_content_type": "physicalMeasurement"
}
xrds["Pressure"].attrs = {
    "standard_name": "sea_water_pressure",
    "long_name": "Sea water pressure",
    "units": "dbar",
    "coverage_content_type": "coordinate"
}
xrds["Time"].attrs = {
    "standard_name": "time",
    "long_name": "time",
    "units": ""
}
xrds["Conductivity"].attrs = {
    "standard_name": "sea_water_electrical_conductivity",
    "long_name": "conductivity",
    "units": "mS/cm",
    "converage_content_type": "physical"
}

# Global Attributes
xrds.attrs = {
    "history": f"{time_now}: Modified by Aksel Steen using python",
    "source": "Measurement",
    "date_created": time_now,
    "creator_type": "person",
    "instrument": "SAIV SD204 1432",
}

print(xrds)
