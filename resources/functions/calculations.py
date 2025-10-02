from PIL import Image,ImageDraw,ImageFont
import re
import math
from ..value_sets import fontPads

def ChiWidthCalc(width:int,text:str,ChiFontName:str,EngFontName:str,fontSize:int) -> (
        tuple[list,int,list,bool]
        ):
    #var init
    values = []
    ChiFont = ImageFont.truetype(ChiFontName,fontSize)
    EngFont = ImageFont.truetype(EngFontName,fontSize)
    im = Image.new('RGBA', (128,128), "#000000")
    draw = ImageDraw.Draw(im)

    #main
    def calc(ChiFont:ImageFont.FreeTypeFont,EngFont:ImageFont.FreeTypeFont):
        charFonts = []
        for char in text:
            if re.search("[\u4e00-\u9FFF]",char):
                charWidth = int(draw.textlength(char, font = ChiFont))
                charFonts.append(ChiFont)
            else:
                charWidth = int(draw.textlength(char, font = EngFont))
                charFonts.append(EngFont)
            values.append(charWidth)
        value = sum(values)

        return values, value, charFonts

    values, value, charFonts = calc(ChiFont,EngFont)
    while fontSize >= 14:
        if value > width:
            fontSize -= 1
            ChiFont = ImageFont.truetype(ChiFontName,fontSize)
            EngFont = ImageFont.truetype(EngFontName,fontSize)
            values, value, charFonts = calc(ChiFont,EngFont)
            if fontSize < 14:
                print("Chinese text is too long! Please shorten it.")
                break
        else:
            ok = True
            break
    
    return values, value, charFonts, ok

def padCalc(text,fontName,font):
    
    #Var Init
    im = Image.new('RGBA', (128,128), "#000000")
    draw = ImageDraw.Draw(im)
    padL = 0
    padR = 0
    
    #Calculations
    if text[0] == "1":
        padL = fontPads[fontName][0]
    if text[-1] == "1":
        padR = fontPads[fontName][1]
        
    padM = padL + padR
    print(draw.textlength("1",font=font)*padM)
    if padM < 0:
        pad = math.ceil(draw.textlength("1",font=font)*padM)
    else:
        pad = math.floor(draw.textlength("1",font=font)*padM)
        
    print(pad)
    
    return pad

def RTLineName_titleFontCalc(titleText,titleSize,titleNarrow):
    
    #Var init
    im = Image.open("output.png")
    draw = ImageDraw.Draw(im)
    
    TFName = "resources/fonts/arial.ttf"
    TFNName = "resources/fonts/arialn.ttf"
    titleFont = ImageFont.truetype("resources/fonts/arial.ttf", titleSize)
    titleFontS = ImageFont.truetype("resources/fonts/arial.ttf", int(titleSize*0.75))
    titleFontN = ImageFont.truetype("resources/fonts/arialn.ttf", titleSize)
    titleFontNS = ImageFont.truetype("resources/fonts/arialn.ttf", int(titleSize*0.75))
    
    #Calculations
    if titleNarrow:
        font = titleFontN
        fontName = TFNName
        titleWidth = draw.textlength(titleText, font = titleFontN)
    else:
        font = titleFont
        fontName = TFName
        titleWidth = draw.textlength(titleText, font = titleFont)
    print(titleWidth)

    #Check if too big
    if titleWidth > 96:
        if titleNarrow:
            font = titleFontNS
            titleWidth = draw.textlength(titleText, font = titleFontNS)
        else:
            font = titleFontS
            titleWidth = draw.textlength(titleText, font = titleFontS)
        print("New Size:", titleWidth)
        
    return fontName,font,titleWidth

