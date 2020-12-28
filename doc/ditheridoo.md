# Ditheridoo

**Pixel By Pixel**

Ditheridoo is a multicolor bitmap editor for Commodore 64.
It runs on 64 bit versions of Linux, MacOS and Windows.



# Usage

For a list of quick keyboard shortcuts and other information see file [cheatsheet](cheatsheet.md).



# File Format

The multicolor bitmap is stored in the widely-spread KoalaPainter (C64) format:

* 2 bytes load address
* 8000 bytes raw bitmap data
* 1000 bytes raw "Video Matrix" (screen) data
* 1000 bytes raw "Color RAM" data
* 1 byte background data



# Authors

* fieserWolF/Abyss-Connection - *code, graphics* - [https://github.com/fieserWolF](https://github.com/fieserWolF) [https://csdb.dk/scener/?id=3623](https://csdb.dk/scener/?id=3623)
* The Mysterious Art/Abyss-Connection - *graphics* - [https://csdb.dk/scener/?id=3501](https://csdb.dk/scener/?id=3501)
* Pararaum/The 7th Division - *example image* - [https://csdb.dk/scener/?id=31223](https://csdb.dk/scener/?id=31223)
* Mirage/Booze Design - *example image* - [https://csdb.dk/scener/?id=739](https://csdb.dk/scener/?id=739)


# Getting Started

Ditheridoo comes in two flavours:

- standalone executable for 64-bit systems Linux, MacOS/Darwin and Windows
- Python3 script

## Run the standalone executable

Just download your bundle and enjoy. Keep in mind that only 64bit systems are supported as I could not find a 32bit system to generate the bundle.

### Note for Windows users

If some antivirus scanner puts Ditheridoo into quanartine because it suspects a trojan or virus, simply put it out there again.
It isn`t harmful, I used PyInstaller to bundle the standalone executable for you.
Unfortunately, the PyInstaller bootloader triggers a false alarm on some systems.
I even tried my best and re-compiled the PyInstaller bootloader so that this should not happen anymore. Keep your fingers crossed ;)

### Note for MacOS users

Your system might complain that the code is not signed by a certificated developer. Well, I am not, so I signed the program on my own. 
```
"Ditheridoo" can`t be opened because it is from an unidentified developer.
```
You need to right-click or Control-click the app and select “Open”.



## Run the Python3 script directly

Download _ditheridoo.py_ and the whole _resource_ - directory into the same folder on your computer.

### Prerequisites

At least this is needed to run the script directly:

- python 3
- python tkinter module
- python "The Python Imaging Library" (PIL)

On my Debian GNU/Linux machine I use apt-get to install everything needed:
```
apt-get update
apt-get install python3 python3-tk python3-pil
```


# Changelog

## Future plans

- implement sanity check: accept only standard koala format files
- implement real undo for all functions
- implement hires drawing mode
- implement different pencil sizes

Any help and support in any form is highly appreciated.

If you have a feature request, a bug report or if you want to offer help, please contact me:

[http://csdb.dk/scener/?id=3623](http://csdb.dk/scener/?id=3623)
or
[wolf@abyss-connection.de](wolf@abyss-connection.de)


## Changes in 1.0

- initial release


# License

_Ditheridoo multicolor bitmap editor for Commodore 64._

_Copyright (C) 2020 fieserWolF / Abyss-Connection_

This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;
without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with this program.  If not, see [http://www.gnu.org/licenses/](http://www.gnu.org/licenses/).

See the [gnu-gpl-v3.0.md](gnu-gpl-v3.0.md) file for details.

For futher questions, please contact me at
[http://csdb.dk/scener/?id=3623](http://csdb.dk/scener/?id=3623)
or
[wolf@abyss-connection.de](wolf@abyss-connection.de)

For Python3, The Python Imaging Library (PIL), Tcl/Tk and other used source licenses see file [license_others.md](license_others.md).


