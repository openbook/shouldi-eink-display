#!/bin/bash
cd /home/pi
# Install dependencies for building the display screens
# Add mstcore fonts to avoid using defaults
sudo apt install git python3-pandas python3-pip python3-matplotlib msttcorefonts -yqq

# Remove the matplib cache so that the font files are rebuilt
# see https://stackoverflow.com/questions/42097053/matplotlib-cannot-find-basic-fonts
rm ~/.cache/matplotlib -rf

## Install Inky dependencies
curl https://get.pimoroni.com/inky | bash

## Fetch the display repo code
git clone -b develop https://github.com/openbook/shouldi-eink-display.git
cd /home/pi/shouldi-eink-display

### Install pytimezones
pip3 install pytz

# Add cron schedule for 5 & 35 mins past the hour
# Add a reboot cron command so that the display initially updates on first reboot
sudo touch /var/spool/cron/pi
sudo /usr/bin/crontab /var/spool/cron/pi
line="5,35 * * * * cd $(pwd) && python3 display.py
@reboot cd $(pwd) && python3 display.py"
(crontab -u pi -l; echo "$line" ) | crontab -u pi -

# Save a tiny bit more power by turning off the LED
# https://www.jeffgeerling.com/blogs/jeff-geerling/controlling-pwr-act-leds-raspberry-pi
echo 'dtparam=act_led_trigger=none' | sudo tee -a /boot/config.txt
echo 'dtparam=act_led_activelow=on' | sudo tee -a /boot/config.txt

# Copy the config.ini.example to config.ini so that we can perform git updates
# on the codebase in the future without conflicts
cp /home/pi/shouldi-eink-display/config.ini.example /home/pi/shouldi-eink-display/config.ini

# Perform a reboot so that inky and required libs are loaded correctly
sudo reboot
