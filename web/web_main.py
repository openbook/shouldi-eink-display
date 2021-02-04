from flask import Flask, render_template, request
from configparser import ConfigParser
import os, sys, inspect

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
    if request.method == "POST":
        display_type = request.form["display"]
        config.read("config.ini")
        config.set("main", "display", display_type)
        config.write(open("config.ini", "w"))
        if display_type == "combined":
            display_combined.main()
        elif display_type == "forecast":
            display_forecast.main()
        elif display_type == "octopus":
            display_octopus_agile.main()
        elif display_type == "generation":
            display_now.main()

    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=8080)
