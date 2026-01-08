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
import tkinter
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
    #myGlobals.root.grid_columnconfigure(0, weight=10)
    #myGlobals.root.grid_rowconfigure(0, weight=10)
    action.set_title()
    myGlobals.root.iconphoto(False, tkinter.PhotoImage(file=myGlobals.RES_GFX_ICON))
    myGlobals.root.resizable(0, 0)
    
    gui.create_drop_down_menu(myGlobals.root)
    gui.create_gui_main()
    gui_preview.create_gui_preview_image()

    myGlobals.root.config(cursor=myGlobals.CURSOR_NOTHING)
    myGlobals.root.bind_all("<Key>", action.keyboard_all)
    myGlobals.root.bind_all("<Control-c>", action.buffer_copy)
    myGlobals.root.bind_all("<Control-h>", gui_help.create_gui_help)
    myGlobals.root.bind_all("<Control-n>", lambda event: myGlobals.user_pencil.set("normal"))
    myGlobals.root.bind_all("<Control-l>", lambda event: myGlobals.user_pencil.set("light"))
    myGlobals.root.bind_all("<Control-d>", lambda event: myGlobals.user_pencil.set("xline"))
    myGlobals.root.bind_all("<Control-b>", lambda event: myGlobals.user_pencil.set("checkerboard"))
    myGlobals.root.bind_all("<Control-y>", lambda event: myGlobals.user_pencil.set("yline"))
    myGlobals.root.bind_all("<Control-p>", gui_preferences.create_gui_preferences)
    myGlobals.root.bind_all("<Control-q>", lambda event: myGlobals.root.quit())
    myGlobals.root.bind_all("<Control-o>", action.OpenFile)
    myGlobals.root.bind_all("<Control-s>", action.SaveFile)
    myGlobals.root.bind_all("<Control-v>", action.buffer_paste)
    myGlobals.root.bind_all("<Control-x>", action.buffer_cut)
    myGlobals.root.bind_all("<Control-z>", action.undo_undo)
    myGlobals.root.bind_all("<g>", lambda event: action.toggle_grid())
    myGlobals.root.bind_all("<Shift-F1>", lambda event: action.user_set_drawcolor_right(1))
    myGlobals.root.bind_all("<Shift-F2>", lambda event: action.user_set_drawcolor_right(2))
    myGlobals.root.bind_all("<Shift-F3>", lambda event: action.user_set_drawcolor_right(3))
    myGlobals.root.bind_all("<Shift-F4>", lambda event: action.user_set_drawcolor_right(0))
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
        action.refresh_prepare()
        
    action.root_refresh()

    #myGlobals.canvas_editor.itemconfigure('koala_image', image=myGlobals.tmp_photoimage, state='normal')
   
   
    tkinter.mainloop()



if __name__ == '__main__':
    _main_procedure()
