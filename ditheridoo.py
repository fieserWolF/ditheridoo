#!/usr/bin/env python3


"""
Ditheridoo - multicolor bitmap editor for Commodore 64
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

For futher questions, please contact me at
http://csdb.dk/scener/?id=3623
or
wolf@abyss-connection.de

For Python3, The Python Imaging Library (PIL), Numpy, Tcl/Tk and other used source licenses see file "LICENSE_OTHERS".
"""


import os
import sys
import struct
from PIL import ImageTk
import PIL.Image as PilImage    #we need another name, as it collides with tk.Image otherwise
import PIL.ImageDraw as ImageDraw
import tkinter as tk
from tkinter.filedialog import askopenfilename, asksaveasfilename
#import json
import platform

#global constants
def _global_constants():
        return None
PROGNAME = 'Ditheridoo';

#BGCOLOR="#ff0000"
BGCOLOR="#d9d9d9"
ACTIVECOLOR="#e8e8e8"   #mouse hovering over button
SELECTCOLOR="#ffffff"   #button pressed
TEXTBOXCOLOR="#ffffff"

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)
    
RES_VERSION = resource_path('resources/version.txt')
RES_GFX_ICON = resource_path('resources/icon.png')
RES_GFX_AC = resource_path('resources/ac.png')
RES_GFX_LOGO = resource_path('resources/logo.png')
RES_GFX_ABOUT = resource_path('resources/about.png')
RES_DOC_ABOUT = resource_path('resources/about.txt')
RES_DOC_HELP = resource_path('resources/help.txt')

VERSION = open(RES_VERSION).read().rstrip()


C64_CHAR_HEIGHT=25  #200/8
C64_CHAR_WIDTH=40   #320/8

BITMAP_PIXEL_X  = 4
BITMAP_PIXEL_Y  = 8

PALETTEDATA_COLODORE = (
    0,   0,   0,	#0
    255, 255, 255,	#1
    129,  51, 56,	#2
    117, 206, 200,	#3
    142,  60, 151,	#4
    86, 172,  77,	#5
    46,  44, 155,	#6
    237, 241, 113,	#7
    142,  80,  41,	#8
    85,  56,   0,	#9
    196, 108, 113,	#10
    74,  74,  74,	#11
    123, 123, 123,	#12
    169, 255, 159,	#13
    112, 109, 235,	#14
    178, 178, 178	#15
)

PALETTEDATA_PEPTO = (
    0, 0, 0,		# 0 black
    255, 255, 255,	# 1 white
    104, 55, 43,	# 2 red
    112, 164, 178,	# 3 cyan
    111,  61, 134,	# 4 purple
     88, 141,  67,	# 5 green
     53,  40, 121,	# 6 blue
    184, 199, 111,	# 7 yellow
    111,  79,  37,	# 8 orange
     67,  57,   0,	# 9 brown
    154, 103,  89,	# a pink
     68,  68,  68,	# b dark gray
    108, 108, 108,	# c gray
    154, 210, 132,	# d light green
    108,  94, 181,	# e light blue
    149, 149, 149	# f light gray
)

_bd = 2
_padx = 2
_pady = 2

KOALA_WIDTH = 160
KOALA_HEIGHT = 200


EDITORSIZE_TEXT    = (
    "640x400",  #0 640x400
    "1280x800"  #1 1280x800
)

EDITORSIZE_MULTIPLY    = (
    2,  #0 640x400
    4   #1 1280x800
)

EDITORSIZE_DIV_X  = (
    2,  #0 640x400
    1   #1 1280x800
)
EDITORSIZE_DIV_Y  = (
    4,  #0 640x400
    2   #1 1280x800
)

PREVIEWSIZE_DIV_X  = (
    4,  #0 320x200
    2,  #1 640x400
)
PREVIEWSIZE_DIV_Y  = (
    8,  #0 320x200
    4,  #1 640x400
)


ZOOM_MULTIPLY    = (
    1,  #0
    2,  #1
    4,  #2
    8,   #3
    16   #4
)

ZOOM_WIDTH = (
    320,    #0
    160,    #1
    80,     #2
    40,     #3
    20      #4
)
ZOOM_HEIGHT = (
    400,    #0
    200,    #1
    100,    #2
    50,     #3
    25      #4
)


GRID_SIZE = (
    4,  #0
    8, #1
    16, #2
    32, #3
    64 #4
)

PREVIEWSIZE_MULTIPLY    = (
    1,  #0 320x200
    2  #1 640x400
)

PREVIEWSIZE_TEXT    = (
    "320x200",  #0 320x200
    "640x400"  #1 640x400
)


#https://anzeljg.github.io/rin2/book2/2405/docs/tkinter/cursors.html
CURSOR_HAND = 'hand2'
CURSOR_EDIT = 'arrow'
CURSOR_NOTHING = 'circle'
CURSOR_MOVE = 'fleur'
CURSOR_MARKER_START = 'top_left_corner'
CURSOR_MARKER_END = 'bottom_right_corner'



#global variables
def _global_variables():
        return None
        
root = tk.Tk()

preview_window = None
preview_window_open = False
preferences_window = None
preferences_window_open = False
help_window = None
help_window_open = False
about_window = None
about_window_open = False

frame_replace_color = tk.Frame()


editor_mode = 'edit'

operating_system = platform.system()

koala_bitmap=[0]*8000
koala_col12=[0]*1000
koala_col3=[0]*1000
koala_bg=0

buffer_bitmap=[0]*8000
buffer_col12=[0]*1000
buffer_col3=[0]*1000
marker_posx=0
marker_posy=0
marker_width=0
marker_height=0

buffer_posx = 0
buffer_posy = 0
buffer_width = 0
buffer_height = 0

koala_colorindex_data = [0] * KOALA_WIDTH*KOALA_HEIGHT

user_palette = tk.StringVar()
user_palette.set("pepto")   #default palette

user_drawmode = tk.StringVar()
#user_drawmode.set("keep")
#user_drawmode.set("dye")
user_drawmode.set("replace")
#user_drawmode.set("select")

user_pencil = tk.StringVar()
user_pencil.set("normal")


user_editorsize = tk.IntVar()
user_editorsize.set(0)  #default editorsize
editor_width   = KOALA_WIDTH*2 *EDITORSIZE_MULTIPLY[user_editorsize.get()]
editor_height  = KOALA_HEIGHT *EDITORSIZE_MULTIPLY[user_editorsize.get()]

user_previewsize = tk.IntVar()
user_previewsize.set(0)  #default previewsize
preview_width   = KOALA_WIDTH*2 *PREVIEWSIZE_MULTIPLY[user_previewsize.get()]
preview_height  = KOALA_HEIGHT *PREVIEWSIZE_MULTIPLY[user_previewsize.get()]



current_filename = ""

user_start_address = tk.StringVar()
user_start_address.set("6000")
user_start_address_checkbutton = tk.IntVar()
user_start_address_checkbutton.set(1)

user_drawcolor_left = tk.IntVar()
user_drawcolor_left.set(0)
user_drawcolor_right = tk.IntVar()
user_drawcolor_right.set(1)

used_color_bg = tk.IntVar()
used_color_bg.set(1)
used_color_col1 = tk.IntVar()
used_color_col1.set(1)
used_color_col2 = tk.IntVar()
used_color_col2.set(1)
used_color_col3 = tk.IntVar()
used_color_col3.set(1)

user_replace_color = tk.IntVar()
user_replace_color.set(99)

current_color = tk.IntVar()
current_color.set(99)



cursorx_variable = tk.IntVar()
cursorx_variable.set(0)
cursory_variable = tk.IntVar()
cursory_variable.set(0)

blockx_variable = tk.IntVar()
blockx_variable.set(0)
blocky_variable = tk.IntVar()
blocky_variable.set(0)

editorimage_posx_variable = tk.IntVar()
editorimage_posx_variable.set(0)
editorimage_posy_variable = tk.IntVar()
editorimage_posy_variable.set(0)


mousex_variable = tk.IntVar()
mousex_variable.set(0)
mousey_variable = tk.IntVar()
mousey_variable.set(0)

undo_variable = tk.IntVar()
undo_variable.set(0)



koala_image = PilImage.new("P", (KOALA_WIDTH,KOALA_HEIGHT))
marker_image = PilImage.new("P", (KOALA_WIDTH,KOALA_HEIGHT))
editor_image = PilImage.new("P", (editor_width, editor_height))
background_image = PilImage.new("RGBA", (editor_width, editor_height))
preview_image = PilImage.new("P", (preview_width, preview_height))
grid1_image = PilImage.new("RGBA", (editor_width, editor_height))
grid2_image = PilImage.new("RGBA", (editor_width, editor_height))
grid3_image = PilImage.new("RGBA", (editor_width, editor_height))
grid4_image = PilImage.new("RGBA", (editor_width, editor_height))

label_editor_image = tk.Label()
label_preview_image = tk.Label()

mouse_posx  = 0
mouse_posy  = 0

zoom_preview    = 1
zoom    = 1
my_focus = "unset"

space_pressed   = False

editorimage_posx    = 0
editorimage_posy    = 0

my_prv_posx = 0
my_prv_posy = 0

block_x = 0
block_y = 0
block_x_absolute = 0
block_y_absolute = 0

radiobutton_replace_bg = tk.Radiobutton()
radiobutton_replace_col1 = tk.Radiobutton()
radiobutton_replace_col2 = tk.Radiobutton()
radiobutton_replace_col3 = tk.Radiobutton()

radiobutton_current_bg = tk.Radiobutton()
radiobutton_current_col1 = tk.Radiobutton()
radiobutton_current_col2 = tk.Radiobutton()
radiobutton_current_col3 = tk.Radiobutton()

undo_stack = []



def draw_background():
    global background_image

    background_image = PilImage.new("RGBA", (editor_width, editor_height), "#888888ff")
    draw = ImageDraw.Draw(background_image)

    CHECKER_SIZE = 32

    a = 0
    for y in range(0,editor_height,CHECKER_SIZE) :
        for x in range(0,editor_width,CHECKER_SIZE) :
            if ( a%2 == 0) :
                #https://pillow.readthedocs.io/en/stable/reference/ImageDraw.html#PIL.ImageDraw.ImageDraw.rectangle
                draw.rectangle( ( (x,y) , (x+CHECKER_SIZE-1,y+CHECKER_SIZE-1) ), fill="#777777ff")
            a += 1
        a += 1


    
    
    
def draw_grids():
    global draw1, draw2, draw3, draw4
    global grid1_image, grid2_image, grid3_image, grid4_image

    grid1_image = PilImage.new("RGBA", (editor_width, editor_height))
    grid2_image = PilImage.new("RGBA", (editor_width, editor_height))
    grid3_image = PilImage.new("RGBA", (editor_width, editor_height))
    grid4_image = PilImage.new("RGBA", (editor_width, editor_height))

    draw1 = ImageDraw.Draw(grid1_image, 'RGBA')
    draw2 = ImageDraw.Draw(grid2_image, 'RGBA')
    draw3 = ImageDraw.Draw(grid3_image, 'RGBA')
    draw4 = ImageDraw.Draw(grid4_image, 'RGBA')

    multi = EDITORSIZE_MULTIPLY[user_editorsize.get()]

    #y-axis
    for y in range(0,editor_height,(GRID_SIZE[1] * multi)) : draw1.line((0,y,editor_width,y), fill="#88888888")
    for y in range(0,editor_height,(GRID_SIZE[2] * multi)) : draw2.line((0,y,editor_width,y), fill="#88888888")
    for y in range(0,editor_height,(GRID_SIZE[3] * multi)) : draw3.line((0,y,editor_width,y), fill="#88888888")
    for y in range(0,editor_height,(GRID_SIZE[4] * multi)) : draw4.line((0,y,editor_width,y), fill="#88888888")

    #x-axis
    for x in range(0,editor_width,(GRID_SIZE[1] * multi)) : draw1.line((x,0,x,editor_height), fill="#88888888")
    for x in range(0,editor_width,(GRID_SIZE[2] * multi)) : draw2.line((x,0,x,editor_height), fill="#88888888")
    for x in range(0,editor_width,(GRID_SIZE[3] * multi)) : draw3.line((x,0,x,editor_height), fill="#88888888")
    for x in range(0,editor_width,(GRID_SIZE[4] * multi)) : draw4.line((x,0,x,editor_height), fill="#88888888")





    
    
