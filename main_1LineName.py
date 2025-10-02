from PIL import Image, ImageDraw, ImageFont

def title(titleText,titleSize,titleBgHeight,titleColor="#FFFFFF",titleBgOutln="#FFFFFF",titleBgFill=None):
    
    #Var Init
    W, H = (128,128)
    
    #Open image
    im = Image.open("output.png")
    draw = ImageDraw.Draw(im)

    ##TITLE
    
    #Var init
    TitleFont = ImageFont.truetype("resources/fonts/Britannic-Bold.ttf", titleSize)
    TitleFontSmall = ImageFont.truetype("resources/fonts/Britannic-Bold.ttf", int(titleSize*0.75))
    titleShrink = False
    titleWidth = draw.textlength(titleText, font = TitleFont)
    print(titleWidth)

    #Check if too big
    if titleWidth > 96: # titleHeight > 60(won't happen)
        titleWidth = draw.textlength(titleText, font = TitleFontSmall)
        print("New Size:", titleWidth)
        titleShrink = True

    #Title Background 
    if titleBgHeight == None:
        titleBgHeight = titleSize
    
    if titleWidth <= 60:
        draw.rectangle([32, 12, 95, 75], fill = titleBgFill, outline = titleBgOutln, width = 3)#[32, 44-titleBgHeight/2, 95, 44+titleBgHeight/2-1]
    else:
        draw.rectangle([(W-titleWidth)/2-4, 44-titleBgHeight/2, (W+titleWidth)/2+3, 44+titleBgHeight/2-1], fill = titleBgFill, outline = titleBgOutln, width = 3)

    #Title Text
    if titleShrink:
        draw.text((W/2,44), titleText, fill = titleColor, font = TitleFontSmall, anchor = "mm")
    elif title == "X1":
        draw.text((W/2+4,44), titleText, fill = titleColor, font = TitleFont, anchor = "mm")
    else:
        draw.text((W/2,44), titleText, fill = titleColor, font = TitleFont, anchor = "mm")
    
    #save image
    im.save("output.png")

def English(EnglishText, EnglishTextColor = "#FFFFFF"):
    
    #Var Init
    W, H = (128,128)

    #Open image
    im = Image.open("output.png")
    draw = ImageDraw.Draw(im)

    ##ENGLISH TEXT

    #Var Init
    EnglishFont = ImageFont.truetype("resources/fonts/Britannic-Bold.ttf", 16)
    EnglishFontSmall = ImageFont.truetype("resources/fonts/Britannic-Bold.ttf", 15)
    EngTextShrink = False
    EnglishWidth = draw.textlength(EnglishText, font = EnglishFont)
    print(EnglishWidth)

    #Check if too big
    if  EnglishWidth > 120: #EnglishHeight > 60(won't happen)
        EnglishWidth = draw.textlength(EnglishText, font = EnglishFontSmall)
        print("New Size:", EnglishWidth)
        EngTextShrink = True
    
    #Text
    if EngTextShrink:
        draw.text((W/2,93), EnglishText, fill = EnglishTextColor, font = EnglishFontSmall, anchor = "ms")
    else:
        draw.text((W/2,93), EnglishText, fill = EnglishTextColor, font = EnglishFont, anchor = "ms")
    
    #save image
    im.save("output.png")
    
def Chinese(ChineseText, ChineseTextColor = "#FFFFFF"):
   
    #Var Init
    W, H = (128,128)

    #Open image
    im = Image.open("output.png")
    draw = ImageDraw.Draw(im)

    ##CHINESE TEXT
    
    #Var Init
    ChineseFont = ImageFont.truetype("resources/fonts/Britannic-ZhengHei.ttf", 16)
    ChineseFontSmall = ImageFont.truetype("resources/fonts/Britannic-ZhengHei.ttf", 15)
    ChiTextShrink = False
    ChineseWidth = draw.textlength(ChineseText, font = ChineseFont)
    print(ChineseWidth)

    #Check if too big
    if ChineseWidth > 120: #ChineseHeight > 60(won't happen)
        ChineseWidth = draw.textlength(ChineseText, font = ChineseFontSmall)
        print("New Size:", ChineseWidth)
        ChiTextShrink = True
    
    #Text
    if ChiTextShrink:
        draw.text((W/2,116), ChineseText, fill = ChineseTextColor, font = ChineseFontSmall, anchor = "ms")
    else:
        draw.text((W/2,116), ChineseText, fill = ChineseTextColor, font = ChineseFont, anchor = "ms")
    
    #save image
    im.save("output.png")





#EnglishFont = ImageFont.truetype("~/Library/Fonts/Britannic-Bold.ttf", 16)
#ChineseFont = ImageFont.truetype("~/Library/Fonts/微软正黑体.ttf", 16)
