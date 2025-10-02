from PIL import Image, ImageDraw, ImageFont
from resources.functions.shapes import roundRect
from resources.functions.calculations import ChiWidthCalc,padCalc,RTLineName_titleFontCalc

def title(lineColor,titleText,titleSize,titleNarrow,titleBgHeight,titleColor="#FFFFFF",titleBgOutln=None):
    
    #Var Init
    W, H = (128,128)
    
    #Open image
    im = Image.open("output.png")
    draw = ImageDraw.Draw(im)

    ##TITLE
        
    fontName,font,titleWidth = RTLineName_titleFontCalc(titleText,titleSize,titleNarrow)

    #Title Background Height
    if titleBgHeight == None:
        titleBgHeight = titleSize
    
    if titleWidth <= 60:
        roundRect(im,[32,43-titleBgHeight/2,95,43+titleBgHeight/2-1], 12, lineColor, titleBgOutln,2)
    elif titleWidth <= 92:
        roundRect(im,[16,int(43-titleBgHeight/2),111,int(43+titleBgHeight/2-1)], 12, lineColor, titleBgOutln,2)
    else:
        roundRect(im,[11,int(43-titleBgHeight/2),116,int(43+titleBgHeight/2-1)], 12, lineColor, titleBgOutln,2)

    pad = padCalc(titleText,fontName,font)
    xpos = (W+pad)/2

    #Title Text
    draw.text((xpos,43), titleText, fill = titleColor, font = font, anchor = "mm")
    
    #save image
    im.save("output.png")

def English(bgColor,EnglishText):
    
    #Var Init
    W, H = (128,128)
    EnglishFontSize = 16
    if bgColor == 1:
        fgColor = "black"
    else:
        fgColor = "white"

    #Open image
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
                print("English line name is too long! Please shorten it.")
                break
        else:
            ok = True
            break
    
    #Text
    if ok:
        draw.text((W/2,94), EnglishText, fill = fgColor, font = EnglishFont, anchor = "ms")

    #save image
    im.save("output.png")
    
def Chinese(bgColor,ChineseText):
   
    #Var Init
    W, H = (128,128)

    if bgColor == 1:
        fgColor = "black"
    else:
        fgColor = "white"

    #Open image
    im = Image.open("output.png")
    draw = ImageDraw.Draw(im)

    ##CHINESE TEXT
    
    #Var Init
    ChineseFont = "resources/fonts/msjh.ttf"
    EnglishFont = "resources/fonts/arial.ttf"
    fontSize = 16

    #Length Calc
    ChineseWidths,ChiWidthTotal,charFonts,ok = ChiWidthCalc(W,ChineseText,ChineseFont,EnglishFont,fontSize)
    
    #Text
    if ok:
        for i in range(len(ChineseWidths)):
            startPoint = (W-ChiWidthTotal)/2 + sum(ChineseWidths[:i])
            draw.text((startPoint,117), ChineseText[i], fill = fgColor, font = charFonts[i], anchor = "ls")

    #save image
    im.save("output.png")
