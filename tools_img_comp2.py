from PIL import Image

originalPath = "examples/psap_zym_co_next_circled.png"

im = Image.open(originalPath)
imoutput = im.resize((128,128),Image.Resampling.BILINEAR)

imoutput.save("output2.png")