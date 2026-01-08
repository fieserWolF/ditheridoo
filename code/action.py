import code.myGlobals as myGlobals
import struct
import os
import tkinter.filedialog


def redraw_canvas (event):
    #https://www.youtube.com/watch?v=oVueT2pkcOw
    #c.coords(item, 0,0, event.width, event.height)
    #print('w=%d / h=%d'%(event.width, event.height))
    myGlobals.canvas_width = event.width
    myGlobals.canvas_height = event.height
    #print('redraw_canvas')
    refresh_show()
    


def convert_to_photo_image(
    my_width,
    my_height,
    my_data
) :
    #https://tkdocs.com/pyref/photoimage.html

    #https://en.wikipedia.org/wiki/Netpbm#Description
    #"PPM" portable pixmap
    #header
    #picture data (an array of bytes)
    
    #https://www.programiz.com/python-programming/methods/string/encode
    #https://www.programiz.com/python-programming/methods/built-in/bytearray
    tmp_ppm = ('P6 '+str(my_width)+' '+str(my_height)+' 255 ').encode(encoding='UTF-8',errors='strict') + bytearray(my_data)

    return tkinter.PhotoImage(width=my_width, height=my_height, data=tmp_ppm, format='PPM')


def convert_to_photo_image_data(
    my_width,
    my_height,
    my_data
) :
    #https://tkdocs.com/pyref/photoimage.html

    #https://en.wikipedia.org/wiki/Netpbm#Description
    #"PPM" portable pixmap
    #header
    #picture data (an array of bytes)
    
    #https://www.programiz.com/python-programming/methods/string/encode
    #https://www.programiz.com/python-programming/methods/built-in/bytearray
    tmp_ppm = ('P6 '+str(my_width)+' '+str(my_height)+' 255 ').encode(encoding='UTF-8',errors='strict') + bytearray(my_data)

    return tmp_ppm


def save_ppm(filename):
    switcher_palette = {
        'pepto': myGlobals.PALETTEDATA_PEPTO,
        'colodore': myGlobals.PALETTEDATA_COLODORE,
    }
    my_palettedata = switcher_palette.get(myGlobals.user_palette.get(), myGlobals.PALETTEDATA_PEPTO)
    
    #indexed image to RGB image
    my_bytes = []
    for i in myGlobals.koala_colorindex_data :
        my_bytes.append(my_palettedata[i*3+0])  #r
        my_bytes.append(my_palettedata[i*3+1])  #g
        my_bytes.append(my_palettedata[i*3+2])  #b

        #koala: double pixels
        my_bytes.append(my_palettedata[i*3+0])  #r  
        my_bytes.append(my_palettedata[i*3+1])  #g
        my_bytes.append(my_palettedata[i*3+2])  #b

    my_data = ('P6 '+str(myGlobals.KOALA_WIDTH*2)+' '+str(myGlobals.KOALA_HEIGHT)+' 255 ').encode(encoding='UTF-8',errors='strict') + bytearray(my_bytes)
    save_some_data(filename, my_data)



def save_some_data(
    filename,
    data
):
    print ('    Opening file "%s" for writing data (%d ($%04x) bytes)...' % (filename, len(data), len(data)))
    try:
        file_out = open(filename , 'wb')
    except IOError as err:
        print('I/O error: {0}'.format(err))
        return None
    file_out.write(bytearray(data))
    file_out.close()



def draw_background():
    #is only called at the start and if editor size is changed
    CHECKER_SIZE = 32
    CHECKER_COLOR1="#777777"
    CHECKER_COLOR2="#555555"
    MY_STATE='normal'
    #MY_STATE='hidden'

    #https://anzeljg.github.io/rin2/book2/2405/docs/tkinter/create_rectangle.html
    myGlobals.canvas_editor.create_rectangle(
        0,0,
        myGlobals.canvas_width,
        myGlobals.canvas_height,
        fill=CHECKER_COLOR2,
        width=0,
        tags='background',
        state=MY_STATE
    )
    
    for y in range(0,myGlobals.canvas_height,CHECKER_SIZE) :
        a=0
        if (int(y%(CHECKER_SIZE*2)) != 0) : a=1
        for x in range(0,myGlobals.canvas_width,CHECKER_SIZE) :
            if ( a%2 == 0) :
                myGlobals.canvas_editor.create_rectangle(
                x,y,
                x+CHECKER_SIZE,
                y+CHECKER_SIZE,
                fill=CHECKER_COLOR1,
                width=0,
                tags='background',
                state=MY_STATE)
            a += 1

    
def draw_marker(
    colorindex_data
):
    MARKER_COLOR=1  #C64 color index
        
    startx = (myGlobals.marker_posx)*4
    starty = (myGlobals.marker_posy)*8
    endx = (myGlobals.marker_posx+myGlobals.marker_width+1)*4
    endy = (myGlobals.marker_posy+myGlobals.marker_height+1)*8
    for x in range(startx,endx) :
        colorindex_data[(starty*myGlobals.KOALA_WIDTH)+x] = MARKER_COLOR
        colorindex_data[((endy-1)*myGlobals.KOALA_WIDTH)+x] = MARKER_COLOR
    for y in range(starty+1,endy-1) :
        colorindex_data[(y*myGlobals.KOALA_WIDTH)+startx] = MARKER_COLOR
        colorindex_data[(y*myGlobals.KOALA_WIDTH)+endx-1] = MARKER_COLOR
    
    return colorindex_data


def set_editor_dimensions():
    
    myGlobals.canvas_editor.configure(
        width=myGlobals.EDITOR_PRE_WIDTH[myGlobals.user_editorsize.get()],
        height=myGlobals.EDITOR_PRE_HEIGHT[myGlobals.user_editorsize.get()]
    )

    """
    #https://stackoverflow.com/questions/66516760/get-height-width-of-tkinter-canvas
    myGlobals.canvas_width = myGlobals.canvas_editor.winfo_width()
    myGlobals.canvas_height = myGlobals.canvas_editor.winfo_height()
    myGlobals.canvas_width_old = myGlobals.canvas_width
    """
    refresh_show()




def draw_grids():
    #multi = myGlobals.EDITORSIZE_MULTIPLY[myGlobals.user_editorsize.get()]
    multi = 2
    #print("create_draw_canvas_grid()")
    GRID_COLOR = '#888888'
    #MY_STATE='normal'
    MY_STATE='hidden'

    myGlobals.canvas_editor.delete('grid1')
    myGlobals.canvas_editor.delete('grid2')
    myGlobals.canvas_editor.delete('grid3')
    myGlobals.canvas_editor.delete('grid4')

    #https://anzeljg.github.io/rin2/book2/2405/docs/tkinter/create_line.html
    #y-axis
    for y in range(0,myGlobals.canvas_height,(myGlobals.GRID_SIZE[1] * multi)) : myGlobals.canvas_editor.create_line(0,y,myGlobals.canvas_width,y,fill=GRID_COLOR,tags='grid1', state=MY_STATE)
    for y in range(0,myGlobals.canvas_height,(myGlobals.GRID_SIZE[2] * multi)) : myGlobals.canvas_editor.create_line(0,y,myGlobals.canvas_width,y,fill=GRID_COLOR,tags='grid2', state=MY_STATE)
    for y in range(0,myGlobals.canvas_height,(myGlobals.GRID_SIZE[3] * multi)) : myGlobals.canvas_editor.create_line(0,y,myGlobals.canvas_width,y,fill=GRID_COLOR,tags='grid3', state=MY_STATE)
    for y in range(0,myGlobals.canvas_height,(myGlobals.GRID_SIZE[4] * multi)) : myGlobals.canvas_editor.create_line(0,y,myGlobals.canvas_width,y,fill=GRID_COLOR,tags='grid4', state=MY_STATE)

    #x-axis
    for x in range(0,myGlobals.canvas_width,(myGlobals.GRID_SIZE[1] * multi)) : myGlobals.canvas_editor.create_line(x,0,x,myGlobals.canvas_height,fill=GRID_COLOR,tags='grid1', state=MY_STATE)
    for x in range(0,myGlobals.canvas_width,(myGlobals.GRID_SIZE[2] * multi)) : myGlobals.canvas_editor.create_line(x,0,x,myGlobals.canvas_height,fill=GRID_COLOR,tags='grid2', state=MY_STATE)
    for x in range(0,myGlobals.canvas_width,(myGlobals.GRID_SIZE[3] * multi)) : myGlobals.canvas_editor.create_line(x,0,x,myGlobals.canvas_height,fill=GRID_COLOR,tags='grid3', state=MY_STATE)
    for x in range(0,myGlobals.canvas_width,(myGlobals.GRID_SIZE[4] * multi)) : myGlobals.canvas_editor.create_line(x,0,x,myGlobals.canvas_height,fill=GRID_COLOR,tags='grid4', state=MY_STATE)


    
