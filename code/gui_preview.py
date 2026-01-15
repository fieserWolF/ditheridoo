import code.myGlobals as myGlobals
import code.action as action
import tkinter

    
def create_gui_preview_image () :

    def close_window():
        #writes: myGlobals.preview_window
        #writes: myGlobals.preview_window_open
        
        if (myGlobals.preview_window_open == True) :
            myGlobals.preview_window.destroy()
            myGlobals.preview_window_open = False

    #writes: myGlobals.canvas_preview
    #writes: myGlobals.preview_window
    #writes: myGlobals.preview_window_open
    
    if (myGlobals.preview_window_open == True) :
        return None
    myGlobals.preview_window_open = True
        
    myGlobals.preview_window = tkinter.Toplevel(bd=10)
    myGlobals.preview_window.title("preview")
    myGlobals.preview_window.protocol("WM_DELETE_WINDOW", close_window)
    myGlobals.preview_window.iconphoto(False, tkinter.PhotoImage(file=myGlobals.RES_GFX_ICON))
    myGlobals.preview_window.configure(background=myGlobals.BGCOLOR)
    myGlobals.preview_window.resizable(0, 0)
    #myGlobals.preview_window.resizable(1, 1)

    photo = tkinter.PhotoImage()

    myGlobals.label_preview_image = tkinter.Label(myGlobals.preview_window, width=myGlobals.preview_width, height=myGlobals.preview_height, background="#000000")
    #myGlobals.canvas_preview = tkinter.Canvas(myGlobals.preview_window, width=myGlobals.preview_width, height=myGlobals.preview_height, background="#000000")
    #myGlobals.canvas_preview.delete("all")
    
    #https://anzeljg.github.io/rin2/book2/2405/docs/tkinter/create_rectangle.html
    #myGlobals.canvas_draw.create_rectangle(0, 0, myGlobals.FULL_SCREEN_WIDTH, myGlobals.FULL_SCREEN_HEIGHT, fill='#000000', tags='border')
    
    #https://anzeljg.github.io/rin2/book2/2405/docs/tkinter/create_image.html
    #myGlobals.canvas_preview.create_image(0, 0, image=myGlobals.preview_image, anchor=tkinter.NW, tags='preview_image')

    #myGlobals.canvas_preview.create_image(1, 1, anchor=tkinter.NW, tags='preview_image')
    #myGlobals.label_preview.create_image(1, 1, anchor=tkinter.NW, tags='preview_image')

    myGlobals.label_preview_image = tkinter.Label(
        myGlobals.preview_window,
        bg=myGlobals.BGCOLOR,
        bd=0,
        image=photo,
        padx=0,
        pady=0
    )
    myGlobals.label_preview_image.image = photo # keep a reference!


    #myGlobals.canvas_preview.grid(
    myGlobals.label_preview_image.grid(
        row=0,
        column=0,
        sticky=tkinter.W+tkinter.E+tkinter.N+tkinter.S
    )
    #myGlobals.label_preview_image.grid_columnconfigure(0, weight=1)
    #myGlobals.label_preview_image.grid_rowconfigure(0, weight=1)

    myGlobals.label_preview_image.bind('<Button-1>', mouse_left_button_preview)
    #myGlobals.canvas_preview.bind('<Button-1>', mouse_left_button_preview)

    myGlobals.label_preview_image.bind('<Button-4>', mouse_wheel_preview)
    myGlobals.label_preview_image.bind('<Button-5>', mouse_wheel_preview)
            
    action.refresh_show()



def mouse_left_button_preview(event):
    #writes: myGlobals.global mouse_posx, myGlobals.mouse_posy
    myGlobals.mouse_posx, myGlobals.mouse_posy = event.x, event.y
    action.update_infos_preview()
    action.zoom_perform()
    action.refresh_show()


def mouse_wheel_preview(event):
    if (
        (event.num == 5) |
        (int(event.delta / 120) == -1) |
        (event.delta == -1)
    ) :
        #mouse wheel down
        action.zoom_preview_out(0)

    if (
        (event.num == 4) |
        (int(event.delta / 120) == 1) |
        (event.delta == 1)
    ) :
        #mouse wheel up
        action.zoom_preview_in(0)

