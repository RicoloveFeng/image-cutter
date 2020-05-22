import argparse, os
from PIL import Image

parser = argparse.ArgumentParser()

parser.add_argument("--mode", "-m", help="cutting mode", choices=["s","l"], default="s")
parser.add_argument("--file", "-f", help="image path", required=True)

args = parser.parse_args()

mode = args.mode
file = args.file

image = Image.open(file)
imageWidth = image.size[0]
imageHeight = image.size[1]
fileFormat = file.split(".")[-1]
folder = "./" + os.path.basename(file)[:-len(fileFormat)-1] + "/"


if mode == "s":
    x1 = max (imageWidth - imageHeight, 0) // 2
    y1 = max (imageHeight - imageWidth, 0) // 2
    x2 = imageWidth - x1
    y2 = imageHeight - y1
    image = image.crop((x1,y1,x2,y2))

else: # mode == "l"
    newsize = max (imageWidth, imageHeight)
    bg = Image.new("RGB", (newsize, newsize), "White")
    x1 = max (newsize - imageWidth, 0) // 2
    y1 = max (newsize - imageHeight, 0) // 2
    bg.paste(image, (x1, y1))
    image = bg

imageWidth = image.size[0]
imageHeight = image.size[1]
dw = imageWidth // 3
dh = imageHeight // 3

if not os.path.exists(folder):
    os.makedirs(folder)

for i in range(3):
    for j in range(3):
        subimg = image.crop(
            (
                dw * j,
                dh * i,
                min(dw * (j + 1), imageWidth),
                min(dh * (i + 1), imageHeight)
            )
        )
        subimg.save(folder +str(i*3 + j + 1) + "." + fileFormat)





