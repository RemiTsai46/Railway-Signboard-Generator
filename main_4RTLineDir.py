from PIL import Image, ImageDraw, ImageFont
from resources.value_sets import lineDir
from resources.functions.calculations import padCalc,ChiWidthCalc,RTLineDir_BWCalc
from resources.functions.shapes import roundRect

def targetSta(bgColor,dir,lineData):
    
    #Var Init
    W, H = (128,128)
    if bgColor == 1:
        fgColor = "#0d0d0d"
    else:
        fgColor = "white"

    #Open Image
    im = Image.open("output.png")
    draw = ImageDraw.Draw(im)
    

    ##DIRECTION/TO
    #Var Init
    ChineseFont = ImageFont.truetype("resources/fonts/msjh.ttf",16)
    EnglishFont = ImageFont.truetype("resources/fonts/arial.ttf",16)
    pos = [16,112] if dir == "cw" or dir == "ccw" else [24,104]
    
    #dir-Chinese
    draw.text((pos[0],22),lineDir[dir][0],fill=fgColor,font=ChineseFont,anchor="ls")
    #dir-English
    draw.text((pos[1],22),lineDir[dir][1],fill=fgColor,font=EnglishFont,anchor="rs")
    #central line
    draw.line([16,27,112,27],fill=fgColor,width = 2)
    #to-Chinese
    draw.text((40,47),"往",fill=fgColor,font=ChineseFont,anchor="ls")
    #to-English
    draw.text((88,47),"To",fill=fgColor,font=EnglishFont,anchor="rs")

    ##TITLE
    #Var Init
    fontName = "resources/fonts/arial.ttf" # for padcalc
    font = ImageFont.truetype("resources/fonts/arial.ttf",16) #12px
    rectWidthOk = False
    
    rectWidth,font,rectWidthOk = RTLineDir_BWCalc(lineData,font)
    # print(rectWidth)
    
    if rectWidthOk:
        #Rectangle
        if rectWidth % 2 == 1:
            rectWidth += 1
        #startpoint calc
        startPoint = (W-rectWidth)/2
        SCstart = startPoint + draw.textlength(lineData[0], font = font) + 6

        #Numbers
        padLN = padCalc(lineData[0],fontName,font)
        padSC = padCalc(lineData[3],fontName,font)
        # padLN = 0
        # padSC = 0
        
        roundRect(im,[startPoint,56,SCstart-1,75],radius=4,fill=lineData[1],corners=[True,False,False,True])
        roundRect(im,[SCstart,56,startPoint+rectWidth-1,75],radius=4,fill="#696969",corners=[False,True,True,False])
        draw.text((startPoint+3+padLN,72), lineData[0], fill=lineData[2],font=font,anchor="ls")
        draw.text((SCstart+3+padSC,72), lineData[3], fill = fgColor, font = font,anchor="ls")
    
    im.save("output.png")

def Chinese(bgColor,ChineseText):

    #Var Init
    W, H = (128,128)
    if bgColor == 1:
        fgColor = "#0d0d0d"
    else:
        fgColor = "white"

    #Open Image
    im = Image.open("output.png")
    draw = ImageDraw.Draw(im)
    
    ##CHINESE TEXT
    
    #Var Init
    ChineseFont = "resources/fonts/msjh.ttf"
    EnglishFont = "resources/fonts/arial.ttf"
    fontSize = 16
    
    ChineseWidths,ChiWidthTotal,charFonts,ok = ChiWidthCalc(W,ChineseText,ChineseFont,EnglishFont,fontSize)
    
    #Text
    if ok:
        for i in range(len(ChineseWidths)):
            startPoint = (W-ChiWidthTotal)/2 + sum(ChineseWidths[:i])
            draw.text((startPoint,98), ChineseText[i], fill = fgColor, font = charFonts[i], anchor = "ls")
            
    im.save("output.png")

def English(bgColor,EnglishText):
    
    #Var Init
    W, H = (128,128)
    EnglishFontSize = 16
    ok = False
    if bgColor == 1:
        fgColor = "black"
    else:
        fgColor = "white"

    #Open Image
    im = Image.open("output.png")
    draw = ImageDraw.Draw(im)
    

    ##ENGLISH TEXT
    
    #Var Init
    EnglishFont = ImageFont.truetype("resources/fonts/arial.ttf",EnglishFontSize)
    EnglishWidth = draw.textlength(EnglishText, font = EnglishFont)
    
    while EnglishFontSize >= 10:
        if EnglishWidth > W-6:
            EnglishFontSize -= 1
            EnglishFont = ImageFont.truetype("resources/fonts/arial.ttf", EnglishFontSize)
            EnglishWidth = draw.textlength(EnglishText, font = EnglishFont)
            if EnglishFontSize < 10:
                print("English target station name is too long! Please shorten it.")
                break
        else:
            ok = True
            break
        
    if ok:
        draw.text((W/2,119), EnglishText, fill = fgColor, font = EnglishFont, anchor = "ms")
        
    im.save("output.png")