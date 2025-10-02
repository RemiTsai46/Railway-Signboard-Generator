from main_4aLineDirNew import *
from PIL import Image,ImageDraw,ImageFont


#Var init
bgColor = 0

direction = "s" #e/w/n/s/cw/ccw
lineData = ["R1","#CC99FF","black","05"] #"line short name","line color","line text color","stn code"
ChineseText = "森林新村"
EnglishText = "Forest Village"


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

targetSta(bgColor,direction,lineData)
Chinese(bgColor,ChineseText)
English(bgColor,EnglishText)