def action_image_refresh_prepare():
        global koala_image

        switcher_palette = {
            'pepto': PALETTEDATA_PEPTO,
            'colodore': PALETTEDATA_COLODORE,
        }
        my_palettedata = switcher_palette.get(user_palette.get(), PALETTEDATA_PEPTO)
        koala_image.putpalette(my_palettedata)

        koala_image.putdata(koala_colorindex_data)

        action_image_refresh_show()

        return None
        

def editorimage_pos_sanity_check() :
        global editorimage_posx, editorimage_posy
        
        #sanity checks
        if (editorimage_posx < C64_CHAR_WIDTH*-1+1) : editorimage_posx = C64_CHAR_WIDTH*-1+1
        if (editorimage_posy < C64_CHAR_HEIGHT*-1+1) : editorimage_posy = C64_CHAR_HEIGHT*-1+1
        if (editorimage_posx > C64_CHAR_WIDTH-1) : editorimage_posx = C64_CHAR_WIDTH-1
        if (editorimage_posy > C64_CHAR_HEIGHT-1) : editorimage_posy = C64_CHAR_HEIGHT-1
        
        #zoom
        if (
            (zoom==0) |
            (zoom==1)
        ) :
            editorimage_posx = 0
            editorimage_posy = 0
        
        
def action_image_refresh_show():
        #copy, move and zoom: koala_image to editor_image
        global editor_width, editor_height
        global editor_image
        global label_editor_image, label_preview_image
        global marker_image

        #draw marker
        marker_image = koala_image.copy()
        if ((marker_height > 0) & (marker_width > 0) ) :
            startx = (marker_posx)*4
            starty = (marker_posy)*8
            endx = (marker_posx+marker_width+1)*4
            endy = (marker_posy+marker_height+1)*8
            for x in range(startx,endx) :
                marker_image.putpixel((x,starty),4)
                marker_image.putpixel((x,endy-1),4)
            for y in range(starty+1,endy-1) :
                marker_image.putpixel((startx,y),4)
                marker_image.putpixel((endx-1,y),4)

        # update dimensions
        editor_width_old = editor_width
        editor_width   = KOALA_WIDTH*2 * EDITORSIZE_MULTIPLY[user_editorsize.get()]
        editor_height  = KOALA_HEIGHT * EDITORSIZE_MULTIPLY[user_editorsize.get()]
        if (editor_width != editor_width_old) :
            draw_grids()
            draw_background()

        editor_image = background_image.copy()

        editorimage_pos_sanity_check()

        scale_startx = 0
        scale_starty = 0
        scale_endx = C64_CHAR_WIDTH
        scale_endy = C64_CHAR_HEIGHT
        box_startx = editorimage_posx
        box_starty = editorimage_posy
        box_endx = editorimage_posx+C64_CHAR_WIDTH
        box_endy = editorimage_posy+C64_CHAR_HEIGHT

       
        if (box_startx < 0) :
            scale_startx = abs(box_startx)
            scale_endx = C64_CHAR_WIDTH - scale_startx
            box_endx = C64_CHAR_WIDTH - scale_startx
            box_startx = 0
        if (box_starty < 0) :
            scale_starty = abs(box_starty)
            scale_endy = C64_CHAR_HEIGHT - scale_starty
            box_endy = C64_CHAR_HEIGHT - scale_starty
            box_starty = 0
            
        if (box_endx > C64_CHAR_WIDTH) :
            scale_endx = C64_CHAR_WIDTH - box_startx
            box_endx = C64_CHAR_WIDTH
        if (box_endy > C64_CHAR_HEIGHT) :
            scale_endy = C64_CHAR_HEIGHT - box_starty
            box_endy = C64_CHAR_HEIGHT



        #copy, crop and resize
        box = (
            int(box_startx*BITMAP_PIXEL_X),
            int(box_starty*BITMAP_PIXEL_Y),
            int(box_endx*BITMAP_PIXEL_X),
            int(box_endy*BITMAP_PIXEL_Y)
        )

        editor_multi = 4 * EDITORSIZE_MULTIPLY[user_editorsize.get()] * ZOOM_MULTIPLY[zoom]
        my_width   = scale_endx * editor_multi
        my_height  = scale_endy * editor_multi
        scale_startx = scale_startx * editor_multi
        scale_starty = scale_starty * editor_multi

        editor_image.paste( marker_image.crop(box).resize((my_width,my_height)).convert("RGB") , (scale_startx, scale_starty) )
        
        #add grid
        if (zoom==1) : editor_image.paste(grid1_image, (0,0), grid1_image)
        if (zoom==2) : editor_image.paste(grid2_image, (0,0), grid2_image)
        if (zoom==3) : editor_image.paste(grid3_image, (0,0), grid3_image)
        if (zoom==4) : editor_image.paste(grid4_image, (0,0), grid4_image)
        
        #copy to label_edit_image
        image_koalaTk = ImageTk.PhotoImage(editor_image)
        label_editor_image.configure(image=image_koalaTk)
        label_editor_image.image = image_koalaTk # keep a reference!

        #prepare preview image
        preview_width   = KOALA_WIDTH * 2 * PREVIEWSIZE_MULTIPLY[user_previewsize.get()]
        preview_height  = KOALA_HEIGHT * 1 * PREVIEWSIZE_MULTIPLY[user_previewsize.get()]
        preview2_image = koala_image.resize((preview_width,preview_height)).convert("RGB")

        #copy to label_preview_image
        if ( preview_window_open == True ) :
            image2_koalaTk = ImageTk.PhotoImage(preview2_image)
            label_preview_image.configure(image=image2_koalaTk)
            label_preview_image.image = image2_koalaTk # keep a reference!







def koala_index_to_colorindex(
    index,  #0..3
    x,
    y
) :
    location = (y*C64_CHAR_WIDTH)+x
        
    switcher = {
        0 : koala_bg,    #=koala_bg;	// pixel not set = $d021 colour
        1 : koala_col12[location] >> 4,   #=koala_col12[(y*C64_CHAR_WIDTH)+x] SHR 4;
        2 : koala_col12[location] & 0b00001111,    #=koala_col12[(y*C64_CHAR_WIDTH)+x] and %00001111;
        3 : koala_col3[location] & 0b00001111    #=koala_col3[(y*C64_CHAR_WIDTH)+x] and %00001111;
    }
    return switcher.get(index,0)





def koala_to_image_single_block(x,y) :
    global koala_colorindex_data

    SHR_PRE = [
        6,
        4,
        2,
        0
    ]

    pos = ((y*C64_CHAR_WIDTH)+x)*8
    this_block = koala_bitmap[ pos:pos+8]   #this_block holds 8 bytes

    for row in range(0, 8):
        this_row = this_block[row]
        
        for column in range(0, 4):
            iy = y*8    +row
            ix = x*4    +column

            #normal data
            koalaindex = (this_row >> SHR_PRE[column]) & 0b00000011 #result should be 0..3
            koala_colorindex_data[iy*KOALA_WIDTH+ix] = koala_index_to_colorindex(koalaindex,x,y)




def koala_to_image(
):
    for y in range(0, C64_CHAR_HEIGHT):
        for x in range(0, C64_CHAR_WIDTH):
            koala_to_image_single_block(x,y)

    return None





def load_koala(
    filename_in
) :
    """
    loads and parses a koala file for debugging the koala_to_image conversion
    * reads: filename
    * sets: koala_bitmap, koala_col12, koala_col3 and koala_bg
    """
    global koala_bitmap
    global koala_col12
    global koala_col3
    global koala_bg
    
#load a koala
    print ("Opening koala \"%s\"..." % filename_in)
    file_in = open(filename_in , "rb")
    # read file into buffer
    buffer=[]
    while True:
        data = file_in.read(1)  #read 1 byte
        if not data: break
        temp = struct.unpack('B',data)
        buffer.append(temp[0])
    file_in.close()

#parse koala
    koala_bitmap    = buffer[2                  :2+8000]
    koala_col12     = buffer[2+8000             :2+8000+1000]
    koala_col3      = buffer[2+8000+1000        :2+8000+1000+1000]
    koala_bg        = buffer[2+8000+1000+1000   :2+8000+1000+1000+1][0]

    koala_to_image()
  
    return None


    

def update_infos_preview():
    global editorimage_posx, editorimage_posy
    global block_x, block_y
    
    factor_x = GRID_SIZE[zoom_preview]/PREVIEWSIZE_DIV_X[user_previewsize.get()]
    factor_y = GRID_SIZE[zoom_preview]/PREVIEWSIZE_DIV_Y[user_previewsize.get()]
    
    cursorx = int(mouse_posx/factor_x)
    cursory = int(mouse_posy/factor_y)
    
    #sanity checks:
    if (cursorx <0 ) : cursorx = 0
    if (cursory <0 ) : cursory = 0
    if (cursorx >159 ) : cursorx = 159
    if (cursory >199 ) : cursory = 199
        
    block_x = int(cursorx/BITMAP_PIXEL_X)
    block_y = int(cursory/BITMAP_PIXEL_Y)


    cursorx_variable.set(cursorx)
    cursory_variable.set(cursory)
    blockx_variable.set(block_x)
    blocky_variable.set(block_y)
    editorimage_posx_variable.set(editorimage_posx)
    editorimage_posy_variable.set(editorimage_posy)
    mousex_variable.set(mouse_posx)
    mousey_variable.set(mouse_posy)
    
    #print("preview cursorx=",cursorx," cursory=",cursory)
    #print("preview block_x=",block_x," block_y=",block_y, "editorimage_posx=",editorimage_posx," editorimage_posy=",editorimage_posy)





