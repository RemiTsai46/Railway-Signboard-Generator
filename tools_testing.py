# import re
# string = "哈哈3"
# for char in string:
#     if re.search("[\u4e00-\u9FFF]",char):
#         print("zh")
#     else:
#         print("no")

n = 'k'
n2 = 'b'
n3 = 't'
if n in [n3,n2]:
    print("yes")
else: 
    print("no")

a = 114.114514
print(a%1)
b=0.1+0.2
print(f"{b:.40f}")


# from PIL import Image, ImageDraw

# im = Image.new("RGBA",(128,128),"#666666")
# draw = ImageDraw.Draw(im)

# draw.ellipse([32,32,95,95],fill=None,outline="#000000",width=2)
# im = im.resize((128,128),Image.Resampling.BOX)

# im.save("output3.png")

# a = input()
# print(type(a))

# x = 0x12  # 0x12 is hex(12) 
# print(x,16)
# print((hex(x)))

# x=0b101
# y=0b010
# x |= y
# print(float(x))
# print(bin(x)[2:])


# a = int(input("Enter size: "))

# for i in range(1,a+1):
#     print(" "*(a-i)+" ".join("*"*i))