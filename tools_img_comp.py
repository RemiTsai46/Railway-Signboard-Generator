from PIL import Image

originalPath = r"examples\bx_ilc_zym\502006_psap_b2_jt.png"
im = Image.open(originalPath)
imoutput = im.resize((128,128),resample=Image.Resampling.NEAREST)

savelocation = input("Override? (y/N):\n")

imoutput.save("output2.png")
if savelocation == "y" or "Y":
    imoutput.save(originalPath)