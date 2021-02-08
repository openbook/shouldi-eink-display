#!/bin/bash
cd /home/pi
sudo apt install git python3-pandas python3-pip python3-matplotlib msttcorefonts -yqq
rm ~/.cache/matplotlib -rf

## Install Inky dependencies
curl https://get.pimoroni.com/inky | bash

## Fetch the display repo code
git clone https://github.com/openbook/shouldi-eink-display.git
cd /home/pi/shouldi-eink-display

### pi specific pandas
pip3 install pytz
# Add cron schedule
sudo touch /var/spool/cron/pi
sudo /usr/bin/crontab /var/spool/cron/pi
line="5,35 * * * * cd $(pwd) && python3 display.py"
(crontab -u pi -l; echo "$line" ) | crontab -u pi -

# Save a tiny bit more power by turning off the LED
# https://www.jeffgeerling.com/blogs/jeff-geerling/controlling-pwr-act-leds-raspberry-pi
echo none | sudo tee /sys/class/leds/led0/trigger

sudo reboot
