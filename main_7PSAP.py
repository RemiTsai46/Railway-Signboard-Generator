from PIL import Image, ImageDraw, ImageFont

def bgBox(isCurrSta, ChineseText, EnglishText):

    if isCurrSta:

        #Var Init
        W = 128
        EnglishFontSize = 13
        boxWidth = 0

        #Open image
        im = Image.open("output.png")
        draw = ImageDraw.Draw(im)
        #Var Init
        ChineseFont = ImageFont.truetype("resources/msjh.ttf", 18)
        ChineseWidth = draw.textlength(ChineseText, font = ChineseFont)
        EnglishFont = ImageFont.truetype("resources/arial.ttf", EnglishFontSize)
        EnglishWidth = draw.textlength(EnglishText, font = EnglishFont)

        #Check if too long
        while EnglishFontSize >= 9:
            if EnglishWidth > 122:
                EnglishFontSize = EnglishFontSize - 1
                EnglishFont = ImageFont.truetype("resources/arial.ttf", EnglishFontSize)
                EnglishWidth = draw.textlength(EnglishText, font = EnglishFont)
                if EnglishFontSize < 9:
                    print("English station name is too long! Please shorten the name.")
                    break
            else:
                break

        #Calc box width
        boxWidth = max(ChineseWidth,EnglishWidth) + 16
        if boxWidth > 126:
            boxWidth = 126
        if boxWidth % 2 == 1:
            boxWidth = boxWidth + 1

        draw.rectangle([16,(W-boxWidth)/2,65,(W+boxWidth)/2],fill="black")
        
def Chinese(isCurrSta, ChineseText):
    
    #Var Init
    W = 384
 
    #Open image
    im = Image.open("output.png")
    draw = ImageDraw.Draw(im)

    ##CHINESE TEXT

    ChineseFont = ImageFont.truetype("resources/msjh.ttf", 18)
    ChineseFontSmall = ImageFont.truetype("resources/msjh.ttf", 14)
    if isCurrSta:
        draw.text((W/2,44), ChineseText, fill = "white", font = ChineseFont, anchor = "ms")
    else:
        draw.text((W/2,44), ChineseText, fill = "black", font = ChineseFontSmall, anchor = "ms")


    im.save("output.png")

def English(isCurrSta, EnglishText):
    
    #Var Init
    W = 384
    EnglishFontSize = 13
    EnglishFontSmallSize = 9
    EnglishWidthOk = False

    #Open image
    im = Image.open("output.png")
    draw = ImageDraw.Draw(im)

    ##ENGLISH TEXT

    #Var Init
    EnglishFont = ImageFont.truetype("resources/arial.ttf", EnglishFontSize)
    EnglishFontSmall = ImageFont.truetype("resources/msjh.ttf", EnglishFontSmallSize)
    EnglishWidth = draw.textlength(EnglishText, font = EnglishFont)
    
    #Check if too long
    while EnglishFontSize >= 9:
        if EnglishWidth > 122:
            EnglishFontSize = EnglishFontSize - 1
            EnglishFont = ImageFont.truetype("resources/arial.ttf", EnglishFontSize)
            EnglishWidth = draw.textlength(EnglishText, font = EnglishFont)
            if EnglishFontSize < 9:
                print("English station name is too long! Please shorten the name.")
                break
        else:
            EnglishWidthOk = True
            break

    if EnglishWidthOk:
        if isCurrSta:
            draw.text((W/2,58), EnglishText, fill = "white", font = EnglishFont, anchor = "mm")
        else:
            draw.text((W/2,58), EnglishText, fill = "black", font = EnglishFontSmall, anchor = "mm")
    
    im.save("output.png")