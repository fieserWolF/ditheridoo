# Ditheridoo

**Dither me like one of your French girls.**

Ditheridoo is a multicolor bitmap editor for Commodore 64.
It runs on Linux, MacOS, Windows and other systems supported by Python. 

![screenshot](./screenshot.png)


# Why Ditheridoo?

reason | description
---|---
open source | easy to modify and to improve, any useful contribution is highly welcome
portable | available on Linux, MacOS, Windows and any other system supported by Python3
easy dithering | checkerboard, x-line, y-line, light dither modes available, more might be implemented in the future
interesting for coders | total control which values are set in draw-modes "select color" and "dye", see built-in help or [cheatsheet.md](cheatsheet.md) for details


# Usage

For a list of quick keyboard shortcuts and other information see file [cheatsheet.md](cheatsheet.md) or the full documentation in /doc.



# Commandline options

	Ditheridoo v1.1.0 [build 251229-234134] *** by WolF
	usage: ditheridoo.py [-h] [-i IMAGE_FILENAME]

	Ditheridoo is a multicolor bitmap editor for Commodore 64.

	options:
	  -h, --help            show this help message and exit
	  -i, --image IMAGE_FILENAME
							koala image filename

	Example: ./ditheridoo.py -i image.koa



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

Ditheridoo comes in two flavors:

- standalone executable for Linux, MacOS/Darwin and Windows (see [releases](https://github.com/fieserWolF/ditheridoo/releases))
- Python3 script

## Run the standalone executable

Just download your bundle at [releases](https://github.com/fieserWolF/ditheridoo/releases) and enjoy.


### Note for Windows users

If some antivirus scanner puts Ditheridoo into quarantine because it suspects a trojan or virus, simply put it out there again.
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

Python3 is needed to run PetPet. Everything else needed should be provided in your Python3 installation by default:

- tkinter
- argparse
- "The Python Imaging Library" (PIL)


### Install Python on Windows or Mac

* Download Python from [https://www.python.org](https://www.python.org).
* Install Python on your computer.

### Install Python on Linux

On my Debian GNU/Linux machine I use apt to install everything needed:
```
apt update
apt install python3 python3-tk python3-pil python3-pil.imagetk
```

Alternatively, you can use pip to install missing modules:
```
pip3 install tk pillow argparse
```

### Download Ditheridoo

* Go to [https://github.com/fieserWolF/ditheridoo](https://github.com/fieserWolF/ditheridoo).
* Click on the green "Code" button and "Download ZIP".
* Extract the downloaded ZIP-file to any folder.


# Changelog

## Future plans

- implement sanity check: accept only standard koala format files
- implement real undo for all functions
- implement hires drawing mode
- implement different pencil sizes
- implement: freely adjustable edit window
- maybe: preview window: indicate current view with a visible frame
- maybe: preview window: move visible frame by dragging the mouse
- maybe: "draw mode: select": avoid moving of the controls


Any help and support in any form is highly appreciated.

If you have a feature request, a bug report or if you want to offer help, please, contact me:

[http://csdb.dk/scener/?id=3623](http://csdb.dk/scener/?id=3623)
or
[wolf@abyss-connection.de](wolf@abyss-connection.de)


## Changes in 1.1 (at Dream210 Party 2025)

- mostly rewritten code, split up into segments
- commandline options
- bug fixes


## Changes in 1.0

- initial release


# License

_Ditheridoo multicolor bitmap editor for Commodore 64._

_Copyright (C) 2025 fieserWolF / Abyss-Connection_

This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;
without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with this program.
If not, see [http://www.gnu.org/licenses/](http://www.gnu.org/licenses/).

See the [LICENSE](LICENSE) file for details.

For further questions, please contact me at
[http://csdb.dk/scener/?id=3623](http://csdb.dk/scener/?id=3623)
or
[wolf@abyss-connection.de](wolf@abyss-connection.de)

For Python3, The Python Imaging Library (PIL), Tcl/Tk and other used source licenses see file [LICENSE_OTHERS](LICENSE_OTHERS).


