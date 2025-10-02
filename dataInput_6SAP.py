from main_6SAP import *
from PIL import Image

bgColor = 0 # 0(black) or 1(white)

currStnData = ["青石谷", 
               "Greenstone Valley", 
               "05"]
nextStnData = ["青石谷", 
               "Greenstone Valley", 
               "05"]
countOfLines = 2
platformLine = 0
direction = "right" # left / right
lines = [[
    ["8","#95576c","white"],
    ["R1","#B380E6","white"],
    ]]
    #"line short name","line color","line text color"

# ==================== IMAGE INITIALIZING ==================== #

#Var Init
W, H = (384,128)

#New image
if bgColor == 1:
    im = Image.new("RGBA",(W,H),"white")
else:
    im = Image.new("RGBA",(W,H),"#0d0d0d")

im.save("output.png")

Chinese(bgColor, currStnData)
English(bgColor, currStnData)
lineArrow(bgColor, direction, platformLine, lines, currStnData, countOfLines)
transferLineColors(platformLine, countOfLines, lines)
transferLineNames(platformLine, countOfLines, lines)
nextStop(bgColor, platformLine, lines, nextStnData, direction)