def refresh_prepare():
        #writes: myGlobals.koala_image

        #apply the correct colors
        switcher_palette = {
            'pepto': myGlobals.PALETTEDATA_PEPTO,
            'colodore': myGlobals.PALETTEDATA_COLODORE,
        }
        my_palettedata = switcher_palette.get(myGlobals.user_palette.get(), myGlobals.PALETTEDATA_PEPTO)

        
        #koala indexed image to RGB image byte_array
        my_bytes = []
        for i in myGlobals.koala_colorindex_data :
            my_bytes.append(my_palettedata[i*3+0])
            my_bytes.append(my_palettedata[i*3+1])
            my_bytes.append(my_palettedata[i*3+2])

        #apply to myGlobals.preview_photoimage (a tkinter.PhotoImage)
        multiply_preview = myGlobals.PREVIEWSIZE_MULTIPLY[myGlobals.user_previewsize.get()]
        if (myGlobals.preview_window_open == True) :
            #myGlobals.preview_photoimage = convert_to_photo_image(myGlobals.KOALA_WIDTH,myGlobals.KOALA_HEIGHT, my_bytes).zoom(multiply_preview*2,multiply_preview)
            myGlobals.preview_photoimage.config(
                width=myGlobals.KOALA_WIDTH,
                height=myGlobals.KOALA_HEIGHT,
                data=convert_to_photo_image_data(myGlobals.KOALA_WIDTH,myGlobals.KOALA_HEIGHT, my_bytes),
                format='PPM'
            )
            #.zoom(multiply_preview*2,multiply_preview)


        #koala_photoimage: indexed image to RGB image
        #multiply_editor = myGlobals.EDITORSIZE_MULTIPLY[myGlobals.user_editorsize.get()]
        if ((myGlobals.marker_height > 0) & (myGlobals.marker_width > 0) ) :
            #if we have a marker-box: prepare new my_bytes[] with markers
            koala_with_markers_colorindex_data = draw_marker(myGlobals.koala_colorindex_data)
            my_bytes = []
            for i in koala_with_markers_colorindex_data :
                my_bytes.append(my_palettedata[i*3+0])
                my_bytes.append(my_palettedata[i*3+1])
                my_bytes.append(my_palettedata[i*3+2])
        #apply to myGlobals.koala_photoimage (a tkinter.PhotoImage)
        #https://tkdocs.com/pyref/photoimage.html
        #myGlobals.koala_photoimage = convert_to_photo_image(myGlobals.KOALA_WIDTH,myGlobals.KOALA_HEIGHT, my_bytes)
        #myGlobals.koala_photoimage = tkinter.PhotoImage(width=my_width, height=my_height, data=tmp_ppm, format='PPM')
        myGlobals.koala_photoimage.config(
            width=myGlobals.KOALA_WIDTH,
            height=myGlobals.KOALA_HEIGHT,
            data=convert_to_photo_image_data(myGlobals.KOALA_WIDTH,myGlobals.KOALA_HEIGHT, my_bytes),
            format='PPM'
        )

        #print(myGlobals.koala_photoimage)
        #myGlobals.koala_photoimage = tmp.copy()

        refresh_show()
        

def editorimage_pos_sanity_check() :
        #writes: myGlobals.editorimage_posx, myGlobals.editorimage_posy
        
        #sanity checks
        if (myGlobals.editorimage_posx < myGlobals.C64_CHAR_WIDTH*-1+1) : myGlobals.editorimage_posx = myGlobals.C64_CHAR_WIDTH*-1+1
        if (myGlobals.editorimage_posy < myGlobals.C64_CHAR_HEIGHT*-1+1) : myGlobals.editorimage_posy = myGlobals.C64_CHAR_HEIGHT*-1+1
        if (myGlobals.editorimage_posx > myGlobals.C64_CHAR_WIDTH-1) : myGlobals.editorimage_posx = myGlobals.C64_CHAR_WIDTH-1
        if (myGlobals.editorimage_posy > myGlobals.C64_CHAR_HEIGHT-1) : myGlobals.editorimage_posy = myGlobals.C64_CHAR_HEIGHT-1
        
        #zoom
        if (
            (myGlobals.zoom==0) |
            (myGlobals.zoom==1)
        ) :
            myGlobals.editorimage_posx = 0
            myGlobals.editorimage_posy = 0

    

def refresh_show():
        #copy, move and zoom: koala_image to editor_image
        #writes
        #myGlobals.editor_image
        #myGlobals.label_editor_image, myGlobals.label_preview_image
        #myGlobals.marker_image

        #sanity check
        if (
            (myGlobals.koala_photoimage.width() != myGlobals.KOALA_WIDTH) &
            (myGlobals.koala_photoimage.height() != myGlobals.KOALA_HEIGHT)
        ) :
            #dimensions do not match koala format
            return None


        # update dimensions
        # only if new editor size is selected in preferences window
        editor_width = myGlobals.canvas_width-2
        editor_height = myGlobals.canvas_height-2
        if (myGlobals.canvas_width != myGlobals.canvas_width_old) :
            draw_background()
            draw_grids()
            myGlobals.canvas_editor.configure(
                width=editor_width,
                height=editor_height)

        myGlobals.canvas_width_old = myGlobals.canvas_width


        #show correct offset
        LIMIT_WIDTH = int(myGlobals.canvas_width  / (myGlobals.ZOOM_MULTIPLY[myGlobals.zoom]*8))
        LIMIT_HEIGHT = int(myGlobals.canvas_height / (myGlobals.ZOOM_MULTIPLY[myGlobals.zoom]*8))
        if (LIMIT_WIDTH > myGlobals.C64_CHAR_WIDTH) : LIMIT_WIDTH = myGlobals.C64_CHAR_WIDTH
        if (LIMIT_HEIGHT > myGlobals.C64_CHAR_HEIGHT) : LIMIT_HEIGHT = myGlobals.C64_CHAR_HEIGHT

        start_x = myGlobals.editorimage_posx
        start_y = myGlobals.editorimage_posy
        #sanity checks
        if (start_x+LIMIT_WIDTH > myGlobals.koala_photoimage.width()/4) : start_x = int(myGlobals.koala_photoimage.width()/4)-LIMIT_WIDTH
        if (start_y+LIMIT_HEIGHT > myGlobals.koala_photoimage.height()/8) : start_y = int(myGlobals.koala_photoimage.height()/8)-LIMIT_HEIGHT
        if (start_x < 0) : start_x = 0
        if (start_y < 0) : start_y = 0

        end_x = start_x+LIMIT_WIDTH
        end_y = start_y+LIMIT_HEIGHT

        myGlobals.editorimage_posx = start_x
        myGlobals.editorimage_posy = start_y

        #https://tkdocs.com/pyref/photoimage.html
        myGlobals.tmp_photoimage = myGlobals.koala_photoimage.copy(
            zoom=(
                myGlobals.ZOOM_MULTIPLY[myGlobals.zoom]*2,  #double pixels in multicolor koala mode
                myGlobals.ZOOM_MULTIPLY[myGlobals.zoom]
            ),
            from_coords=(
                start_x*4,    #x0 multicolor koala format holds 4 pixels in a char-column
                start_y*8,    #y0 multicolor koala format holds 8 pixels in a char-row
                end_x*4,      #x1 multicolor koala format holds 4 pixels in a char-column
                end_y*8       #y1 multicolor koala format holds 8 pixels in a char-row
            )
        )

        #update image in canvas_editor
        myGlobals.canvas_editor.itemconfigure('koala_image', image=myGlobals.tmp_photoimage, state='normal')

        #hide all grids
        #myGlobals.canvas_editor.itemconfigure('background', state='hidden')
        myGlobals.canvas_editor.itemconfigure('koala_image', state='normal')
        myGlobals.canvas_editor.itemconfigure('grid1', state='hidden')
        myGlobals.canvas_editor.itemconfigure('grid2', state='hidden')
        myGlobals.canvas_editor.itemconfigure('grid3', state='hidden')
        myGlobals.canvas_editor.itemconfigure('grid4', state='hidden')

        #show grid
        if (myGlobals.grid_enabled) :
            if (myGlobals.zoom == 1) : myGlobals.canvas_editor.itemconfigure("grid1", state='normal')
            if (myGlobals.zoom == 2) : myGlobals.canvas_editor.itemconfigure("grid2", state='normal')
            if (myGlobals.zoom == 3) : myGlobals.canvas_editor.itemconfigure("grid3", state='normal')
            if (myGlobals.zoom == 4) : myGlobals.canvas_editor.itemconfigure("grid4", state='normal')
        
        # put "background" at the bottom
        myGlobals.canvas_editor.tag_lower("background")

        #update image in label_preview image
        if (myGlobals.preview_window_open == True) :
            multiply_preview = myGlobals.PREVIEWSIZE_MULTIPLY[myGlobals.user_previewsize.get()]
            myGlobals.tmp_preview_photoimage = myGlobals.preview_photoimage.copy(zoom=(multiply_preview*2,multiply_preview))
            myGlobals.label_preview_image.configure(image=myGlobals.tmp_preview_photoimage)




