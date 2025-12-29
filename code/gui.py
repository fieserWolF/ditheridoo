import code.myGlobals as myGlobals
import code.action as action
import code.gui_help as gui_help
import code.gui_about as gui_about
import code.gui_preferences as gui_preferences
import code.gui_preview as gui_preview
import tkinter as tk
import tkinter.filedialog as filedialog





def create_gui_main ():
    frame_top = tk.Frame(myGlobals.root, bg=myGlobals.BGCOLOR)
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



    frame_bottom = tk.Frame(myGlobals.root, bg=myGlobals.BGCOLOR)
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

    frame_left = tk.Frame(frame_bottom, bg=myGlobals.BGCOLOR)
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

    frame_right = tk.Frame(frame_bottom, bg=myGlobals.BGCOLOR)
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
    


def create_gui_drawmode (
	root,
    _row,
    _column
) :
    frame_border = tk.Frame(
        root,
        bg=myGlobals.BGCOLOR,
        bd=myGlobals._bd,
    )
    frame_border.grid(
        row=_row,
        column=_column
    )
    frame_inner = tk.Frame(
        frame_border,
        bg=myGlobals.BGCOLOR,
        bd=1,
        padx = myGlobals._padx,
        pady = myGlobals._pady,
        relief=tk.RAISED
        )
    frame_inner.grid()
    frame_inner.grid_columnconfigure(0, weight=1)
    frame_inner.grid_rowconfigure(0, weight=1)

    label = tk.Label(
        frame_inner,
        bg=myGlobals.BGCOLOR,
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
            bg=myGlobals.BGCOLOR,
            activebackground=myGlobals.ACTIVECOLOR,
            selectcolor=myGlobals.SELECTCOLOR,
            text = text,
            value = mode,
            indicatoron=0,
            variable=myGlobals.user_drawmode,
            cursor=myGlobals.CURSOR_HAND,
            command=action.root_refresh
        )
        radiobutton_user_mode.grid(
            row=row,
            column=column,
            sticky=tk.W+tk.E
        )
        
        

def create_gui_pencil (
	root,
    _row,
    _column
) :
    frame_border = tk.Frame(
        root,
        bg=myGlobals.BGCOLOR,
        bd=myGlobals._bd,
    )
    frame_border.grid(
        row=_row,
        column=_column
    )
    frame_inner = tk.Frame(
        frame_border,
        bg=myGlobals.BGCOLOR,
        bd=1,
        padx = myGlobals._padx,
        pady = myGlobals._pady,
        relief=tk.RAISED
        )
    frame_inner.grid()
    frame_inner.grid_columnconfigure(0, weight=1)
    frame_inner.grid_rowconfigure(0, weight=1)

    label = tk.Label(
        frame_inner,
        bg=myGlobals.BGCOLOR,
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
            bg=myGlobals.BGCOLOR,
            activebackground=myGlobals.ACTIVECOLOR,
            selectcolor=myGlobals.SELECTCOLOR,
            text = text,
            value = mode,
            indicatoron=0,
            variable=myGlobals.user_pencil,
            cursor=myGlobals.CURSOR_HAND,
#            command=action_image_refresh_prepare
        )
        radiobutton_pencil.grid(
            row=row,
            column=col,
            sticky=tk.W+tk.E
        )






