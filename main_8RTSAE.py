from PIL import Image, ImageDraw, ImageFont
from resources.functions.shapes import ellipse
from resources.functions.calculations import padCalc,RTSAE
from resources.value_sets import RTSAE_posSet
import math

def Chinese(width, ChineseText):
    
    #Var Init
    W = 128*width
    fgColor = "white"
 
    #Open image
    im = Image.open("output.png")
    draw = ImageDraw.Draw(im)

    ##CHINESE TEXT
    ChineseFont = ImageFont.truetype("resources/fonts/msjh.ttf", 16)
    draw.text((W/2,24), ChineseText, fill = fgColor, font = ChineseFont, anchor = "ms")

    im.save("output.png")

def English(width, EnglishText):
    
    #Var Init
    W = 128*width
    EnglishFontSize = 12
    ok = False
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
        draw.text((W/2,40), EnglishText, fill = fgColor, font = EnglishFont, anchor = "ms")

    im.save("output.png")
    
def Svenska(width, SvenskText):
    
    #Var Init
    W = 128*width
    SvenskFontSize = 12
    ok = False
    fgColor = "white"

    #Open image
    im = Image.open("output.png")
    draw = ImageDraw.Draw(im)

    ##ENGLISH TEXT

    #Check if too long
    SvenskFont = ImageFont.truetype("resources/fonts/arial.ttf", SvenskFontSize)
    SvenskWidth = draw.textlength(SvenskText, font = SvenskFont)
    
    while SvenskFontSize >= 10:
        if SvenskWidth > W-6:
            SvenskFontSize -= 1
            SvenskFont = ImageFont.truetype("resources/fonts/arial.ttf", SvenskFontSize)
            SvenskWidth = draw.textlength(SvenskText, font = SvenskFont)
            if SvenskFontSize < 10:
                print("Svenska stationsnamnet är för långt! Välj en större canvasstorlek.")
                break
        else:
            ok = True
            break

    if ok:
        draw.text((W/2,56), SvenskText, fill = fgColor, font = SvenskFont, anchor = "ms")

    im.save("output.png")

# def lineColors(width, pStyle, COL, linesGrouped):

#     #Var Init
#     W = 128*width

#     #Ungrouping lines
#     lines = []
#     for l in range(len(linesGrouped)):
#         if isinstance(linesGrouped[l][0],list):
#             for m in range(len(linesGrouped[l])):
#                 lines.append(linesGrouped[l][m])
#         else:
#             lines.append(linesGrouped[l])

#     #Open image
#     im = Image.open("output.png")
#     draw = ImageDraw.Draw(im)

#     ##LINE COLORS

#     if pStyle:
#         LRTColor = "#dddddd"
#     else:
#         LRTColor = "#222222"

#     if COL == 1:
#         lineWidth = 6
#     else:
#         lineWidth = 4
    
#     for l in range(COL):
#         if lines[l][0] == "LRT":
#             draw.rectangle([2, 74+4*(l-COL/2), W-3, 74+4*(l-COL/2)+lineWidth-1], fill = LRTColor)
#         else:
#             draw.rectangle([2, 74+4*(l-COL/2), W-3, 74+4*(l-COL/2)+lineWidth-1], fill = lines[l][1])
    
#     #center circle
#     ellipse(im,[(W-24)/2,62,(W+24)/2-1,85],fill="#ffffff",outline="black",width=3)
    
#     #save image
#     im.save("output.png")

