# MegaPixel

MegaPixel is a multicolor bitmap editor for Commodore 64.



# Getting Started

MegaPixel comes in two flavours:

- standalone executable for 64-bit systems Linux, MacOS/Darwin and Windows
- Python3 script

## Standalone executable

Just download your bundle and enjoy. Keep in mind that only 64bit systems are supported as I could not find a 32bit system to generate the bundle.

Note on Windows users: If some antivirus scanner puts MegaPixel into quanartine because it suspects a trojan or virus, simply put it out there again.
It isn`t harmful, I used PyInstaller to bundle the standalone executable for you.
Unfortunately, the PyInstaller bootloader triggers a false alarm on some systems.
I even tried my best and re-compiled the PyInstaller bootloader so that this should not happen anymore. Keep your fingers crossed ;)



## Python3 script prerequisites

At least this is needed to run the script directly:

- python 3
- python tkinter module
- python "The Python Imaging Library" (PIL)

On my Debian GNU/Linux machine I use apt-get to install everything needed:
```
apt-get update
apt-get install python3 python3-tk python3-pil
```

# Usage

For a list of quick keyboard shortcuts and other information see file [cheatsheet](cheatsheet.md).




# Authors

* fieserWolF/Abyss-Connection - *Initial work* - [fieserWolF on github](https://github.com/fieserWolF) [fieserWolF on CSDB](https://csdb.dk/scener/?id=3623)
* Pararaum/The 7th Division - *example image* - [Pararaum on CSDB](https://csdb.dk/scener/?id=31223)
* Mirage/Booze Design - *example image* - [Mirage on CSDB](https://csdb.dk/scener/?id=739)



# License

MegaPixel Commodore 64 graphics converter

Copyright (C) 2020 fieserWolF / Abyss-Connection

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.

See the [LICENSE](LICENSE) file for details.

For futher questions, please contact me at
http://csdb.dk/scener/?id=3623
or
wolf@abyss-connection.de

For Python3, The Python Imaging Library (PIL), Tcl/Tk and other used source licenses see file [LICENSE_OTHERS](LICENSE_OTHERS).
