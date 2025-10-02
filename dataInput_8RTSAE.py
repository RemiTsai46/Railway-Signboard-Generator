from main_8RTSAE import *
from PIL import Image, ImageDraw

# bgColor = "#333333"
partnerStyle = False
width = 1            # 1 to 3, timed by 128

ChineseText = "時代廣場"
EnglishText = "Times Square"
SvenskText = "Tiderstorget" # can be ignored, TBA move other 2 downwards
countOfLines = 2 #REMEMBER TO CHANGE TO FIT "lines" VARIABLE
lines = [
    [
        ["CT","#FF99FF","black","06"],
        ["TC","#FF9999","black","03"],
    ]
]
    #"line short name","line color","line text color","stn num"
    # if LRT, stnnum = None
    # line groups:
    # same group will stay in the same row, but if only 1 group exists, the groups will be seperable no matter what.
rows = 1

# ==================== IMAGE INITIALIZING ==================== #

#Var Init
W, H = (128*width,128)

#New image and Image Outline

im = Image.new("RGBA",(W,H),"#110022")
draw = ImageDraw.Draw(im)
draw.rectangle([0,0,W-1,127], outline = "white", width = 2)

#save image
im.save("output.png")

Chinese(width, ChineseText)
English(width, EnglishText)
Svenska(width, SvenskText)
# lineColors(width, partnerStyle, countOfLines, lines)
stationCodes(width, partnerStyle, countOfLines, lines)
