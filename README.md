# GB Renewable Forecast Display

## Why
Knowing 

## Hardware components 
1. Raspberry Pi Zero
2. Flash Memory card
3. Inky eInk Display
4. Case or 

## Raspberry Pi Setup

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
curl https://raw.githubusercontent.com/openbook/shouldi-eink-display/main/install.sh | bash

Enter y when prompted whether you want to install inky
Enter n when prompted for full install
