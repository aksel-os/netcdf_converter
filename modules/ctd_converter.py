import os
import xarray as xr
from datetime import datetime as dt
from datetime import UTC
import numpy as np
import pandas as pd

class CTD_Converter:
    def __init__(self, filename: str) -> None:
        self._path: str = f"/Users/kepler/prosjekter/netcdf_converter/test_data/{filename}"
        self._time_now: str = dt.now(UTC).strftime("%Y-%m-%dT%H:%M:%SZ")
        self._df = pd.read_csv(self._path, sep='\t', header=3, encoding="unicode_escape")

        # Converts date format
        self._df["Date"] = pd.to_datetime(self._df["Date"]).dt.strftime("%Y-%m-%d")
        self._df["Event_Date"] = self._df["Date"] + "T" + self._df["Time"] + "Z"

    def array_convertion(self):
        xrds = xr.Dataset(
            coords={
                "Pressure": self._df["Press"],
                "Date": self._df["Event_Date"],
                "Time": self._df["Time"],
            },
            data_vars={
                "Temperature": ("", self._df["Temp"]),
                "Salinity": ("", self._df["Sal."]),
                "Conductivity": ("", self._df["Cond."]),
                "Fluorescence": ("", self._df["F (µg/l)"]),
                "Oxygen Saturation": ("", self._df["OpOx %"]),
                "Dissolved Oxygen":  ("", self._df["Opmg/l"]),
                "Sound Velocity": ("", self._df["S. vel."]),
                "Density": ("", self._df["Density"]),
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
            "history": f"{self._time_now}: Modified by Aksel Steen using python",
            "source": "Measurement",
            "date_created": self._time_now,
            "creator_type": "person",
            "instrument": "SAIV SD204 1432",
        }

        return xrds
