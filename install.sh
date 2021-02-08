#!/bin/bash
# curl https://raw.githubusercontent.com/openbook/shouldi-eink-display/main/install.sh | bash
sudo apt install git python3-pandas python3-pip python3-matplotlib msttcorefonts -yqq
rm ~/.cache/matplotlib -rf

## Install Inky dependencies
curl https://get.pimoroni.com/inky | bash

## Fetch the display repo code
git clone https://github.com/openbook/shouldi-eink-display.git
cd should-eink-display

### pi specific pandas
pip3 install pytz
# Add cron schedule
line="*/30 * * * * $(pwd)/display.py"
echo $line
(crontab -u pi -l; echo "$line" ) | crontab -u pi -
