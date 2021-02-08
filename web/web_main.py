from flask import Flask, render_template, request
from configparser import ConfigParser
import os, sys, inspect
import re

current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)
import display_combined
import display_forecast
import display_octopus_agile
import display_now

config = ConfigParser()

app = Flask(__name__)


@app.route("/", methods=("GET", "POST"))
def index():
    config.read("config.ini")
    updated = False
    if request.method == "POST":
        display_type = request.form["display"]
        config.set("main", "display", display_type)
        if display_type == "generation":
            config.set("location", "postcode", request.form["postcode"].upper())
            config.set("location", "placename", request.form["placename"])
        config.write(open("config.ini", "w"))

        if display_type == "combined":
            display_combined.main()
        elif display_type == "forecast":
            display_forecast.main()
        elif display_type == "agile":
            display_octopus_agile.main()
        elif display_type == "generation":
            display_now.main()

        updated = True

    print(config.get("location", "placename"))

    return render_template(
        "index.html",
        display=config.get("main", "display"),
        placename=config.get("location", "placename"),
        postcode=config.get("location", "postcode"),
        updated=updated
    )


if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=8080)
