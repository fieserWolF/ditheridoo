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



def _main_procedure() :
    print("%s %s *** by WolF"% (myGlobals.PROGNAME, myGlobals.VERSION))

    #https://docs.python.org/3/library/argparse.html
    parser = argparse.ArgumentParser(
        description='Ditheridoo is a multicolor bitmap editor for Commodore 64.',
        epilog='Example: '+sys.argv[0]+' -i image.koa'
    )
    parser.add_argument('-i', '--image', dest='image_filename', help='koala image filename')
    #parser.add_argument('-p', '--petscii_file', dest='petscii_filename', help='petscii filename (.json)')
    #parser.add_argument('-c', '--config_file', dest='config_filename', help='name of configuration file (.json) default: "'+myGlobals.RES_CONFIG+'"', default=myGlobals.RES_CONFIG)
    #parser.add_argument('-f', '--font_file', dest='font_filename', help='name of font (2048 bytes) default: "'+myGlobals.CHARROM_UPPERCASE+'"', default=myGlobals.CHARROM_UPPERCASE)
    myGlobals.args = parser.parse_args()


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


    if (myGlobals.args.image_filename) :
        action.loadFile(myGlobals.args.image_filename)
    else :
        #loadFile(resource_path('new.koa'))
        action.draw_new_image()
        
    action.root_refresh()
    tk.mainloop()



if __name__ == '__main__':
    _main_procedure()