def stationCodes(width, pStyle, COL, linesGrouped):
    
    #Var Init
    W = 128*width
    calc = RTSAE()

    #Open image
    im = Image.open("output.png")
    draw = ImageDraw.Draw(im)

    ##STATION CODES

    #Var Init
    boxWidths = []
    BWTotal = 0
    boxGap = 3
    fgColor = "white"
    rows = 1 #spl = 1 # 1st object of 2nd row
    ok = False
    
    lines = [] #ungrouped linesGrouped
    groupOfLines = [] # current group which a line is in
    groupLens = [] #length of each group
    
    #Ungrouping lines
    for l in range(len(linesGrouped)):
        if isinstance(linesGrouped[l][0],list):
            for m in range(len(linesGrouped[l])):
                lines.append(linesGrouped[l][m])
                groupOfLines.append(l)
            groupLens.append(len(linesGrouped[l]))
        else:
            lines.append(linesGrouped[l])
            groupOfLines.append(l)
            groupLens.append(1)
    
    fontName = "arial"
    font = ImageFont.truetype("resources/fonts/arial.ttf", 10) #stnCodeFont

    #Length Calculating
    boxWidths = calc.boxWidths(len(lines),lines,font,3)

    for i in range(3):
        BWTotals = []
        boxGaps = []
        if rows > 1:
            boxWidths = calc.boxWidths(len(lines),lines,font,3) # recalc if rows >= 2
            splits = calc.splitCalc(len(lines),boxWidths,groupOfLines,groupLens,rows)
        else:
            splits = (0,len(lines))
        for r in range(rows): # calc every row length
            rowInfo = calc.rowLen(W,boxWidths,(splits[r],splits[r+1]),boxGap)
            BWTotals.append(rowInfo[0])
            boxGaps.append(rowInfo[1])
            if rowInfo[2]: #addRow = True
                ok = False
                if rows == 3:
                    print("Too many lines! Please choose a bigger canvas size.")
                else:
                    rows += 1
                    break
            else:
                if r == rows-1:
                    ok = True
            
        if ok:
            break

    for r in range(rows):
        for l in range(splits[r],splits[r+1]):
            
            #calc starting point
            startPoint = (W-BWTotals[r])/2 + sum(boxWidths[splits[r]:l]) + boxGaps[r]*(l-splits[r])
            SCstart = startPoint + draw.textlength(lines[l][0], font = font) + 4
            padLN = padCalc(lines[l][0],fontName,font)
            #print(padLN)
            padSC = padCalc(lines[l][3],fontName,font)
            #print(padSC)
            
            pos = RTSAE_posSet[r]
            
            # if lines[m][0] == "LRT":
            #         draw.rectangle([startPoint,pos[0],startPoint+boxWidths[m]-1,pos[1]], colors[0])
            #         draw.text((startPoint+boxWidths[m]/2+padLN,pos[2]), lines[m][0], fill=colors[1],font=lineNameFont,anchor="ms")
            
            draw.rounded_rectangle([startPoint,pos[0],startPoint+boxWidths[l]-1,pos[1]],radius=2,fill=lines[l][1])
            draw.rounded_rectangle([SCstart,pos[0],startPoint+boxWidths[l]-1,pos[1]],radius=2,fill="#666666",corners=[False,True,True,False])
            draw.text((startPoint+2+padLN,pos[2]), lines[l][0], fill=lines[l][2],font=font,anchor="ls")
            draw.text((SCstart+2+padSC,pos[2]), lines[l][3], fill = fgColor, font = font,anchor="ls")
    
    '''
    #TBR    
    boxWidths,BWTotal,boxGap,boxWidthsOk = RTSAE_BWCalc(W, COL, lines, stnCodeFont)
    print(boxWidths)

    #Start drawing
    if boxWidthsOk:
        if BWTotal % 2 == 1:
            BWTotal = BWTotal+1
        for m in range(COL):
            startPoint = (W-BWTotal)/2 + sum(boxWidths[:m]) + boxGap*(len(boxWidths[:m]))
            SCstart = startPoint + draw.textlength(lines[m][0], font = stnCodeFont) + 4
            padLN = padCalc(lines[m][0],SCFontName,stnCodeFont)
            print(padLN)
            padSC = padCalc(lines[m][3],SCFontName,stnCodeFont)
            print(padSC)
            
            draw.rounded_rectangle([startPoint,86,startPoint+boxWidths[m]-1,96],radius=2,fill=lines[m][1])
            draw.rounded_rectangle([SCstart,86,startPoint+boxWidths[m]-1,96],radius=2,fill="#666666",corners=[False,True,True,False])
            draw.text((startPoint+2+padLN,95), lines[m][0], fill=lines[m][2],font=stnCodeFont,anchor="ls")
            draw.text((SCstart+2+padSC,95), lines[m][3], fill = fgColor, font = stnCodeFont,anchor="ls")
    '''
    im.save("output.png")