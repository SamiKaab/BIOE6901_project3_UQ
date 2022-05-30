# BIOE6901_project3_UQ
Photogrammetry project

## Required Equipment
* Raspberry Pi 4B (at least 2 and their required power supply)
* Ethernet cable (at least 2)
* Usb to ethernet adaptor (at least 2)
### Optional
* External monitor and display cable (at least one)
* Mouse and keyboard (at least one)
* Ximea camera (Used in this example, max 6)

## Setup
If the Raspberry Pi is connected to an external monitor, connect it the internet via wifi and run 
```sh
sudo apt update
sudo apt-get upgrade
sudo apt install build-essential
```
If your accessing the Raspberry Pi via ssh, you will have to add the following to `/etc/wpa_supplicant/wpa_supplicant.conf`: 
```sh
sudo nano /etc/wpa_supplicant/wpa_supplicant.conf
```
```sh
network={
   ssid="wifi_name"
   psk="password"
}
```
You may have to reboot the Raspberry Pi
Once you are connected to the internet run the previously specified command before continuing.

Python should come pre-installed, you can check using the `which python` or `which python3`, which sould return the location of the program (probably `/usr/bin/`). If it is not installed, install it with : `sudo apt-get install python3.8`

### Python dependencies and Ximea camera setup

Install the following dependencies
  ```sh
  pip3 install opencv-python
  pip install -U numpy
  ```
You may also have to  install the following if you get a cv2 related error:
  ```sh
  sudo apt-get install libcblas-dev
  sudo apt-get install libhdf5-dev
  sudo apt-get install libhdf5-serial-dev
  sudo apt-get install libatlas-base-dev
  sudo apt-get install libjasper-dev 
  sudo apt-get install libqtgui4 
  sudo apt-get install libqt4-test
  ```
**Note some of the above dependencies may fail to install, simply continue with the rest of the set up**

Run the following commands **only if you are using the ximea cameras**:
  ```sh
  wget https://www.ximea.com/downloads/recent/XIMEA_Linux_SP.tgz
  tar xzf XIMEA_Linux_SP.tgz
  cd package
  ./install
  ```
 You may want to install vs code as well:
 ```sh
 sudo apt-get install code
 ```
 
### Communication between raspberry pis
We are trying to send images from two Raspberry Pis (RPi1 and RPi2) to one central Raspberry Pi (RPi0) 

RPi1 --> RPi0 <-- RPi2

In order for the Raspberry Pis to communicate through ethernet we will need to set a static IP address for each Raspberry Pi. To do so, add the following lines to `\etc\dhcpcd.conf` in each Raspberry:
```sh
interface eth0
static ip_address=192.168.0.03/24
static routers=192.168.0.1
static domain_name_servers=192.168.0.1 8.8.8.8

interface eth1
static ip_address=192.168.0.04/24

interface eth2
static ip_address=192.168.0.05/24
```
**Don't forget to change the ip address (xx) in `static ip_address=192.168.0.xx/24` to a different value in each raspberry Pi to avoid IP address conflicts.**

The above line will set up a static ip for eth0 (ethernet port) and, eth1 and eth2 through the two usb ports. This will enable us to communicate between 2 device. However if we want to connect to multiple Raspberry Pis (RPi1 and RPi2) from a single Raspbery Pi (RPi0) simultaneously (through 2 seperate interface) we will also need to set up a bridge:

```sh
sudo brctl addbr br0
sudo brctl addif br0 eth0 eth1 eth2
```
**Note: you must first switch on and connect the other raspberry pis before adding the interfaces to the bridge**

Running the command `sudo brctl show` show give an output similar to the following:
```sh
bridge name	bridge id		STP enabled	interfaces
br0		8000.dca632ea7185	no		eth0
                                                        eth1
                                                        eth2
```
you must also add the following lines to `/etc/network/interfaces` (if not already there):
```sh
iface eth2 inet manual
iface eth1 inet manual
iface eth0 inet manual

# Bridge setup
iface br0 inet static
    bridge_ports eth0 eth1 eth2
    address 192.168.0.2
    netmask 255.255.255.0
    gateway 192.168.0.1

auto br0
iface br0 inet manual
bridge_ports eth2 eth1 eth0
```
Finally run `sudo systemctl restart dhcpcd.service` in order for the changes to take effect.
**Note that  we have to run `sudo brctl addif br0 eth0 eth1 eth2` every time we reboot the Raspberry Pis

We should now be able to simultaneously ping RPi1 and RPi2 from RPi0

## Running the program
The [cam.py](cam.py) should be added to and ran on all Raspberry Pis. The [simpleServer.py](simpleServer.py) should only be added to the main controlling Raspberry Pi (RPi0) while the [simpleclient.py](simpleclient.py) should be put in the secondary Raspberry Pis (RP1 and RP2).
