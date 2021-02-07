#!/bin/bash
sudo apt install nginx

cd /home/pi/should-eink-display

### pi specific pandas
pip3 install uwsgi flask

# Copy nginx config file

# Setup service

#https://www.digitalocean.com/community/tutorials/how-to-serve-flask-applications-with-uswgi-and-nginx-on-ubuntu-18-04
