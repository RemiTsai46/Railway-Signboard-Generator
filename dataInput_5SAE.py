from main_5SAE import *
from PIL import Image, ImageDraw

bgColor = 0          # 0(black) or 1(white)
partnerStyle = False
width = 1            # 1 to 3, timed by 128

ChineseText = "時代廣場"
EnglishText = "Times Square"
countOfLines = 2
lines = [
    ["CT","#FF99FF","black","06"],
    ["TC","#FF9999","black","03"],
    ]
    #"line short name","line color","line text color","stn num"
    # if LRT, stncode = None
    #If partnerStyle is chosen, please do not generate LRT as it doesn't exist in Original Edition.

# ==================== IMAGE INITIALIZING ==================== #

#Var Init
W, H = (128*width,128)

#New image and Image Outline
if bgColor == 1 or partnerStyle:
    im = Image.new("RGBA",(W,H),"white")
    draw = ImageDraw.Draw(im)
    draw.rectangle([0,0,W-1,127], outline = "black", width = 2)
else:
    im = Image.new("RGBA",(W,H),"black")
    draw = ImageDraw.Draw(im)
    draw.rectangle([0,0,W-1,127], outline = "white", width = 2)

#save image
im.save("output.png")

Chinese(width, partnerStyle, bgColor, ChineseText)
English(width, partnerStyle, bgColor, EnglishText)
lineColors(width, partnerStyle, countOfLines, lines)
stationCodes(width, partnerStyle, bgColor, countOfLines, lines)
