import code.myGlobals as myGlobals
import code.action as action

import tkinter as tk







def create_gui_preview_image_from_menu () :
    create_gui_preview_image(None)
    

    
    
def create_gui_preview_image (self) :

    def close_window():
        #global preview_window
        #global preview_window_open
        
        if (myGlobals.preview_window_open == True) :
            myGlobals.preview_window.destroy()
            myGlobals.preview_window_open = False

    #global label_preview_image
    #global preview_window
    #global preview_window_open
    
    if (myGlobals.preview_window_open == True) :
        return None
    myGlobals.preview_window_open = True
        
    myGlobals.preview_window = tk.Toplevel(bd=10)
    myGlobals.preview_window.title("preview")
    myGlobals.preview_window.protocol("WM_DELETE_WINDOW", close_window)
    myGlobals.preview_window.iconphoto(False, tk.PhotoImage(file=myGlobals.RES_GFX_ICON))
    myGlobals.preview_window.configure(background=myGlobals.BGCOLOR)
    myGlobals.preview_window.resizable(0, 0)


    myGlobals.label_preview_image = tk.Label(
        myGlobals.preview_window,
        bg=myGlobals.BGCOLOR
    )

    myGlobals.label_preview_image.grid(
        row=0,
        column=0,
        sticky=tk.W+tk.E
    )

    myGlobals.label_preview_image.bind('<Button-1>', input_mouse_left_button_preview)
            
    action.action_image_refresh_show()




def input_mouse_left_button_preview(event):
    #global mouse_posx, mouse_posy
    myGlobals.mouse_posx, myGlobals.mouse_posy = event.x, event.y
    update_infos_preview()
    zoom_perform()
    action.action_image_refresh_show()
