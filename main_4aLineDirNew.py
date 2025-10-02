from PIL import Image, ImageDraw, ImageFont
from resources.value_sets import lineDir
from resources.functions.calculations import padCalc,ChiWidthCalc,LineDirNew_BWCalc

def targetSta(bgColor,dir,lineData):
    
    #Var Init
    W, H = (128,128)
    if bgColor == 1:
        fgColor = "black"
    else:
        fgColor = "white"

    #Open Image
    im = Image.open("output.png")
    draw = ImageDraw.Draw(im)
    

    ##DIRECTION/TO
    #Var Init
    ChineseFont = ImageFont.truetype("resources/fonts/msjh.ttf",16)
    EnglishFont = ImageFont.truetype("resources/fonts/arial.ttf",16)
    
    #dir-Chinese
    draw.text((4,19),lineDir[dir][0],fill=fgColor,font=ChineseFont,anchor="ls")
    #dir-English
    draw.text((124,19),lineDir[dir][1],fill=fgColor,font=EnglishFont,anchor="rs")
    #to-Chinese
    draw.text((27,51),"往",fill=fgColor,font=ChineseFont,anchor="rs")
    #to-English
    draw.text((27,71),"To",fill=fgColor,font=EnglishFont,anchor="rs")

    im.save("output.png")

    ##TITLE
    #Var Init
    LNFontName = "resources/fonts/arial.ttf"
    SCFontName = "resources/fonts/arial.ttf"
    lineNameFont = ImageFont.truetype("resources/fonts/arial.ttf",19) #14px
    stnCodeFont = ImageFont.truetype("resources/fonts/arial.ttf",16) #12px
    rectWidthOk = False
    
    rectWidth,lineNameFont,stnCodeFont,rectWidthOk = LineDirNew_BWCalc(lineData,lineNameFont,stnCodeFont)
    print(rectWidth)
    
    if rectWidthOk:
        #Rectangle
        if rectWidth % 2 == 1:
            rectWidth += 1
        startPoint = 77-rectWidth/2
        draw.rounded_rectangle([startPoint,24,startPoint+rectWidth-1,71],radius=5,outline=lineData[1],width=3)
        #this line below is for better look of the rectangle
        draw.rounded_rectangle([startPoint,24,startPoint+rectWidth-1,71],radius=3,outline=lineData[1],width=3)
        draw.rectangle([startPoint,27,startPoint+rectWidth-1,47],fill=lineData[1])

        #Numbers
        pad = padCalc(lineData[0],LNFontName,lineNameFont)
        xpos = 77 + pad
        draw.text((xpos,36),text=lineData[0],fill=lineData[2],font=lineNameFont,anchor="mm")
        draw.text((77,58),text=lineData[3],fill=fgColor,font=stnCodeFont,anchor="mm")
    
    im.save("output.png")

def Chinese(bgColor,ChineseText):

    #Var Init
    W, H = (128,128)
    if bgColor == 1:
        fgColor = "black"
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
            draw.text((startPoint,94), ChineseText[i], fill = fgColor, font = charFonts[i], anchor = "ls")
            
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
        draw.text((W/2,115), EnglishText, fill = fgColor, font = EnglishFont, anchor = "ms")
        
    im.save("output.png")