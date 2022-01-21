#/usr/bin/python3

from email.policy import default
from tkinter import *
from tkinter import filedialog
from PIL import ImageTk
import PIL
from PIL import Image
from itertools import product
import os
from os import path, listdir
from os.path import isfile, join


# global variables
dir_out = 'img_slices'
if not os.path.exists(dir_out):
    os.mkdir(dir_out)

new_img = None
original_image_path = None
message = None

### Decorators
def output_message(func):
    def wrapper():
        lbl_message.configure(text = "")
        try:
            func()
        except Exception as e:
            lbl_message.configure(text = e)
    return wrapper


### Button functions
@output_message
def get_image():
    global orig_img
    global original_image_path
    original_image_path = filedialog.askopenfilename(initialdir= path.dirname(__file__))
    img = Image.open(original_image_path)
    w, h = img.size
    lbl_openimage.configure(text=f"{os.path.basename(original_image_path)}: {w}x{h}")

    spin_widthSlices.configure(to=int(w))
    spin_heightSlices.configure(to=int(h))
    sliceImage()


@output_message
def generate_output_image():
    global new_img
    img_files = [f for f in listdir(dir_out) if isfile(join(dir_out, f))]
    print(f"Length is {len(img_files)}")
    images = [PIL.Image.open(os.path.join(dir_out, file)).rotate(int(my_varRotateSlices.get())) for file in img_files]
    spin_outputImageColumns.configure(to=len(img_files))
    num_columns = len(img_files) if chk_state_singleRow.get() else int(spin_outputImageColumns.get())

    grid = image_grid(images, num_columns)
    grid.save("new_grid_image.jpg")

    if new_img:
        new_img.grid_remove()

    img = ImageTk.PhotoImage(Image.open("new_grid_image.jpg"))
    original_img_label = Label(imgFrame, image = img)
    original_img_label.image = img
    original_img_label.grid(row=1, column=0)
    new_img = original_img_label



@output_message
def sliceImage():
    slice(original_image_path, dir_out, int(spin_heightSlices.get()), int(spin_widthSlices.get()))
    generate_output_image()

@output_message
def toggle_single_row():
    if chk_state_singleRow.get() == True:
        spin_outputImageColumns.configure(state = 'disabled')
    else:
        spin_outputImageColumns.configure(state = 'normal')
    generate_output_image()


### Helper Functions
def slice(filepath, dir_out, dh, dw):
    for f in os.listdir(dir_out):
        os.remove(os.path.join(dir_out, f))
 
    name, ext = os.path.splitext(os.path.basename(filepath))
    img = Image.open(filepath)
    w, h = img.size
    print(f"Image size: {w}x{h}")
    
    grid = product(range(0, h-h%dh, dh), range(0, w-w%dw, dw))
    print(range(0, h-h%dh, dh), range(0, w-w%dw, dw))
    
    for i, j in grid:
        # print(i)
        box = (j, i, j+dw, i+dh)
        out = os.path.join(dir_out, f'{name}_{i}_{j}{ext}')
        img.crop(box).save(out)



def image_grid(imgs, cols):
    rows = int(len(imgs) / cols)
    w, h = imgs[0].size
    grid = Image.new('RGB', size=(cols*w, rows*h))
    grid_w, grid_h = grid.size
    
    for i, img in enumerate(imgs):
        grid.paste(img, box=(i%cols*w, i//cols*h))
    return grid

window = Tk()
gridFrame = Frame(window)
gridFrame.grid()


# Frame Row 1: Input Image Info
buttonGrid = Frame(window)
buttonGrid.grid(sticky=W)

btn = Button(buttonGrid, justify=LEFT, text="Open Image", command=get_image)
btn.grid(column=0, row=0)

lbl_openimage = Label(buttonGrid, text="",font=("Arial Bold", 10))
lbl_openimage.grid(column=1,row=0)


# Frame Row 2: Input Slicing settings
buttonGrid2 = Frame(window, width=500, height=500)
buttonGrid2.grid(sticky=W)


lbl = Label(buttonGrid2, justify=LEFT, text="Width Slices (px)", font=("Arial Bold", 10))
my_varWidthSlices = StringVar(window)
my_varWidthSlices.set("100")
spin_widthSlices = Spinbox(buttonGrid2, from_=0, to=500, increment=1, width=10, textvariable=my_varWidthSlices, validate="focusout", validatecommand=sliceImage, command=sliceImage)
lbl.grid(column=0,row=1)
spin_widthSlices.grid(column=0,row=2)

lbl = Label(buttonGrid2, text="Height Slices (px)", font=("Arial Bold", 10))
my_varHeightSlices = StringVar(window)
my_varHeightSlices.set("100")
spin_heightSlices = Spinbox(buttonGrid2, from_=0, to=500, increment=1, width=10, textvariable=my_varHeightSlices, validate="focusout", validatecommand=sliceImage, command=sliceImage)
lbl.grid(column=3,row=1)
spin_heightSlices.grid(column=3,row=2)

# Frame Row 3: Output settings
buttonGrid3 = Frame(window, width=500, height=500)
buttonGrid3.grid(sticky=W)

lbl = Label(buttonGrid3, text="Output Images Columns", font=("Arial Bold", 10))
my_varOutputColumns = StringVar(window)
my_varOutputColumns.set("25")
spin_outputImageColumns = Spinbox(buttonGrid3, from_=1, to=500, increment=1, width=10, textvariable=my_varOutputColumns, command=generate_output_image)
lbl.grid(column=0,row=0)
spin_outputImageColumns.grid(column=3,row=0)

chk_state_singleRow = BooleanVar()
chk_state_singleRow.set(False) #set check state
chk = Checkbutton(buttonGrid3, text='Single Row', var=chk_state_singleRow, command=toggle_single_row)
chk.grid(column=3, row=1)

lbl = Label(buttonGrid3, text="Rotate Slices (degrees)", font=("Arial Bold", 10))
my_varRotateSlices = StringVar(window)
my_varRotateSlices.set("0")
spin_outputRotateSlices = Spinbox(buttonGrid3, from_=0, to=360, increment=90, width=10, textvariable=my_varRotateSlices, command=generate_output_image)
lbl.grid(column=0,row=2)
spin_outputRotateSlices.grid(column=3,row=2)




# Frame Row 4: output image
buttonGrid4 = Frame(window, width=500, height=500)
buttonGrid4.grid()

lbl_message = Label(buttonGrid4, fg='red')
lbl_message.grid(row=0, column=0)


imgFrame = Frame(window, width=500, height=500)
imgFrame.grid()


original_img_label = Label(imgFrame, text = "New Image: new_grid_image.jpg")
original_img_label.grid(row=0, column=0)



window.mainloop()