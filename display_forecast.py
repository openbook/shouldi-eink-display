#!/usr/bin/python3
import sys
import os
import datetime
import logging
from PIL import ImageOps, Image, ImageFont, ImageDraw
from inky.auto import auto

if os.path.exists("lib"):
    sys.path.append("lib")

from carbonintensityforecast import CarbonIntensityForecastGB
import fonts

imgdir = os.path.join(
    os.path.dirname(os.path.dirname(os.path.relpath(__file__))), "assets"
)


def main():

    inky_display = auto()
    img = Image.new("P", inky_display.resolution)
    draw = ImageDraw.Draw(img)
    try:
        carbon_intensity = CarbonIntensityForecastGB()
    except Exception as e:
        return logging.error('Unable to update forecast display')
    ci_daily_max = carbon_intensity.forecast_max()

    draw.rectangle([(0, 0), (400, 60)], inky_display.BLACK)
    if carbon_intensity.now("bool"):
        draw.text((10, 5), "Right now, ", inky_display.WHITE, font=fonts.raleway_reg_40)
        draw.text((214, 5), "bake!", inky_display.WHITE, font=fonts.raleway_bold_40)
    else:
        draw.text(
            (10, 5), "Can baking wait?", inky_display.WHITE, font=fonts.raleway_reg_40
        )

    draw.text((243, 70), "Ngt", inky_display.BLACK, font=fonts.raleway_light_15)
    draw.text((286, 70), "Mor", inky_display.BLACK, font=fonts.raleway_light_15)
    draw.text((325, 70), "Aft", inky_display.BLACK, font=fonts.raleway_light_15)
    draw.text((364, 70), "Eve", inky_display.BLACK, font=fonts.raleway_light_15)

    # Display icons
    trueImage = Image.open(os.path.join(imgdir, "check.png"))
    falseImage = Image.open(os.path.join(imgdir, "remove.png"))

    index = 1
    max_x_options = {"night": 240, "morning": 280, "afternoon": 320, "evening": 360}
    for date, value in carbon_intensity.forecast("bool").items():
        if index > 4:
            break
        day = datetime.datetime.strptime(date, "%Y-%m-%d")
        if index == 1:
            dayname = "Today"
        elif index == 2:
            dayname = "Tomorrow"
        else:
            dayname = day.strftime("%A")

        yValue = (index * 50) + 45
        draw.text(
            (5, yValue - 5), dayname, inky_display.BLACK, font=fonts.raleway_reg_30
        )
        if "night" in value:
            img.paste(trueImage if value["night"] else falseImage, (240, yValue))
        if "morning" in value:
            img.paste(trueImage if value["morning"] else falseImage, (280, yValue))
        if "afternoon" in value:
            img.paste(trueImage if value["afternoon"] else falseImage, (320, yValue))
        if "evening" in value:
            img.paste(trueImage if value["evening"] else falseImage, (360, yValue))

        max_slot, max_value = ci_daily_max[date]
        max_value = max_x_options.get(max_slot, "Invalid max")
        draw.rectangle(
            [(max_value + 4, yValue + 33), (max_value + 28, yValue + 35)],
            inky_display.BLACK,
        )
        index += 1

    dateNow = datetime.datetime.now()
    draw.text(
        (300, 285),
        "Updated :" + dateNow.strftime("%H:%M"),
        inky_display.BLACK,
        font=fonts.raleway_light_13,
    )

    inky_display.set_image(img)
    inky_display.show()


if __name__ == "__main__":
    main()