def update_infos():
    global cursorx_variable, cursory_variable
    global blockx_variable, blocky_variable
    global editorimage_posx_variable, editorimage_posy_variable
    global mousex_variable, mousey_variable
    global used_color_bg, used_color_col1, used_color_col2, used_color_col3
    global editorimage_posx, editorimage_posy
    global block_x, block_y
    global radiobutton_replace_bg, radiobutton_replace_col1, radiobutton_replace_col2, radiobutton_replace_col3
    global radiobutton_current_bg, radiobutton_current_col1, radiobutton_current_col2, radiobutton_current_col3
    global undo_variable

    undo_variable.set(len(undo_stack))

    factor_x = GRID_SIZE[zoom]/EDITORSIZE_DIV_X[user_editorsize.get()]
    factor_y = GRID_SIZE[zoom]/EDITORSIZE_DIV_Y[user_editorsize.get()]

    #https://docs.python.org/3/library/platform.html
    #platform.system() : 'Linux', 'Darwin', 'Java', 'Windows'
    if (operating_system == 'Darwin') :
        adjustx=-4
        adjusty=-6
    else:
        adjustx=-2
        adjusty=-2

    
    cursorx = int( ((mouse_posx+adjustx)/factor_x) + (editorimage_posx*BITMAP_PIXEL_X) )
    cursory = int( ((mouse_posy+adjusty)/factor_y) + (editorimage_posy*BITMAP_PIXEL_Y) )
    
    #sanity checks:
    if (cursorx <0 ) : cursorx = 0
    if (cursory <0 ) : cursory = 0
    if (cursorx >159 ) : cursorx = 159
    if (cursory >199 ) : cursory = 199
        
    block_x = int(cursorx/BITMAP_PIXEL_X)
    block_y = int(cursory/BITMAP_PIXEL_Y)

    cursorx_variable.set(cursorx)
    cursory_variable.set(cursory)
    blockx_variable.set(block_x)
    blocky_variable.set(block_y)
    editorimage_posx_variable.set(editorimage_posx)
    editorimage_posy_variable.set(editorimage_posy)
    mousex_variable.set(mouse_posx)
    mousey_variable.set(mouse_posy)


    #update all color-buttons
    col_bg = koala_bg
    col1 = int(koala_col12[(block_y*40)+block_x] >> 4)
    col2 = koala_col12[(block_y*40)+block_x]& 0b00001111
    col3 = koala_col3[(block_y*40)+block_x]& 0b00001111
    
    used_color_bg.set(col_bg)
    used_color_col1.set(col1)
    used_color_col2.set(col2)
    used_color_col3.set(col3)

    mycolor = '#%02x%02x%02x' % (
        PALETTEDATA_PEPTO[col_bg*3+0],
        PALETTEDATA_PEPTO[col_bg*3+1],
        PALETTEDATA_PEPTO[col_bg*3+2]
    )
    radiobutton_replace_bg.configure(background=mycolor)
    radiobutton_replace_bg.configure(activebackground=mycolor)
    radiobutton_replace_bg.configure(selectcolor=mycolor)
    radiobutton_current_bg.configure(background=mycolor)
    radiobutton_current_bg.configure(activebackground=mycolor)
    radiobutton_current_bg.configure(selectcolor=mycolor)

    mycolor = '#%02x%02x%02x' % (
        PALETTEDATA_PEPTO[col1*3+0],
        PALETTEDATA_PEPTO[col1*3+1],
        PALETTEDATA_PEPTO[col1*3+2]
    )
    radiobutton_replace_col1.configure(background=mycolor)
    radiobutton_replace_col1.configure(activebackground=mycolor)
    radiobutton_replace_col1.configure(selectcolor=mycolor)
    radiobutton_current_col1.configure(background=mycolor)
    radiobutton_current_col1.configure(activebackground=mycolor)
    radiobutton_current_col1.configure(selectcolor=mycolor)

    mycolor = '#%02x%02x%02x' % (
        PALETTEDATA_PEPTO[col2*3+0],
        PALETTEDATA_PEPTO[col2*3+1],
        PALETTEDATA_PEPTO[col2*3+2]
    )
    radiobutton_replace_col2.configure(background=mycolor)
    radiobutton_replace_col2.configure(activebackground=mycolor)
    radiobutton_replace_col2.configure(selectcolor=mycolor)
    radiobutton_current_col2.configure(background=mycolor)
    radiobutton_current_col2.configure(activebackground=mycolor)
    radiobutton_current_col2.configure(selectcolor=mycolor)

    mycolor = '#%02x%02x%02x' % (
        PALETTEDATA_PEPTO[col3*3+0],
        PALETTEDATA_PEPTO[col3*3+1],
        PALETTEDATA_PEPTO[col3*3+2]
    )
    radiobutton_replace_col3.configure(background=mycolor)
    radiobutton_replace_col3.configure(activebackground=mycolor)
    radiobutton_replace_col3.configure(selectcolor=mycolor)
    radiobutton_current_col3.configure(background=mycolor)
    radiobutton_current_col3.configure(activebackground=mycolor)
    radiobutton_current_col3.configure(selectcolor=mycolor)
    
    my_block = block_y*C64_CHAR_WIDTH+block_x
    current_color.set(set_pixel_get_index_at_pixel(my_block, cursorx, cursory))






def input_mouse_motion_edit_window(event):
#    global label_editor_image
#    global space_pressed
    global mouse_posx, mouse_posy

    mouse_posx, mouse_posy = event.x, event.y

    update_infos()

#    label_editor_image.focus_set()
#    if (space_pressed == True) :
#        print ("move!")
#        space_pressed = False





def set_pixel_optimize_palette(my_block):
    col = []
    col.append(koala_bg)
    col.append(koala_col12[my_block] >> 4)
    col.append(koala_col12[my_block] & 0b00001111)
    col.append(koala_col3[my_block] & 0b00001111)

    palette = []
    for x in col:
        if x not in palette:
            palette.append(x)
    
    return palette




def set_pixel_replace_colors(my_block, c, color):
    global koala_bg, koala_col12, koala_col3
    # replace bg, screen or colorram

    #print("replace color: write color ",color, " to index ",c)

    if (c==0) : koala_bg = color; return None
    if (c==1) : koala_col12[my_block] = (koala_col12[my_block] & 0b00001111) + (color << 4); return None
    if (c==2) : koala_col12[my_block] = (koala_col12[my_block] & 0b11110000) + color; return None
    if (c==3) : koala_col3[my_block] = color; return None

    return None


def set_pixel_replace_bitmap(my_block,x,y,c) :
    global koala_bitmap
    #update koala bitmap data
    
    #print("replace bitmap with index=",c)

    SHIFT_LEFT = (
        6,  #0
        4,  #1
        2,  #2
        0   #3
    )

    AND_PRE = (
        0b00111111,  #0
        0b11001111,  #1
        0b11110011,  #2
        0b11111100  #3
    )
    
    bitmap_position_y = (my_block*8)+ (y & 0b00000111)
    bitmap_position_x = x & 0b00000011 #only 0-3
    koala_bitmap[bitmap_position_y] = (koala_bitmap[bitmap_position_y] & AND_PRE[bitmap_position_x]) + (c << SHIFT_LEFT[bitmap_position_x])




def set_pixel_update_preview_block (pos, old_color, color) :
    #replace all pixels with old_color with color in this block
    global koala_colorindex_data

    for y in range(0,8) :
        for x in range(0,4) :
            if (koala_colorindex_data[pos+(y*160)+x] == old_color ) :
                koala_colorindex_data[pos+(y*160)+x] = color



def set_pixel__left(posx, posy, color):
    if (user_pencil.get() == "light") :
        if ( (posy & 0b00000001) != 0) : return None
        if ( (posx & 0b00000011) != (posy & 0b00000011)) : return None
    if (user_pencil.get() == "checkerboard") :
        if ( (posx & 0b00000001) != (posy & 0b00000001)) : return None
    if (user_pencil.get() == "xline") :
        if ( (posy & 0b00000001) != 0) : return None
    if (user_pencil.get() == "yline") :
        if ( (posx & 0b00000001) != 0) : return None
    set_pixel(posx, posy, color)



def set_pixel__right(posx, posy, color):
    if (user_pencil.get() == "light") :
        if ( (posy & 0b00000001) != 0) : return None
        if ( ((posx+2) & 0b00000011) != (posy & 0b00000011)) : return None
    if (user_pencil.get() == "checkerboard") :
        if ( (posx & 0b00000001) == (posy & 0b00000001)) : return None
    if (user_pencil.get() == "xline") :
        if ( (posy & 0b00000001) == 0) : return None
    if (user_pencil.get() == "yline") :
        if ( (posx & 0b00000001) == 0) : return None
    set_pixel(posx, posy, color)



def set_pixel(posx, posy, color):
    if (user_drawmode.get() == 'dye') : set_pixel__dye_mode(posx, posy, color); return None
    if (user_drawmode.get() == 'keep') : set_pixel__keep_mode(False,posx, posy, color); return None
    if (user_drawmode.get() == 'replace') : set_pixel__keep_mode(True,posx, posy, color); return None
    if (user_drawmode.get() == 'select') : set_pixel__select_mode(posx, posy, color); return None



def set_pixel_get_best_index_for_color(my_block, color):
    #0 = background, 1=screen1, 2=screen2, 3=colorram, 99=nothing
    if (color==koala_bg) : return 0
    if (color==koala_col12[my_block] >> 4) : return 1
    if (color==koala_col12[my_block] & 0b00001111) : return 2
    if (color==koala_col3[my_block] & 0b00001111) : return 3
    return False

def set_pixel_get_color_by_index(my_block, index):
    if (index==0) : return koala_bg
    if (index==1) : return (koala_col12[my_block] >> 4)
    if (index==2) : return (koala_col12[my_block] & 0b00001111)
    if (index==3) : return (koala_col3[my_block] & 0b00001111)
    return False




def set_pixel__select_mode(posx, posy, color):
    undo_save_already_done = False
    my_block = block_y*C64_CHAR_WIDTH+block_x
    user_replace_this = user_replace_color.get()    #0 = background, 1=screen1, 2=screen2, 3=colorram, 99=nothing

    flag_new_colors = False
    flag_new_bitmap = False

    # deal with colors
    if ( user_replace_this == 99) :
        #do not overwrite anything
        replace_this = set_pixel_get_best_index_for_color(my_block, color)   #0 = background, 1=screen1, 2=screen2, 3=colorram, 99=nothing
        if (replace_this is False) : return None   # 99=color not found: drawing not possible -> so exiting
    else :
        #if this is a new color: overwrite a color
        if (color != set_pixel_get_color_by_index(my_block, user_replace_this) ) :
            flag_new_colors = True
        replace_this = user_replace_this
    
    #check if old and new bitmap matrices differ
    if (set_pixel_get_index_at_pixel(my_block, posx, posy) != replace_this) : flag_new_bitmap = True

    #exit if colors or bitmap are not new
    if (flag_new_colors == False) & (flag_new_bitmap == False) : return None

    # update colors and bitmap
    undo_save();
    if (flag_new_colors == True) : set_pixel_replace_colors(my_block, replace_this, color) # replace bg, screen or colorram
    if (flag_new_bitmap == True) : set_pixel_replace_bitmap(my_block, posx, posy, replace_this)   #update koala bitmap data
    
    # update preview
    if ( user_replace_this == 0):
        koala_to_image()    #background is changed: convert whole koala to image again
    else :
        koala_to_image_single_block(block_x, block_y)   #update preview image only for this block (faster than converting whole koala to image again)

    action_image_refresh_prepare()
    update_infos()




def set_pixel__dye_mode(posx, posy, color):
    undo_save_already_done = False
    my_block = block_y*C64_CHAR_WIDTH+block_x
    user_replace_this = user_replace_color.get()    #0 = background, 1=screen1, 2=screen2, 3=colorram, 99=nothing

    replace_this = set_pixel_get_index_at_pixel(my_block, posx, posy)

    if (color == set_pixel_get_color_by_index(my_block, replace_this)) : return None

    # update colors
    undo_save();
    set_pixel_replace_colors(my_block, replace_this, color) # replace bg, screen or colorram
    
    # update preview
    if ( replace_this == 0):
        koala_to_image()    #background is changed: convert whole koala to image again
    else :
        koala_to_image_single_block(block_x, block_y)   #update preview image only for this block (faster than converting whole koala to image again)

    action_image_refresh_prepare()
    update_infos()




def set_pixel_get_index_at_pixel(my_block, x,y) :
    # find out what (bg, screen1, screen2 or colram) this color uses
    SHIFT_RIGHT = (
        6,  #0
        4,  #1
        2,  #2
        0   #3
    )

    bitmap_position_y = (my_block*8)+ (y & 0b00000111)
    bitmap_position_x = x & 0b00000011 #only 0-3
    return (koala_bitmap[bitmap_position_y] >> SHIFT_RIGHT[bitmap_position_x]) & 0b00000011 #only 0-3
    

def set_pixel_color_is_used_in_block(my_block, color_type):
    for y in range (0,8) :
        for x in range (0,4) :
            if (color_type == set_pixel_get_index_at_pixel(my_block, x,y)) :
                return True
    # not found
    return False



def set_pixel_fill_used_array(my_block):
    my_type = (
        1,  #screen1
        2,  #screen2
        3   #colram
    )
    
    used = []
    
    for col in my_type :
        used.append(set_pixel_color_is_used_in_block(my_block, col))

    return used





def set_pixel__keep_mode(okay_to_overwrite, posx, posy, color):
    global user_replace_color
    undo_save_already_done = False

    my_block = block_y*C64_CHAR_WIDTH+block_x

    flag_new_colors = False
    flag_new_bitmap = False

    used_array = set_pixel_fill_used_array(my_block)
    
    used_colors = 0
    for a in used_array :
        if (a == True): used_colors += 1
    
    index_here = set_pixel_get_index_at_pixel(my_block, posx ,posy)
    index_new = set_pixel_get_best_index_for_color(my_block, color)   #0 = background, 1=screen1, 2=screen2, 3=colorram, 99=nothing

#    print("")
#    print("index_new=",index_new)
    if (index_new is False) :
        #print ("no matching color found:")

        if (used_colors > 2) :
            #print ("-too many colours:")
            
            if ( okay_to_overwrite == False ) :
                #print ("--overwriting color not allowed: giving up")
                return None
                
            else :
                #print ("--just overwriting color")
                # find out what (bg, screen1, screen2 or colram) this color uses
                user_replace_color.set(index_here)
                if (index_here == 0) :
                    #print("11 not replacing background color!")
                    return None
                else :
                    #print ("---index here=",index_here," / color=",color)
                    flag_new_colors = True
                    index_new = index_here

                    #update preview image only for this block (faster than converting whole koala to image again)
