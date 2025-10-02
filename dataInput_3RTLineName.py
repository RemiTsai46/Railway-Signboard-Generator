from main_3RTLineName import title, English, Chinese
from PIL import Image, ImageDraw, ImageFont


#Size
big = 64
mid = 54
small = 48

bgColor = 0 # 0 = black, 1 = white

lineColor = "#b380e6"
titleText = "R1"
titleSize = 48   #big/small/any number(height)
titleNarrow = True #T/F
titleColor = "#ffffff" #default: white
titleBgOutln = None #default: None
titleBgHeight = big #default: as titleSize
#titleBgWidth: "64" or "titleWidth + 8"

EnglishText = "RCTR W. Suburban L."#"SCM Central Line"
ChineseText = "米鐵西副都心線"

##IMAGE INITIALIZING

#Var Init
W, H = (128,128)

#New image
if bgColor == 1:
    im = Image.new("RGBA",(W,H),"white")
    draw = ImageDraw.Draw(im)
    draw.rectangle([0,0,127,127], outline = "black", width = 1)
else:
    im = Image.new("RGBA",(W,H),"black")
    draw = ImageDraw.Draw(im)
    draw.rectangle([0,0,127,127], outline = "white", width = 1)

#save image
im.save("output.png")

title(lineColor,titleText,titleSize,titleNarrow,titleBgHeight,titleColor,titleBgOutln)
English(bgColor,EnglishText)
Chinese(bgColor,ChineseText)