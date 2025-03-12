import os
import xarray as xr
from datetime import datetime as dt
from datetime import UTC
import numpy as np
import pandas as pd

class CTD_Converter:
    def __init__(self, filename: str) -> None:
        # Initializing Variables
        self._path: str = f"/Users/kepler/prosjekter/netcdf_converter/test_data/{filename}"
        self._time_now: str = dt.now(UTC).strftime("%Y-%m-%dT%H:%M:%SZ")
        self._df = pd.read_csv(self._path, sep='\t', header=3, encoding="unicode_escape", decimal=',')

        # Converts date format
        self._df["Date"] = pd.to_datetime(self._df["Date"]).dt.strftime("%Y-%m-%d")
        self._df["Event_Date"] = (self._df["Date"] + "T" + self._df["Time"] + "Z").apply(pd.to_datetime)

        self._time_start = self._df["Event_Date"][0]
        self._df["seconds_since_start"] = (self._df["Event_Date"] - self._time_start)
        print(self._df["seconds_since_start"])

        # Converts typing from object to float
        self._df[["Temp", "Sal.", "Cond.", "F (µg/l)", "OpOx %", "Opmg/l", "S. vel.", "Density"]] = \
            self._df[["Temp", "Sal.", "Cond.", "F (µg/l)", "OpOx %", "Opmg/l", "S. vel.", "Density"]].apply(pd.to_numeric)

    def array_convertion(self):
        xrds = xr.Dataset(
            coords={
                "Pressure": self._df["Press"]
            },
            data_vars={
                "Temperature": ("Pressure", self._df["Temp"]),
                "Salinity": ("Pressure", self._df["Sal."]),
                "Conductivity": ("Pressure", self._df["Cond."]),
                "Fluorescence": ("Pressure", self._df["F (µg/l)"]),
                "Oxygen Saturation": ("Pressure", self._df["OpOx %"]),
                "Dissolved Oxygen":  ("Pressure", self._df["Opmg/l"]),
                "Sound Velocity": ("Pressure", self._df["S. vel."]),
                "Density": ("Pressure", self._df["Density"]),
                "Date": ("", self._df["Event_Date"]),
                "Time": ("", self._df["Time"])
            }
        )

        # CF Compliance | coords
        xrds["Pressure"].attrs = {
            "standard_name": "sea_water_pressure",
            "long_name": "Sea water pressure",
            "units": "dbar",
            "coverage_content_type": "coordinate"
        }
        
        # CF Compliance | data_vars
        xrds["Time"].attrs = {
            "standard_name": "time",
            "long_name": "time",
            "units": f"seconds since {self._time_start}"
        }
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
            # Required


            # Highly Reccomended
            "title": "",
            "summary": "",
            "keywords": "",
            "Conventions": "ACDD-1.3, ",

            # Reccomended
            "id": "",
            "naming_authority": "",
            "history": f"{self._time_now}: Modified by Aksel Steen using python",
            "source": "Measurement",
            "processing_level": "",
            "comment": "",
            "acknowledgement": "",
            "license": "",
            "standard_name_vocabulary": "",
            "date_created": self._time_now,
            "creator_name": "",
            "creator_email": "",
            "creator_url": "",
            "institution": "",
            "project": "",
            "publisher_name": "",
            "publisher_email": "",
            "publisher_url" : "",
            "geospatial_bounds": "",
            "geospatial_bounds_crs": "",
            "geospatial_bounds_vertical_crs": "",
            "geospatial_lat_min": "",
            "geospatial_lat_max": "",
            "geospatial_lon_min": "",
            "geospatial_lon_max": "",
            "geospatial_vertical_min": "",
            "geospatial_vertical_max": "",
            "time_coverage_start": "",
            "time_coverage_end": "",
            "time_coverage_duration": "",
            "time_coverage_resolution": "",

            # Suggested
            "creator_type": "person",
            "instrument": "SAIV SD204 1432",
        }

        return xrds