def RTLineDir_BWCalc(lineData, font):
    #var init
    value = 0
    width = 128
    fontSize = 16
    ok = False
    im = Image.new('RGBA', (128,128), "#000000")
    draw = ImageDraw.Draw(im)
    
    #main
    #Calculating arguments
    value = (draw.textlength(lineData[0], font = font) + 
             draw.textlength(lineData[3], font = font)+12)
    #value = TLUpperline+TLLowerline+12
    
    #Check if too big(to be modified)
    while fontSize >= 10:
        if value > width:
            #linename shrink
            fontSize -= 1
            font = ImageFont.truetype("resources/fonts/arial.ttf",fontSize)
            value = (draw.textlength(lineData[0], font = font) + 
                  draw.textlength(lineData[3], font = font)+12)
            if fontSize < 10:
                print("Line Name / Station Code value too long! Please shorten them.")
                break
        else:
            ok = True
            break
    
    return value,font,ok

def LineDirNew_BWCalc(lineData, upperFont, lowerFont):
    #var init
    value = 0
    width = 92
    upperFontSize = 19
    lowerFontSize = 16
    ok = False
    im = Image.new('RGBA', (128,128), "#000000")
    draw = ImageDraw.Draw(im)
    
    #main
    #Calculating arguments
    TLUpperline = draw.textlength(lineData[0], font = upperFont)
    TLLowerline = draw.textlength(lineData[3], font = lowerFont)
    value = max(TLUpperline, TLLowerline)+6
    
    #Check if too big(to be modified)
    while upperFontSize >= 10 or lowerFontSize >= 10:
        if value > width:
            if TLUpperline > width-6:
                upperFontSize -= 1
                upperFont = ImageFont.truetype("resources/fonts/arial.ttf",upperFontSize)
                TLUpperline = draw.textlength(lineData[0], font = upperFont)
            if TLLowerline > width-6:
                lowerFontSize -= 1
                lowerFont = ImageFont.truetype("resources/fonts/arial.ttf",lowerFontSize)
                TLLowerline = draw.textlength(lineData[3], font = lowerFont)
            value = max(TLUpperline, TLLowerline)+6
            if upperFontSize < 10 or lowerFontSize < 10:
                print("Line Name / Station Code value too long! Please shorten them.")
                break
        else:
            if lowerFontSize > upperFontSize:
                lowerFontSize = upperFontSize
            ok = True
            break
    
    return value,upperFont,lowerFont,ok

def SAE_BWCalc(width:int,partnerStyle:bool, COL:int, lines, upperFont, lowerFont):
    #var init
    values = []
    boxGap = 3
    im = Image.new('RGBA', (128,128), "#000000")
    draw = ImageDraw.Draw(im)
    
    #main
    for l in range(COL):
        #Calculating arguments
        TWUpperline = draw.textlength(lines[l][0], font = upperFont)
        if lines[l][3] == None or partnerStyle:
            TWLowerLine = 0
        else:
            TWLowerLine = draw.textlength(lines[l][3], font = lowerFont)

        #Calculating final value
        if TWLowerLine == 0:
            values.append(TWUpperline + 6)
        else:
            values.append(max(TWUpperline, TWLowerLine)+6)
            
    #Total Length Calculating
    total = sum(values) + boxGap*(COL-1)
    
    #Check if too big
    while boxGap > 0:
        if total > width-6:
            boxGap -= 1
            total -= (COL-1)
            if boxGap < 1:
                print("Too many lines! Please choose a bigger canvas size.")
        else:
            ok = True
            break
    
    return values,total,boxGap,ok

