import datetime
import math
from numpy import polyfit as pf


#command = input("input command\n")
path_to_data = "../thunderbolt_data/06/"
#first_date = input("Enter starting date in format yy/mm/dd\n")
first_date = "2016/06/09"
#first_time = input("Enter starting time in format hh:mm:ss\n")
first_time = "00:00:00"
#second_date = input("Enter starting date in format yy/mm/dd\n")
second_date = "2016/06/15"
#second_time = input("Enter starting time in format hh:mm:ss\n")
second_time = "12:00:00"

up_border = float(input("Enter the latitude of the upper border\n"))
down_border = float(input("Enter the latitude of the bottom border\n"))
left_border = float(input("Enter the longitude of the left border\n"))
right_border = float(input("Enter the longitude of the right border\n"))

width = int(input("Enter horizontal resolution\n"))
height = int(input("Enter vertical resolution\n"))
max_cell_size = int(input("Enter the maximum size of cells\n"))
geometric_progression_step = int(input("Enter geometric progression step\n"))

if max_cell_size < 2:
    max_cell_size = 2

if max_cell_size > height:
    max_cell_size = height

if max_cell_size > width:
    max_cell_size = width

zone = []
for i in range(height):
    zone.append([False] * width)

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
thunderbolt_detected_flag = False

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

        if not(down_border < lat < up_border):
            continue

        if left_border < right_border:
            if not(left_border < lon < right_border):
                continue

            lon = lon - left_border
            lon = math.trunc((lon / (right_border - left_border)) * width)

            lat = up_border - lat
            lat = math.trunc((lat / (up_border - down_border)) * height)

            thunderbolt_detected_flag = True
            zone[lat][lon] = True

        if right_border < left_border:
            if lat < right_border:
                lat += 360
            right_border += 360

            lon = lon - left_border
            lon = math.trunc((lon / (right_border - left_border)) * width)

            lat = up_border - lat
            lat = math.trunc((lat / (up_border - down_border)) * height)

            thunderbolt_detected_flag = True
            zone[lat][lon] = True

    current_date = datetime.date(current_date.year, current_date.month, current_date.day + 1)

if not thunderbolt_detected_flag:
    print("Lightning discharges not detected\n")
    sys.exit

cell_size_list = []
number_of_cells_with_object_list = []
current_cell_size = 1

while current_cell_size < max_cell_size:
    counter = 0
    for y in range(0, height, current_cell_size):
        for x in range(0, width, current_cell_size):
            cell_result = False
            for yy in range(y, y+current_cell_size):
                for xx in range(x, x+current_cell_size):
                    if xx < width and yy < height:
                        cell_result |= zone[yy][xx]

            counter += cell_result

    number_of_cells_with_object_list.append(counter)
    cell_size_list.append(current_cell_size)

    current_cell_size *= geometric_progression_step

number_of_cells_with_object_list.reverse()
cell_size_list.reverse()

for i in range(len(cell_size_list)):
    cell_size_list[i] = math.log(1 / cell_size_list[i], 10)
    number_of_cells_with_object_list[i] = math.log(number_of_cells_with_object_list[i], 10)

linear_coefficients = pf(cell_size_list, number_of_cells_with_object_list, 1)
print("Fractal dimension = " + str(linear_coefficients[0]))
