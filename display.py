from configparser import ConfigParser
import display_combined
import display_forecast
import display_octopus_agile
import display_now

config = ConfigParser()
config.read("config.ini")
display_type = config.get("main", "display")
if display_type == "combined":
    display_combined.main()
elif display_type == "forecast":
    display_forecast.main()
elif display_type == "agile":
    display_octopus_agile.main()
elif display_type == "generation":
    display_now.main()
