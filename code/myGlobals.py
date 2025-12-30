import os
import sys
import tkinter as tk
from PIL import ImageTk, ImageEnhance, ImageFilter, ImageDraw
import PIL.Image as PilImage    #we need another name, as it collides with tkinter.Image otherwise
import platform



#global constants
def _global_constants():
        return None


#https://stackoverflow.com/questions/48210090/how-to-use-bundled-program-after-pyinstaller-add-binary
def resource_path(relative_path):
    #Get absolute path to resource, works for dev and for PyInstaller
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)
    


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

RESOURCES_PATH = '../resources'

RES_VERSION = resource_path(RESOURCES_PATH+'/version.txt')
RES_GFX_ICON = resource_path(RESOURCES_PATH+'/icon.png')
RES_GFX_AC = resource_path(RESOURCES_PATH+'/ac.png')
RES_GFX_LOGO = resource_path(RESOURCES_PATH+'/logo.png')
RES_GFX_ABOUT = resource_path(RESOURCES_PATH+'/about.png')
RES_DOC_ABOUT = resource_path(RESOURCES_PATH+'/about.txt')
RES_DOC_HELP = resource_path(RESOURCES_PATH+'/help.txt')

VERSION = open(RES_VERSION, encoding="utf_8").read().rstrip()


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

special_modifier_pressed = False


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

args = []
