import datetime
from PIL import Image, ImageDraw
import math

#command = input("input command\n")
path_to_data = "../thunderbolt_data/06/"
#first_date = input("Enter starting date in format yy/mm/dd\n")
first_date = "2016/06/01"
#first_time = input("Enter starting time in format hh:mm:ss\n")
first_time = "00:00:00"
#second_date = input("Enter starting date in format yy/mm/dd\n")
second_date = "2016/06/29"
#second_time = input("Enter starting time in format hh:mm:ss\n")
second_time = "23:59:59"

first_date = first_date.split('/')
first_time = first_time.split(':')
first_date = datetime.date(int(first_date[0]), int(first_date[1]), int(first_date[2]))
first_time = float(first_time[0]) * 3600 + float(first_time[1]) * 60 + float(first_time[2])

second_date = second_date.split('/')
second_time = second_time.split(':')
second_date = datetime.date(int(second_date[0]), int(second_date[1]), int(second_date[2]))
second_time = float(second_time[0]) * 3600 + float(second_time[1]) * 60 + float(second_time[2])

current_date = first_date
counter = 0

figure = Image.open("blue_marble_HD.jpg")
draw = ImageDraw.Draw(figure)
width = figure.size[0]
height = figure.size[1]
pix = figure.load()

while current_date <= second_date:
    file = open(path_to_data + "A" + str(current_date.year) + (('0' + str(current_date.month))[-2::])
                + (('0' + str(current_date.day))[-2::]) + ".loc")
    for line in file:
        line = line.split(',')
        date = line[0]
        current_time = line[1].split(':')
        current_time = float(current_time[0]) * 3600 + float(current_time[1]) * 60 + float(current_time[2])

        if current_date == first_date and current_time < first_time:
            continue
        if current_date == second_date and current_time >= second_time:
            break

        lat, lon = float(line[2]), float(line[3])

        lat = lat * -1
        lat = lat + 90
        lat = math.trunc(lat / 180 * height)

        lon = lon + 180
        lon = math.trunc(lon / 360 * width)

        draw.point((lon, lat), (255, 0, 0))
        #print(str(lon) + ' ' + str(lat))

    current_date = datetime.date(current_date.year, current_date.month, current_date.day + 1)

figure.save("result.jpg", "JPEG")