def toggle_grid(
) :
    if (myGlobals.grid_enabled) :
        myGlobals.grid_enabled = False
    else :
        myGlobals.grid_enabled = True
    refresh_show()
        


def koala_index_to_colorindex(
    index,  #0..3
    x,
    y
) :
    location = (y*myGlobals.C64_CHAR_WIDTH)+x
        
    switcher = {
        0 : myGlobals.koala_bg,    #=koala_bg;	// pixel not set = $d021 colour
        1 : myGlobals.koala_col12[location] >> 4,   #=koala_col12[(y*C64_CHAR_WIDTH)+x] SHR 4;
        2 : myGlobals.koala_col12[location] & 0b00001111,    #=koala_col12[(y*C64_CHAR_WIDTH)+x] and %00001111;
        3 : myGlobals.koala_col3[location] & 0b00001111    #=koala_col3[(y*C64_CHAR_WIDTH)+x] and %00001111;
    }
    return switcher.get(index,0)


def koala_to_image_single_block(x,y) :
    #global koala_colorindex_data

    SHR_PRE = [
        6,
        4,
        2,
        0
    ]

    pos = ((y*myGlobals.C64_CHAR_WIDTH)+x)*8
    this_block = myGlobals.koala_bitmap[ pos:pos+8]   #this_block holds 8 bytes

    for row in range(0, 8):
        this_row = this_block[row]
        
        for column in range(0, 4):
            iy = y*8    +row
            ix = x*4    +column

            #normal data
            koalaindex = (this_row >> SHR_PRE[column]) & 0b00000011 #result should be 0..3
            myGlobals.koala_colorindex_data[iy*myGlobals.KOALA_WIDTH+ix] = koala_index_to_colorindex(koalaindex,x,y)


def koala_to_image(
):
    for y in range(0, myGlobals.C64_CHAR_HEIGHT):
        for x in range(0, myGlobals.C64_CHAR_WIDTH):
            koala_to_image_single_block(x,y)




def load_koala(
    filename_in
) :
    """
    loads and parses a koala file for debugging the koala_to_image conversion
    * reads: filename
    * sets: koala_bitmap, koala_col12, koala_col3 and koala_bg
    """
    #writes:
    #myGlobals.koala_bitmap
    #myGlobals.koala_col12
    #myGlobals.koala_col3
    #myGlobals.koala_bg
    
    #load a koala
    print ("Opening koala \"%s\"..." % filename_in)
    file_in = open(filename_in , "rb")
    # read file into buffer
    buffer=[]
    while True:
        data = file_in.read(1)  #read 1 byte
        if not data: break
        temp = struct.unpack('B',data)
        buffer.append(temp[0])
    file_in.close()

    #parse koala
    myGlobals.koala_bitmap    = buffer[2                  :2+8000]
    myGlobals.koala_col12     = buffer[2+8000             :2+8000+1000]
    myGlobals.koala_col3      = buffer[2+8000+1000        :2+8000+1000+1000]
    myGlobals.koala_bg        = buffer[2+8000+1000+1000   :2+8000+1000+1000+1][0]

    koala_to_image()


    

def update_infos_preview():
    #writes:
    #myGlobals.editorimage_posx, myGlobals.editorimage_posy
    #myGlobals.block_x, myGlobals.block_y
    
    factor_x = myGlobals.GRID_SIZE[myGlobals.zoom_preview]/myGlobals.PREVIEWSIZE_DIV_X[myGlobals.user_previewsize.get()]
    factor_y = myGlobals.GRID_SIZE[myGlobals.zoom_preview]/myGlobals.PREVIEWSIZE_DIV_Y[myGlobals.user_previewsize.get()]
    
    cursorx = int(myGlobals.mouse_posx/factor_x)
    cursory = int(myGlobals.mouse_posy/factor_y)
    
    #sanity checks:
    if (cursorx <0 ) : cursorx = 0
    if (cursory <0 ) : cursory = 0
    if (cursorx >159 ) : cursorx = 159
    if (cursory >199 ) : cursory = 199
        
    myGlobals.block_x = int(cursorx/myGlobals.BITMAP_PIXEL_X)
    myGlobals.block_y = int(cursory/myGlobals.BITMAP_PIXEL_Y)


    myGlobals.cursorx_variable.set(cursorx)
    myGlobals.cursory_variable.set(cursory)
    myGlobals.blockx_variable.set(myGlobals.block_x)
    myGlobals.blocky_variable.set(myGlobals.block_y)
    myGlobals.editorimage_posx_variable.set(myGlobals.editorimage_posx)
    myGlobals.editorimage_posy_variable.set(myGlobals.editorimage_posy)
    myGlobals.mousex_variable.set(myGlobals.mouse_posx)
    myGlobals.mousey_variable.set(myGlobals.mouse_posy)
    
    #print("preview cursorx=",cursorx," cursory=",cursory)
    #print("preview block_x=",myGlobals.block_x," block_y=",myGlobals.block_y, "editorimage_posx=",myGlobals.editorimage_posx," editorimage_posy=",myGlobals.editorimage_posy)





