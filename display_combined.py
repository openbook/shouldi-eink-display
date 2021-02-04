#!/usr/bin/python3
import sys
import os
import datetime
from PIL import ImageOps, Image, ImageFont, ImageDraw
from inky.auto import auto

imgdir = os.path.join(
    os.path.dirname(os.path.dirname(os.path.relpath(__file__))), "assets"
)

if os.path.exists("lib"):
    sys.path.append("lib")
from carbonintensityforecast import CarbonIntensityForecastGB
import fonts


def main():

    inky_display = auto()

    img = Image.new("P", inky_display.resolution)
    draw = ImageDraw.Draw(img)

    template = Image.open(os.path.join(imgdir, "template-combined.png"))
    img.paste(template, (0, 0))

    carbon_intensity = CarbonIntensityForecastGB()
    intensity_data = carbon_intensity.now()
    ci_daily_max = carbon_intensity.forecast_max()
    total_value = carbon_intensity.now("total")

    total = 0
    draw.text((15, 3), "Now", inky_display.WHITE, font=fonts.raleway_reg_40)
    for value in intensity_data:
        percentage_value = int(round(value["perc"]))
        coordsx = 100
        coordsy = 0
        total += percentage_value
        if value["fuel"] == "wind":
            coordsy = 75
        if value["fuel"] == "hydro":
            coordsy = 150
        if value["fuel"] == "solar":
            coordsy = 225
        draw.text(
            (coordsx, coordsy),
            str(percentage_value) + "%",
            inky_display.WHITE,
            font=fonts.raleway_reg_40,
        )

    draw.text((270, 3), "Forecast", inky_display.BLACK, font=fonts.raleway_reg_30)
    rhs_start = 215
    draw.text((248, 50), "Mor", inky_display.BLACK, font=fonts.raleway_light_15)
    draw.text((291, 50), "Aft", inky_display.BLACK, font=fonts.raleway_light_15)
    draw.text((328, 50), "Eve", inky_display.BLACK, font=fonts.raleway_light_15)
    draw.text((369, 50), "Ngt", inky_display.BLACK, font=fonts.raleway_light_15)

    # Display icons
    trueImage = Image.open(os.path.join(imgdir, "check.png"))
    falseImage = Image.open(os.path.join(imgdir, "remove.png"))

    index = 1
    max_x_options = {"morning": 240, "afternoon": 285, "evening": 325, "night": 365}
    for date, value in carbon_intensity.forecast("bool").items():
        if index > 4:
            break
        day = datetime.datetime.strptime(date, "%Y-%m-%d")
        dayname = day.strftime("%A")

        yValue = (index * 50) + 35
        draw.text(
            (210, yValue + 3),
            dayname[0:1],
            inky_display.BLACK,
            font=fonts.raleway_reg_25,
        )
        img.paste(trueImage if value["morning"] else falseImage, (245, yValue))
        img.paste(trueImage if value["afternoon"] else falseImage, (285, yValue))
        img.paste(trueImage if value["evening"] else falseImage, (325, yValue))
        img.paste(trueImage if value["night"] else falseImage, (365, yValue))
        max_value = max_x_options.get(ci_daily_max[date], "Invalid max")
        draw.rectangle(
            [(max_value + 4, yValue + 33), (max_value + 28, yValue + 35)],
            inky_display.BLACK,
        )
        index += 1

    date_now = datetime.datetime.now()
    draw.text(
        (245, 280),
        "Updated :" + date_now.strftime("%H:%M"),
        inky_display.BLACK,
        font=fonts.raleway_light_13,
    )

    inky_display.set_image(img)
    inky_display.show()


if __name__ == "__main__":
    main()
