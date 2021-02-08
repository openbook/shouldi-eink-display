import requests
import pytz, datetime

tz = pytz.timezone("Europe/London")


class CarbonIntensityForecastGB:
    def __init__(
        self,
        gen_limit=33,
        gen_mix=["solar", "wind", "hydro"],
        date_start="",
        date_end="",
        region="",
        postcode="",
    ):
        self.api_base = "https://api.carbonintensity.org.uk"
        self.adjust_time = (
            True
            if tz.utcoffset(datetime.datetime.now().now()).total_seconds() > 0
            else False
        )
        self.gen_limit = gen_limit
        self.date_start = date_start
        self.date_end = date_end
        self.region = region
        self.postcode = postcode
        self.response_data = {}
        self.parsed_data = {}
        self.gen_mix = gen_mix
        self.set_date_range()
        self.fetch_data()

    def fetch_data(self):
        response_forecast = requests.get(self.get_request_url())
        response = response_forecast.json()
        self.response_data = (
            response["data"]["data"]
            if self.region != "" or self.postcode != ""
            else response["data"]
        )

    def get_request_url(self):
        url = self.api_base
        url += (
            "/regional/intensity/"
            if self.region != "" or self.postcode != ""
            else "/generation/"
        )
        url += self.date_start.isoformat() + "/" + self.date_end.isoformat()
        if self.postcode != "":
            url += "/postcode/" + self.postcode
        if self.region != "":
            url += "/regionid/" + self.region
        return url

    def get_response_renewable_mix(self):
        formatted = {}
        for d in self.response_data:
            date = datetime.datetime.strptime(d["from"], "%Y-%m-%dT%H:%MZ")
            if pytz.UTC.localize(date) < self.date_start:
                continue
            date_key = date.strftime("%Y-%m-%d")
            if date_key not in formatted:
                formatted[date_key] = {}
            if d["from"] not in formatted[date_key]:
                formatted[date_key][d["from"]] = {}
            formatted[date_key][d["from"]] = self.get_generation_mix(d)

        return formatted

    def get_max_response_by_slot(self):
        data_out = {}
        gen = self.get_response_by_slot()
        for day, items in gen.items():
            data_out[day] = max(items.items(), key=lambda k: k[1])
        return data_out

    def get_response_by_slot(self, return_type="total"):
        data_out = {}
        formatted = {}
        for d in self.response_data:
            date = datetime.datetime.strptime(d["from"], "%Y-%m-%dT%H:%MZ")
            if pytz.UTC.localize(date) < self.date_start:
                continue
            date_key = date.strftime("%Y-%m-%d")
            if date_key not in formatted:
                formatted[date_key] = {}
            slot = self.get_slot_name(d["from"])
            if not slot:
                continue
            if slot not in formatted[date_key]:
                formatted[date_key][slot] = []
            formatted[date_key][slot].append(self.get_generation_mix_total_for_slot(d))
        for day in formatted:
            if day not in data_out:
                data_out[day] = {}
            for slot in formatted[day]:
                if slot not in data_out[day]:
                    data_out[day][slot] = []
                total = sum(formatted[day][slot])
                if return_type == "bool":
                    data_out[day][slot] = (
                        True
                        if total / len(formatted[day][slot]) > self.gen_limit
                        else False
                    )
                else:
                    data_out[day][slot] = total / len(formatted[day][slot])

        return data_out

    def get_slot_name(self, date_in):
        date = datetime.datetime.strptime(date_in, "%Y-%m-%dT%H:%MZ")
        if self.adjust_time:
            if 0 <= date.hour < 6:
                return "night"
            if 6 <= date.hour < 12:
                return "morning"
            if 12 <= date.hour < 18:
                return "afternoon"
            if 18 <= date.hour <= 23:
                return "evening"
        else:
            if 0 <= date.hour < 5:
                return "night"
            if 5 <= date.hour < 11:
                return "morning"
            if 11 <= date.hour < 17:
                return "afternoon"
            if 17 <= date.hour <= 23:
                return "evening"

        return False

    def set_date_range(self):
        start_hour = 1 if self.adjust_time else 0
        if self.date_start == "":
            self.date_start = datetime.datetime.now(datetime.timezone.utc).replace(
                hour=start_hour, minute=0, second=0, microsecond=0
            )
        else:
            self.date_start = datetime.datetime.strptime(
                self.date_start, "%Y-%m-%dT%H:%MZ"
            )

        if self.date_end == "":
            self.date_end = self.date_start + datetime.timedelta(days=5)
        else:
            self.date_end = datetime.datetime.strptime(self.date_end, "%Y-%m-%dT%H:%MZ")

    def get_generation_mix_total(self, data_in):
        return sum(c["perc"] for c in data_in)

    def get_generation_mix_total_for_slot(self, slot_data):
        gen_mix = self.get_generation_mix(slot_data)
        return self.get_generation_mix_total(gen_mix)

    def get_generation_mix(self, data):
        data_out = []
        for d in data["generationmix"]:
            if d["fuel"] in self.gen_mix:
                data_out.append(d)
        return data_out

    def now(self, return_type="data"):
        minutes_now = 30 if datetime.datetime.now().time().minute > 30 else 0
        key = (
            datetime.datetime.now()
            .replace(minute=minutes_now, second=0, microsecond=0)
            .strftime("%Y-%m-%dT%H:%MZ")
        )
        data_out = {}
        for data in self.response_data:
            if data["from"] == key:
                data_out = self.get_generation_mix(data)
                break

        if return_type == "bool":
            return (
                True
                if self.get_generation_mix_total(data_out) > self.gen_limit
                else False
            )
        elif return_type == "total":
            return self.get_generation_mix_total(data_out)
        else:
            return data_out

    def forecast(self, return_type="data"):
        if return_type == "bool":
            return self.get_response_by_slot("bool")
        elif return_type == "total":
            return self.get_response_by_slot()
        else:
            return self.get_response_renewable_mix()

    def forecast_max(self):
        return self.get_max_response_by_slot()
