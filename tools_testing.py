# import re
# string = "哈哈3"
# for char in string:
#     if re.search("[\u4e00-\u9FFF]",char):
#         print("zh")
#     else:
#         print("no")

# x = 0x12  # 0x12 is hex(12) 
# print(x,16)
# print((hex(x)))

# from PIL import Image, ImageDraw

# im = Image.new("RGBA",(512,512),"#666666")
# draw = ImageDraw.Draw(im)

# draw.ellipse([128,128,383,383],fill=None,outline="#000000",width=8)
# im = im.resize((128,128),Image.Resampling.BOX)

# im.save("output3.png")

# a = input()
# print(type(a))

# x=0b101
# y=0b010
# x |= y
# print(float(x))
# print(bin(x)[2:])

a = int(input("Enter size: "))

for i in range(1,a+1):
    print(" "*(a-i)+" ".join("*"*i))