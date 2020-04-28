from PIL import Image
img = Image.open("gradient.jpg")
print(img.getpixel((200, 0)))
#img.show()
