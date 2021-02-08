# GB Renewable Forecast Display
Using data from the National Grid's carbon intensity API & Octopus Agile Tariff API endpoints, this display aims to help you
better plan when to use 

## Why
Knowing 

## Components
1. Raspberry Pi Zero
2. Flash Memory card
3. Inky eInk Display
4. Case or

## Install and setup

### Raspberry Pi Setup

### 1. Flash pi with Raspberry Pi OS lite (no desktop)
* Using something Raspberry Pi Imager is simplest.
* Select SD card
* Choose "Raspberry Pi OS (other)" > "Raspberry Pi OS"

### 2. Configure Wifi && Enable SSH (create file /Volumes/boot/ssh)
* copy conf/wpa_supplicant.conf to /Volumes/boot/
* Create an empty file called 'ssh' in the boot directory
  
### 3. Power up the pi and SSH onto the device
```
ssh pi@raspberrypi.local
password=raspberry
```

### 4. Run install script
* ` curl https://raw.githubusercontent.com/openbook/shouldi-eink-display/main/install.sh | bash`
* When prompted enter Y to install the required inky libraries
* When prompted 'Do you wish to perform a full install?' enter N 

### 

### Optionally install web interface
You can 


## Frame

### Licenses
