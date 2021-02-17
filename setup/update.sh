cd /home/pi/shouldi-eink-display
git checkout ./ && git pull
echo "Restarting web server"
sudo service shouldi-web restart
