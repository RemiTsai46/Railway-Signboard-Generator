from PIL import Image, ImageDraw, ImageFont
from resources.functions.shapes import ellipse
from resources.functions.calculations import padCalc,SAE_BWCalc
import math

def Chinese(width, pStyle, bgColor, ChineseText):
    
    #Var Init
    W = 128*width
    if bgColor == 1 or pStyle:
        fgColor = "black"
    else:
        fgColor = "white"
 
    #Open image
    im = Image.open("output.png")
    draw = ImageDraw.Draw(im)

    ##CHINESE TEXT

    ChineseFont = ImageFont.truetype("resources/fonts/msjh.ttf", 22)
    ChineseFontP = ImageFont.truetype("resources/fonts/msjh.ttf", 18)
    if pStyle:
        draw.text((W/2,38), ChineseText, fill = fgColor, font = ChineseFontP, anchor = "ms")
    else:
        draw.text((W/2,38), ChineseText, fill = fgColor, font = ChineseFont, anchor = "ms")

    im.save("output.png")

def English(width, pStyle, bgColor, EnglishText):
    
    #Var Init
    W = 128*width
    EnglishFontSize = 13
    ok = False
    if bgColor == 1 or pStyle:
        fgColor = "black"
    else:
        fgColor = "white"

    #Open image
    im = Image.open("output.png")
    draw = ImageDraw.Draw(im)

    ##ENGLISH TEXT

    #Check if too long
    EnglishFont = ImageFont.truetype("resources/fonts/arial.ttf", EnglishFontSize)
    EnglishWidth = draw.textlength(EnglishText, font = EnglishFont)
    
    while EnglishFontSize >= 10:
        if EnglishWidth > W-6:
            EnglishFontSize -= 1
            EnglishFont = ImageFont.truetype("resources/fonts/arial.ttf", EnglishFontSize)
            EnglishWidth = draw.textlength(EnglishText, font = EnglishFont)
            if EnglishFontSize < 10:
                print("English station name is too long! Please choose a bigger canvas size.")
                break
        else:
            ok = True
            break

    if ok:
        draw.text((W/2,57), EnglishText, fill = fgColor, font = EnglishFont, anchor = "mm")

    im.save("output.png")

def lineColors(width, pStyle, COL, lines):

    #Var Init
    W = 128*width

    #Open image
    im = Image.open("output.png")
    draw = ImageDraw.Draw(im)

    ##LINE COLORS

    if pStyle:
        LRTColor = "#dddddd"
    else:
        LRTColor = "#222222"

    if COL == 1:
        lineWidth = 6
    else:
        lineWidth = 4
    
    for l in range(COL):
        if lines[l][0] == "LRT":
            draw.rectangle([2, 81+4*(l-COL/2), W-3, 81+4*(l-COL/2)+lineWidth-1], fill = LRTColor)
        else:
            draw.rectangle([2, 81+4*(l-COL/2), W-3, 81+4*(l-COL/2)+lineWidth-1], fill = lines[l][1])
    
    #center circle
    ellipse(im,[(W-24)/2,69,(W+24)/2-1,92],fill="white",outline="black",width=3)
    
    #save image
    im.save("output.png")

def stationCodes(width, pStyle, bgColor, COL, lines):
    
    #Var Init
    W = 128*width
    if bgColor == 1:
        fgColor = "black"
    else:
        fgColor = "white"

    #Open image
    im = Image.open("output.png")
    draw = ImageDraw.Draw(im)

    ##STATION CODES

    #Var Init
    boxWidths = []
    BWTotal = 0
    boxGap = 3
    boxWidthsOk = False
    
    LNFontName = "resources/fonts/arial.ttf"
    SCFontName = "resources/fonts/arial.ttf"
    lineNameFont = ImageFont.truetype("resources/fonts/arial.ttf", 11)
    stnNumFont = ImageFont.truetype("resources/fonts/arial.ttf", 8)

    #Length Calculating
    boxWidths,BWTotal,boxGap,boxWidthsOk = SAE_BWCalc(W,pStyle, COL, lines, lineNameFont, stnNumFont)
    print(boxWidths)

    #Start drawing
    if boxWidthsOk:
        if BWTotal % 2 == 1:
            BWTotal = BWTotal+1
        for m in range(COL):
            startPoint = (W-BWTotal)/2 + sum(boxWidths[:m]) + boxGap*(len(boxWidths[:m]))
            padLN = padCalc(lines[m][0],LNFontName,lineNameFont)
            print(padLN)
            padSC = padCalc(lines[m][3],SCFontName,stnNumFont)
            print(padSC)
            if pStyle or lines[m][3] == None:
                #no-station-code draw
                if pStyle:
                    pos = [106, 120, 117]
                    colors = ["#dddddd","#666666"]
                elif lines[m][3] == None:
                    pos = [103, 117, 114]
                    colors = ["#222222","#666666"]

                if lines[m][0] == "LRT":
                    draw.rectangle([startPoint,pos[0],startPoint+boxWidths[m]-1,pos[1]], colors[0])
                    draw.text((startPoint+boxWidths[m]/2+padLN,pos[2]), lines[m][0], fill=colors[1],font=lineNameFont,anchor="ms")
                else:
                    draw.rectangle([startPoint,pos[0],startPoint+boxWidths[m]-1,pos[1]], fill=lines[m][1])
                    draw.text((startPoint+boxWidths[m]/2+padLN,pos[2]), lines[m][0], fill=lines[m][2],font=lineNameFont,anchor="ms")
            else:
                draw.rectangle([startPoint,99,startPoint+boxWidths[m]-1,120], outline=lines[m][1], width=2)
                draw.rectangle([startPoint,99,startPoint+boxWidths[m]-1,108], fill=lines[m][1])
                draw.text((startPoint+boxWidths[m]/2+padLN,108), lines[m][0], fill=lines[m][2],font=lineNameFont,anchor="ms")
                draw.text((startPoint+boxWidths[m]/2+padSC,117), lines[m][3], fill = fgColor, font = stnNumFont,anchor="ms")

    im.save("output.png")