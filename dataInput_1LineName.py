from main_1LineName import title, English, Chinese
from PIL import Image, ImageDraw, ImageFont


#Size
big = 64
mid = 54
small = 48

lineColor = "#99FFCC"
titleText = "CT"
titleSize = big   #big/small/any number
titleColor = "#000000"   #default: white
titleBgOutln = "#000000" #default: white
titleBgFill = None  #default: none
titleBgHeight = mid #default: as titleSize
#titleBgWidth: "64" or "titleWidth + 8"(96 or 106?)

EnglishText = "Aoshima Line" #"Subway Line 1"
EnglishTextColor = "#000000"
ChineseText = "地鐵 1 號線"
ChineseTextColor = "#000000"


##IMAGE INITIALIZING

#Var Init
W, H = (128,128)

#New image
im = Image.new("RGBA",(W,H),lineColor)
draw = ImageDraw.Draw(im)

#Image Outline
draw.rectangle([0,0,127,127], outline = "#FFFFFF")

#save image
im.save("output.png")

title(titleText,titleSize,titleBgHeight,titleColor,titleBgOutln,titleBgFill)
English(EnglishText, EnglishTextColor)
Chinese(ChineseText, ChineseTextColor)