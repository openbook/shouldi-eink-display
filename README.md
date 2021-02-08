# GB Renewable Forecast Display
Using data from the National Grid's carbon intensity this Raspberry Pi powered eInk display aims
to give you a quick way to time your home energy usage to help balance the grid, reduce carbon emissions (& if you're an agile tariff user, save money)

This project takes the same approach as shouldibake.com and the Baking Forecast to give you quick visual 
aid when making that decision, showing you when to renewable generation is above or below 33%.

## Why
We include solar, wind and hydro in our definition of renewable generation.  Relying on the weather for our energy means there will naturally be peaks and troughs 
both in terms of how much energy is generated, but also because we use different amounts of energy during the day. 

By timing when we bake, hoover, use the washing machine, charge our cars or batteries to coincide with when renewable generation is highest we can:
1. help the National Grid balance demand and reduce the carbon emission 
2. (if you're using one of the increasingly prevalent [agile pricing tariffs](https://octopus.energy/agile/)) rely on cheaper prices to save money.

Every little helps!

## Components
1. Raspberry Pi Zero soldered (~£14) ([piehut](https://thepihut.com/products/raspberry-pi-zero-wh-with-pre-soldered-header) | [pimoroni](https://shop.pimoroni.com/products/raspberry-pi-zero-wh-with-pre-soldered-header))
2. Micro SD card (~£7) ([piehut](https://thepihut.com/collections/raspberry-pi-sd-cards-and-adapters/products/noobs-preinstalled-sd-card) | [pimoroni](https://shop.pimoroni.com/products/noobs-32gb-microsd-card-3-1?variant=31703694245971))
3. Inky wHAT (ePaper/eInk/EPD) - Black/White (£45) ([piehut](https://thepihut.com/products/inky-what-epaper-eink-epd-black-white) | [pimoroni](https://shop.pimoroni.com/products/inky-what?variant=21214020436051))
4. Power supply - micro USB connection ([piehut](https://thepihut.com/products/official-raspberry-pi-universal-power-supply) | [pimoroni](https://shop.pimoroni.com/products/raspberry-pi-universal-power-supply)) 
5. Case (see notes below)

## Install and setup

### Raspberry Pi Setup

### 1. Flash pi with Raspberry Pi OS lite (no desktop)
* Use [Raspberry Pi Imager](https://www.raspberrypi.org/software/) to copy the Raspberry Pi OS image to the SD card 
* Select SD card
* Choose "Raspberry Pi OS (other)" > "Raspberry Pi OS Lite (32-bit)" (we wont require a GUI desktop)
* Select write

### 2. Configure Wifi & Enable SSH (create file /Volumes/boot/ssh)
* Once the Rapsberry Pi OS image has been saved to the SD card, open a file client so that you can view the contents of the 'boot' folder
* Create a new file `wpa_supplicant.conf` in the boot folder & add the following, adding your SSID and password for your wifi network
```
  ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
  network={
    ssid="YOUR_SSID"
    psk="YOUR_WIFI_PASSWORD"
    key_mgmt=WPA-PSK
  }
```
Example file: [conf/wpa_supplicant.conf](https://github.com/openbook/shouldi-eink-display/blob/main/conf/wpa_supplicant.conf)
* Create an empty file called 'ssh' in the boot directory, this will enable SSD by default when you first power up the pi
  
### 3. Power up the pi and SSH onto the device
* Plug the pi in 
```
ssh pi@raspberrypi.local
password=raspberry
```

### 4. Run install script
* ` curl https://raw.githubusercontent.com/openbook/shouldi-eink-display/main/install.sh | bash`
* When prompted enter Y to install the required inky libraries
* When prompted 'Do you wish to perform a full install?' enter N 

### 5. Set the display configuration

### 6. (Optionally) install web interface so you can change the display from a browser
You can 


## Frame

### Licenses
