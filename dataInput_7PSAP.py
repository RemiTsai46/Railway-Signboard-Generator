from main_7PSAP import *
from PIL import Image, ImageDraw

dotSize = "big" # big / small
isCurrSta = True

ChineseText = "兔嶼"
EnglishText = "Usagishima"
countOfLines = 3
platformLine = 0
lines = [
    ["R1","#B380E6","white"],
    ["AS","#99FFFF","black"],
    ["LRT","#808080","white"],
    ["0","#000000","white"],
    ]

# ==================== IMAGE INITIALIZING ==================== #

#Var Init
W, H = (128,128)

#New image
im = Image.new("RGBA",(W,H),"white")
draw = ImageDraw.Draw(im)

im.save("output.png")

bgBox(isCurrSta,ChineseText,EnglishText)
Chinese(isCurrSta,ChineseText)
English(isCurrSta,EnglishText)