#                    pos = block_y * 8 * 160 + (block_x * 4)
#                    set_pixel_update_preview_block(pos, old_color, color)   #replace all pixels with old_color with color in this block

        else :
            # no matching color found, so reorganize bitmap and add a new color
            #print ("-reorganize bitmap and add a new color")
            
            for a in range(0,len(used_array)) :
                if (used_array[a] == False) : 
                    break
            a += 1        
#            print('free color at ',a)
            flag_new_colors = True
            flag_new_bitmap = True
            index_new = a
    else :
        #print ("matching color found")
        if (index_new == index_here) : return None     #same color. nothing to do.
        #print ("- just update bitmap")
        flag_new_bitmap = True



    if ((flag_new_colors == False) & (flag_new_bitmap == False)) :
        #print ("Nothing to do")
        return None

    undo_save();
    if (flag_new_colors == True): set_pixel_replace_colors(my_block, index_new, color) # replace bg, screen or colorram
    if (flag_new_bitmap == True): set_pixel_replace_bitmap(my_block, posx, posy ,index_new)
    
    #update preview
    koala_to_image_single_block(block_x, block_y)   #update preview image only for this block (faster than converting whole koala to image again)
    action_image_refresh_prepare()
    update_infos()



        


def input_mouse_left_button_preview(event):
    global mouse_posx, mouse_posy
    mouse_posx, mouse_posy = event.x, event.y
    update_infos_preview()
    zoom_perform()
    action_image_refresh_show()


def input_mouse_left_button_editor(event):
    global mouse_posx, mouse_posy
    mouse_posx, mouse_posy = event.x, event.y
    update_infos()
    
    if (editor_mode == 'marker_start') :
        marker_start()
        return None

    if (editor_mode == 'marker_end') :
        marker_end()
        return None
        
    if (editor_mode == 'edit') :
        set_pixel__left(cursorx_variable.get(), cursory_variable.get(), user_drawcolor_left.get())


def input_mouse_right_button(event):
    global mouse_posx, mouse_posy
    mouse_posx, mouse_posy = event.x, event.y
    update_infos()
    set_pixel__right(cursorx_variable.get(), cursory_variable.get(), user_drawcolor_right.get())


def input_mouse_middle_button_release(event):
    global label_editor_image
    label_editor_image.config(cursor=CURSOR_EDIT)
    
def input_mouse_middle_button_press(event):
    global block_x_absolute, block_y_absolute
    global label_editor_image
    
    label_editor_image.config(cursor=CURSOR_MOVE)

    factor_x = GRID_SIZE[zoom]/EDITORSIZE_DIV_X[user_editorsize.get()]
    factor_y = GRID_SIZE[zoom]/EDITORSIZE_DIV_Y[user_editorsize.get()]
 
    block_x_absolute = int( (mouse_posx/factor_x/BITMAP_PIXEL_X) )
    block_y_absolute = int( (mouse_posy/factor_y/BITMAP_PIXEL_Y) )


def input_mouse_middle_button_motion(event):
    global mouse_posx, mouse_posy
    global editorimage_posx, editorimage_posy
    global block_x_absolute, block_y_absolute

    mouse_posx, mouse_posy = event.x, event.y
    update_infos()
    
    old_x = block_x_absolute
    old_y = block_y_absolute

    factor_x = GRID_SIZE[zoom]/EDITORSIZE_DIV_X[user_editorsize.get()]
    factor_y = GRID_SIZE[zoom]/EDITORSIZE_DIV_Y[user_editorsize.get()]
 
    block_x_absolute = int( (mouse_posx/factor_x/BITMAP_PIXEL_X) )
    block_y_absolute = int( (mouse_posy/factor_y/BITMAP_PIXEL_Y) )
  
    diff_x = old_x - block_x_absolute
    diff_y = old_y - block_y_absolute
    

    if (
        (abs(diff_x) != 0) |
        (abs(diff_y) != 0)
    ) :
        editorimage_posx += diff_x
        editorimage_posy += diff_y
        action_image_refresh_show()
        

    return None
    




def zoom_perform() :
    global editorimage_posx, editorimage_posy

    zoom_center_x = block_x
    zoom_center_y = block_y

    if (zoom==0) :
        editorimage_posx = int( zoom_center_x- C64_CHAR_WIDTH/1 )
        editorimage_posy = int( zoom_center_y- C64_CHAR_HEIGHT/1 )
    if (zoom==1) :
        editorimage_posx = int( zoom_center_x- C64_CHAR_WIDTH/2 )
        editorimage_posy = int( zoom_center_y- C64_CHAR_HEIGHT/2 )
    if (zoom==2) :
        editorimage_posx = int( zoom_center_x- C64_CHAR_WIDTH/4 )
        editorimage_posy = int( zoom_center_y- C64_CHAR_HEIGHT/4 )
    if (zoom==3) :
        editorimage_posx = int( zoom_center_x- C64_CHAR_WIDTH/8 )
        editorimage_posy = int( zoom_center_y- C64_CHAR_HEIGHT/8 )
    if (zoom==4) :
        editorimage_posx = int( zoom_center_x- C64_CHAR_WIDTH/16 )
        editorimage_posy = int( zoom_center_y- C64_CHAR_HEIGHT/16 )

    action_image_refresh_prepare()
    #print("zoom=",zoom)
    #print("block_x=",block_x," block_y=",block_y, "editorimage_posx=",editorimage_posx," editorimage_posy=",editorimage_posy)
    update_infos()


def zoom_in(self) :
    global zoom
    if (zoom < 4) :
        zoom += 1
        zoom_perform()


def zoom_out(self) :
    global zoom
    if (zoom > 0) :
        zoom -= 1
        zoom_perform()



def input_mouse_wheel(event):
    if (
        (event.num == 5) |
        (int(event.delta / 120) == -1) |
        (event.delta == -1)
    ) :
        #mouse wheel down
        zoom_out(0)

    if (
        (event.num == 4) |
        (int(event.delta / 120) == 1) |
        (event.delta == 1)
    ) :
        #mouse wheel up
        zoom_in(0)


#https://stackoverflow.com/questions/48210090/how-to-use-bundled-program-after-pyinstaller-add-binary
def resource_path(relative_path):
    #Get absolute path to resource, works for dev and for PyInstaller
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)
    

def action_OpenFile_from_menu():
    action_OpenFile(None)
    
def action_OpenFile(self):
    ftypes = [('Image Files', '*.koa *.kla')]
    load_filename = askopenfilename(filetypes = ftypes)
    if not load_filename : return None
    
    loadFile(load_filename)
    return None


def shorten_filename (filename) :
    if (len(current_filename) > 20) :
        return "..."+current_filename[-20:]
    else :
        return current_filename

def set_title():
    root.title(PROGNAME+" \""+shorten_filename(current_filename)+"\"")

def loadFile(filename):
    global current_filename
    global undo_stack
    
    current_filename = filename
    set_title()
    load_koala(filename)
    undo_stack = []
    update_infos()
    action_image_refresh_prepare()


def undo_save():
    global undo_stack

    my_block = block_y*C64_CHAR_WIDTH+block_x
    
    my_undo = []
    my_undo.append(block_x)
    my_undo.append(block_y)
    my_undo.append(koala_col12[my_block])
    my_undo.append(koala_col3[my_block])
    my_undo.append(koala_bitmap[ (my_block*8) : ((my_block+1)*8) ])
 
    undo_stack.append(my_undo)
    update_infos()



def undo_undo_from_menu():
    undo_undo(None)
    
def undo_undo(self):
    global undo_stack
    
    if (len(undo_stack)>0) :
        value = undo_stack.pop()

        undo_x = value[0]
        undo_y = value[1]
        undo_col12 = value[2]
        undo_col3 = value[3]
        undo_bitmap = value[4]

        my_block = undo_y*C64_CHAR_WIDTH+undo_x
        
        koala_col12[my_block] = undo_col12
        koala_col3[my_block] = undo_col3
        for y in range(0,8) :
            koala_bitmap[(my_block*8)+y] = undo_bitmap[y]
        koala_to_image_single_block(undo_x,undo_y)
        action_image_refresh_prepare()
        update_infos()



def marker_select_from_menu () :
    marker_select(None)

def marker_select(self):
    global editor_mode
    editor_mode = 'marker_start'
    label_editor_image.config(cursor=CURSOR_MARKER_START)


def marker_start():
    global editor_mode
    global marker_posx, marker_posy
    editor_mode = 'marker_end'
    label_editor_image.config(cursor=CURSOR_MARKER_END)
    marker_posx = block_x
    marker_posy = block_y

def marker_end():
    global editor_mode
    global marker_width, marker_height
    
    editor_mode = 'edit'
    label_editor_image.config(cursor=CURSOR_EDIT)
    
    marker_width = block_x - marker_posx
    marker_height = block_y - marker_posy
    action_image_refresh_show()


def buffer_copy_data():
    global buffer_bitmap, buffer_col12, buffer_col3
    global buffer_width, buffer_height, buffer_posx, buffer_posy
    
    buffer_posx = marker_posx
    buffer_posy = marker_posy
    buffer_width = marker_width
    buffer_height = marker_height
    
    for y in range(0, marker_height+1) :
        for x in range(0, marker_width+1) :
            block = (marker_posy+y)*C64_CHAR_WIDTH+(marker_posx+x)
            buffer_col12[block] = koala_col12[block]
            buffer_col3[block] = koala_col3[block]
            for c in range(0,8) :
                buffer_bitmap[block*8+c] = koala_bitmap[block*8+c]


def marker_reset():
    global marker_posx, marker_posy, marker_width, marker_height
    marker_posx = 0
    marker_posy = 0
    marker_width = 0
    marker_height = 0

def buffer_copy_from_menu():
    buffer_copy(None)
    
def buffer_copy(self):
    buffer_copy_data()
    marker_reset()
    koala_to_image()
    action_image_refresh_prepare()


def buffer_paste_from_menu():
    buffer_paste(None)
    
def buffer_paste(self):
    global koala_bitmap, koala_col12, koala_col3

    for y in range(0, buffer_height+1) :
        for x in range(0, buffer_width+1) :
            if (
             ((block_y+y) < C64_CHAR_HEIGHT) &
             ((block_x+x) < C64_CHAR_WIDTH)
            ) :
                block_src = (buffer_posy+y)*C64_CHAR_WIDTH+(buffer_posx+x)
                block_dst = (block_y+y)*C64_CHAR_WIDTH+(block_x+x)
                koala_col12[block_dst] = buffer_col12[block_src]
                koala_col3[block_dst] = buffer_col3[block_src]
                for c in range(0,8) :
                    koala_bitmap[block_dst*8+c] = buffer_bitmap[block_src*8+c]

    koala_to_image()
    action_image_refresh_prepare()

def buffer_cut_from_menu():
    buffer_cut(None)
    
def buffer_cut(self):
    global koala_bitmap
    
    if (
     (marker_height == 0) | (marker_width == 0)
    ) : return None
    
    buffer_copy_data()
    
    for y in range(0,marker_height+1) :
        for x in range(0,marker_width+1) :
            for c in range(0,8) :
                block = (marker_posy+y)*C64_CHAR_WIDTH+(marker_posx+x)
                koala_bitmap[block*8+c] = 0  #background color

    marker_reset()
    koala_to_image()
    action_image_refresh_prepare()



def draw_new_image():
    global current_filename
    global koala_bitmap, koala_bg, koala_col12, koala_col3

    current_filename = "new.koa"

    set_title()

    koala_bitmap=[0]*8000
    koala_col12=[0]*1000
    koala_col3=[0]*1000
    koala_bg=0

    koala_to_image()

    #create palette
    koala_image.putpalette(PALETTEDATA_COLODORE)
    koala_image.putdata(koala_colorindex_data)

    action_image_refresh_show() 



def action_SaveFile_from_menu():
    action_SaveFile(None)

