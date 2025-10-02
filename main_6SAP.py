from PIL import Image, ImageDraw, ImageFont
from resources.functions.calculations import SAP
from resources.value_sets import SAP_posSet

def Chinese(bgColor, curr):
    
    #Var Init
    W = 384
    if bgColor == 1:
        fgColor = "#0d0d0d"
    else:
        fgColor = "white"
 
    #Open image
    im = Image.open("output.png")
    draw = ImageDraw.Draw(im)

    ##CHINESE TEXT

    ChineseFont = ImageFont.truetype("resources/fonts/msjh.ttf", 22)
    draw.text((W/2,44), curr[0], fill = fgColor, font = ChineseFont, anchor = "ms")

    im.save("output.png")

def English(bgColor, curr):
    
    #Var Init
    W = 384
    EnglishFontSize = 13
    EnglishWidthOk = False
    if bgColor == 1:
        fgColor = "#0d0d0d" 
    else:
        fgColor = "white"

    #Open image
    im = Image.open("output.png")
    draw = ImageDraw.Draw(im)

    ##ENGLISH TEXT

    #Var Init
    EnglishFont = ImageFont.truetype("resources/fonts/arial.ttf", EnglishFontSize)
    EnglishWidth = draw.textlength(curr[1], font = EnglishFont)
    
    #Check if too long
    while EnglishFontSize >= 10:
        if EnglishWidth > 122:
            EnglishFontSize = EnglishFontSize - 1
            EnglishFont = ImageFont.truetype("resources/fonts/arial.ttf", EnglishFontSize)
            EnglishWidth = draw.textlength(curr[1], font = EnglishFont)
            if EnglishFontSize < 10:
                print("English station name is too long! Please shorten the name.")
                break
        else:
            EnglishWidthOk = True
            break

    if EnglishWidthOk:
        draw.text((W/2,58), curr[1], fill = fgColor, font = EnglishFont, anchor = "mm")

    im.save("output.png")

def lineArrow(bgColor, dir, p, linesGrouped, curr, COL):

    #Var Init
    W = 384
    if bgColor == 1:
        bgColor = "white"
        fgColor = "#0d0d0d"
    else:
        bgColor = "#0d0d0d"
        fgColor = "white"
    
    #Ungrouping lines
    lines = []
    for l in range(len(linesGrouped)):
        if isinstance(linesGrouped[l][0],list):
            for m in range(len(linesGrouped[l])):
                lines.append(linesGrouped[l][m])
        else:
            lines.append(linesGrouped[l])

    #Open image
    im = Image.open("output.png")
    draw = ImageDraw.Draw(im)

    ##LINE ARROW
    
    ##Arrow
    if dir == "left":
        draw.rectangle([47,78,319,83], fill = lines[p][1])
        draw.polygon([(18,83),(46,83),(46,69)], fill = lines[p][1])
    elif dir == "right":
        draw.rectangle([64,78,336,83], fill = lines[p][1])
        draw.polygon([(365,83),(337,83),(337,69)], fill = lines[p][1])

    ##Box

    #Var Init
    lineNameFont = ImageFont.truetype("resources/fonts/arial.ttf", 12)
    stnNumFont = ImageFont.truetype("resources/fonts/arial.ttf", 11)
    boxLen = draw.textlength(lines[p][0], font = lineNameFont)

    #Check if need to lengthen the box
    if boxLen > 28 or COL >= 16:
        boxLen = max(boxLen, 2*COL)+2
        if boxLen % 2 == 1:
            boxLen = boxLen + 1
    else:
        boxLen = 32

    draw.rectangle([(W-boxLen)/2,71,(W+boxLen)/2-1,95], fill = bgColor, outline=lines[p][1], width=2)
    draw.rectangle([(W-boxLen)/2,71,(W+boxLen)/2-1,81], fill=lines[p][1])
    draw.text((W/2,81), lines[p][0], fill = lines[p][2], font = lineNameFont, anchor = "ms")
    draw.text((W/2,92), curr[2], fill = fgColor, font = stnNumFont, anchor = "ms")

    im.save("output.png")

def transferLineColors(p, COL, linesGrouped):
    
    #Var Init
    W = 384
    
    #Open image
    im = Image.open("output.png")
    draw = ImageDraw.Draw(im)

    ##TRANSFER LINE COLORS

    #Var Init
    plSkipped = False
    lineWidth = 4
    
    #Ungrouping lines
    lines = []
    for l in range(len(linesGrouped)):
        if isinstance(linesGrouped[l][0],list):
            for m in range(len(linesGrouped[l])):
                lines.append(linesGrouped[l][m])
        else:
            lines.append(linesGrouped[l])

    #Check if too wide
    while lineWidth >= 2:
        if lineWidth * (COL-1) >= 32:
            lineWidth = lineWidth - 1
            if lineWidth < 2:
                lineWidth = 2
                break
        else:
            break

    for l in range(COL):
        if l == p:
            plSkipped = True
            continue
        else:
            if plSkipped:
                startPoint = W/2 + lineWidth*((l-1)-(COL-1)/2)
            else:
                startPoint = W/2 + lineWidth*(l-(COL-1)/2)
            if lines[l][0] == "LRT":
                draw.rectangle([startPoint,96,startPoint+3,101], fill = "#222222")
            else:
                draw.rectangle([startPoint,96,startPoint+3,101], fill = lines[l][1])

    im.save("output.png")

