from main_4RTLineDir import *
from PIL import Image,ImageDraw,ImageFont


#Var init
bgColor = 0

direction = "cw" #e/w/n/s/cw/ccw
lineData = ["R1","#B380E6","black","19"] #"line short name","line color","line text color","stn code"
ChineseText = "學園碼頭"
EnglishText = "Academy Pier"


##IMAGE INITIALIZING

#Var Init
W, H = (128,128)

#New image
if bgColor == 1:
    im = Image.new("RGBA",(W,H),"white")
    draw = ImageDraw.Draw(im)
    draw.rectangle([0,0,127,127], outline = "#0d0d0d", width = 1)
else:
    im = Image.new("RGBA",(W,H),"#0d0d0d")
    draw = ImageDraw.Draw(im)
    draw.rectangle([0,0,127,127], outline = "white", width = 1)

#save image
im.save("output.png")

targetSta(bgColor,direction,lineData)
Chinese(bgColor,ChineseText)
English(bgColor,EnglishText)