def update_infos():
    #writes:
    #myGlobals.cursorx_variable, myGlobals.cursory_variable
    #myGlobals.blockx_variable, myGlobals.blocky_variable
    #myGlobals.editorimage_posx_variable, myGlobals.editorimage_posy_variable
    #myGlobals.mousex_variable, myGlobals.mousey_variable
    #myGlobals.used_color_bg, myGlobals.used_color_col1, myGlobals.used_color_col2, myGlobals.used_color_col3
    #myGlobals.editorimage_posx, myGlobals.editorimage_posy
    #myGlobals.block_x, myGlobals.block_y
    #myGlobals.radiobutton_replace_bg, myGlobals.radiobutton_replace_col1, myGlobals.radiobutton_replace_col2, myGlobals.radiobutton_replace_col3
    #myGlobals.radiobutton_current_bg, myGlobals.radiobutton_current_col1, myGlobals.radiobutton_current_col2, myGlobals.radiobutton_current_col3
    #myGlobals.undo_variable

    myGlobals.undo_variable.set(len(myGlobals.undo_stack))

    #factor_x = myGlobals.GRID_SIZE[myGlobals.zoom] / myGlobals.EDITORSIZE_DIV_X[0]
    #factor_y = myGlobals.GRID_SIZE[myGlobals.zoom] / myGlobals.EDITORSIZE_DIV_Y[0]
    #debug
    factor_x = myGlobals.GRID_SIZE[myGlobals.zoom] / myGlobals.EDITORSIZE_DIV_X[myGlobals.user_editorsize.get()]
    factor_y = myGlobals.GRID_SIZE[myGlobals.zoom] / myGlobals.EDITORSIZE_DIV_Y[myGlobals.user_editorsize.get()]

    #https://docs.python.org/3/library/platform.html
    #platform.system() : 'Linux', 'Darwin', 'Java', 'Windows'
    if (myGlobals.operating_system == 'Darwin') :
        adjustx=-4
        adjusty=-6
    else:
        adjustx=-2
        adjusty=-2

    
    cursorx = int( ((myGlobals.mouse_posx+adjustx)/factor_x) + (myGlobals.editorimage_posx*myGlobals.BITMAP_PIXEL_X) )
    cursory = int( ((myGlobals.mouse_posy+adjusty)/factor_y) + (myGlobals.editorimage_posy*myGlobals.BITMAP_PIXEL_Y) )
    
    #sanity checks:
    if (cursorx <0 ) : cursorx = 0
    if (cursory <0 ) : cursory = 0
    if (cursorx >159 ) : cursorx = 159
    if (cursory >199 ) : cursory = 199
        
    myGlobals.block_x = int(cursorx / myGlobals.BITMAP_PIXEL_X)
    myGlobals.block_y = int(cursory / myGlobals.BITMAP_PIXEL_Y)

    myGlobals.cursorx_variable.set(cursorx)
    myGlobals.cursory_variable.set(cursory)
    myGlobals.blockx_variable.set(myGlobals.block_x)
    myGlobals.blocky_variable.set(myGlobals.block_y)
    myGlobals.editorimage_posx_variable.set(myGlobals.editorimage_posx)
    myGlobals.editorimage_posy_variable.set(myGlobals.editorimage_posy)
    myGlobals.mousex_variable.set(myGlobals.mouse_posx)
    myGlobals.mousey_variable.set(myGlobals.mouse_posy)


    #update all color-buttons
    col_bg = myGlobals.koala_bg
    col1 = int(myGlobals.koala_col12[(myGlobals.block_y*40)+myGlobals.block_x] >> 4)
    col2 = myGlobals.koala_col12[(myGlobals.block_y*40)+myGlobals.block_x]& 0b00001111
    col3 = myGlobals.koala_col3[(myGlobals.block_y*40)+myGlobals.block_x]& 0b00001111
    
    myGlobals.used_color_bg.set(col_bg)
    myGlobals.used_color_col1.set(col1)
    myGlobals.used_color_col2.set(col2)
    myGlobals.used_color_col3.set(col3)

    mycolor = '#%02x%02x%02x' % (
        myGlobals.PALETTEDATA_PEPTO[col_bg*3+0],
        myGlobals.PALETTEDATA_PEPTO[col_bg*3+1],
        myGlobals.PALETTEDATA_PEPTO[col_bg*3+2]
    )
    myGlobals.radiobutton_replace_bg.configure(background=mycolor)
    myGlobals.radiobutton_replace_bg.configure(activebackground=mycolor)
    myGlobals.radiobutton_replace_bg.configure(selectcolor=mycolor)
    myGlobals.radiobutton_current_bg.configure(background=mycolor)
    myGlobals.radiobutton_current_bg.configure(activebackground=mycolor)
    myGlobals.radiobutton_current_bg.configure(selectcolor=mycolor)

    mycolor = '#%02x%02x%02x' % (
        myGlobals.PALETTEDATA_PEPTO[col1*3+0],
        myGlobals.PALETTEDATA_PEPTO[col1*3+1],
        myGlobals.PALETTEDATA_PEPTO[col1*3+2]
    )
    myGlobals.radiobutton_replace_col1.configure(background=mycolor)
    myGlobals.radiobutton_replace_col1.configure(activebackground=mycolor)
    myGlobals.radiobutton_replace_col1.configure(selectcolor=mycolor)
    myGlobals.radiobutton_current_col1.configure(background=mycolor)
    myGlobals.radiobutton_current_col1.configure(activebackground=mycolor)
    myGlobals.radiobutton_current_col1.configure(selectcolor=mycolor)

    mycolor = '#%02x%02x%02x' % (
        myGlobals.PALETTEDATA_PEPTO[col2*3+0],
        myGlobals.PALETTEDATA_PEPTO[col2*3+1],
        myGlobals.PALETTEDATA_PEPTO[col2*3+2]
    )
    myGlobals.radiobutton_replace_col2.configure(background=mycolor)
    myGlobals.radiobutton_replace_col2.configure(activebackground=mycolor)
    myGlobals.radiobutton_replace_col2.configure(selectcolor=mycolor)
    myGlobals.radiobutton_current_col2.configure(background=mycolor)
    myGlobals.radiobutton_current_col2.configure(activebackground=mycolor)
    myGlobals.radiobutton_current_col2.configure(selectcolor=mycolor)

    mycolor = '#%02x%02x%02x' % (
        myGlobals.PALETTEDATA_PEPTO[col3*3+0],
        myGlobals.PALETTEDATA_PEPTO[col3*3+1],
        myGlobals.PALETTEDATA_PEPTO[col3*3+2]
    )
    myGlobals.radiobutton_replace_col3.configure(background=mycolor)
    myGlobals.radiobutton_replace_col3.configure(activebackground=mycolor)
    myGlobals.radiobutton_replace_col3.configure(selectcolor=mycolor)
    myGlobals.radiobutton_current_col3.configure(background=mycolor)
    myGlobals.radiobutton_current_col3.configure(activebackground=mycolor)
    myGlobals.radiobutton_current_col3.configure(selectcolor=mycolor)
    
    my_block = myGlobals.block_y*myGlobals.C64_CHAR_WIDTH+myGlobals.block_x
    myGlobals.current_color.set(set_pixel_get_index_at_pixel(my_block, cursorx, cursory))






def mouse_motion_edit_window(event):
    #writes:
    #myGlobals.mouse_posx, myGlobals.mouse_posy

    myGlobals.mouse_posx, myGlobals.mouse_posy = event.x, event.y

    update_infos()

#    label_editor_image.focus_set()
#    if (space_pressed == True) :
#        print ("move!")
#        space_pressed = False





def set_pixel_optimize_palette(my_block):
    col = []
    col.append(myGlobals.koala_bg)
    col.append(myGlobals.koala_col12[my_block] >> 4)
    col.append(myGlobals.koala_col12[my_block] & 0b00001111)
    col.append(myGlobals.koala_col3[my_block] & 0b00001111)

    palette = []
    for x in col:
        if x not in palette:
            palette.append(x)
    
    return palette




def set_pixel_replace_colors(my_block, c, color):
    #myGlobals.koala_bg, myGlobals.koala_col12, myGlobals.koala_col3
    # replace myGlobals.bg, myGlobals.screen or myGlobals.colorram

    #print("replace color: write color ",color, " to index ",c)

    if (c==0) : myGlobals.koala_bg = color; return None
    if (c==1) : myGlobals.koala_col12[my_block] = (myGlobals.koala_col12[my_block] & 0b00001111) + (color << 4); return None
    if (c==2) : myGlobals.koala_col12[my_block] = (myGlobals.koala_col12[my_block] & 0b11110000) + color; return None
    if (c==3) : myGlobals.koala_col3[my_block] = color; return None

    return None


def set_pixel_replace_bitmap(my_block,x,y,c) :
    #myGlobals.koala_bitmap
    #update myGlobals.koala myGlobals.bitmap myGlobals.data
    
    #print("replace bitmap with index=",c)

    SHIFT_LEFT = (
        6,  #0
        4,  #1
        2,  #2
        0   #3
    )

    AND_PRE = (
        0b00111111,  #0
        0b11001111,  #1
        0b11110011,  #2
        0b11111100  #3
    )
    
    bitmap_position_y = (my_block*8)+ (y & 0b00000111)
    bitmap_position_x = x & 0b00000011 #only 0-3
    myGlobals.koala_bitmap[bitmap_position_y] = (myGlobals.koala_bitmap[bitmap_position_y] & AND_PRE[bitmap_position_x]) + (c << SHIFT_LEFT[bitmap_position_x])




