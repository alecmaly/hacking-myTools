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
imgHeight = None
imgWidth = None
slices_to_original_cols = None
slices = None

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
    global imgHeight
    global imgWidth
    original_image_path = filedialog.askopenfilename(initialdir= path.dirname(__file__))
    img = Image.open(original_image_path)
    w, h = img.size
    imgWidth = w
    imgHeight = h
    lbl_openimage.configure(text=f"{os.path.basename(original_image_path)}: {w}x{h}")

    spin_widthSlices.configure(to=int(w))
    spin_heightSlices.configure(to=int(h))
    sliceImage()

# int(my_varCropLeft.get()), int(my_varCropTop.get()), int(my_varCropRight.get()), int(my_varCropBottom.get())
@output_message
def generate_output_image():
    global new_img
    global slices
    # img_files = [f for f in listdir(dir_out) if isfile(join(dir_out, f))]
    print(f"Length is {len(slices)}")
    slice = slices[0]
    w, h = slice.size

    images = [slice
                    # .crop((int(my_varCropLeft.get()), int(my_varCropTop.get()), w - int(my_varCropRight.get()), h - int(my_varCropBottom.get())))
                    # .resize((int(w * int(my_varResizeSlicesWidth.get()) / 100), int(h * int(my_varResizeSlicesHeight.get()) / 100)))
                    # .rotate(int(my_varRotateSlices.get()))
                for slice in slices]
    spin_outputImageColumns.configure(to=len(slices))
    num_columns = len(slices) if chk_state_singleRow.get() else int(spin_outputImageColumns.get())

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
    spin_cropSlicesLeft.configure(to=int(spin_widthSlices.get()))
    spin_cropSlicesRight.configure(to=int(spin_widthSlices.get()))
    spin_cropSlicesTop.configure(to=int(spin_heightSlices.get()))
    spin_cropSlicesBottom.configure(to=int(spin_heightSlices.get()))
    generate_output_image()

@output_message
def toggle_single_row():
    if chk_state_singleRow.get() == True:
        spin_outputImageColumns.configure(state = 'disabled')
    else:
        spin_outputImageColumns.configure(state = 'normal')
    generate_output_image()

@output_message
def setMax():
    my_varWidthSlices.set(imgWidth)
    my_varHeightSlices.set(imgHeight)
    chk_state_singleRow.set(True)
    spin_outputImageColumns.configure(state = 'disabled')
    sliceImage()

@output_message
def originalWidthColumns():
    my_varOutputColumns.set(str(int(slices_to_original_cols)))
    generate_output_image()

### Helper Functions
def slice(filepath, dir_out, dh, dw):
    global slices_to_original_cols
    global slices
    slices = []
    
    name, ext = os.path.splitext(os.path.basename(filepath))
    img = Image.open(filepath)
    w, h = img.size
    print(f"Image size: {w}x{h} : cols {w / dw}")
    slices_to_original_cols = w / dw
    
    grid = product(range(0, h-h%dh, dh), range(0, w-w%dw, dw))
    print(range(0, h-h%dh, dh), range(0, w-w%dw, dw))
    
    for i, j in grid:
        # print(i)
        box = (j, i, j+dw, i+dh)
        out = os.path.join(dir_out, f'{name}_{i}_{j}{ext}')
        # img.crop(box).save(out)
        a = (img
            .crop(box)
            .crop((int(my_varCropLeft.get()), int(my_varCropTop.get()), dw - int(my_varCropRight.get()), dh - int(my_varCropBottom.get())))
            .resize((int(dw * int(my_varResizeSlicesWidth.get()) / 100), int(dh * int(my_varResizeSlicesHeight.get()) / 100)))
            .rotate(int(my_varRotateSlices.get()))
        )
        # slices.append(img.crop(box))
        slices.append(a)

