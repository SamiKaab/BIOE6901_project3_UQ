# BIOE6901_project3_UQ
photogrammetry project

## Requirements
* Raspberry Pi 4B (and required power supply)
* Ethernet cable (at least 2)
* Usb to ethernet adaptor (at least 2)

## Setup

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