def set_pixel_update_preview_block (pos, old_color, color) :
    #replace all pixels with old_color with color in this block
    #myGlobals.koala_colorindex_data

    for y in range(0,8) :
        for x in range(0,4) :
            if (myGlobals.koala_colorindex_data[pos+(y*160)+x] == old_color ) :
                myGlobals.koala_colorindex_data[pos+(y*160)+x] = color



def set_pixel__left(posx, posy, color):
    if (myGlobals.user_pencil.get() == "light") :
        if ( (posy & 0b00000001) != 0) : return None
        if ( (posx & 0b00000011) != (posy & 0b00000011)) : return None
    if (myGlobals.user_pencil.get() == "checkerboard") :
        if ( (posx & 0b00000001) != (posy & 0b00000001)) : return None
    if (myGlobals.user_pencil.get() == "xline") :
        if ( (posy & 0b00000001) != 0) : return None
    if (myGlobals.user_pencil.get() == "yline") :
        if ( (posx & 0b00000001) != 0) : return None
    set_pixel(posx, posy, color)



def set_pixel__right(posx, posy, color):
    if (myGlobals.user_pencil.get() == "light") :
        if ( (posy & 0b00000001) != 0) : return None
        if ( ((posx+2) & 0b00000011) != (posy & 0b00000011)) : return None
    if (myGlobals.user_pencil.get() == "checkerboard") :
        if ( (posx & 0b00000001) == (posy & 0b00000001)) : return None
    if (myGlobals.user_pencil.get() == "xline") :
        if ( (posy & 0b00000001) == 0) : return None
    if (myGlobals.user_pencil.get() == "yline") :
        if ( (posx & 0b00000001) == 0) : return None
    set_pixel(posx, posy, color)



def set_pixel(posx, posy, color):
    if (myGlobals.user_drawmode.get() == 'dye') : set_pixel__dye_mode(posx, posy, color); return None
    if (myGlobals.user_drawmode.get() == 'keep') : set_pixel__keep_mode(False,posx, posy, color); return None
    if (myGlobals.user_drawmode.get() == 'replace') : set_pixel__keep_mode(True,posx, posy, color); return None
    if (myGlobals.user_drawmode.get() == 'select') : set_pixel__select_mode(posx, posy, color); return None



def set_pixel_get_best_index_for_color(my_block, color):
    #0 = background, 1=screen1, 2=screen2, 3=colorram, 99=nothing
    if (color==myGlobals.koala_bg) : return 0
    if (color==myGlobals.koala_col12[my_block] >> 4) : return 1
    if (color==myGlobals.koala_col12[my_block] & 0b00001111) : return 2
    if (color==myGlobals.koala_col3[my_block] & 0b00001111) : return 3
    return False

def set_pixel_get_color_by_index(my_block, index):
    if (index==0) : return myGlobals.koala_bg
    if (index==1) : return (myGlobals.koala_col12[my_block] >> 4)
    if (index==2) : return (myGlobals.koala_col12[my_block] & 0b00001111)
    if (index==3) : return (myGlobals.koala_col3[my_block] & 0b00001111)
    return False




def set_pixel__select_mode(posx, posy, color):
    undo_save_already_done = False
    my_block = myGlobals.block_y*myGlobals.C64_CHAR_WIDTH+myGlobals.block_x
    user_replace_this = myGlobals.user_replace_color.get()    #0 = background, 1=screen1, 2=screen2, 3=colorram, 99=nothing

    flag_new_colors = False
    flag_new_bitmap = False

    # deal with colors
    if ( user_replace_this == 99) :
        #do not overwrite anything
        replace_this = set_pixel_get_best_index_for_color(my_block, color)   #0 = background, 1=screen1, 2=screen2, 3=colorram, 99=nothing
        if (replace_this is False) : return None   # 99=color not found: drawing not possible -> so exiting
    else :
        #if this is a new color: overwrite a color
        if (color != set_pixel_get_color_by_index(my_block, user_replace_this) ) :
            flag_new_colors = True
        replace_this = user_replace_this
    
    #check if old and new bitmap matrices differ
    if (set_pixel_get_index_at_pixel(my_block, posx, posy) != replace_this) : flag_new_bitmap = True

    #exit if colors or bitmap are not new
    if (flag_new_colors == False) & (flag_new_bitmap == False) : return None

    # update colors and bitmap
    undo_save();
    if (flag_new_colors == True) : set_pixel_replace_colors(my_block, replace_this, color) # replace bg, screen or colorram
    if (flag_new_bitmap == True) : set_pixel_replace_bitmap(my_block, posx, posy, replace_this)   #update koala bitmap data
    
    # update preview
    if ( user_replace_this == 0):
        koala_to_image()    #background is changed: convert whole koala to image again
    else :
        koala_to_image_single_block(myGlobals.block_x, myGlobals.block_y)   #update preview image only for this block (faster than converting whole koala to image again)

    refresh_prepare()
    update_infos()




def set_pixel__dye_mode(posx, posy, color):
    undo_save_already_done = False
    my_block = myGlobals.block_y*myGlobals.C64_CHAR_WIDTH+myGlobals.block_x
    user_replace_this = myGlobals.user_replace_color.get()    #0 = background, 1=screen1, 2=screen2, 3=colorram, 99=nothing

    replace_this = set_pixel_get_index_at_pixel(my_block, posx, posy)

    if (color == set_pixel_get_color_by_index(my_block, replace_this)) : return None

    # update colors
    undo_save();
    set_pixel_replace_colors(my_block, replace_this, color) # replace bg, screen or colorram
    
    # update preview
    if ( replace_this == 0):
        koala_to_image()    #background is changed: convert whole koala to image again
    else :
        koala_to_image_single_block(myGlobals.block_x, myGlobals.block_y)   #update preview image only for this block (faster than converting whole koala to image again)

    refresh_prepare()
    update_infos()




def set_pixel_get_index_at_pixel(my_block, x,y) :
    # find out what (bg, screen1, screen2 or colram) this color uses
    SHIFT_RIGHT = (
        6,  #0
        4,  #1
        2,  #2
        0   #3
    )

    bitmap_position_y = (my_block*8)+ (y & 0b00000111)
    bitmap_position_x = x & 0b00000011 #only 0-3
    return (myGlobals.koala_bitmap[bitmap_position_y] >> SHIFT_RIGHT[bitmap_position_x]) & 0b00000011 #only 0-3
    

def set_pixel_color_is_used_in_block(my_block, color_type):
    for y in range (0,8) :
        for x in range (0,4) :
            if (color_type == set_pixel_get_index_at_pixel(my_block, x,y)) :
                return True
    # not found
    return False



def set_pixel_fill_used_array(my_block):
    my_type = (
        1,  #screen1
        2,  #screen2
        3   #colram
    )
    
    used = []
    
    for col in my_type :
        used.append(set_pixel_color_is_used_in_block(my_block, col))

    return used





def set_pixel__keep_mode(okay_to_overwrite, posx, posy, color):
    #writes: myGlobals.user_replace_color
    undo_save_already_done = False

    my_block = myGlobals.block_y*myGlobals.C64_CHAR_WIDTH+myGlobals.block_x

    flag_new_colors = False
    flag_new_bitmap = False

    used_array = set_pixel_fill_used_array(my_block)
    
    used_colors = 0
    for a in used_array :
        if (a == True): used_colors += 1
    
    index_here = set_pixel_get_index_at_pixel(my_block, posx ,posy)
    index_new = set_pixel_get_best_index_for_color(my_block, color)   #0 = background, 1=screen1, 2=screen2, 3=colorram, 99=nothing

