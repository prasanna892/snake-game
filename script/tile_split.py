# Importing Image class from PIL module
import os
import traceback
from PIL import Image
import numpy as np
tile_size = 42 #[0,0,20,20] [20,0,40,20] [40,0,60,20] [0,20] [20,40] [40,60]
sizec = 3
sizer = 3
lr = []
for i in range(1,sizec+1):
    lr.append((tile_size*(i-1), tile_size*i))
tb = []
for i in range(1,sizer+1):
    tb.append((tile_size*(i-1), tile_size*i))

lst = []
for i in range(len(lr)):
    for j in range(len(tb)):
        lst.append((lr[i][0], tb[j][0], lr[i][1], tb[j][1]))
#lst=[[line * tile_size, line * tile_size, line * tile_size, line * tile_size] for line in range(0, 3)]
print(lst)

# Opens a image in RGB mode
im = Image.open(f"./resource/image/snake.png")

# Size of the image in pixels (size of original image)
# (This is not mandatory)
width, height = im.size
i = 0
for left,top,right,bottom in lst:

    # Cropped image of above dimension
    # (It will not change original image)
    im1 = im.crop((left, top, right, bottom))
    
    #resize
    newsize = (20, 20)
    im1 = im1.resize(newsize)

    #make image transparent
    im1 = im1.convert("RGBA")
    im1np = np.array(im1)
    white = np.sum(im1np[:,:,:3], axis=2)
    white_mask = np.where(white == 0*3, 1, 0)
    alpha = np.where(white_mask, 0, im1np[:,:,-1])
    im1np[:,:,-1] = alpha 
    im1 = Image.fromarray(np.uint8(im1np))

    
    im1.save(f"./resource/image/{i}.png")
    i+=1