def action_SaveFile(self):
    global user_filename_save
    global current_filename
    
    user_filename_save = ""

    try:
        var_start_address = int (user_start_address.get(),16)
    except ValueError:
        var_start_address = 0
    var_start_address_checkbutton = user_start_address_checkbutton.get()

    #sanity checks
    sanity_check = True
    if (
        (var_start_address > 0xffff) &
        (var_start_address_checkbutton)
    ) :
        textbox.insert(tk.END, "*** error: Start address has to be 0-65535 (2bytes).\n")
        sanity_check = False


    user_filename_save = asksaveasfilename(
     defaultextension='.koa',
     filetypes=[("koala", '*.koa')],
     initialfile=os.path.basename(current_filename),
     title="Choose filename"
    )

#     initialdir=self.default_path_to_pref,

    if not user_filename_save : return None

    #action_convert()

    #write stuff...
    file_out = open(user_filename_save , "wb")

    out_buffer = []
    
    #start address
    if var_start_address_checkbutton :
        i=var_start_address & 0xff  #low
        out_buffer.append(i)
        i=var_start_address >> 8    #high
        out_buffer.append(i)
        
    #koala data
    for i in range(0,8000):
        out_buffer.append(koala_bitmap[i])
    for i in koala_col12:
        out_buffer.append(i)
    for i in koala_col3:
        out_buffer.append(i)
    out_buffer.append(koala_bg)
    
    file_out.write(bytearray(out_buffer))
    file_out.close()
    
    current_filename = user_filename_save
    set_title()
    
    return None



def create_gui_drawmode (
	root,
    _row,
    _column
) :
    frame_border = tk.Frame(
        root,
        bg=BGCOLOR,
        bd=_bd,
    )
    frame_border.grid(
        row=_row,
        column=_column
    )
    frame_inner = tk.Frame(
        frame_border,
        bg=BGCOLOR,
        bd=1,
        padx = _padx,
        pady = _pady,
        relief=tk.RAISED
        )
    frame_inner.grid()
    frame_inner.grid_columnconfigure(0, weight=1)
    frame_inner.grid_rowconfigure(0, weight=1)

    label = tk.Label(
        frame_inner,
        bg=BGCOLOR,
        text="draw mode:",
        wraplength=100,
        anchor='c',
        justify='left',
        fg="#000088"
    )
    label.grid(
        row=0,
        column=0,
        sticky=tk.N,
        columnspan=2
    )
    MODES = [
            ("keep", "keep", 1, 0),
            ("replace", "replace", 1, 1),
            ("select", "select", 2, 0),
            ("dye", "dye", 2, 1)
        ]

    for text, mode, row, column in MODES:
        radiobutton_user_mode = tk.Radiobutton(
            frame_inner,
            bg=BGCOLOR,
            activebackground=ACTIVECOLOR,
            selectcolor=SELECTCOLOR,
            text = text,
            value = mode,
            indicatoron=0,
            variable=user_drawmode,
            cursor=CURSOR_HAND,
            command=root_refresh
        )
        radiobutton_user_mode.grid(
            row=row,
            column=column,
            sticky=tk.W+tk.E
        )


def root_refresh() :
    global frame_replace_color
    
    if (user_drawmode.get() == 'select') : 
        frame_replace_color.grid()
    else :
        frame_replace_color.grid_remove()
    
    

def create_gui_preferences_editorsize (
	root,
    _row,
    _column
) :
    frame_border = tk.Frame(
        root,
        bg=BGCOLOR,
        bd=_bd,
    )
    frame_border.grid(
        row=_row,
        column=_column
    )
    frame_inner = tk.Frame(
        frame_border,
        bg=BGCOLOR,
        bd=1,
        padx = _padx,
        pady = _pady,
        relief=tk.RAISED
        )
    frame_inner.grid()
    frame_inner.grid_columnconfigure(0, weight=1)
    frame_inner.grid_rowconfigure(0, weight=1)

    _row = 0
    label = tk.Label(
        frame_inner,
        bg=BGCOLOR,
        text="editor size",
        wraplength=100,
        anchor='c',
        justify='left',
        fg="#000088"
    )
    label.grid(
        row=_row,
        column=1,
        sticky=tk.W+tk.E
    )
    MODES = [
            (EDITORSIZE_TEXT[0], 0),
            (EDITORSIZE_TEXT[1], 1)
        ]

    for text, mode in MODES:
        radiobutton = tk.Radiobutton(
            frame_inner,
            bg=BGCOLOR,
            activebackground=ACTIVECOLOR,
            selectcolor=SELECTCOLOR,
            text = text,
            value = mode,
            indicatoron=0,
            variable=user_editorsize,
            cursor=CURSOR_HAND,
            command=action_image_refresh_prepare
        )
        _row += 1
        radiobutton.grid(
            row=_row,
            column=1,
            sticky=tk.W+tk.E
        )

def create_gui_preferences_previewsize (
	root,
    _row,
    _column
) :
    frame_border = tk.Frame(
        root,
        bg=BGCOLOR,
        bd=_bd,
    )
    frame_border.grid(
        row=_row,
        column=_column
    )
    frame_inner = tk.Frame(
        frame_border,
        bg=BGCOLOR,
        bd=1,
        padx = _padx,
        pady = _pady,
        relief=tk.RAISED
        )
    frame_inner.grid()
    frame_inner.grid_columnconfigure(0, weight=1)
    frame_inner.grid_rowconfigure(0, weight=1)

    _row = 0
    label = tk.Label(
        frame_inner,
        bg=BGCOLOR,
        text="preview size",
        wraplength=100,
        anchor='c',
        justify='left',
        fg="#000088"
    )
    label.grid(
        row=_row,
        column=1,
        sticky=tk.W+tk.E
    )
    MODES = [
            (PREVIEWSIZE_TEXT[0], 0),
            (PREVIEWSIZE_TEXT[1], 1)
        ]

    for text, mode in MODES:
        radiobutton = tk.Radiobutton(
            frame_inner,
            bg=BGCOLOR,
            activebackground=ACTIVECOLOR,
            selectcolor=SELECTCOLOR,
            text = text,
            value = mode,
            indicatoron=0,
            variable=user_previewsize,
            cursor=CURSOR_HAND,
            command=action_image_refresh_prepare
        )
        _row += 1
        radiobutton.grid(
            row=_row,
            column=1,
            sticky=tk.W+tk.E
        )



def create_gui_preferences_palette (
	root,
    _row,
    _column
) :
#palette radiobuttons
#http://effbot.org/tkbook/radiobutton.htm
    frame_border = tk.Frame(
        root,
        bg=BGCOLOR,
        bd=_bd,
    )
    frame_border.grid(
        row=_row,
        column=_column
    )
    frame_inner = tk.Frame(
        frame_border,
        bg=BGCOLOR,
        bd=1,
        padx = _padx,
        pady = _pady,
        relief=tk.RAISED
        )
    frame_inner.grid()
    frame_inner.grid_columnconfigure(0, weight=1)
    frame_inner.grid_rowconfigure(0, weight=1)

    _row = 0
    label = tk.Label(
        frame_inner,
        bg=BGCOLOR,
        text="palette",
        wraplength=100,
        anchor='c',
        justify='left',
        fg="#000088"
    )
    label.grid(
        row=_row,
        column=1,
        sticky=tk.W+tk.E
    )
    MODES = [
            ("colodore", "colodore"),
            ("pepto", "pepto")
        ]

    for text, mode in MODES:
        radiobutton_user_mode = tk.Radiobutton(
            frame_inner,
            bg=BGCOLOR,
            activebackground=ACTIVECOLOR,
            selectcolor=SELECTCOLOR,
            text = text,
            value = mode,
            indicatoron=0,
            variable=user_palette,
            cursor=CURSOR_HAND,
            command=action_image_refresh_prepare
        )
        _row += 1
        radiobutton_user_mode.grid(
            row=_row,
            column=1,
            sticky=tk.W+tk.E
        )

        
def create_gui_pencil (
	root,
    _row,
    _column
) :
    frame_border = tk.Frame(
        root,
        bg=BGCOLOR,
        bd=_bd,
    )
    frame_border.grid(
        row=_row,
        column=_column
    )
    frame_inner = tk.Frame(
        frame_border,
        bg=BGCOLOR,
        bd=1,
        padx = _padx,
        pady = _pady,
        relief=tk.RAISED
        )
    frame_inner.grid()
    frame_inner.grid_columnconfigure(0, weight=1)
    frame_inner.grid_rowconfigure(0, weight=1)

    label = tk.Label(
        frame_inner,
        bg=BGCOLOR,
        text="pencil",
        wraplength=100,
        anchor='c',
        justify='left',
        fg="#000088"
    )
    label.grid(
        row=0,
        column=0,
        sticky=tk.W+tk.E,
        columnspan=2
    )


    MODES = [
            ("normal", "normal", 1,0),
            ("checkerboard", "checkerboard", 1,1),
            ("x-line dither", "xline", 2,0),
            ("y-line dither", "yline", 2,1),
            ("light", "light", 3,0),
        ]
        
    for text, mode, row, col in MODES:
        radiobutton_pencil = tk.Radiobutton(
            frame_inner,
            bg=BGCOLOR,
            activebackground=ACTIVECOLOR,
            selectcolor=SELECTCOLOR,
            text = text,
            value = mode,
            indicatoron=0,
            variable=user_pencil,
            cursor=CURSOR_HAND,
#            command=action_image_refresh_prepare
        )
        radiobutton_pencil.grid(
            row=row,
            column=col,
            sticky=tk.W+tk.E
        )



def create_gui_preferences_startaddress (
	root,
    _row,
    _column
) :
    frame_border = tk.Frame(
        root,
        bg=BGCOLOR,
        bd=_bd,
    )
    frame_border.grid(
        row=_row,
        column=_column
    )
    frame_inner = tk.Frame(
        frame_border,
        bg=BGCOLOR,
        bd=1,
        padx = _padx,
        pady = _pady,
        relief=tk.RAISED
        )
    frame_inner.grid()
    frame_inner.grid_columnconfigure(0, weight=1)
    frame_inner.grid_rowconfigure(0, weight=1)
    
    label_start_address_title = tk.Label(
        frame_inner,
        bg=BGCOLOR,
        text="start address in hex:",
        anchor='c',
        fg="#000088"
    )
    checkbutton_start_address = tk.Checkbutton(
        frame_inner,
        bg=BGCOLOR,
        variable = user_start_address_checkbutton,
        cursor=CURSOR_HAND,
        )
    label_start_address = tk.Label(
        frame_inner,
        bg=BGCOLOR,
        text="values $0-$ffff $",
        anchor='c'
    )
    entry_start_address= tk.Entry(
        frame_inner,
        bg=TEXTBOXCOLOR,
        width=8,
        textvariable = user_start_address
    )
    
    #placement in grid layout
    label_start_address_title.grid(
        row=0,
        column=0,
        sticky=tk.W+tk.E,
        columnspan=3
    )
    checkbutton_start_address.grid(
        row=1,
        column=0,
        sticky=tk.W
    )
    label_start_address.grid(
        row=1,
        column=1,
        sticky=tk.W+tk.E
    )
    entry_start_address.grid(
        row=1,
        column=2,
        sticky=tk.E
    )