#    print("")
#    print("index_new=",index_new)
    if (index_new is False) :
        #print ("no matching color found:")

        if (used_colors > 2) :
            #print ("-too many colours:")
            
            if ( okay_to_overwrite == False ) :
                #print ("--overwriting color not allowed: giving up")
                return None
                
            else :
                #print ("--just overwriting color")
                # find out what (bg, screen1, screen2 or colram) this color uses
                myGlobals.user_replace_color.set(index_here)
                if (index_here == 0) :
                    #print("11 not replacing background color!")
                    return None
                else :
                    #print ("---index here=",index_here," / color=",color)
                    flag_new_colors = True
                    index_new = index_here

                    #update preview image only for this block (faster than converting whole koala to image again)
#                    pos = myGlobals.block_y * 8 * 160 + (myGlobals.block_x * 4)
#                    set_pixel_update_preview_block(pos, old_color, color)   #replace all pixels with old_color with color in this block

        else :
            # no matching color found, so reorganize bitmap and add a new color
            #print ("-reorganize bitmap and add a new color")
            
            for a in range(0,len(used_array)) :
                if (used_array[a] == False) : 
                    break
            a += 1        
#            print('free color at ',a)
            flag_new_colors = True
            flag_new_bitmap = True
            index_new = a
    else :
        #print ("matching color found")
        if (index_new == index_here) : return None     #same color. nothing to do.
        #print ("- just update bitmap")
        flag_new_bitmap = True



    if ((flag_new_colors == False) & (flag_new_bitmap == False)) :
        #print ("Nothing to do")
        return None

    undo_save();
    if (flag_new_colors == True): set_pixel_replace_colors(my_block, index_new, color) # replace bg, screen or colorram
    if (flag_new_bitmap == True): set_pixel_replace_bitmap(my_block, posx, posy ,index_new)
    
    #update preview
    koala_to_image_single_block(myGlobals.block_x, myGlobals.block_y)   #update preview image only for this block (faster than converting whole koala to image again)
    refresh_prepare()
    update_infos()



        



def mouse_left_button_editor(event):
    #writes: myGlobals.mouse_posx, myGlobals.mouse_posy
    myGlobals.mouse_posx, myGlobals.mouse_posy = event.x, event.y
    update_infos()
    
    if (myGlobals.editor_mode == 'marker_start') :
        marker_start()
        return None

    if (myGlobals.editor_mode == 'marker_end') :
        marker_end()
        return None
        
    if (myGlobals.editor_mode == 'edit') :
        set_pixel__left(myGlobals.cursorx_variable.get(), myGlobals.cursory_variable.get(), myGlobals.user_drawcolor_left.get())


def mouse_right_button(event):
    #writes: myGlobals.mouse_posx, myGlobals.mouse_posy
    myGlobals.mouse_posx, myGlobals.mouse_posy = event.x, event.y
    update_infos()
    set_pixel__right(myGlobals.cursorx_variable.get(), myGlobals.cursory_variable.get(), myGlobals.user_drawcolor_right.get())


def mouse_middle_button_release(event):
    #writes: myGlobals.label_editor_image
    myGlobals.canvas_editor.config(cursor=myGlobals.CURSOR_EDIT)
    
def mouse_middle_button_press(event):
    #writes: myGlobals.block_x_absolute, myGlobals.block_y_absolute
    #writes: myGlobals.label_editor_image
    
    myGlobals.canvas_editor.config(cursor=myGlobals.CURSOR_MOVE)

    factor_x = myGlobals.GRID_SIZE[myGlobals.zoom] / myGlobals.EDITORSIZE_DIV_X[myGlobals.user_editorsize.get()]
    factor_y = myGlobals.GRID_SIZE[myGlobals.zoom] / myGlobals.EDITORSIZE_DIV_Y[myGlobals.user_editorsize.get()]
 
    myGlobals.block_x_absolute = int( (myGlobals.mouse_posx / factor_x / myGlobals.BITMAP_PIXEL_X) )
    myGlobals.block_y_absolute = int( (myGlobals.mouse_posy / factor_y / myGlobals.BITMAP_PIXEL_Y) )


def mouse_middle_button_motion(event):
    #writes: myGlobals.mouse_posx, myGlobals.mouse_posy
    #writes: myGlobals.editorimage_posx, myGlobals.editorimage_posy
    #writes: myGlobals.block_x_absolute, myGlobals.block_y_absolute
    
    myGlobals.mouse_posx, myGlobals.mouse_posy = event.x, event.y
    update_infos()
    
    old_x = myGlobals.block_x_absolute
    old_y = myGlobals.block_y_absolute

    factor_x = myGlobals.GRID_SIZE[myGlobals.zoom] / myGlobals.EDITORSIZE_DIV_X[myGlobals.user_editorsize.get()]
    factor_y = myGlobals.GRID_SIZE[myGlobals.zoom] / myGlobals.EDITORSIZE_DIV_Y[myGlobals.user_editorsize.get()]
 
    myGlobals.block_x_absolute = int( (myGlobals.mouse_posx / factor_x / myGlobals.BITMAP_PIXEL_X) )
    myGlobals.block_y_absolute = int( (myGlobals.mouse_posy / factor_y / myGlobals.BITMAP_PIXEL_Y) )
  
    diff_x = old_x - myGlobals.block_x_absolute
    diff_y = old_y - myGlobals.block_y_absolute
    

    if (
        (abs(diff_x) != 0) |
        (abs(diff_y) != 0)
    ) :
        myGlobals.editorimage_posx += diff_x
        myGlobals.editorimage_posy += diff_y
        refresh_show()
        

    




def zoom_perform() :
    #writes: myGlobals.editorimage_posx, myGlobals.editorimage_posy

    zoom_center_x = myGlobals.block_x
    zoom_center_y = myGlobals.block_y

    if (myGlobals.zoom==0) :
        myGlobals.editorimage_posx = int( zoom_center_x- myGlobals.C64_CHAR_WIDTH/1 )
        myGlobals.editorimage_posy = int( zoom_center_y- myGlobals.C64_CHAR_HEIGHT/1 )
    if (myGlobals.zoom==1) :
        myGlobals.editorimage_posx = int( zoom_center_x- myGlobals.C64_CHAR_WIDTH/2 )
        myGlobals.editorimage_posy = int( zoom_center_y- myGlobals.C64_CHAR_HEIGHT/2 )
    if (myGlobals.zoom==2) :
        myGlobals.editorimage_posx = int( zoom_center_x- myGlobals.C64_CHAR_WIDTH/4 )
        myGlobals.editorimage_posy = int( zoom_center_y- myGlobals.C64_CHAR_HEIGHT/4 )
    if (myGlobals.zoom==3) :
        myGlobals.editorimage_posx = int( zoom_center_x- myGlobals.C64_CHAR_WIDTH/8 )
        myGlobals.editorimage_posy = int( zoom_center_y- myGlobals.C64_CHAR_HEIGHT/8 )
    if (myGlobals.zoom==4) :
        myGlobals.editorimage_posx = int( zoom_center_x- myGlobals.C64_CHAR_WIDTH/16 )
        myGlobals.editorimage_posy = int( zoom_center_y- myGlobals.C64_CHAR_HEIGHT/16 )

    refresh_prepare()
    #print("zoom=",myGlobals.zoom)
    #print("block_x=",myGlobals.block_x," block_y=",myGlobals.block_y, "editorimage_posx=",myGlobals.editorimage_posx," editorimage_posy=",myGlobals.editorimage_posy)
    update_infos()


def zoom_in(self) :
    #writes: myGlobals.zoom
    
    if (myGlobals.zoom < 4) :
        myGlobals.zoom += 1
        zoom_perform()


def zoom_out(self) :
    #writes: myGlobals.zoom
    
    if (myGlobals.zoom > 0) :
        myGlobals.zoom -= 1
        zoom_perform()



def mouse_wheel(event):
    if (
        (event.num == 5) |
        (int(event.delta / 120) == -1) |
        (event.delta == -1)
    ) :
        #mouse wheel down
        zoom_out(0)

    if (
        (event.num == 4) |
        (int(event.delta / 120) == 1) |
        (event.delta == 1)
    ) :
        #mouse wheel up
        zoom_in(0)



def OpenFile_from_menu():
    OpenFile(None)
    
def OpenFile(self):
    ftypes = [('Image Files', '*.koa *.kla')]
    load_filename = tkinter.filedialog.askopenfilename(filetypes = ftypes)
    if not load_filename : return None
    
    loadFile(load_filename)
    return None


