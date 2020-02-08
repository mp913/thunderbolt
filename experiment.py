from PIL import Image, ImageDraw


figure = Image.open("exp.jpg")
draw = ImageDraw.Draw(figure)

draw.point((10, 20), (255, 0, 0))

figure.save("exp.jpg", "JPEG")