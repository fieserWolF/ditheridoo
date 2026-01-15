import code.myGlobals as myGlobals
import code.action as action
import tkinter


def create_gui_preferences_from_menu () :
    create_gui_preferences(None)
    
def create_gui_preferences (self) :

    def close_window():
        #global preferences_window
        #global preferences_window_open
        
        if (myGlobals.preferences_window_open == True) :
            myGlobals.preferences_window.destroy()
            myGlobals.preferences_window_open = False

    def close_window_key(self):
        close_window()


    #global preferences_window
    #global preferences_window_open
    if (myGlobals.preferences_window_open == True) : return None
    myGlobals.preferences_window_open = True

    _padx = 10
    _pady = 10
    
	#http://effbot.org/tkbook/toplevel.htm
    myGlobals.preferences_window = tkinter.Toplevel(
        bd=10
    )
    myGlobals.preferences_window.title("Configure Settings")
    myGlobals.preferences_window.iconphoto(False, tkinter.PhotoImage(file=myGlobals.RES_GFX_ICON))
    myGlobals.preferences_window.protocol("WM_DELETE_WINDOW", close_window)
    myGlobals.preferences_window.bind("<Escape>", close_window_key)
    myGlobals.preferences_window.configure(background=myGlobals.BGCOLOR)
    myGlobals.preferences_window.resizable(0, 0)

    create_gui_preferences_palette(
        myGlobals.preferences_window,
        0,  #row
        0   #column
    )

    create_gui_preferences_startaddress(
        myGlobals.preferences_window,
        1,  #row
        0   #column
    )

    """
    create_gui_preferences_editorsize(
        myGlobals.preferences_window,
        0,  #row
        1   #column
    )
    """

    create_gui_preferences_previewsize(
        myGlobals.preferences_window,
        0,  #row
        #1,  #row
        1   #column
    )

    #button
    button = tkinter.Button(
        myGlobals.preferences_window,
        text="OK",
        bg=myGlobals.BGCOLOR,
        activebackground=myGlobals.ACTIVECOLOR,
        command=close_window,
        padx=_padx,
        pady=_pady,
        cursor=myGlobals.CURSOR_HAND,
    )
    button.grid(
        row=2,
        column=0,
        sticky=tkinter.N,
        columnspan=2
    )


    
"""
def create_gui_preferences_editorsize (
	root,
    _row,
    _column
) :
    frame_border = tkinter.Frame(
        root,
        bg=myGlobals.BGCOLOR,
        bd=myGlobals._bd,
    )
    frame_border.grid(
        row=_row,
        column=_column
    )
    frame_inner = tkinter.Frame(
        frame_border,
        bg=myGlobals.BGCOLOR,
        bd=1,
        padx = myGlobals._padx,
        pady = myGlobals._pady,
        relief=tkinter.RAISED
        )
    frame_inner.grid()

    _row = 0
    label = tkinter.Label(
        frame_inner,
        bg=myGlobals.BGCOLOR,
        text="editor size",
        wraplength=100,
        anchor='c',
        justify='left',
        fg="#000088"
    )
    label.grid(
        row=_row,
        column=1,
        sticky=tkinter.W+tkinter.E
    )
    MODES = [
            (myGlobals.EDITORSIZE_TEXT[0], 0),
            (myGlobals.EDITORSIZE_TEXT[1], 1)
        ]

    for text, mode in MODES:
        radiobutton = tkinter.Radiobutton(
            frame_inner,
            bg=myGlobals.BGCOLOR,
            activebackground=myGlobals.ACTIVECOLOR,
            selectcolor=myGlobals.SELECTCOLOR,
            text = text,
            value = mode,
            indicatoron=0,
            variable=myGlobals.user_editorsize,
            cursor=myGlobals.CURSOR_HAND,
            command=action.set_editor_dimensions
        )
        _row += 1
        radiobutton.grid(
            row=_row,
            column=1,
            sticky=tkinter.W+tkinter.E
        )
"""