def shorten_filename (filename) :
    if (len(filename) > 20) :
        return "..."+filename[-20:]
    else :
        return filename

def set_title():
    myGlobals.root.title(myGlobals.PROGNAME+" \""+shorten_filename(myGlobals.current_filename)+"\"")

def loadFile(filename):
    #writes: myGlobals.current_filename
    #writes: myGlobals.undo_stack
    
    myGlobals.current_filename = filename
    set_title()
    load_koala(filename)
    myGlobals.undo_stack = []
    update_infos()
    refresh_prepare()


def undo_save():
    #writes: myGlobals.undo_stack

    my_block = myGlobals.block_y*myGlobals.C64_CHAR_WIDTH+myGlobals.block_x
    
    my_undo = []
    my_undo.append(myGlobals.block_x)
    my_undo.append(myGlobals.block_y)
    my_undo.append(myGlobals.koala_col12[my_block])
    my_undo.append(myGlobals.koala_col3[my_block])
    my_undo.append(myGlobals.koala_bitmap[ (my_block*8) : ((my_block+1)*8) ])
 
    myGlobals.undo_stack.append(my_undo)
    update_infos()



def undo_undo_from_menu():
    undo_undo(None)
    
def undo_undo(self):
    #writes: myGlobals.undo_stack
    
    if (len(myGlobals.undo_stack)>0) :
        value = myGlobals.undo_stack.pop()

        undo_x = value[0]
        undo_y = value[1]
        undo_col12 = value[2]
        undo_col3 = value[3]
        undo_bitmap = value[4]

        my_block = undo_y*myGlobals.C64_CHAR_WIDTH+undo_x
        
        myGlobals.koala_col12[my_block] = undo_col12
        myGlobals.koala_col3[my_block] = undo_col3
        for y in range(0,8) :
            myGlobals.koala_bitmap[(my_block*8)+y] = undo_bitmap[y]
        koala_to_image_single_block(undo_x,undo_y)
        refresh_prepare()
        update_infos()



def marker_select_from_menu () :
    marker_select(None)

def marker_select(self):
    #writes: myGlobals.editor_mode
    myGlobals.editor_mode = 'marker_start'
    myGlobals.canvas_editor.config(cursor=myGlobals.CURSOR_MARKER_START)

    myGlobals.marker_height = 0
    myGlobals.marker_width = 0
    koala_to_image()
    refresh_prepare()
    refresh_show()



def marker_start():
    #writes: myGlobals.editor_mode
    #writes: myGlobals.marker_posx, myGlobals.marker_posy

    myGlobals.editor_mode = 'marker_end'
    myGlobals.canvas_editor.config(cursor=myGlobals.CURSOR_MARKER_END)
    myGlobals.marker_posx = myGlobals.block_x
    myGlobals.marker_posy = myGlobals.block_y

def marker_end():
    #writes: myGlobals.editor_mode
    #writes: myGlobals.marker_width, myGlobals.marker_height
    
    myGlobals.editor_mode = 'edit'
    myGlobals.canvas_editor.config(cursor=myGlobals.CURSOR_EDIT)
    
    myGlobals.marker_width = myGlobals.block_x - myGlobals.marker_posx
    myGlobals.marker_height = myGlobals.block_y - myGlobals.marker_posy
    refresh_prepare()
    refresh_show()


def buffer_copy_data():
    #writes: myGlobals.buffer_bitmap, myGlobals.buffer_col12, myGlobals.buffer_col3
    #writes: myGlobals.buffer_width, myGlobals.buffer_height, myGlobals.buffer_posx, myGlobals.buffer_posy
    
    myGlobals.buffer_posx = myGlobals.marker_posx
    myGlobals.buffer_posy = myGlobals.marker_posy
    myGlobals.buffer_width = myGlobals.marker_width
    myGlobals.buffer_height = myGlobals.marker_height
    
    for y in range(0, myGlobals.marker_height+1) :
        for x in range(0, myGlobals.marker_width+1) :
            block = (myGlobals.marker_posy+y)*myGlobals.C64_CHAR_WIDTH+(myGlobals.marker_posx+x)
            myGlobals.buffer_col12[block] = myGlobals.koala_col12[block]
            myGlobals.buffer_col3[block] = myGlobals.koala_col3[block]
            for c in range(0,8) :
                myGlobals.buffer_bitmap[block*8+c] = myGlobals.koala_bitmap[block*8+c]


def marker_reset():
    #writes: myGlobals.marker_posx, myGlobals.marker_posy, myGlobals.marker_width, myGlobals.marker_height
    myGlobals.marker_posx = 0
    myGlobals.marker_posy = 0
    myGlobals.marker_width = 0
    myGlobals.marker_height = 0

def buffer_copy_from_menu():
    buffer_copy(None)
    
def buffer_copy(self):
    buffer_copy_data()
    marker_reset()
    koala_to_image()
    refresh_prepare()


def buffer_paste_from_menu():
    buffer_paste(None)
    
def buffer_paste(self):
    #writes: myGlobals.koala_bitmap, myGlobals.koala_col12, myGlobals.koala_col3

    for y in range(0, myGlobals.buffer_height+1) :
        for x in range(0, myGlobals.buffer_width+1) :
            if (
             ((myGlobals.block_y+y) < myGlobals.C64_CHAR_HEIGHT) &
             ((myGlobals.block_x+x) < myGlobals.C64_CHAR_WIDTH)
            ) :
                block_src = (myGlobals.buffer_posy+y) * myGlobals.C64_CHAR_WIDTH + (myGlobals.buffer_posx+x)
                block_dst = (myGlobals.block_y+y) * myGlobals.C64_CHAR_WIDTH + (myGlobals.block_x+x)
                myGlobals.koala_col12[block_dst] = myGlobals.buffer_col12[block_src]
                myGlobals.koala_col3[block_dst] = myGlobals.buffer_col3[block_src]
                for c in range(0,8) :
                    myGlobals.koala_bitmap[block_dst*8+c] = myGlobals.buffer_bitmap[block_src*8+c]

    koala_to_image()
    refresh_prepare()

def buffer_cut_from_menu():
    buffer_cut(None)
    
def buffer_cut(self):
    #writes: myGlobals.koala_bitmap
    
    if (
     (myGlobals.marker_height == 0) | (myGlobals.marker_width == 0)
    ) : return None
    
    buffer_copy_data()
    
    for y in range(0,myGlobals.marker_height+1) :
        for x in range(0,myGlobals.marker_width+1) :
            for c in range(0,8) :
                block = (myGlobals.marker_posy+y)*myGlobals.C64_CHAR_WIDTH+(myGlobals.marker_posx+x)
                myGlobals.koala_bitmap[block*8+c] = 0  #background color

    marker_reset()
    koala_to_image()
    refresh_prepare()



def draw_new_image():
    #writes: myGlobals.current_filename
    #writes: myGlobals.koala_bitmap, myGlobals.koala_bg, myGlobals.koala_col12, myGlobals.koala_col3

    current_filename = "new.koa"

    set_title()

    myGlobals.koala_bitmap=[0]*8000
    myGlobals.koala_col12=[0]*1000
    myGlobals.koala_col3=[0]*1000
    myGlobals.koala_bg=0

    koala_to_image()

    #create palette
    #myGlobals.koala_image.putpalette(myGlobals.PALETTEDATA_COLODORE)
    #myGlobals.koala_image.putdata(myGlobals.koala_colorindex_data)

    refresh_prepare()
    refresh_show() 



def SaveFile_from_menu():
    SaveFile(None)

def SaveFile(self):
    #writes: myGlobals.user_filename_save
    #writes: myGlobals.current_filename
    
    user_filename_save = ""

    try:
        var_start_address = int (myGlobals.user_start_address.get(),16)
    except ValueError:
        var_start_address = 0
    var_start_address_checkbutton = myGlobals.user_start_address_checkbutton.get()

    #sanity checks
    sanity_check = True
    if (
        (var_start_address > 0xffff) &
        (var_start_address_checkbutton)
    ) :
        myGlobals.textbox.insert(tk.END, "*** error: Start address has to be 0-65535 (2bytes).\n")
        sanity_check = False


    user_filename_save = tkinter.filedialog.asksaveasfilename(
        defaultextension='.koa',
        filetypes=[("koala", '*.koa')],
        initialfile=os.path.basename(myGlobals.current_filename),
        title="Choose filename"
    )

