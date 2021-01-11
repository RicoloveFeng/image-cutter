import argparse, os, time
from PIL import Image, ImageDraw


parser = argparse.ArgumentParser()

parser.add_argument("--mode", "-m", help="cutting mode", choices=["s","l","r"], default="s")
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

if mode in ["s","l"]:
    if mode == "s":
        x1 = max (imageWidth - imageHeight, 0) // 2
        y1 = max (imageHeight - imageWidth, 0) // 2
        x2 = imageWidth - x1
        y2 = imageHeight - y1
        image = image.crop((x1,y1,x2,y2))

    elif mode == "l":
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
    pass

elif mode == "r":
    # code by 燃玉 on matlab
    # port by Ricolove
    #assert(fileFormat != "png")
    channelNum = len(image.getpixel((0, 0)))
    lineNum = 90
    lightCoef = 0.3
    lineDis = int(imageHeight / lineNum / 2) * 2 - 1
    lineDisHalf = int((lineDis - 1) / 2)
    lineIndex = lineDisHalf
    
    # debug
    lineCount = 0

    # 图片预加载
    draw = ImageDraw.Draw(image)
    pixels = image.load()

    # 运行计时
    now = time.time()

    # 对每一条斑马色线进行处理
    while lineIndex < imageHeight:
        # 确定色线所占区域
        upperBound = max(lineIndex - lineDisHalf, 0)
        lowerBound = min(lineIndex + lineDisHalf + 1, imageHeight)

        # 对每一列进行处理
        for i in range(imageWidth):
            # 对该列的像素颜色值求和
            pixelSum = [0] * 3
            for j in range(upperBound, lowerBound):
                pixel = pixels[i, j]
                for channel in range(3):
                    pixelSum[channel] += pixel[channel]

            # 算出每个 channel 对应的满颜色的行数
            # 记最后余量所填充的行数是第 N 行, 颜色值总和为 S, 则应该满足：
            # 255 * (2N - 1) = S 
            lightBound = [int((pixelSum[k] + 255) / 511) for k in range(3)]  
            
            # 算出未满颜色行的颜色值
            # TODO: 这是什么意思
            lightColor = [int((pixelSum[k] + 256) % 512 / 2 * lightCoef) for k in range(3)]

            # 针对像素所处位置，分别进行涂色
            def getColorByBound(dis: int, lightBound: list, lightColor: list) -> tuple:
                color = [0] * 3
                for k in range(3):
                    if dis > lightBound[k]:
                        color[k] = 0
                    elif dis == lightBound[k]:
                        color[k] = lightColor[k]
                    else:
                        color[k] = 255
                return color
            
            # 当一行高度很大时，使用ImageDraw.line方法会比单个像素着色快很多
            # 而当高度不大时，直接一个个着色会更快一点
            # 12 这个参数是我随便调的，没有确实地优化过
            if lineDisHalf > 12 or channelNum < 4:
                bounds = sorted(list(set([0, lineDisHalf] + [min(max(x + y, 0), lineDisHalf) for x in lightBound for y in range(-1,2)])))
                for bound in reversed(bounds):
                    color = getColorByBound(bound, lightBound, lightColor)
                    draw.line([i, lineIndex + bound, i, lineIndex - bound], tuple(color))
            else:      
                for j in range(upperBound, lowerBound):
                    distance = abs(j - lineIndex)
                    pixels[i, j] = tuple(getColorByBound(distance, lightBound, lightColor) + [pixels[i, j][3]] if channelNum == 4 else [])
            pass
            
        lineIndex += lineDis
        lineCount += 1
    #debug
    print("time cost:", time.time()-now)
    image.save(folder + "line." + fileFormat)

else:
    print("Using unsupported mode")
    pass