def create_gui_preferences_previewsize (
	root,
    _row,
    _column
) :
    frame_border = tkinter.Frame(
        root,
        bg=myGlobals.BGCOLOR,
        bd=myGlobals._bd,
    )
    frame_border.grid(
        row=_row,
        column=_column
    )
    frame_inner = tkinter.Frame(
        frame_border,
        bg=myGlobals.BGCOLOR,
        bd=1,
        padx = myGlobals._padx,
        pady = myGlobals._pady,
        relief=tkinter.RAISED
        )
    frame_inner.grid()

    _row = 0
    label = tkinter.Label(
        frame_inner,
        bg=myGlobals.BGCOLOR,
        text="preview size",
        wraplength=100,
        anchor='c',
        justify='left',
        fg="#000088"
    )
    label.grid(
        row=_row,
        column=1,
        sticky=tkinter.W+tkinter.E
    )
    MODES = [
            (myGlobals.PREVIEWSIZE_TEXT[0], 0),
            (myGlobals.PREVIEWSIZE_TEXT[1], 1),
            (myGlobals.PREVIEWSIZE_TEXT[2], 2),
            (myGlobals.PREVIEWSIZE_TEXT[3], 3),
            (myGlobals.PREVIEWSIZE_TEXT[4], 4)
        ]

    for text, mode in MODES:
        radiobutton = tkinter.Radiobutton(
            frame_inner,
            bg=myGlobals.BGCOLOR,
            activebackground=myGlobals.ACTIVECOLOR,
            selectcolor=myGlobals.SELECTCOLOR,
            text = text,
            value = mode,
            indicatoron=0,
            variable=myGlobals.user_previewsize,
            cursor=myGlobals.CURSOR_HAND,
            command=action.refresh_prepare
        )
        _row += 1
        radiobutton.grid(
            row=_row,
            column=1,
            sticky=tkinter.W+tkinter.E
        )



def create_gui_preferences_palette (
	root,
    _row,
    _column
) :
#palette radiobuttons
#http://effbot.org/tkbook/radiobutton.htm
    frame_border = tkinter.Frame(
        root,
        bg=myGlobals.BGCOLOR,
        bd=myGlobals._bd,
    )
    frame_border.grid(
        row=_row,
        column=_column
    )
    frame_inner = tkinter.Frame(
        frame_border,
        bg=myGlobals.BGCOLOR,
        bd=1,
        padx = myGlobals._padx,
        pady = myGlobals._pady,
        relief=tkinter.RAISED
        )
    frame_inner.grid()

    _row = 0
    label = tkinter.Label(
        frame_inner,
        bg=myGlobals.BGCOLOR,
        text="palette",
        wraplength=100,
        anchor='c',
        justify='left',
        fg="#000088"
    )
    label.grid(
        row=_row,
        column=1,
        sticky=tkinter.W+tkinter.E
    )
    MODES = [
            ("colodore", "colodore"),
            ("pepto", "pepto")
        ]

    for text, mode in MODES:
        radiobutton_user_mode = tkinter.Radiobutton(
            frame_inner,
            bg=myGlobals.BGCOLOR,
            activebackground=myGlobals.ACTIVECOLOR,
            selectcolor=myGlobals.SELECTCOLOR,
            text = text,
            value = mode,
            indicatoron=0,
            variable=myGlobals.user_palette,
            cursor=myGlobals.CURSOR_HAND,
            command=action.refresh_prepare
        )
        _row += 1
        radiobutton_user_mode.grid(
            row=_row,
            column=1,
            sticky=tkinter.W+tkinter.E
        )

        


def create_gui_preferences_startaddress (
	root,
    _row,
    _column
) :
    frame_border = tkinter.Frame(
        root,
        bg=myGlobals.BGCOLOR,
        bd=myGlobals._bd,
    )
    frame_border.grid(
        row=_row,
        column=_column
    )
    frame_inner = tkinter.Frame(
        frame_border,
        bg=myGlobals.BGCOLOR,
        bd=1,
        padx = myGlobals._padx,
        pady = myGlobals._pady,
        relief=tkinter.RAISED
        )
    frame_inner.grid()
    
    label_start_address_title = tkinter.Label(
        frame_inner,
        bg=myGlobals.BGCOLOR,
        text="start address in hex:",
        anchor='c',
        fg="#000088"
    )
    checkbutton_start_address = tkinter.Checkbutton(
        frame_inner,
        bg=myGlobals.BGCOLOR,
        variable = myGlobals.user_start_address_checkbutton,
        cursor=myGlobals.CURSOR_HAND,
        )
    label_start_address = tkinter.Label(
        frame_inner,
        bg=myGlobals.BGCOLOR,
        text="values $0-$ffff $",
        anchor='c'
    )
    entry_start_address= tkinter.Entry(
        frame_inner,
        bg=myGlobals.TEXTBOXCOLOR,
        width=8,
        textvariable = myGlobals.user_start_address
    )
    
    #placement in grid layout
    label_start_address_title.grid(
        row=0,
        column=0,
        sticky=tkinter.W+tkinter.E,
        columnspan=3
    )
    checkbutton_start_address.grid(
        row=1,
        column=0,
        sticky=tkinter.W
    )
    label_start_address.grid(
        row=1,
        column=1,
        sticky=tkinter.W+tkinter.E
    )
    entry_start_address.grid(
        row=1,
        column=2,
        sticky=tkinter.E
    )
