from PIL import Image

originalPath = r"examples\x2_route_map_desc.png"
im = Image.open(originalPath)
imoutput = im.resize((640,256),resample=Image.Resampling.NEAREST)

savelocation = input("Override? (y/N):\n")

imoutput.save("output2.png")
if savelocation == "y" or "Y":
    imoutput.save(originalPath)