class SAP:
    
    def boxWidths(self,p,COL,lines,font:ImageFont.truetype,textPad:int):
        value = 0
        values = []
        
        im = Image.new('RGBA', (128,128), "#000000")
        draw = ImageDraw.Draw(im)
        
        for l in range(COL):
            if lines[l][0] == lines[p][0]:
                values.append(0)
            else:
                value = draw.textlength(lines[l][0], font = font)
                values.append(value + 2*textPad)
                
        return values

    def rowLen(self,p:int,boxWidths,lineRange:tuple[int,int],boxGap:int): # p=platformline
        #var init
        total = 0
        addRow = False
        col = lineRange[1]-lineRange[0]
                
        total = sum(boxWidths[lineRange[0]:lineRange[1]]) + boxGap*(col-1)
        if p in range(*lineRange):
            total -= boxGap
                
        while boxGap > 0:
            if total > 122:
                boxGap -= 1
                total -= (col-1)
                if p in range(*lineRange):
                    total -= 1
                if boxGap < 1:
                    addRow = True
                    boxGap = 1
                    break
            else:
                break
            
        if total % 2 == 1:
            total += 1
        
        return total,boxGap,addRow

    def splitCalc(self,p,CoL,boxWidths,groupOfLines:list,groupLens,rows):
        #Recalc
        boxGap = 3
        BWTotal = sum(boxWidths[:CoL]) + boxGap*(CoL-rows-1) # rows = rowgap + end, 1=platformline
        groupOfLines.append(groupOfLines[-1]+1)
        splits = [0]
        #Calc 2 rows' individual width and CoL
        for r in range(rows):
            for s in range(CoL):
                
                if s == p: #skip platformline
                    continue
                
                if groupOfLines[s+1] == groupOfLines[s]: #skip until group split point
                    continue
                
                groupLen = groupLens[groupOfLines[s]] # grouplines[s] = current group num
                temp1 = sum(boxWidths[:s+1-groupLen]) + boxGap*(s-groupLen) #rewind 1 group
                temp2 = sum(boxWidths[:s+1]) + boxGap*s # no rewind
                
                if temp2 >= BWTotal*(r+1/rows):
                    if abs(BWTotal*(r+1/rows)-temp1) < abs(BWTotal*(r+1/rows)-temp2) and s > groupLen:
                        splits.append(s+1-groupLen)# if rewind 1 group is closer, use it
                    else:
                        splits.append(s+1)
                    break
                
        splits.append(CoL)
            
        return splits

class RTSAE: # objectify as calc
    
    def boxWidths(self,CoL,lines,font:ImageFont.truetype,textPad:int):

        #var init
        values = []
        
        im = Image.new('RGBA', (128,128), "#000000")
        draw = ImageDraw.Draw(im)
        
        for l in range(CoL):
            #Calculating arguments (TW = text width)
            TWLineName = draw.textlength(lines[l][0], font = font)
            TWStnCode = draw.textlength(lines[l][3], font = font)

            #Calculating final value
            values.append(TWLineName+TWStnCode+8)
        
        return values
        
    def rowLen(self,width:int,boxWidths,lineRange:tuple[int,int],boxGap:int): # p=platformline
        #var init
        total = 0
        addRow = False
        col = lineRange[1]-lineRange[0]
                
        total = sum(boxWidths[lineRange[0]:lineRange[1]]) + boxGap*(col-1)
        
        while boxGap > 0:
            if total > width-6:
                boxGap -= 1
                total -= (col-1)
                if boxGap < 1:
                    addRow = True
                    boxGap = 1
                    break
            else:
                break
            
        if total % 2 == 1:
            total += 1
        
        return total,boxGap,addRow
    
    def splitCalc(self,CoL,boxWidths,groupOfLines:list,groupLens,rows):
        #Recalc
        boxGap = 3
        BWTotal = sum(boxWidths[:CoL]) + boxGap*(CoL-rows) # rows-1 = rowgapcount
        groupOfLines.append(groupOfLines[-1]+1)
        splits = [0] # split = next row first object
        #Calc rows' individual width and CoL
        for r in range(rows-1):
            for s in range(CoL):
                if groupOfLines[s+1] == groupOfLines[s]: #skip until group split point(don't if last)
                    continue
                
                groupLen = groupLens[groupOfLines[s]] # grouplines[s-1] = current group num
                temp1 = sum(boxWidths[:s+1-groupLen]) + boxGap*(s-groupLen) # rewind 1 group
                temp2 = sum(boxWidths[:s+1]) + boxGap*s # no rewind
                
                if temp2 >= BWTotal*(r+1/rows):
                    if abs(BWTotal*(r+1/rows)-temp1) < abs(BWTotal*(r+1/rows)-temp2) and s > groupLen:
                        splits.append(s+1-groupLen)# if rewind 1 group is closer, use it
                    else:
                        splits.append(s+1)
                    break
                
        splits.append(CoL)
            
        return splits
