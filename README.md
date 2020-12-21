# MegaPixel

MegaPixel is a multicolor bitmap editor for Commodore 64.

# credits

* **fieserWolF/Abyss-Connection** - *Initial work* - [fieserWolF on github](https://github.com/fieserWolF) [fieserWolF on CSDB](https://csdb.dk/scener/?id=3623)
* **Pararaum/The 7th Division** - *example image* - [Pararaum on CSDB](https://csdb.dk/scener/?id=31223)
* **Mirage/Booze Design** - *example image* - [Mirage on CSDB](https://csdb.dk/scener/?id=739)


# cheatsheet

## GUI controls

- Alt+q = quit MegaPixel
- Alt+o = open file
- Alt+s = save file
- Alt+c = configure
- Alt+p = show preview window
- Alt+h = this help

## mouse control

- right mouse button = set color
- left mouse button = set other color
- middle mouse button = scroll image
- mouse wheel = zoom in and out

## editing

- Ctrl+z = undo (single pixel editing only, not for block-commands like cut or paste)
- Ctrl+x = cut
- Ctrl+c = copy
- Ctrl+p = paste
- m = set marker
- Alt+n = normal pencil
- Alt+b = checkerboard dither pencil
- Alt+x = x-line dither pencil
- Alt+y = y-line dither pencil
- Alt+l = light dither pencil

## editor visuals

- plus/ minus = zoom in and out
- cursor keys = scroll image

## left mouse-button color

- 0-9...a-f = select color
- F1 = screen-color-1 of block
- F2 = screen-color-2 of block
- F3 = colorram of block
- F4 = background

## right mouse-button color

- Shift+ 0-9...a-f = select color
- Shift+F1 = screen-color-1 of block
- Shift+F2 = screen-color-2 of block
- Shift+F3 = colorram of block
- Shift+F4 = background

## color to replace (only when in draw mode 'select'):

- F5 = screen-color-1 of block
- F6 = screen-color-2 of block
- F7 = colorram of block
- F8 = background
Space = no overwriting

## notes: draw-modes

Can be set in settings window.
Behaviour if too many colors are used (color-clash):

- keep color    = keep color if too many colors are used
- replace color = replace color if too many colors are used
- select color  = overwrite selected data: screen-color1, screen-color2, colorram or background
- dye  = do not touch bitmap, only overwrite color







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
