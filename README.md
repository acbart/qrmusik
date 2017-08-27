# qrmusik

**This project has been superseded by the more-advanced and better-working project 'nfcmusik'** (https://github.com/ehansis/nfcmusik).


*Goal:* build a simple mp3 player that is usable for toddlers, based on a raspberry pi.

Music is started via putting a piece of cardboard with a QR code printed in front
of the raspi camera, and stopped by removing it. That's all the user interface there is.


## Requirements

### Base OS

Built and tested with Raspian Jessie (2016-05-27).

### System packages

Install these via `apt-get install <package>`, after doing an `apt-get upgrade`
* python-picamera
* qrencode
* zbar

Optional:
* vim
* ipython

### Python packages

Install these with `pip install <package>`
* qrtools


## Usage

Clone into a directory of your choice on the RasPi. Run `controller.py` to start. 
See comment in `controller.py` for how to autostart on reboot.


## QR code tokens

The script `make_code_sheet.py` can be used to generate sheets of QR codes and icons,
to be printed on a photo printer. See there for usage instructions. The following
settings worked well for me for printing 10 cm photos for making tokens out
of 5 Euro Cent coins (the additional lines are examples for code generation):
```
2784 1856 300 2 3
music play cha-cha-cha.mp3, rasseln.jpg
music play bella-bimba.mp3, bell-295520_960_720.png
music vol 30, 30.png
music vol 50, 50.png
```


