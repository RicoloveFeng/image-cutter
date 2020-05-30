import argparse, os
from PIL import Image

parser = argparse.ArgumentParser()

parser.add_argument("--mode", "-m", help="cutting mode", choices=["s","l"], default="s")
parser.add_argument("--file", "-f", help="image path", required=True)
parser.add_argument("--gap", "-g", help="consider gap when cutting", choices=[True, False], default=True)

args = parser.parse_args()

mode = args.mode
file = args.file
gap = args.gap

image = Image.open(file)
imageWidth = image.size[0]
imageHeight = image.size[1]
fileFormat = file.split(".")[-1]
folder = "./" + os.path.basename(file)[:-len(fileFormat)-1] + "/"

if not os.path.exists(folder):
    os.makedirs(folder)

if mode == "s":
    x1 = max (imageWidth - imageHeight, 0) // 2
    y1 = max (imageHeight - imageWidth, 0) // 2
    x2 = imageWidth - x1
    y2 = imageHeight - y1
    image = image.crop((x1,y1,x2,y2))

else: # mode == "l"
    newsize = max (imageWidth, imageHeight)
    bg = Image.new("RGBA", (newsize, newsize)) if image.format == "PNG" else Image.new("RGB", (newsize, newsize), "White")
    x1 = max (newsize - imageWidth, 0) // 2
    y1 = max (newsize - imageHeight, 0) // 2
    bg.paste(image, (x1, y1))
    image = bg

gapValue = round(image.size[0] / 422 * 2) if gap else 0
subImageLength = round((image.size[0] - 2 * gapValue) / 3)
imageLength = subImageLength * 3 + gapValue * 2 
image = image.resize((imageLength, imageLength), Image.ANTIALIAS)

for i in range(3):
    for j in range(3):
        subimg = image.crop(
            (
                subImageLength * j + gapValue * j,
                subImageLength * i + gapValue * i,
                subImageLength * (j + 1) + gapValue * j,
                subImageLength * (i + 1) + gapValue * i,
            )
        )
        subimg.save(folder +str(i*3 + j + 1) + "." + fileFormat)
