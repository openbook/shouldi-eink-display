#!/bin/bash
sudo apt install nginx
cd /home/pi/shouldi-eink-display

pip3 install uwsgi flask

# Backup default sites-enabled & Copy nginx config file
sudo mv /etc/nginx/sites-enabled/default /etc/nginx/sites-available/default.bak
sudo cp ./conf/nginx.conf /etc/nginx/sites-enabled/default
sudo nginx -t

# Setup service
sudo cp ./conf/shouldi-web.service /etc/systemd/system/shouldi-web.service
sudo systemctl start shouldi-web
sudo systemctl enable shouldi-web

sudo systemctl restart nginx

ip=$(hostname -I)
echo "Install complete, web interface ready at http://${ip}"