def create_gui_replace_color (
	root,
    _row,
    _column
) :
    global frame_replace_color
    global radiobutton_replace_bg, radiobutton_replace_col1, radiobutton_replace_col2, radiobutton_replace_col3

    frame_replace_color = tk.Frame(
        root,
        bg=BGCOLOR,
        bd=_bd,
    )
    frame_replace_color.grid(
        row=_row,
        column=_column
    )
    frame_inner = tk.Frame(
        frame_replace_color,
        bg=BGCOLOR,
        bd=1,
        padx = _padx,
        pady = _pady,
        relief=tk.RAISED
        )
    frame_inner.grid()
    frame_inner.grid_columnconfigure(0, weight=1)
    frame_inner.grid_rowconfigure(0, weight=1)

    

    label = tk.Label(
        frame_inner,
        bg=BGCOLOR,
        text="select mode: replace",
        anchor="c",
        justify='left',
        fg="#000088"
    )
    label.grid(
        row=0,
        column=0,
        sticky=tk.W+tk.E,
        columnspan=8
    )


    #replace color
    label_none = tk.Label(
        frame_inner,
        bg=BGCOLOR,
        text="none",
        anchor='c',
        fg="#000088"
    )
    radiobutton_used_color_none = tk.Radiobutton(
        frame_inner,
        value = 99,
        width=2,
        indicatoron=0,
        activebackground=ACTIVECOLOR,
        selectcolor=SELECTCOLOR,
        variable=user_replace_color,
        bg=BGCOLOR,
        cursor=CURSOR_HAND,
        bd=4,
        relief=tk.GROOVE,
        offrelief=tk.RAISED,
        #command=action_debug
    )

    label_replace_color = tk.Label(
        frame_inner,
        bg=BGCOLOR,
        text="color",
        anchor='c',
        fg="#000088"
    )
    
    radiobutton_replace_col1 = tk.Radiobutton(
        frame_inner,
        value = 1,
        width=2,
        indicatoron=0,
        variable=user_replace_color,
        bg=BGCOLOR,
        activebackground="#000000",
        selectcolor="#000000",
        cursor=CURSOR_HAND,
        bd=4,
        relief=tk.GROOVE,
        offrelief=tk.RAISED,
        #command=action_debug
    )
    
    radiobutton_replace_col2 = tk.Radiobutton(
        frame_inner,
        value = 2,
        width=2,
        indicatoron=0,
        variable=user_replace_color,
        bg=BGCOLOR,
        activebackground="#000000",
        selectcolor="#000000",
        cursor=CURSOR_HAND,
        bd=4,
        relief=tk.GROOVE,
        offrelief=tk.RAISED,
        #command=action_debug
    )
    
    radiobutton_replace_col3 = tk.Radiobutton(
        frame_inner,
        value = 3,
        width=2,
        indicatoron=0,
        variable=user_replace_color,
        bg=BGCOLOR,
        activebackground="#000000",
        selectcolor="#000000",
        cursor=CURSOR_HAND,
        bd=4,
        relief=tk.GROOVE,
        offrelief=tk.RAISED,
        #command=action_debug
    )
    radiobutton_replace_bg = tk.Radiobutton(
        frame_inner,
        value = 0,
        width=2,
        indicatoron=0,
        variable=user_replace_color,
        bg=BGCOLOR,
        activebackground="#000000",
        selectcolor="#000000",
        cursor=CURSOR_HAND,
        bd=4,
        relief=tk.GROOVE,
        offrelief=tk.RAISED,
        #command=action_debug
    )
    

    #placement in grid
    label_none.grid(
        row=1,
        column=0,
        sticky=tk.W+tk.E
    )
    radiobutton_used_color_none.grid(
        row=1,
        column=1,
        sticky=tk.W+tk.E,
        columnspan=4
    )

    label_replace_color.grid(
        row=2,
        column=0,
        sticky=tk.W+tk.E
    )
    radiobutton_replace_col1.grid(
        row=2,
        column=1,
        sticky=tk.W+tk.E
    )
    radiobutton_replace_col2.grid(
        row=2,
        column=2,
        sticky=tk.W+tk.E
    )
    radiobutton_replace_col3.grid(
        row=2,
        column=3,
        sticky=tk.W+tk.E
    )
    radiobutton_replace_bg.grid(
        row=2,
        column=4,
        sticky=tk.W+tk.E
    )



def create_gui_current_color (
	root,
    _row,
    _column
) :
    global radiobutton_current_bg, radiobutton_current_col1, radiobutton_current_col2, radiobutton_current_col3

    frame_border = tk.Frame(
        root,
        bd=_bd,
    )
    frame_border.configure(background=BGCOLOR)
    frame_border.grid(
        row=_row,
        column=_column
    )
    frame_inner = tk.Frame(
        frame_border,
        bd=1,
        padx = _padx,
        pady = _pady,
        relief=tk.RAISED
        )
    frame_inner.configure(background=BGCOLOR)
    frame_inner.grid()
    frame_inner.grid_columnconfigure(0, weight=1)
    frame_inner.grid_rowconfigure(0, weight=1)

    

    #current color
    label_current_color = tk.Label(
        frame_inner,
        bg=BGCOLOR,
        text="block",
        anchor='c',
        fg="#000088"
    )
    
    radiobutton_current_col1 = tk.Radiobutton(
        frame_inner,
        value = 1,
        width=2,
        indicatoron=0,
        state=tk.DISABLED,
        variable=current_color,
        background="#000000",
        activebackground="#000000",
        selectcolor="#000000",
        bd=4,
        relief=tk.GROOVE,
        offrelief=tk.RAISED,
        #command=action_debug
    )
    
    radiobutton_current_col2 = tk.Radiobutton(
        frame_inner,
        value = 2,
        width=2,
        indicatoron=0,
        state=tk.DISABLED,
        variable=current_color,
        background="#000000",
        activebackground="#000000",
        selectcolor="#000000",
        bd=4,
        relief=tk.GROOVE,
        offrelief=tk.RAISED,
        #command=action_debug
    )
    
    radiobutton_current_col3 = tk.Radiobutton(
        frame_inner,
        value = 3,
        width=2,
        indicatoron=0,
        state=tk.DISABLED,
        variable=current_color,
        background="#000000",
        activebackground="#000000",
        selectcolor="#000000",
        bd=4,
        relief=tk.GROOVE,
        offrelief=tk.RAISED,
        #command=action_debug
    )
    radiobutton_current_bg = tk.Radiobutton(
        frame_inner,
        value = 0,
        width=2,
        indicatoron=0,
        state=tk.DISABLED,
        variable=current_color,
        background="#000000",
        activebackground="#000000",
        selectcolor="#000000",
        bd=4,
        relief=tk.GROOVE,
        offrelief=tk.RAISED,
        #command=action_debug
    )



    

    #placement in grid
    label_current_color.grid(
        row=0,
        column=0,
        sticky=tk.W+tk.E
    )
    radiobutton_current_col1.grid(
        row=0,
        column=1,
        sticky=tk.W+tk.E
    )
    radiobutton_current_col2.grid(
        row=0,
        column=2,
        sticky=tk.W+tk.E
    )
    radiobutton_current_col3.grid(
        row=0,
        column=3,
        sticky=tk.W+tk.E
    )
    radiobutton_current_bg.grid(
        row=0,
        column=4,
        sticky=tk.W+tk.E
    )





def create_gui_color_left (
	root,
    _row,
    _column
) :
    frame_border = tk.Frame(
        root,
        bd=_bd,
        bg=BGCOLOR
    )
    frame_border.grid(
        row=_row,
        column=_column
    )
    frame_inner = tk.Frame(
        frame_border,
        bd=1,
        bg=BGCOLOR,
        padx = _padx,
        pady = _pady,
        relief=tk.RAISED
        )
    frame_inner.grid()
    frame_inner.grid_columnconfigure(0, weight=1)
    frame_inner.grid_rowconfigure(0, weight=1)

    _row = 0
    label = tk.Label(
        frame_inner,
        text="left",
        anchor="c",
        justify='left',
        bg=BGCOLOR,
        fg="#000088"
    )
    label.grid(
        row=_row,
        column=1,
        sticky=tk.W+tk.E,
        columnspan=8
    )

    MODES = [
            ("black", 		 0, 0,0),	#text,value,row,column
            ("white",		 1, 0,1),
            ("red",			 2, 0,2),
            ("cyan",		 3, 0,3),
            ("purple",		 4, 0,4),
            ("green",		 5, 0,5),
            ("blue",		 6, 0,6),
            ("yellow",		 7, 0,7),
            ("orange",		 8, 1,0),
            ("brown",		 9, 1,1),
            ("light red",	10, 1,2),
            ("dark gray",	11, 1,3),
            ("gray", 		12, 1,4),
            ("light green",	13, 1,5),
            ("light blue",	14, 1,6),
            ("light gray",	15, 1,7),
    ]

    for text, value, my_row, my_column in MODES:
        mycolor = '#%02x%02x%02x' % (
            PALETTEDATA_PEPTO[(value*3)+0],
            PALETTEDATA_PEPTO[(value*3)+1],
            PALETTEDATA_PEPTO[(value*3)+2]
        )
        radiobutton_user_value = tk.Radiobutton(
            frame_inner,
            value = value,
            width=2,
            indicatoron=0,
            variable=user_drawcolor_left,
            background=mycolor,
            activebackground=mycolor,
            selectcolor=mycolor,
            cursor=CURSOR_HAND,
            bd=4,
            relief=tk.GROOVE,
            offrelief=tk.RAISED,
            #command=action_debug
        )
        radiobutton_user_value.grid(
            row=2+my_row,
            column=my_column,
            sticky=tk.W+tk.E
        )

def create_gui_color_right (
	root,
    _row,
    _column
) :
    frame_border = tk.Frame(
        root,
        bd=_bd,
    )
    frame_border.configure(background=BGCOLOR)
    frame_border.grid(
        row=_row,
        column=_column
    )
    frame_inner = tk.Frame(
        frame_border,
        bd=1,
        bg=BGCOLOR,
        padx = _padx,
        pady = _pady,
        relief=tk.RAISED
        )
    frame_inner.grid()
    frame_inner.grid_columnconfigure(0, weight=1)
    frame_inner.grid_rowconfigure(0, weight=1)

    _row = 0
    label = tk.Label(
        frame_inner,
        bg=BGCOLOR,
        text="right",
        anchor="c",
        justify='left',
        fg="#000088"
    )
    label.grid(
        row=_row,
        column=1,
        sticky=tk.W+tk.E,
        columnspan=8
    )

    MODES = [
            ("black", 		 0, 0,0),	#text,value,row,column
            ("white",		 1, 0,1),
            ("red",			 2, 0,2),
            ("cyan",		 3, 0,3),
            ("purple",		 4, 0,4),
            ("green",		 5, 0,5),
            ("blue",		 6, 0,6),
            ("yellow",		 7, 0,7),
            ("orange",		 8, 1,0),
            ("brown",		 9, 1,1),
            ("light red",	10, 1,2),
            ("dark gray",	11, 1,3),
            ("gray", 		12, 1,4),
            ("light green",	13, 1,5),
            ("light blue",	14, 1,6),
            ("light gray",	15, 1,7),
    ]

    for text, value, my_row, my_column in MODES:
        mycolor = '#%02x%02x%02x' % (
            PALETTEDATA_PEPTO[(value*3)+0],
            PALETTEDATA_PEPTO[(value*3)+1],
            PALETTEDATA_PEPTO[(value*3)+2]
        )
        radiobutton_user_value = tk.Radiobutton(
            frame_inner,
            value = value,
            width=2,
            indicatoron=0,
            variable=user_drawcolor_right,
            background=mycolor,
            activebackground=mycolor,
            selectcolor=mycolor,
            cursor=CURSOR_HAND,
            bd=4,
            relief=tk.GROOVE,
            offrelief=tk.RAISED,
            #command=action_convert
        )
        radiobutton_user_value.grid(
            row=2+my_row,
            column=my_column,
            sticky=tk.W+tk.E
        )