def image_grid(imgs, cols):
    rows = int(len(imgs) / cols)
    w, h = imgs[0].size
    grid = Image.new('RGB', size=(cols*w, rows*h))
    grid_w, grid_h = grid.size
    
    for i, img in enumerate(imgs):
        grid.paste(img, box=(i%cols*w, i//cols*h))
    return grid

def saveSlices():
    for f in os.listdir(dir_out):
        os.remove(os.path.join(dir_out, f))

    name, ext = os.path.splitext(os.path.basename(original_image_path))
    for i, slice in enumerate(slices):
        out = os.path.join(dir_out, f'slice_{i}{ext}')
        slice.save(out)
        

def bindFn(event=None):
    sliceImage()

window = Tk()
window.bind('<Return>', bindFn)
gridFrame = Frame(window)
gridFrame.grid()


# Frame Row 1: Input Image Info
buttonGrid = Frame(window)
buttonGrid.grid(sticky=W)

btn = Button(buttonGrid, justify=LEFT, text="Open Image", command=get_image)
btn.grid(column=0, row=0)

lbl_openimage = Label(buttonGrid, text="",font=("Arial Bold", 10))
lbl_openimage.grid(column=1,row=0)

btn = Button(buttonGrid, text="Save Slices", command=saveSlices)
btn.grid(column=3, row=0)


# Frame Row 2: Input Slicing settings
buttonGrid2 = Frame(window, width=500, height=500)
buttonGrid2.grid(sticky=W)

lbl = Label(buttonGrid2, justify=LEFT, text="Slices Width (px)", font=("Arial Bold", 10))
my_varWidthSlices = StringVar(window)
my_varWidthSlices.set("100")
spin_widthSlices = Spinbox(buttonGrid2, from_=0, to=500, increment=1, width=10, textvariable=my_varWidthSlices, validate="focusout", validatecommand=sliceImage, command=sliceImage)
lbl.grid(column=0,row=1)
spin_widthSlices.grid(column=0,row=2)

lbl = Label(buttonGrid2, text="Slices: Height (px)", font=("Arial Bold", 10))
my_varHeightSlices = StringVar(window)
my_varHeightSlices.set("100")
spin_heightSlices = Spinbox(buttonGrid2, from_=0, to=500, increment=1, width=10, textvariable=my_varHeightSlices, validate="focusout", validatecommand=sliceImage, command=sliceImage)
lbl.grid(column=3,row=1)
spin_heightSlices.grid(column=3,row=2)

chk = Button(buttonGrid2, text='Set Max', command=setMax)
chk.grid(column=4, row=2)




# Frame Row 3: Output settings
buttonGrid3 = Frame(window, width=500, height=600)
buttonGrid3.grid(sticky=W)

lbl = Label(buttonGrid3, text="Output Images Columns", font=("Arial Bold", 10))
my_varOutputColumns = StringVar(window)
my_varOutputColumns.set("25")
spin_outputImageColumns = Spinbox(buttonGrid3, from_=1, to=500, increment=1, width=10, textvariable=my_varOutputColumns, command=sliceImage)
lbl.grid(column=0,row=0)
spin_outputImageColumns.grid(column=3,row=0)

chk_state_singleRow = BooleanVar()
chk_state_singleRow.set(False) #set check state
chk = Checkbutton(buttonGrid3, text='Single Row', var=chk_state_singleRow, command=toggle_single_row)
chk.grid(column=3, row=1)


chk = Button(buttonGrid3, text='Approx Original Width', command=originalWidthColumns)
chk.grid(column=4, row=1)




lbl = Label(buttonGrid3, text="Crop Slices (px)", font=("Arial Bold", 10))
lbl.grid(column=0,row=2)
lbl = Label(buttonGrid3, text="left", font=("Arial Bold", 10))
lbl.grid(column=3,row=3)
my_varCropLeft = StringVar(window)
my_varCropLeft.set("0")
spin_cropSlicesLeft = Spinbox(buttonGrid3, from_=0, width=10, textvariable=my_varCropLeft, command=sliceImage)
spin_cropSlicesLeft.grid(column=3, row=2)
my_varCropRight = StringVar(window)
my_varCropRight.set("0")
lbl = Label(buttonGrid3, text="right", font=("Arial Bold", 10))
lbl.grid(column=4,row=3)
spin_cropSlicesRight = Spinbox(buttonGrid3, from_=0, width=10, textvariable=my_varCropRight, command=sliceImage)
spin_cropSlicesRight.grid(column=4, row=2)
my_varCropTop = StringVar(window)
my_varCropTop.set("0")
lbl = Label(buttonGrid3, text="top", font=("Arial Bold", 10))
lbl.grid(column=5,row=3)
spin_cropSlicesTop = Spinbox(buttonGrid3, from_=0, width=10, textvariable=my_varCropTop, command=sliceImage)
spin_cropSlicesTop.grid(column=5, row=2)
my_varCropBottom = StringVar(window)
my_varCropBottom.set("0")
lbl = Label(buttonGrid3, text="bottom", font=("Arial Bold", 10))
lbl.grid(column=6,row=3)
spin_cropSlicesBottom = Spinbox(buttonGrid3, from_=0, width=10, textvariable=my_varCropBottom, command=sliceImage)
spin_cropSlicesBottom.grid(column=6, row=2)


lbl = Label(buttonGrid3, text="Resize (Scale) Slices %", font=("Arial Bold", 10))
lbl.grid(column=0,row=4)
lbl = Label(buttonGrid3, text="width", font=("Arial Bold", 10))
lbl.grid(column=3,row=5)
my_varResizeSlicesWidth = StringVar(window)
my_varResizeSlicesWidth.set("100")
spin_outputResizeSlicesWidth = Spinbox(buttonGrid3, from_=1, to=100, width=10, textvariable=my_varResizeSlicesWidth, command=sliceImage)
spin_outputResizeSlicesWidth.grid(column=3,row=4)
lbl = Label(buttonGrid3, text="height", font=("Arial Bold", 10))
lbl.grid(column=4,row=5)
my_varResizeSlicesHeight = StringVar(window)
my_varResizeSlicesHeight.set("100")
spin_outputResizeSlicesWidth = Spinbox(buttonGrid3, from_=1, to=100, width=10, textvariable=my_varResizeSlicesHeight, command=sliceImage)
spin_outputResizeSlicesWidth.grid(column=4,row=4)



lbl = Label(buttonGrid3, text="Rotate Slices (degrees)", font=("Arial Bold", 10))
my_varRotateSlices = StringVar(window)
my_varRotateSlices.set("0")
spin_outputRotateSlices = Spinbox(buttonGrid3, from_=0, to=360, increment=90, width=10, textvariable=my_varRotateSlices, command=sliceImage)
lbl.grid(column=0,row=6)
spin_outputRotateSlices.grid(column=3,row=6)




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