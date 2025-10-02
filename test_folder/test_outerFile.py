from os import path
from PIL import Image

print(path.abspath("test_outerFile.py"))
#absPath = path.abspath("test_outerFile.py")
print(path.dirname(path.abspath("test_outerFile.py")))
parentFolder = path.dirname(path.abspath("test_outerFile.py"))

imagePath = path.abspath(path.join(parentFolder,"output.png"))
print(imagePath)

im = Image.open(imagePath)
im.show()