def create_gui_about () :

    def close_window():
        global about_window
        global about_window_open
        
        if (about_window_open == True) :
            about_window.destroy()
            about_window_open = False

    def close_window_key(self):
        close_window()


    global about_window
    global about_window_open
    if (about_window_open == True) : return None
    about_window_open = True

    _padx = 10
    _pady = 10
    
	#http://effbot.org/tkbook/toplevel.htm
    about_window = tk.Toplevel(
        bd=10
    )
    about_window.title("About")
    about_window.iconphoto(False, tk.PhotoImage(file=RES_GFX_ICON))
    about_window.protocol("WM_DELETE_WINDOW", close_window)
    about_window.bind("<Escape>", close_window_key)
    about_window.configure(background=BGCOLOR)
    about_window.resizable(0, 0)


    #top
    frame_top = tk.Frame( about_window)
    frame_top.grid(
        row=0,
        column=0,
        sticky=tk.N
    )

    #label with image: http://effbot.org/tkbook/photoimage.htm
    photo = tk.PhotoImage(file=RES_GFX_LOGO)
    label_logo = tk.Label(
        frame_top,
        bg=BGCOLOR,
        bd=0,
        image=photo,
        padx=0,
        pady=0
    )
    label_logo.image = photo # keep a reference!

    label_version = tk.Label(
        frame_top,
        bg=BGCOLOR,
        bd=0,
        text="build "+VERSION,
        padx=0,
        pady=0
    )

    label_logo.grid(
        row=0,
        column=0,
        sticky=tk.W+tk.S+tk.W+tk.E
    )

    label_version.grid(
        row=1,
        column=0,
        sticky=tk.W+tk.S+tk.W+tk.E
    )




    #bottom
    frame_bottom = tk.Frame( about_window)
    frame_bottom.configure(background=BGCOLOR)
    frame_bottom.grid(
        row=1,
        column=0,
        sticky=tk.S
    )

    # right frame
    frame_right = tk.Frame( frame_bottom)
    frame_right.grid(
        row=0,
        column=1,
        sticky=tk.W
    )

    #http://effbot.org/tkbook/message.htm
    msg = tk.Text(
        frame_right,
        bg=TEXTBOXCOLOR,
#        bd=10,
        relief=tk.FLAT,
        width=80,
        height=30
    )

    #scrollbar
    msg_scrollBar = tk.Scrollbar(
        frame_right,
        bg=BGCOLOR,
    )
    msg_scrollBar.config(command=msg.yview)
    msg.config(yscrollcommand=msg_scrollBar.set)
    msg.insert(tk.END, open(RES_DOC_ABOUT, encoding="utf_8").read())
    msg.config(state=tk.DISABLED)

    #placement in grid
    msg.grid(
        row=0,
        column=0,
        sticky=tk.W
    )
    msg_scrollBar.grid(
        row=0,
        column=1,
        sticky=tk.N+tk.S
    )




    # left frame
    frame_left = tk.Frame( frame_bottom)
    frame_left.grid(
        row=0,
        column=0,
        sticky=tk.W
    )

    #label with image: http://effbot.org/tkbook/photoimage.htm
    photo = tk.PhotoImage(file=RES_GFX_ABOUT)
    label_image = tk.Label(
        frame_left,
        bg=BGCOLOR,
#        bd=10,
        image=photo,
        padx=_padx,
        pady=_pady
    )
    label_image.image = photo # keep a reference!


    #button
    button = tk.Button(
        frame_left,
        bg=BGCOLOR,
        activebackground=ACTIVECOLOR,
        text="OK",
        command=close_window,
        padx=_padx,
        pady=_pady,
        cursor=CURSOR_HAND,
    )

    #placement in grid
    label_image.grid(
        row=0,
        column=0,
        sticky=tk.W
    )
    button.grid(
        row=1,
        column=0,
        sticky=tk.W+tk.E
    )






def create_gui_help_from_menu () :
    create_gui_help(None)
    
def create_gui_help (self) :

    def close_window():
        global help_window
        global help_window_open
        
        if (help_window_open == True) :
            help_window.destroy()
            help_window_open = False

    def close_window_key(self):
        close_window()



    global help_window
    global help_window_open
    if (help_window_open == True) : return None
    help_window_open = True

    _padx = 10
    _pady = 10
    
	#http://effbot.org/tkbook/toplevel.htm
    help_window = tk.Toplevel(bd=10)
    help_window.title("Help")
    help_window.iconphoto(False, tk.PhotoImage(file=RES_GFX_ICON))
    help_window.protocol("WM_DELETE_WINDOW", close_window)
    help_window.bind("<Escape>", close_window_key)
    help_window.configure(background=BGCOLOR)
    help_window.resizable(0, 0)

    # right frame
    frame_right = tk.Frame( help_window)
    frame_right.grid(
        row=0,
        column=1,
        sticky=tk.W+tk.E+tk.S+tk.N
    )

    #http://effbot.org/tkbook/message.htm
    msg = tk.Text(
        frame_right,
        bg=TEXTBOXCOLOR,
        relief=tk.FLAT,
        width=80,
        height=30
    )

    #scrollbar
    msg_scrollBar = tk.Scrollbar(frame_right)
    msg_scrollBar.config(command=msg.yview)
    msg.config(yscrollcommand=msg_scrollBar.set)
    msg.insert(tk.END, open(RES_DOC_HELP, encoding="utf_8").read())
    msg.config(state=tk.DISABLED)

    # placement in grid
    msg.grid(
        row=0,
        column=0,
        sticky=tk.W+tk.E+tk.S+tk.N
    )
    msg_scrollBar.grid(
        row=0,
        column=1,
        sticky=tk.W+tk.E+tk.S+tk.N
    )



    # left frame
    frame_left = tk.Frame( help_window)
    frame_left.grid(
        row=0,
        column=0,
        sticky=tk.W
    )

    #label with image: http://effbot.org/tkbook/photoimage.htm
    photo = tk.PhotoImage(file=RES_GFX_ICON)
    label_image = tk.Label(
        frame_left,
        bg=BGCOLOR,
#        bd=10,
        image=photo,
        padx=_padx,
        pady=_pady
    )
    label_image.image = photo # keep a reference!

    #button
    button = tk.Button(
        frame_left,
        bg=BGCOLOR,
        activebackground=ACTIVECOLOR,
        text="OK",
        command=close_window,
        padx=_padx,
        pady=_pady,
        cursor=CURSOR_HAND,
    )

    # placement in grid
    label_image.grid(
        row=0,
        column=0,
        sticky=tk.W
    )
    button.grid(
        row=1,
        column=0,
        sticky=tk.W+tk.E
    )







def create_gui_preferences_from_menu () :
    create_gui_preferences(None)
    
def create_gui_preferences (self) :

    def close_window():
        global preferences_window
        global preferences_window_open
        
        if (preferences_window_open == True) :
            preferences_window.destroy()
            preferences_window_open = False

    def close_window_key(self):
        close_window()


    global preferences_window
    global preferences_window_open
    if (preferences_window_open == True) : return None
    preferences_window_open = True

    _padx = 10
    _pady = 10
    
	#http://effbot.org/tkbook/toplevel.htm
    preferences_window = tk.Toplevel(
        bd=10
    )
    preferences_window.title("Configure Settings")
    preferences_window.iconphoto(False, tk.PhotoImage(file=RES_GFX_ICON))
    preferences_window.protocol("WM_DELETE_WINDOW", close_window)
    preferences_window.bind("<Escape>", close_window_key)
    preferences_window.configure(background=BGCOLOR)
    preferences_window.resizable(0, 0)

    create_gui_preferences_palette(
        preferences_window,
        0,  #row
        0   #column
    )

    create_gui_preferences_startaddress(
        preferences_window,
        1,  #row
        0   #column
    )


    create_gui_preferences_editorsize(
        preferences_window,
        0,  #row
        1   #column
    )

    create_gui_preferences_previewsize(
        preferences_window,
        1,  #row
        1   #column
    )

    #button
    button = tk.Button(
        preferences_window,
        text="OK",
        bg=BGCOLOR,
        activebackground=ACTIVECOLOR,
        command=close_window,
        padx=_padx,
        pady=_pady,
        cursor=CURSOR_HAND,
    )
    button.grid(
        row=2,
        column=0,
        sticky=tk.N,
        columnspan=2
    )


    



def create_gui_preview_image_from_menu () :
    create_gui_preview_image(None)
    

    
    
def create_gui_preview_image (self) :

    def close_window():
        global preview_window
        global preview_window_open
        
        if (preview_window_open == True) :
            preview_window.destroy()
            preview_window_open = False

    global label_preview_image
    global preview_window
    global preview_window_open
    
    if (preview_window_open == True) :
        return None
    preview_window_open = True
        
    preview_window = tk.Toplevel(bd=10)
    preview_window.title("preview")
    preview_window.protocol("WM_DELETE_WINDOW", close_window)
    preview_window.iconphoto(False, tk.PhotoImage(file=RES_GFX_ICON))
    preview_window.configure(background=BGCOLOR)
    preview_window.resizable(0, 0)


    label_preview_image = tk.Label(
        preview_window,
        bg=BGCOLOR
    )

    label_preview_image.grid(
        row=0,
        column=0,
        sticky=tk.W+tk.E
    )

    label_preview_image.bind('<Button-1>', input_mouse_left_button_preview)
            
    action_image_refresh_show()

	

def create_drop_down_menu (
	root
) :    
    menu = tk.Menu(root)
    root.config(menu=menu)

    filemenu = tk.Menu(menu, tearoff=0)
    filemenu.add_command(label="new", command=draw_new_image)
    filemenu.add_separator()
    filemenu.add_command(label="open...", command=action_OpenFile_from_menu, underline=0, accelerator="Control+o")
    filemenu.add_command(label="save...", command=action_SaveFile_from_menu, underline=0, accelerator="Control+s")
    filemenu.add_separator()
    filemenu.add_command(label="preferences", command=create_gui_preferences_from_menu, underline=0, accelerator="Control+p")
    filemenu.add_command(label="show preview", command=create_gui_preview_image_from_menu)
    filemenu.add_separator()
    filemenu.add_command(label="quit", command=root.quit, underline=0, accelerator="Control+q")

    editmenu = tk.Menu(menu, tearoff=0)
    editmenu.add_command(label="undo", command=undo_undo_from_menu, accelerator="Ctrl+z")
    editmenu.add_separator()
    editmenu.add_command(label="marker", command=marker_select_from_menu, underline=0, accelerator="m")
    editmenu.add_separator()
    editmenu.add_command(label="cut", command=buffer_cut_from_menu, accelerator="Ctrl+x")
    editmenu.add_command(label="copy", command=buffer_copy_from_menu, accelerator="Ctrl+c")
    #editmenu.add_command(label="paste", command=buffer_paste_from_menu, accelerator="Ctrl+v")

    infomenu = tk.Menu(menu, tearoff=0)
    infomenu.add_command(label="about", command=create_gui_about)
    infomenu.add_command(label="help", command=create_gui_help_from_menu, underline=0, accelerator="Control+h")

    #add all menus
    menu.add_cascade(label="File", menu=filemenu)
    menu.add_cascade(label="Edit", menu=editmenu)
    menu.add_cascade(label="Info", menu=infomenu)



def create_gui_info (
	root,
    _row,
    _column
) :
    
    frame_border = tk.Frame(
        root,
        bg=BGCOLOR,
        bd=_bd,
    )
    frame_border.grid(
        row=_row,
        column=_column
    )
    frame_inner = tk.Frame(
        frame_border,
        bg=BGCOLOR,
        bd=1,
        padx = _padx,
        pady = _pady,
        relief=tk.RAISED
        )
    frame_inner.grid()
    frame_inner.grid_columnconfigure(0, weight=1)
    frame_inner.grid_rowconfigure(0, weight=1)
    

    #cursor
    label_title_cursor = tk.Label(
        frame_inner,
        bg=BGCOLOR,
        text="position:",
        anchor='ne',
        fg="#000088"
    )
    label_cursor_posx = tk.Label(
        frame_inner,
        bg=BGCOLOR,
        textvariable = cursorx_variable,
        anchor='c'
    )
    label_cursor_posy = tk.Label(
        frame_inner,
        bg=BGCOLOR,
        textvariable = cursory_variable,
        anchor='c'
    )
    
    #block
    label_title_block = tk.Label(
        frame_inner,
        bg=BGCOLOR,
        text="block:",
        anchor='ne',
        fg="#000088"
    )
    label_block_posx = tk.Label(
        frame_inner,
        bg=BGCOLOR,
        textvariable = blockx_variable,
        anchor='c'
    )
    label_block_posy = tk.Label(
        frame_inner,
        bg=BGCOLOR,
        textvariable = blocky_variable,
        anchor='c'
    )

    #undo
    label_title_undo = tk.Label(
        frame_inner,
        bg=BGCOLOR,
        text="undo steps:",
        anchor='ne',
        fg="#000088"
    )
    label_undo = tk.Label(
        frame_inner,
        bg=BGCOLOR,
        textvariable = undo_variable,
        anchor='c'
    )

    
    #placement in grid layout
    label_title_cursor.grid(
        row=0,
        column=0,
        sticky=tk.W+tk.E
    )
    label_cursor_posx.grid(
        row=0,
        column=1,
        sticky=tk.W+tk.E
    )
    label_cursor_posy.grid(
        row=0,
        column=2,
        sticky=tk.W+tk.E
    )

    label_title_block.grid(
        row=1,
        column=0,
        sticky=tk.W+tk.E
    )
    label_block_posx.grid(
        row=1,
        column=1,
        sticky=tk.W+tk.E
    )
    label_block_posy.grid(
        row=1,
        column=2,
        sticky=tk.W+tk.E
    )


    label_title_undo.grid(
        row=2,
        column=0,
        sticky=tk.W+tk.E
    )
    label_undo.grid(
        row=2,
        column=1,
        sticky=tk.W+tk.E,
        columnspan=2
    )




