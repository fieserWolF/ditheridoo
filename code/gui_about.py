import code.myGlobals as myGlobals
import tkinter as tk



def create_gui_about () :

    TEXT_HEIGHT=30

    def close_window():
        #global about_window
        #global about_window_open
        
        if (myGlobals.about_window_open == True) :
            myGlobals.about_window.destroy()
            myGlobals.about_window_open = False

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

    #global about_window
    #global about_window_open
    if (myGlobals.about_window_open == True) : return None
    myGlobals.about_window_open = True

    _padx = 10
    _pady = 10
    
	#http://effbot.org/tkbook/toplevel.htm
    myGlobals.about_window = tk.Toplevel(
        bd=10
    )
    myGlobals.about_window.title("About")
    myGlobals.about_window.iconphoto(False, tk.PhotoImage(file=myGlobals.RES_GFX_ICON))
    myGlobals.about_window.protocol("WM_DELETE_WINDOW", close_window)
    myGlobals.about_window.bind("<Escape>", close_window_key)
    myGlobals.about_window.configure(background=myGlobals.BGCOLOR)
    myGlobals.about_window.resizable(0, 0)


    #top
    frame_top = tk.Frame( myGlobals.about_window)
    frame_top.grid(
        row=0,
        column=0,
        sticky=tk.N
    )

    #label with image: http://effbot.org/tkbook/photoimage.htm
    photo = tk.PhotoImage(file=myGlobals.RES_GFX_LOGO)
    label_logo = tk.Label(
        frame_top,
        bg=myGlobals.BGCOLOR,
        bd=0,
        image=photo,
        padx=0,
        pady=0
    )
    label_logo.image = photo # keep a reference!

    label_version = tk.Label(
        frame_top,
        bg=myGlobals.BGCOLOR,
        bd=0,
        text=myGlobals.VERSION,
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
    frame_bottom = tk.Frame( myGlobals.about_window)
    frame_bottom.configure(background=myGlobals.BGCOLOR)
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
        bg=myGlobals.TEXTBOXCOLOR,
#        bd=10,
        relief=tk.FLAT,
        width=80,
        height=TEXT_HEIGHT
    )

    #scrollbar
    msg_scrollBar = tk.Scrollbar(
        frame_right,
        bg=myGlobals.BGCOLOR,
    )
    msg_scrollBar.config(command=msg.yview)
    msg.config(yscrollcommand=msg_scrollBar.set)
    msg.insert(tk.END, open(myGlobals.RES_DOC_ABOUT, encoding="utf_8").read())
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
    photo = tk.PhotoImage(file=myGlobals.RES_GFX_ABOUT)
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

    myGlobals.about_window.bind('<Up>', keyboard_up) 
    myGlobals.about_window.bind('<Down>', keyboard_down) 
    myGlobals.about_window.bind('<Next>', keyboard_pageup) 
    myGlobals.about_window.bind('<Prior>', keyboard_pagedown) 


