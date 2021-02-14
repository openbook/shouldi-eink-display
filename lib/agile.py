import datetime
import requests
import pandas as pd
from pandas.io.json import json_normalize

class OctopusAgileTariff:
    def __init__(
            self,
            region="C"
    ):
        self.base_url = "https://api.octopus.energy/v1/products/AGILE-18-02-21/electricity-tariffs/E-1R-AGILE-18-02-21-{reg}/standard-unit-rates/".format(reg=region)
        self.df = {}
        self.fetch_data()

    def fetch_data(self):
        params = {}
        params["period_from"] = (
            datetime.datetime.now()
            .replace(hour=0, minute=0, second=0, microsecond=0)
            .strftime("%Y-%m-%dT%H:%MZ")
        )
        params["period_to"] = (
            datetime.datetime.now()
            .replace(hour=23, minute=0, second=0, microsecond=0)
            .strftime("%Y-%m-%dT%H:%MZ")
        )
        response_forecast = requests.request(method="GET", url=self.base_url, params=params)
        response = response_forecast.json()

        if response_forecast.status_code != 200:
            print("Error")

        df = json_normalize(response["results"])
        df["valid_from"] = pd.to_datetime(df["valid_from"])
        df = df.set_index("valid_from").resample("60min").mean().reset_index("valid_from")
        df = df.assign(pct=df['value_inc_vat'].rank(pct=True))
        self.df = df

    def get_df(self):
        return self.df

    def get_current_hour(self):
        now = self.df[self.df["valid_from"] == datetime.datetime.now().replace(minute=0, second=0, microsecond=0)]
        return round(now["value_inc_vat"].item(),1)

    def get_next_hour(self):
        date_now = datetime.datetime.now().replace(minute=0, second=0, microsecond=0)
        hours_added = datetime.timedelta(hours = 1)
        now = self.df[self.df["valid_from"] == date_now+hours_added]
        return round(now["value_inc_vat"].item(),1)

