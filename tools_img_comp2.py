from PIL import Image

originalPath = "resources/test.png"

im = Image.open(originalPath)
imoutput = im.resize((10,21),Image.Resampling.BILINEAR)

imoutput.save("output2.png")