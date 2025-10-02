from PIL import Image, ImageDraw, ImageFont

W, H = (128,128)

#New image
im = Image.new("RGBA",(W,H),"white")
draw = ImageDraw.Draw(im)

ChineseFont = ImageFont.truetype("resources/fonts/msjh.ttf", 20)
draw.text((64,43),"鐵",fill = "black",font = ChineseFont, anchor="mm")

EnglishFont = ImageFont.truetype("resources/fonts/arial.ttf",10)
EnglishFontN = ImageFont.truetype("resources/fonts/arialn.ttf",16)
draw.text((56,85),"Cl",fill = "black",font = EnglishFont, anchor="mm")
draw.text((72,85),"Cl",fill = "black",font = EnglishFontN, anchor="mm")
textlen = draw.textlength("Clockwise",font=EnglishFont)
print(textlen)
#draw.rectangle([64,64,64+textlen-1,108],outline="red")

test_bool = False

test_int = int(test_bool)
print(test_int)

im.save("outputText.png")