def create_gui_top (
	root,
    _row,
    _column
) :
    frame_border = tk.Frame(
        root,
        bd=_bd,
        bg=BGCOLOR
    )
    frame_border.grid(
        row=_row,
        column=_column
    )

    photo = tk.PhotoImage(file=RES_GFX_AC)
    label_logo = tk.Label(frame_border, image = photo)
    label_logo.image = photo # keep a reference!
    label_logo.grid( row=0, column=0)
    label_logo.configure(background=BGCOLOR)



def create_gui_editor_image (
	root,
    _row,
    _column
) :
    global label_editor_image
    
    #creation of elements
    label_editor_image = tk.Label(
        root,
        bg=BGCOLOR,
        cursor=CURSOR_EDIT,
    )
    
    #placement in grid layout
    label_editor_image.grid(
        row=0,
        column=0,
        padx=0,
        pady=0,
        ipadx=0,
        ipady=0
    )


    # mouse wheel
    #   (Windows)
    label_editor_image.bind('<MouseWheel>' ,input_mouse_wheel)
    #   (Linux)
    label_editor_image.bind('<Button-4>' ,input_mouse_wheel)
    label_editor_image.bind('<Button-5>' ,input_mouse_wheel)
    # mouse wheel-button
    label_editor_image.bind('<Motion>', input_mouse_motion_edit_window)
    # mouse buttons
    label_editor_image.bind('<Button-1>', input_mouse_left_button_editor)
    label_editor_image.bind('<B1-Motion>', input_mouse_left_button_editor)

    #https://docs.python.org/3/library/platform.html
    #platform.system() : 'Linux', 'Darwin', 'Java', 'Windows'
    if (operating_system == 'Darwin') :
        #darwin macos
        label_editor_image.bind('<Button-3>', input_mouse_middle_button_press)
        label_editor_image.bind('<ButtonRelease-3>', input_mouse_middle_button_release)
        label_editor_image.bind('<B3-Motion>', input_mouse_middle_button_motion)
        label_editor_image.bind('<Button-2>', input_mouse_right_button)
        label_editor_image.bind('<B2-Motion>', input_mouse_right_button)
    else :
        #linux and windows
        label_editor_image.bind('<Button-2>', input_mouse_middle_button_press)
        label_editor_image.bind('<ButtonRelease-2>', input_mouse_middle_button_release)
        label_editor_image.bind('<B2-Motion>', input_mouse_middle_button_motion)
        label_editor_image.bind('<Button-3>', input_mouse_right_button)
        label_editor_image.bind('<B3-Motion>', input_mouse_right_button)



def user_set_drawcolor_left(number):
    if (number==0) : user_drawcolor_left.set(used_color_bg.get()); return None
    if (number==1) : user_drawcolor_left.set(used_color_col1.get()); return None
    if (number==2) : user_drawcolor_left.set(used_color_col2.get()); return None
    if (number==3) : user_drawcolor_left.set(used_color_col3.get()); return None

def user_set_drawcolor_right(number):
    if (number==0) : user_drawcolor_right.set(used_color_bg.get()); return None
    if (number==1) : user_drawcolor_right.set(used_color_col1.get()); return None
    if (number==2) : user_drawcolor_right.set(used_color_col2.get()); return None
    if (number==3) : user_drawcolor_right.set(used_color_col3.get()); return None

def keyboard_control_n(self):
    user_pencil.set("normal")
def keyboard_control_b(self):
    user_pencil.set("checkerboard")
def keyboard_control_d(self):
    user_pencil.set("xline")
def keyboard_control_y(self):
    user_pencil.set("yline")
def keyboard_control_l(self):
    user_pencil.set("light")
def keyboard_shift_f1(self):
    user_set_drawcolor_right(1)
def keyboard_shift_f2(self):
    user_set_drawcolor_right(2)
def keyboard_shift_f3(self):
    user_set_drawcolor_right(3)
def keyboard_shift_f4(self):
    user_set_drawcolor_right(0)

def keyboard_shift_f5(self):
    user_replace_color.set(1)
def keyboard_shift_f6(self):
    user_replace_color.set(2)
def keyboard_shift_f7(self):
    user_replace_color.set(3)
def keyboard_shift_f8(self):
    user_replace_color.set(0)



#keyboard shortcuts
def keyboard_quit(self):
    root.quit()
#def keyboard_space(self):
#    global space_pressed
#    if (str(my_focus) == ".!frame.!frame.!frame.!label2") :
#        space_pressed = True
#        #print("space")

def scroll_right(self):
    global editorimage_posx
    editorimage_posx -= 1
    action_image_refresh_show()
    update_infos()
def scroll_left(self):
    global editorimage_posx
    editorimage_posx += 1
    action_image_refresh_show()
    update_infos()
def scroll_down(self):
    global editorimage_posy
    editorimage_posy -= 1
    action_image_refresh_show()
    update_infos()
def scroll_up(self):
    global editorimage_posy
    editorimage_posy += 1
    action_image_refresh_show()
    update_infos()

def keyboard_all(event):
    switcher = {
        'm' : (marker_select,0),
        'space' : (user_replace_color.set,99),
        'F1' : (user_set_drawcolor_left,1),
        'F2' : (user_set_drawcolor_left,2),
        'F3' : (user_set_drawcolor_left,3),
        'F4' : (user_set_drawcolor_left,0),
        'F5' : (user_replace_color.set,1),
        'F6' : (user_replace_color.set,2),
        'F7' : (user_replace_color.set,3),
        'F8' : (user_replace_color.set,0),
        '0' : (user_drawcolor_left.set,0),
        '1' : (user_drawcolor_left.set,1),
        '2' : (user_drawcolor_left.set,2),
        '3' : (user_drawcolor_left.set,3),
        '4' : (user_drawcolor_left.set,4),
        '5' : (user_drawcolor_left.set,5),
        '6' : (user_drawcolor_left.set,6),
        '7' : (user_drawcolor_left.set,7),
        '8' : (user_drawcolor_left.set,8),
        '9' : (user_drawcolor_left.set,9),
        'a' : (user_drawcolor_left.set,10),
        'b' : (user_drawcolor_left.set,11),
        'c' : (user_drawcolor_left.set,12),
        'd' : (user_drawcolor_left.set,13),
        'e' : (user_drawcolor_left.set,14),
        'f' : (user_drawcolor_left.set,15),
        'equal' : (user_drawcolor_right.set,0),
        'exclam' : (user_drawcolor_right.set,1),
        'quotedbl' : (user_drawcolor_right.set,2),
        'section' : (user_drawcolor_right.set,3),
        'dollar' : (user_drawcolor_right.set,4),
        'percent' : (user_drawcolor_right.set,5),
        'ampersand' : (user_drawcolor_right.set,6),
        'slash' : (user_drawcolor_right.set,7),
        'parenleft' : (user_drawcolor_right.set,8),
        'parenright' : (user_drawcolor_right.set,9),
        'A' : (user_drawcolor_right.set,10),
        'B' : (user_drawcolor_right.set,11),
        'C' : (user_drawcolor_right.set,12),
        'D' : (user_drawcolor_right.set,13),
        'E' : (user_drawcolor_right.set,14),
        'F' : (user_drawcolor_right.set,15),
        'minus' : (zoom_out,0),
        'plus' : (zoom_in,0),
        'Left' : (scroll_right,0),
        'Right' : (scroll_left,0),
        'Up' : (scroll_down,0),
        'Down' : (scroll_up,0),
    }
    
    val = switcher.get(event.keysym)

    #if (val == None) : print ('unknown key: char=\"'+event.char+'\" keysym=\"'+event.keysym+'\" num=\"'+event.num+'\"')
    if (val != None) : val[0](val[1])
    


def create_gui_main ():
    frame_top = tk.Frame(root, bg=BGCOLOR)
    frame_top.grid(
        row=0,
        column=0,
        padx=0,
        pady=0,
        ipadx=0,
        ipady=0,
    )
    frame_top.grid_columnconfigure(0, weight=1)
    frame_top.grid_rowconfigure(0, weight=1)

    #frame_top elements
    create_gui_top(
        frame_top,
        0,
        0
    )



    frame_bottom = tk.Frame(root, bg=BGCOLOR)
    frame_bottom.grid(
        row=1,
        column=0,
        sticky=tk.N,
        padx=0,
        pady=0,
        ipadx=0,
        ipady=0,
    )
    frame_bottom.grid_columnconfigure(0, weight=1)
    frame_bottom.grid_rowconfigure(0, weight=1)

    frame_left = tk.Frame(frame_bottom, bg=BGCOLOR)
    frame_left.grid(
        row=0,
        column=0,
        sticky=tk.N,
        padx=0,
        pady=0,
        ipadx=0,
        ipady=0,

    )
    frame_left.grid_columnconfigure(0, weight=0)
    frame_left.grid_rowconfigure(0, weight=0)

    frame_right = tk.Frame(frame_bottom, bg=BGCOLOR)
    frame_right.grid(
        row=0,
        column=1,
        sticky=tk.N,
        padx=0,
        pady=0,
        ipadx=0,
        ipady=0,
    )
    frame_right.grid_columnconfigure(0, weight=1)
    frame_right.grid_rowconfigure(0, weight=1)

    #frame_left elements
    create_gui_editor_image(
        frame_left,
        0,
        0
    )

    #frame_right elements

    create_gui_drawmode(
        frame_right,
        0,  #row
        0   #column
    )

    create_gui_replace_color(
        frame_right,
        1,  #row
        0   #column
    )


    create_gui_pencil(
        frame_right,
        2,  #row
        0   #column
    )

    create_gui_current_color(
        frame_right,
        3,  #row
        0   #column
    )

    create_gui_color_left(
        frame_right,
        4,  #row
        0   #column
    )

    create_gui_color_right(
        frame_right,
        5,  #row
        0   #column
    )

    create_gui_info (
        frame_right,
        6,  #row
        0   #column
    )
    

def _main_procedure() :
    print("%s [build %s] *** by WolF"% (PROGNAME, VERSION))

    #print(RES_GFX_ICON)
    #while (1==1) :
    #    a=1

    root.configure(background=BGCOLOR)
    root.grid_columnconfigure(0, weight=10)
    root.grid_rowconfigure(0, weight=10)
    set_title()
    root.iconphoto(False, tk.PhotoImage(file=RES_GFX_ICON))


    create_drop_down_menu(root)
    create_gui_main()
    create_gui_preview_image(None)

    root.config(cursor=CURSOR_NOTHING)

    root.bind_all("<Key>", keyboard_all)
    root.bind_all("<Control-b>", keyboard_control_b)
    root.bind_all("<Control-c>", buffer_copy)
    root.bind_all("<Control-d>", keyboard_control_d)
    root.bind_all("<Control-h>", create_gui_help)
    root.bind_all("<Control-n>", keyboard_control_n)
    root.bind_all("<Control-l>", keyboard_control_l)
    root.bind_all("<Control-p>", create_gui_preferences)
    root.bind_all("<Control-q>", keyboard_quit)
    root.bind_all("<Control-o>", action_OpenFile)
    root.bind_all("<Control-s>", action_SaveFile)
    root.bind_all("<Control-v>", buffer_paste)
    root.bind_all("<Control-x>", buffer_cut)
    root.bind_all("<Control-y>", keyboard_control_y)
    root.bind_all("<Control-z>", undo_undo)
    root.bind_all("<Shift-F1>", keyboard_shift_f1)
    root.bind_all("<Shift-F2>", keyboard_shift_f2)
    root.bind_all("<Shift-F3>", keyboard_shift_f3)
    root.bind_all("<Shift-F4>", keyboard_shift_f4)

    draw_grids()
    draw_background()
    
    if (len(sys.argv) == 2) :
        loadFile(sys.argv[1])
    else :
        #loadFile(resource_path('new.koa'))
        draw_new_image()
        
    root_refresh()
    tk.mainloop()



if __name__ == '__main__':
    _main_procedure()
