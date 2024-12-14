import os
import xarray as xr
from datetime import datetime as dt
from datetime import UTC
import numpy as np
import pandas as pd

path: str = f"{os.path.dirname(__file__)}/test_data/20230512_MFS_CTD1432.txt"

time_now: str = dt.now(UTC).strftime("%Y-%m-%dT%H:%M:%SZ")

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
        "Fluorescence": ("", df["F (µg/l)"]),
        "Oxygen Saturation": ("", df["OpOx %"]),
        "Dissolved Oxygen":  ("", df["Opmg/l"]),
        "Sound Velocity": ("", df["S. vel."]),
        "Density": ("", df["Density"]),
    }
)

# CF Compliance | coords
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

# CF Compliance | data_vars
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
xrds["Conductivity"].attrs = {
    "standard_name": "sea_water_electrical_conductivity",
    "long_name": "Conductivity of sea water",
    "units": "mS/cm",
    "coverage_content_type": "physicalMeasurement"
}
xrds["Fluorescence"].attrs = {
    "standard_name": "",
    "long_name": "",
    "units": "",
    "coverage_content_type": ""
}
xrds["Oxygen Saturation"].attrs = {
    "standard_name": "",
    "long_name": "",
    "units": "",
    "coverage_content_type": ""
}
xrds["Dissolved Oxygen"].attrs = {
    "standard_name": "",
    "long_name": "",
    "units": "",
    "coverage_content_type": ""
}
xrds["Sound Velocity"].attrs = {
    "standard_name": "speed_of_sound_in_sea_water",
    "long_name": "",
    "units": "m s-1",
    "coverage_content_type": ""
}
xrds["Density"].attrs = {
    "standard_name": "sea_water_density",
    "long_name": "",
    "units": "kg m-3",
    "coverage_content_type": ""
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