def transferLineNames(p, COL, linesGrouped):
    
    #Var Init
    W = 384
    calc = SAP()
    
    #Open image
    im = Image.open("output.png")
    draw = ImageDraw.Draw(im)

    ##TRANSFER LINE NAMES

    #Var Init
    
    boxWidths = []
    BWTotal = 0
    boxGap = 3
    rows = 1
    ok = False

    lines = [] #ungrouped linesGrouped
    groupOfLines = [] # current group which a line is in
    groupLens = [] #length of each group
    #spl = 1 # 1st object of 2nd row
    
    LNFont = ImageFont.truetype("resources/fonts/arial.ttf", 11) #LN = lineName
    LNFontS = ImageFont.truetype("resources/fonts/arial.ttf", 9)

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
    
    #Length Calculating
    font = LNFont
    boxWidths = calc.boxWidths(p,len(lines),lines,font,3)

    for i in range(2):
        BWTotals = []
        boxGaps = []
        if rows > 1:
            font = LNFontS
            boxWidths = calc.boxWidths(p,len(lines),lines,font,3) # recalc if rows >= 2
            splits = calc.splitCalc(p,len(lines),boxWidths,groupOfLines,groupLens,rows)
        else:
            splits = (0,len(lines))
        for r in range(rows):
            rowInfo = calc.rowLen(p,boxWidths,(splits[r],splits[r+1]),boxGap)
            if rowInfo[2]: #addRow = True
                ok = False
                if rows == 2:
                    print("Too many linesGrouped! Please shorten the line codes.")
                else:
                    rows += 1
                break
            else:
                ok = True
            BWTotals.append(rowInfo[0])
            boxGaps.append(rowInfo[1])
        if ok:
            break

    print(splits)
    for r in range(rows):
        for l in range(splits[r],splits[r+1]):
            
            #skip cond
            if l == p:
                continue
            
            #calc starting point
            startPoint = (W-BWTotals[r])/2 + sum(boxWidths[splits[r]:l]) + boxGaps[r]*(l-splits[r])
            if l > p and splits[r] <= p < splits[r+1]:
                startPoint -= boxGap
            
            pos = SAP_posSet[rows-1][r]
            #draw
            if lines[l][0] == "LRT":
                draw.rectangle([startPoint,pos[0],startPoint+boxWidths[l]-1,pos[1]], fill="#222222")
                draw.text((startPoint+boxWidths[l]/2,pos[2]), lines[l][0], fill="#666666",font=font,anchor="ms")
            else:
                draw.rectangle([startPoint,pos[0],startPoint+boxWidths[l]-1,pos[1]], fill=lines[l][1])
                draw.text((startPoint+boxWidths[l]/2,pos[2]), lines[l][0], fill=lines[l][2],font=font,anchor="ms")

    im.save("output.png")

def nextStop(bgColor, p, linesGrouped, next, dir):
    
    #Var Init
    if bgColor == 1:
        bgColor = "white"
        fgColor = "black"
    else:
        bgColor = "black"
        fgColor = "white"

    #Open image
    im = Image.open("output.png")
    draw = ImageDraw.Draw(im)

    ##NEXT STOP

    #Var Init
    boxWidth = 0
    lineNameFont = ImageFont.truetype("resources/fonts/arial.ttf", 11)
    stnNumFont = ImageFont.truetype("resources/fonts/arial.ttf", 8)
    ChineseFont = ImageFont.truetype("resources/fonts/msjh.ttf", 11)
    EnglishFont = ImageFont.truetype("resources/fonts/arial.ttf", 10)
    
    #Ungrouping lines
    lines = []
    for l in range(len(linesGrouped)):
        if isinstance(linesGrouped[l][0],list):
            for m in range(len(linesGrouped[l])):
                lines.append(linesGrouped[l][m])
        else:
            lines.append(linesGrouped[l])

    TWLineName = draw.textlength(lines[p][0], font = lineNameFont)
    TWStnNum = draw.textlength(next[2], font = stnNumFont)
    boxWidth = max(TWLineName, TWStnNum)+4

    if dir == "left":
        setups = [4,10+boxWidth,"ls"]
    elif dir == "right":
        setups = [380-boxWidth,374-boxWidth,"rs"]

    draw.rectangle([setups[0],99,setups[0]+boxWidth-1,120], outline=lines[p][1], width=2)
    draw.rectangle([setups[0],99,setups[0]+boxWidth-1,108], fill=lines[p][1])
    draw.text((setups[0]+boxWidth/2,108), lines[p][0], fill=lines[p][2],font=lineNameFont,anchor="ms")
    draw.text((setups[0]+boxWidth/2,117), next[2], fill = fgColor, font = stnNumFont, anchor="ms")
    draw.text((setups[1],108), next[0], fill = fgColor, font = ChineseFont, anchor = setups[2])
    draw.text((setups[1],120), next[1], fill = fgColor, font = EnglishFont, anchor = setups[2])

    im.save("output.png")