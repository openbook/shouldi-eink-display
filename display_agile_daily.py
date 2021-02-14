#!/usr/bin/python3
import sys
import os
import datetime
import requests

if os.path.exists("lib"):
    sys.path.append("lib")
from agile import OctopusAgileTariff

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import io
from PIL import ImageOps, Image, ImageFont, ImageDraw
from inky.auto import auto
from configparser import ConfigParser


import fonts

imgdir = os.path.join(
    os.path.dirname(os.path.dirname(os.path.relpath(__file__))), "assets"
)


def main():
    inky_display = auto()
    config = ConfigParser()
    config.read("config.ini")
    region = config.get("agile", "region")
    agile_data = OctopusAgileTariff(region=region)
    df = agile_data.get_df()

    plt.style.use("ggplot")
    COLOR = "black"
    plt.rcParams["text.color"] = COLOR
    plt.rcParams["xtick.color"] = COLOR
    plt.rcParams["ytick.color"] = COLOR
    plt.rcParams["axes.grid"] = False
    plt.rcParams["font.family"] = "sans-serif"
    plt.rcParams["font.weight"] = "bold"
    plt.rcParams["font.sans-serif"] = ["Arial"]
    plt.rcParams["axes.spines.left"] = False
    plt.rcParams["axes.spines.right"] = False
    plt.rcParams["axes.spines.top"] = False
    plt.rcParams["axes.spines.bottom"] = False
    plt.rcParams.update({"font.size": 13})
    plt.figure(frameon=False)
    plt.tight_layout()
    figure = plt.gcf()  # get current figure
    ax = plt.gca()
    ax.margins(x=0, y=0)
    df.plot(
        kind="bar",
        x="valid_from",
        y="value_inc_vat",
        ax=ax,
        color="black",
        legend=False,
        figsize=(4.75, 2.6),
    )
    xticks = ["0:00", "06:00", "12:00", "18:00"]
    ax.set_xticklabels(xticks, rotation=0)
    ax.locator_params(nbins=4, axis="x")
    plt.savefig("energy.png", transparent=True, dpi=100)

    img = Image.new("P", inky_display.resolution)
    draw = ImageDraw.Draw(img)
    plot = Image.open("energy.png")
    img.paste(plot, (-28, 45))
    draw.rectangle([(0, 0), (400, 55)], inky_display.BLACK)
    draw.text(
        (10, 10), "Octopus Agile tariff", inky_display.WHITE, font=fonts.raleway_reg_30
    )
    draw.text((338, 28), "p/kWh ", inky_display.WHITE, font=fonts.raleway_reg_15)
    draw.text(
        (330, 5),
        datetime.datetime.now().strftime("%d/%m"),
        inky_display.WHITE,
        font=fonts.raleway_bold_20,
    )
    inky_display.set_image(img)
    inky_display.show()


if __name__ == "__main__":
    main()
