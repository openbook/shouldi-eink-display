import os
from PIL import ImageFont

fontdir = os.path.join(
    os.path.dirname(os.path.dirname(os.path.relpath(__file__))), "fonts"
)

raleway_bold = "Raleway/Raleway-Bold.ttf"
raleway_reg = "Raleway/Raleway-Regular.ttf"
raleway_light = "Raleway/Raleway-Light.ttf"

raleway_bold_30 = ImageFont.truetype(os.path.join(fontdir, raleway_bold), 30)
raleway_bold_40 = ImageFont.truetype(os.path.join(fontdir, raleway_bold), 40)

raleway_reg_25 = ImageFont.truetype(os.path.join(fontdir, raleway_reg), 25)
raleway_reg_20 = ImageFont.truetype(os.path.join(fontdir, raleway_reg), 20)
raleway_reg_30 = ImageFont.truetype(os.path.join(fontdir, raleway_reg), 30)
raleway_reg_40 = ImageFont.truetype(os.path.join(fontdir, raleway_reg), 40)
raleway_reg_50 = ImageFont.truetype(os.path.join(fontdir, raleway_reg), 50)

raleway_light_13 = ImageFont.truetype(os.path.join(fontdir, raleway_light), 13)
raleway_light_15 = ImageFont.truetype(os.path.join(fontdir, raleway_light), 15)
raleway_light_25 = ImageFont.truetype(os.path.join(fontdir, raleway_light), 25)