def create_gui_replace_color (
	root,
    _row,
    _column
) :
    #global frame_replace_color
    #global radiobutton_replace_bg, radiobutton_replace_col1, radiobutton_replace_col2, radiobutton_replace_col3

    myGlobals.frame_replace_color = tk.Frame(
        root,
        bg=myGlobals.BGCOLOR,
        bd=myGlobals._bd,
    )
    myGlobals.frame_replace_color.grid(
        row=_row,
        column=_column
    )
    frame_inner = tk.Frame(
        myGlobals.frame_replace_color,
        bg=myGlobals.BGCOLOR,
        bd=1,
        padx = myGlobals._padx,
        pady = myGlobals._pady,
        relief=tk.RAISED
        )
    frame_inner.grid()
    frame_inner.grid_columnconfigure(0, weight=1)
    frame_inner.grid_rowconfigure(0, weight=1)

    

    label = tk.Label(
        frame_inner,
        bg=myGlobals.BGCOLOR,
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
        bg=myGlobals.BGCOLOR,
        text="none",
        anchor='c',
        fg="#000088"
    )
    radiobutton_used_color_none = tk.Radiobutton(
        frame_inner,
        value = 99,
        width=2,
        indicatoron=0,
        activebackground=myGlobals.ACTIVECOLOR,
        selectcolor=myGlobals.SELECTCOLOR,
        variable=myGlobals.user_replace_color,
        bg=myGlobals.BGCOLOR,
        cursor=myGlobals.CURSOR_HAND,
        bd=4,
        relief=tk.GROOVE,
        offrelief=tk.RAISED,
        #command=action_debug
    )

    label_replace_color = tk.Label(
        frame_inner,
        bg=myGlobals.BGCOLOR,
        text="color",
        anchor='c',
        fg="#000088"
    )
    
    myGlobals.radiobutton_replace_col1 = tk.Radiobutton(
        frame_inner,
        value = 1,
        width=2,
        indicatoron=0,
        variable=myGlobals.user_replace_color,
        bg=myGlobals.BGCOLOR,
        activebackground="#000000",
        selectcolor="#000000",
        cursor=myGlobals.CURSOR_HAND,
        bd=4,
        relief=tk.GROOVE,
        offrelief=tk.RAISED,
        #command=action_debug
    )
    
    myGlobals.radiobutton_replace_col2 = tk.Radiobutton(
        frame_inner,
        value = 2,
        width=2,
        indicatoron=0,
        variable=myGlobals.user_replace_color,
        bg=myGlobals.BGCOLOR,
        activebackground="#000000",
        selectcolor="#000000",
        cursor=myGlobals.CURSOR_HAND,
        bd=4,
        relief=tk.GROOVE,
        offrelief=tk.RAISED,
        #command=action_debug
    )
    
    myGlobals.radiobutton_replace_col3 = tk.Radiobutton(
        frame_inner,
        value = 3,
        width=2,
        indicatoron=0,
        variable=myGlobals.user_replace_color,
        bg=myGlobals.BGCOLOR,
        activebackground="#000000",
        selectcolor="#000000",
        cursor=myGlobals.CURSOR_HAND,
        bd=4,
        relief=tk.GROOVE,
        offrelief=tk.RAISED,
        #command=action_debug
    )
    myGlobals.radiobutton_replace_bg = tk.Radiobutton(
        frame_inner,
        value = 0,
        width=2,
        indicatoron=0,
        variable=myGlobals.user_replace_color,
        bg=myGlobals.BGCOLOR,
        activebackground="#000000",
        selectcolor="#000000",
        cursor=myGlobals.CURSOR_HAND,
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
    myGlobals.radiobutton_replace_col1.grid(
        row=2,
        column=1,
        sticky=tk.W+tk.E
    )
    myGlobals.radiobutton_replace_col2.grid(
        row=2,
        column=2,
        sticky=tk.W+tk.E
    )
    myGlobals.radiobutton_replace_col3.grid(
        row=2,
        column=3,
        sticky=tk.W+tk.E
    )
    myGlobals.radiobutton_replace_bg.grid(
        row=2,
        column=4,
        sticky=tk.W+tk.E
    )



def create_gui_current_color (
	root,
    _row,
    _column
) :
    #global radiobutton_current_bg, radiobutton_current_col1, radiobutton_current_col2, radiobutton_current_col3

    frame_border = tk.Frame(
        root,
        bd=myGlobals._bd,
    )
    frame_border.configure(background=myGlobals.BGCOLOR)
    frame_border.grid(
        row=_row,
        column=_column
    )
    frame_inner = tk.Frame(
        frame_border,
        bd=1,
        padx = myGlobals._padx,
        pady = myGlobals._pady,
        relief=tk.RAISED
        )
    frame_inner.configure(background=myGlobals.BGCOLOR)
    frame_inner.grid()
    frame_inner.grid_columnconfigure(0, weight=1)
    frame_inner.grid_rowconfigure(0, weight=1)

    

    #current color
    label_current_color = tk.Label(
        frame_inner,
        bg=myGlobals.BGCOLOR,
        text="block",
        anchor='c',
        fg="#000088"
    )
    
    myGlobals.radiobutton_current_col1 = tk.Radiobutton(
        frame_inner,
        value = 1,
        width=2,
        indicatoron=0,
        state=tk.DISABLED,
        variable=myGlobals.current_color,
        background="#000000",
        activebackground="#000000",
        selectcolor="#000000",
        bd=4,
        relief=tk.GROOVE,
        offrelief=tk.RAISED,
        #command=action_debug
    )
    
    myGlobals.radiobutton_current_col2 = tk.Radiobutton(
        frame_inner,
        value = 2,
        width=2,
        indicatoron=0,
        state=tk.DISABLED,
        variable=myGlobals.current_color,
        background="#000000",
        activebackground="#000000",
        selectcolor="#000000",
        bd=4,
        relief=tk.GROOVE,
        offrelief=tk.RAISED,
        #command=action_debug
    )
    
    myGlobals.radiobutton_current_col3 = tk.Radiobutton(
        frame_inner,
        value = 3,
        width=2,
        indicatoron=0,
        state=tk.DISABLED,
        variable=myGlobals.current_color,
        background="#000000",
        activebackground="#000000",
        selectcolor="#000000",
        bd=4,
        relief=tk.GROOVE,
        offrelief=tk.RAISED,
        #command=action_debug
    )
    myGlobals.radiobutton_current_bg = tk.Radiobutton(
        frame_inner,
        value = 0,
        width=2,
        indicatoron=0,
        state=tk.DISABLED,
        variable=myGlobals.current_color,
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
    myGlobals.radiobutton_current_col1.grid(
        row=0,
        column=1,
        sticky=tk.W+tk.E
    )
    myGlobals.radiobutton_current_col2.grid(
        row=0,
        column=2,
        sticky=tk.W+tk.E
    )
    myGlobals.radiobutton_current_col3.grid(
        row=0,
        column=3,
        sticky=tk.W+tk.E
    )
    myGlobals.radiobutton_current_bg.grid(
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
        bd=myGlobals._bd,
        bg=myGlobals.BGCOLOR
    )
    frame_border.grid(
        row=_row,
        column=_column
    )
    frame_inner = tk.Frame(
        frame_border,
        bd=1,
        bg=myGlobals.BGCOLOR,
        padx = myGlobals._padx,
        pady = myGlobals._pady,
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
        bg=myGlobals.BGCOLOR,
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
            myGlobals.PALETTEDATA_PEPTO[(value*3)+0],
            myGlobals.PALETTEDATA_PEPTO[(value*3)+1],
            myGlobals.PALETTEDATA_PEPTO[(value*3)+2]
        )
        radiobutton_user_value = tk.Radiobutton(
            frame_inner,
            value = value,
            width=2,
            indicatoron=0,
            variable=myGlobals.user_drawcolor_left,
            background=mycolor,
            activebackground=mycolor,
            selectcolor=mycolor,
            cursor=myGlobals.CURSOR_HAND,
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
        bd=myGlobals._bd,
    )
    frame_border.configure(background=myGlobals.BGCOLOR)
    frame_border.grid(
        row=_row,
        column=_column
    )
    frame_inner = tk.Frame(
        frame_border,
        bd=1,
        bg=myGlobals.BGCOLOR,
        padx = myGlobals._padx,
        pady = myGlobals._pady,
        relief=tk.RAISED
        )
    frame_inner.grid()
    frame_inner.grid_columnconfigure(0, weight=1)
    frame_inner.grid_rowconfigure(0, weight=1)

    _row = 0
    label = tk.Label(
        frame_inner,
        bg=myGlobals.BGCOLOR,
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
            myGlobals.PALETTEDATA_PEPTO[(value*3)+0],
            myGlobals.PALETTEDATA_PEPTO[(value*3)+1],
            myGlobals.PALETTEDATA_PEPTO[(value*3)+2]
        )
        radiobutton_user_value = tk.Radiobutton(
            frame_inner,
            value = value,
            width=2,
            indicatoron=0,
            variable=myGlobals.user_drawcolor_right,
            background=mycolor,
            activebackground=mycolor,
            selectcolor=mycolor,
            cursor=myGlobals.CURSOR_HAND,
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



	

def create_drop_down_menu (
	root
) :    
    menu = tk.Menu(root)
    myGlobals.root.config(menu=menu)

    filemenu = tk.Menu(menu, tearoff=0)
    filemenu.add_command(label="new", command=action.draw_new_image)
    filemenu.add_separator()
    filemenu.add_command(label="open...", command=action.action_OpenFile_from_menu, underline=0, accelerator="Control+o")
    filemenu.add_command(label="save...", command=action.action_SaveFile_from_menu, underline=0, accelerator="Control+s")
    filemenu.add_separator()
    filemenu.add_command(label="preferences", command=gui_preferences.create_gui_preferences_from_menu, underline=0, accelerator="Control+p")
    filemenu.add_command(label="show preview", command=gui_preview.create_gui_preview_image_from_menu)
    filemenu.add_separator()
    filemenu.add_command(label="quit", command=root.quit, underline=0, accelerator="Control+q")

    editmenu = tk.Menu(menu, tearoff=0)
    editmenu.add_command(label="undo", command=action.undo_undo_from_menu, accelerator="Ctrl+z")
    editmenu.add_separator()
    editmenu.add_command(label="marker", command=action.marker_select_from_menu, underline=0, accelerator="m")
    editmenu.add_separator()
    editmenu.add_command(label="cut", command=action.buffer_cut_from_menu, accelerator="Ctrl+x")
    editmenu.add_command(label="copy", command=action.buffer_copy_from_menu, accelerator="Ctrl+c")
    #editmenu.add_command(label="paste", command=action.buffer_paste_from_menu, accelerator="Ctrl+v")

    infomenu = tk.Menu(menu, tearoff=0)
    infomenu.add_command(label="about", command=gui_about.create_gui_about)
    infomenu.add_command(label="help", command=gui_help.create_gui_help_from_menu, underline=0, accelerator="Control+h")

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
        bg=myGlobals.BGCOLOR,
        bd=myGlobals._bd,
    )
    frame_border.grid(
        row=_row,
        column=_column
    )
    frame_inner = tk.Frame(
        frame_border,
        bg=myGlobals.BGCOLOR,
        bd=1,
        padx = myGlobals._padx,
        pady = myGlobals._pady,
        relief=tk.RAISED
        )
    frame_inner.grid()
    frame_inner.grid_columnconfigure(0, weight=1)
    frame_inner.grid_rowconfigure(0, weight=1)
    

    #cursor
    label_title_cursor = tk.Label(
        frame_inner,
        bg=myGlobals.BGCOLOR,
        text="position:",
        anchor='ne',
        fg="#000088"
    )
    label_cursor_posx = tk.Label(
        frame_inner,
        bg=myGlobals.BGCOLOR,
        textvariable = myGlobals.cursorx_variable,
        anchor='c'
    )
    label_cursor_posy = tk.Label(
        frame_inner,
        bg=myGlobals.BGCOLOR,
        textvariable = myGlobals.cursory_variable,
        anchor='c'
    )
    
    #block
    label_title_block = tk.Label(
        frame_inner,
        bg=myGlobals.BGCOLOR,
        text="block:",
        anchor='ne',
        fg="#000088"
    )
    label_block_posx = tk.Label(
        frame_inner,
        bg=myGlobals.BGCOLOR,
        textvariable = myGlobals.blockx_variable,
        anchor='c'
    )
    label_block_posy = tk.Label(
        frame_inner,
        bg=myGlobals.BGCOLOR,
        textvariable = myGlobals.blocky_variable,
        anchor='c'
    )

    #undo
    label_title_undo = tk.Label(
        frame_inner,
        bg=myGlobals.BGCOLOR,
        text="undo steps:",
        anchor='ne',
        fg="#000088"
    )
    label_undo = tk.Label(
        frame_inner,
        bg=myGlobals.BGCOLOR,
        textvariable = myGlobals.undo_variable,
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
        bd=myGlobals._bd,
        bg=myGlobals.BGCOLOR
    )
    frame_border.grid(
        row=_row,
        column=_column
    )

    photo = tk.PhotoImage(file=myGlobals.RES_GFX_AC)
    label_logo = tk.Label(frame_border, image = photo)
    label_logo.image = photo # keep a reference!
    label_logo.grid( row=0, column=0)
    label_logo.configure(background=myGlobals.BGCOLOR)



def create_gui_editor_image (
	root,
    _row,
    _column
) :
    #global label_editor_image
    
    #creation of elements
    myGlobals.label_editor_image = tk.Label(
        root,
        bg=myGlobals.BGCOLOR,
        cursor=myGlobals.CURSOR_EDIT,
    )
    
    #placement in grid layout
    myGlobals.label_editor_image.grid(
        row=0,
        column=0,
        padx=0,
        pady=0,
        ipadx=0,
        ipady=0
    )


    # mouse wheel
    #   (Windows)
    myGlobals.label_editor_image.bind('<MouseWheel>' ,action.input_mouse_wheel)
    #   (Linux)
    myGlobals.label_editor_image.bind('<Button-4>' ,action.input_mouse_wheel)
    myGlobals.label_editor_image.bind('<Button-5>' ,action.input_mouse_wheel)
    # mouse wheel-button
    myGlobals.label_editor_image.bind('<Motion>', action.input_mouse_motion_edit_window)
    # mouse buttons
    myGlobals.label_editor_image.bind('<Button-1>', action.input_mouse_left_button_editor)
    myGlobals.label_editor_image.bind('<B1-Motion>', action.input_mouse_left_button_editor)

    #https://docs.python.org/3/library/platform.html
    #platform.system() : 'Linux', 'Darwin', 'Java', 'Windows'
    if (myGlobals.operating_system == 'Darwin') :
        #darwin macos
        myGlobals.label_editor_image.bind('<Button-3>', action.input_mouse_middle_button_press)
        myGlobals.label_editor_image.bind('<ButtonRelease-3>', action.input_mouse_middle_button_release)
        myGlobals.label_editor_image.bind('<B3-Motion>', action.input_mouse_middle_button_motion)
        myGlobals.label_editor_image.bind('<Button-2>', action.input_mouse_right_button)
        myGlobals.label_editor_image.bind('<B2-Motion>', action.input_mouse_right_button)
    else :
        #linux and windows
        myGlobals.label_editor_image.bind('<Button-2>', action.input_mouse_middle_button_press)
        myGlobals.label_editor_image.bind('<ButtonRelease-2>', action.input_mouse_middle_button_release)
        myGlobals.label_editor_image.bind('<B2-Motion>', action.input_mouse_middle_button_motion)
        myGlobals.label_editor_image.bind('<Button-3>', action.input_mouse_right_button)
        myGlobals.label_editor_image.bind('<B3-Motion>', action.input_mouse_right_button)