#     initialdir=self.default_path_to_pref,

    if not user_filename_save : return None

    #convert()

    #write stuff...
    file_out = open(user_filename_save , "wb")

    out_buffer = []
    
    #start address
    if var_start_address_checkbutton :
        i=var_start_address & 0xff  #low
        out_buffer.append(i)
        i=var_start_address >> 8    #high
        out_buffer.append(i)
        
    #koala data
    for i in range(0,8000):
        out_buffer.append(myGlobals.koala_bitmap[i])
    for i in myGlobals.koala_col12:
        out_buffer.append(i)
    for i in myGlobals.koala_col3:
        out_buffer.append(i)
    out_buffer.append(myGlobals.koala_bg)
    
    file_out.write(bytearray(out_buffer))
    file_out.close()
    
    myGlobals.current_filename = user_filename_save
    set_title()
    
    return None


def root_refresh() :
    #writes: myGlobals.frame_replace_color
    
    if (myGlobals.user_drawmode.get() == 'select') : 
        myGlobals.frame_replace_color.grid()
    else :
        myGlobals.frame_replace_color.grid_remove()
    



def user_set_drawcolor_left(number):
    if (number==0) : myGlobals.user_drawcolor_left.set(myGlobals.used_color_bg.get()); return None
    if (number==1) : myGlobals.user_drawcolor_left.set(myGlobals.used_color_col1.get()); return None
    if (number==2) : myGlobals.user_drawcolor_left.set(myGlobals.used_color_col2.get()); return None
    if (number==3) : myGlobals.user_drawcolor_left.set(myGlobals.used_color_col3.get()); return None

def user_set_drawcolor_right(number):
    if (number==0) : myGlobals.user_drawcolor_right.set(myGlobals.used_color_bg.get()); return None
    if (number==1) : myGlobals.user_drawcolor_right.set(myGlobals.used_color_col1.get()); return None
    if (number==2) : myGlobals.user_drawcolor_right.set(myGlobals.used_color_col2.get()); return None
    if (number==3) : myGlobals.user_drawcolor_right.set(myGlobals.used_color_col3.get()); return None

"""
def keyboard_shift_f5(self):
    myGlobals.user_replace_color.set(1)
def keyboard_shift_f6(self):
    myGlobals.user_replace_color.set(2)
def keyboard_shift_f7(self):
    myGlobals.user_replace_color.set(3)
def keyboard_shift_f8(self):
    myGlobals.user_replace_color.set(0)
"""

def keyboard_special_modifier_pressed(self):
    myGlobals.special_modifier_pressed = True
def keyboard_special_modifier_released(self):
    myGlobals.special_modifier_pressed = False

#keyboard shortcuts
#def keyboard_space(self):
#    if (str(myGlobals.my_focus) == ".!frame.!frame.!frame.!label2") :
#        myGlobals.space_pressed = True
#        #print("space")

def scroll_right(self):
    myGlobals.editorimage_posx -= 1
    refresh_show()
    update_infos()
def scroll_left(self):
    myGlobals.editorimage_posx += 1
    refresh_show()
    update_infos()
def scroll_down(self):
    myGlobals.editorimage_posy -= 1
    refresh_show()
    update_infos()
def scroll_up(self):
    myGlobals.editorimage_posy += 1
    refresh_show()
    update_infos()

def keyboard_all(event):
    switcher = {
        'm' : (marker_select,0),
        'space' : (myGlobals.user_replace_color.set,99),
        'F1' : (user_set_drawcolor_left,1),
        'F2' : (user_set_drawcolor_left,2),
        'F3' : (user_set_drawcolor_left,3),
        'F4' : (user_set_drawcolor_left,0),
        'F5' : (myGlobals.user_replace_color.set,1),
        'F6' : (myGlobals.user_replace_color.set,2),
        'F7' : (myGlobals.user_replace_color.set,3),
        'F8' : (myGlobals.user_replace_color.set,0),
        '0' : (myGlobals.user_drawcolor_left.set,0),
        '1' : (myGlobals.user_drawcolor_left.set,1),
        '2' : (myGlobals.user_drawcolor_left.set,2),
        '3' : (myGlobals.user_drawcolor_left.set,3),
        '4' : (myGlobals.user_drawcolor_left.set,4),
        '5' : (myGlobals.user_drawcolor_left.set,5),
        '6' : (myGlobals.user_drawcolor_left.set,6),
        '7' : (myGlobals.user_drawcolor_left.set,7),
        '8' : (myGlobals.user_drawcolor_left.set,8),
        '9' : (myGlobals.user_drawcolor_left.set,9),
        'a' : (myGlobals.user_drawcolor_left.set,10),
        'b' : (myGlobals.user_drawcolor_left.set,11),
        'c' : (myGlobals.user_drawcolor_left.set,12),
        'd' : (myGlobals.user_drawcolor_left.set,13),
        'e' : (myGlobals.user_drawcolor_left.set,14),
        'f' : (myGlobals.user_drawcolor_left.set,15),
        'equal' : (myGlobals.user_drawcolor_right.set,0),
        'exclam' : (myGlobals.user_drawcolor_right.set,1),
        'quotedbl' : (myGlobals.user_drawcolor_right.set,2),
        'section' : (myGlobals.user_drawcolor_right.set,3),
        'dollar' : (myGlobals.user_drawcolor_right.set,4),
        'percent' : (myGlobals.user_drawcolor_right.set,5),
        'ampersand' : (myGlobals.user_drawcolor_right.set,6),
        'slash' : (myGlobals.user_drawcolor_right.set,7),
        'parenleft' : (myGlobals.user_drawcolor_right.set,8),
        'parenright' : (myGlobals.user_drawcolor_right.set,9),
        'A' : (myGlobals.user_drawcolor_right.set,10),
        'B' : (myGlobals.user_drawcolor_right.set,11),
        'C' : (myGlobals.user_drawcolor_right.set,12),
        'D' : (myGlobals.user_drawcolor_right.set,13),
        'E' : (myGlobals.user_drawcolor_right.set,14),
        'F' : (myGlobals.user_drawcolor_right.set,15),
        'minus' : (zoom_out,0),
        'plus' : (zoom_in,0),
        'Left' : (scroll_right,0),
        'Right' : (scroll_left,0),
        'Up' : (scroll_down,0),
        'Down' : (scroll_up,0),
    }

    switcher_special = {
        '0' : (myGlobals.user_drawcolor_right.set,0),
        '1' : (myGlobals.user_drawcolor_right.set,1),
        '2' : (myGlobals.user_drawcolor_right.set,2),
        '3' : (myGlobals.user_drawcolor_right.set,3),
        '4' : (myGlobals.user_drawcolor_right.set,4),
        '5' : (myGlobals.user_drawcolor_right.set,5),
        '6' : (myGlobals.user_drawcolor_right.set,6),
        '7' : (myGlobals.user_drawcolor_right.set,7),
        '8' : (myGlobals.user_drawcolor_right.set,8),
        '9' : (myGlobals.user_drawcolor_right.set,9),
        'a' : (myGlobals.user_drawcolor_right.set,10),
        'b' : (myGlobals.user_drawcolor_right.set,11),
        'c' : (myGlobals.user_drawcolor_right.set,12),
        'd' : (myGlobals.user_drawcolor_right.set,13),
        'e' : (myGlobals.user_drawcolor_right.set,14),
        'f' : (myGlobals.user_drawcolor_right.set,15),
    }

    if (myGlobals.special_modifier_pressed == False) :
        val = switcher.get(event.keysym)
    else :
        val = switcher_special.get(event.keysym)

    #if (val == None) : print ('unknown key: char=\"'+event.char+'\" keysym=\"'+event.keysym+'\" num=\"'+event.num+'\"')
    if (val != None) : val[0](val[1])
