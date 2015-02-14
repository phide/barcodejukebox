# barcodejukebox

This script is used in a raspberry pi project intendet to create a simple way to play radioplays for kids.
Please note that this script is neither complete nor will it work for everybody. It will only work for speciffic setups wich i intent to explain later.

## requirements

You will need the following things for this to work:

### hardware
* raspberry pi (B+)
* usb hardware barcodescanner (please only use LED-Scanners if you intent to build this for children)
* some kind of loud speakers or headphones

### software
* it imports the python bindings library for vlc wich can be downloaded here:
http://git.videolan.org/?p=vlc/bindings/python.git;a=tree;f=generated;b=HEAD

## basic functionality and design principles

In the attempt to keep it simple and to avoid the need for a database the jukebox script depends on folder and file name conventions.

* Every radioplay is stored in its own folder within a library folder
* The Names of the folders should only use letters, numbers and underscores.
* The filenames should lead with a two number digit to be addressable as numbered chapters

## barcodes

The barcodes I used are Code-128 barcodes with three differend kind of informations wich can be used:

* play all files in one folder: in this case the barcode should simply contain the name of the folder in wich the music is stored
* play from selected file: in this case the barcode should contain the folder name and the file number wich schould be played speparated by a "-". e.g. "folder_10-03" would play file "03" ff in folder "folder_10"
* vlc commands. The barcode should lead with a "CMD" followd by a "-" and the command. i.e. "CMD-NEXT" would skip to the next title

## run script as service on startup

You might want to launch the script at startup. One way to achieve this can be found in this blog post:
http://blog.scphillips.com/2013/07/getting-a-python-script-to-run-in-the-background-as-a-service-on-boot/

Disclaimer: This script comes with no warranty whatsoever and every thing you do with it is at your own risk.