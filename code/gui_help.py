import code.myGlobals as myGlobals
import tkinter as tk





def create_gui_help_from_menu () :
    create_gui_help(None)
    
def create_gui_help (self) :

    TEXT_HEIGHT=30

    def close_window():
        #global help_window
        #global help_window_open
        
        if (myGlobals.help_window_open == True) :
            myGlobals.help_window.destroy()
            myGlobals.help_window_open = False

    def close_window_key(self):
        close_window()


    def keyboard_up(event):
        msg.yview_scroll(-1,"units")

    def keyboard_down(event):
        msg.yview_scroll(1,"units")

    def keyboard_pageup(event):
        msg.yview_scroll(TEXT_HEIGHT,"units")

    def keyboard_pagedown(event):
        msg.yview_scroll(TEXT_HEIGHT*-1,"units")


    #global help_window
    #global help_window_open
    if (myGlobals.help_window_open == True) : return None
    myGlobals.help_window_open = True

    _padx = 10
    _pady = 10
    
	#http://effbot.org/tkbook/toplevel.htm
    myGlobals.help_window = tk.Toplevel(bd=10)
    myGlobals.help_window.title("Help")
    myGlobals.help_window.iconphoto(False, tk.PhotoImage(file=myGlobals.RES_GFX_ICON))
    myGlobals.help_window.protocol("WM_DELETE_WINDOW", close_window)
    myGlobals.help_window.bind("<Escape>", close_window_key)
    myGlobals.help_window.configure(background=myGlobals.BGCOLOR)
    myGlobals.help_window.resizable(0, 0)

    # right frame
    frame_right = tk.Frame( myGlobals.help_window)
    frame_right.grid(
        row=0,
        column=1,
        sticky=tk.W+tk.E+tk.S+tk.N
    )

    #http://effbot.org/tkbook/message.htm
    msg = tk.Text(
        frame_right,
        bg=myGlobals.TEXTBOXCOLOR,
        relief=tk.FLAT,
        width=80,
        height=TEXT_HEIGHT
    )

    #scrollbar
    msg_scrollBar = tk.Scrollbar(frame_right)
    msg_scrollBar.config(command=msg.yview)
    msg.config(yscrollcommand=msg_scrollBar.set)
    msg.insert(tk.END, open(myGlobals.RES_DOC_HELP, encoding="utf_8").read())
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
    frame_left = tk.Frame( myGlobals.help_window)
    frame_left.grid(
        row=0,
        column=0,
        sticky=tk.W
    )

    #label with image: http://effbot.org/tkbook/photoimage.htm
    photo = tk.PhotoImage(file=myGlobals.RES_GFX_ICON)
    label_image = tk.Label(
        frame_left,
        bg=myGlobals.BGCOLOR,
#        bd=10,
        image=photo,
        padx=_padx,
        pady=_pady
    )
    label_image.image = photo # keep a reference!

    #button
    button = tk.Button(
        frame_left,
        bg=myGlobals.BGCOLOR,
        activebackground=myGlobals.ACTIVECOLOR,
        text="OK",
        command=close_window,
        padx=_padx,
        pady=_pady,
        cursor=myGlobals.CURSOR_HAND,
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

    myGlobals.help_window.bind('<Up>', keyboard_up) 
    myGlobals.help_window.bind('<Down>', keyboard_down) 
    myGlobals.help_window.bind('<Next>', keyboard_pageup) 
    myGlobals.help_window.bind('<Prior>', keyboard_pagedown) 


