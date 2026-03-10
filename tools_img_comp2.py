from PIL import Image

originalPath = "resources/test.png"

im = Image.open(originalPath)
imoutput = im.resize((10,10),Image.Resampling.BOX)
# original need: 10,21(?)

# imoutput.save("output2.png")

im2 = Image.new("RGBA",(64,64),"white")
im2.alpha_composite(imoutput,(27,27))

im2.save("output2.png")