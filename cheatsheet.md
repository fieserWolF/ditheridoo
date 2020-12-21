# MegaPixel Cheatsheet

## GUI controls

|key|function|
--------------
|Alt+q | quit MegaPixel |
| Alt+o | open file |
| Alt+s | save file |
| Alt+c | configure |
| Alt+p | show preview window |
| Alt+h | this help |
---------------------

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
- Space = no overwriting

## notes: draw-modes

Can be set in settings window.
Behaviour if too many colors are used (color-clash):

- keep color    = keep color if too many colors are used
- replace color = replace color if too many colors are used
- select color  = overwrite selected data: screen-color1, screen-color2, colorram or background
- dye  = do not touch bitmap, only overwrite color
