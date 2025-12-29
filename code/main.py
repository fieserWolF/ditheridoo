import code.myGlobals as myGlobals
import code.gui_about as gui_about
import code.gui_about as gui_help
import code.gui_preview as gui_preview
import code.gui_preferences as gui_preferences
import code.gui as gui
import code.action as action
import code.gui_help as gui_help
import code.gui_about as gui_about
import sys

import tkinter as tk
import argparse



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
"""



def _main_procedure() :
    print("%s %s *** by WolF"% (myGlobals.PROGNAME, myGlobals.VERSION))

    #print(RES_GFX_ICON)
    #while (1==1) :
    #    a=1

    myGlobals.root.configure(background=myGlobals.BGCOLOR)
    myGlobals.root.grid_columnconfigure(0, weight=10)
    myGlobals.root.grid_rowconfigure(0, weight=10)
    action.set_title()
    myGlobals.root.iconphoto(False, tk.PhotoImage(file=myGlobals.RES_GFX_ICON))


    gui.create_drop_down_menu(myGlobals.root)
    gui.create_gui_main()
    gui_preview.create_gui_preview_image(None)

    myGlobals.root.config(cursor=myGlobals.CURSOR_NOTHING)

    myGlobals.root.bind_all("<Key>", action.keyboard_all)
    myGlobals.root.bind_all("<Control-b>", action.keyboard_control_b)
    myGlobals.root.bind_all("<Control-c>", action.buffer_copy)
    myGlobals.root.bind_all("<Control-d>", action.keyboard_control_d)
    myGlobals.root.bind_all("<Control-h>", gui_help.create_gui_help)
    myGlobals.root.bind_all("<Control-n>", action.keyboard_control_n)
    myGlobals.root.bind_all("<Control-l>", action.keyboard_control_l)
    myGlobals.root.bind_all("<Control-p>", gui_preferences.create_gui_preferences)
    myGlobals.root.bind_all("<Control-q>", action.keyboard_quit)
    myGlobals.root.bind_all("<Control-o>", action.action_OpenFile)
    myGlobals.root.bind_all("<Control-s>", action.action_SaveFile)
    myGlobals.root.bind_all("<Control-v>", action.buffer_paste)
    myGlobals.root.bind_all("<Control-x>", action.buffer_cut)
    myGlobals.root.bind_all("<Control-y>", action.keyboard_control_y)
    myGlobals.root.bind_all("<Control-z>", action.undo_undo)
    myGlobals.root.bind_all("<Shift-F1>", action.keyboard_shift_f1)
    myGlobals.root.bind_all("<Shift-F2>", action.keyboard_shift_f2)
    myGlobals.root.bind_all("<Shift-F3>", action.keyboard_shift_f3)
    myGlobals.root.bind_all("<Shift-F4>", action.keyboard_shift_f4)
    myGlobals.root.bind( "<KeyPress-Meta_L>", action.keyboard_special_modifier_pressed )
    myGlobals.root.bind( "<KeyRelease-Meta_L>", action.keyboard_special_modifier_released )
    myGlobals.root.bind( "<KeyPress-Menu>", action.keyboard_special_modifier_pressed )
    myGlobals.root.bind( "<KeyRelease-Menu>", action.keyboard_special_modifier_released )
    myGlobals.root.bind( "<KeyPress-Super_L>", action.keyboard_special_modifier_pressed )
    myGlobals.root.bind( "<KeyRelease-Super_L>", action.keyboard_special_modifier_released )
    myGlobals.root.bind( "<KeyPress-Alt_L>", action.keyboard_special_modifier_pressed )
    myGlobals.root.bind( "<KeyRelease-Alt_L>", action.keyboard_special_modifier_released )
    #myGlobals.root.bind( "<KeyPress-Win_L>", action.keyboard_special_modifier_pressed )
    #myGlobals.root.bind( "<KeyRelease-Win_L>", action.keyboard_special_modifier_released )

    action.draw_grids()
    action.draw_background()
    
    if (len(sys.argv) == 2) :
        action.loadFile(sys.argv[1])
    else :
        #loadFile(resource_path('new.koa'))
        action.draw_new_image()
        
    action.root_refresh()
    tk.mainloop()



if __name__ == '__main__':
    _main_procedure()
