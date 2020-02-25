import datetime
import math
import matplotlib.pyplot as plt
from numpy import polyfit as pf
import sys
from tkinter import *
from tkinter import scrolledtext


input_text_box_start_date = 1
input_text_box_time_step_size = 1
input_text_box_time_step_count = 1
input_text_box_file_template_name = 1
input_text_box_up_border = 1
input_text_box_down_border = 1
input_text_box_left_border = 1
input_text_box_right_border = 1
input_width = 1
input_height = 1
input_max_cell_size = 1
input_progression_step = 1
log_text_box = 1


def data_collection():
    global input_text_box_start_date
    global input_text_box_time_step_size
    global input_text_box_time_step_count
    global input_text_box_file_template_name
    global input_text_box_up_border
    global input_text_box_down_border
    global input_text_box_left_border
    global input_text_box_right_border
    global input_width
    global input_height
    global input_max_cell_size
    global input_progression_step
    global log_text_box

    path_to_data = "../thunderbolt_data/06/"
    first_date = input_text_box_start_date.get()
    if first_date == '':
        first_date = "2016/06/01"

    time_step_size = input_text_box_time_step_size.get()
    if time_step_size == '':
        time_step_size = 5
    else:
        time_step_size = int(time_step_size)

    time_step_count = input_text_box_time_step_count.get()
    if time_step_count == '':
        time_step_count = 5
    else:
        time_step_count = int(time_step_count)

    file_template = input_text_box_file_template_name.get()
    if file_template == '':
        file_template = '_'

    up_border = input_text_box_up_border.get()
    if up_border == '':
        up_border = 9.1
    else:
        up_border = float(up_border)

    down_border = input_text_box_up_border.get()
    if down_border == '':
        down_border = 8.9
    else:
        down_border = float(down_border)

    left_border = input_text_box_up_border.get()
    if left_border == '':
        left_border = -79.6
    else:
        left_border = float(left_border)

    right_border = input_text_box_up_border.get()
    if right_border == '':
        right_border = -79.4
    else:
        right_border = float(right_border)

    width = input_width.get()
    if width == '':
        width = 200
    else:
        width = int(width)

    height = input_height.get()
    if height == '':
        height = 200
    else:
        height = int(height)

    max_cell_size = input_max_cell_size.get()
    if max_cell_size == '':
        max_cell_size = 200
    else:
        max_cell_size = int(max_cell_size)

    progression_step = input_progression_step.get()
    if progression_step == '':
        progression_step = 2
    else:
        progression_step = int(progression_step)

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
    second_date = datetime.date(int(first_date[0]), int(first_date[1]), int(first_date[2]))
    first_date = datetime.date(int(first_date[0]), int(first_date[1]), int(first_date[2]))

    counter = 0
    thunderbolt_detected_flag = False

    for time_step_cycle_counter in range(time_step_count):
        current_date = datetime.date(second_date.year, second_date.month, second_date.day)
        second_date = current_date + datetime.timedelta(days=time_step_size)
        while current_date <= second_date:
            path_to_data = "../thunderbolt_data/" + '0' * (2 - len(str(current_date.month)))\
                           + str(current_date.month) + '/'
            file = open(path_to_data + "A" + str(current_date.year) + (('0' + str(current_date.month))[-2::])
                        + (('0' + str(current_date.day))[-2::]) + ".loc")
            for line in file:
                line = line.split(',')
                date = line[0]
                current_time = line[1].split(':')
                current_time = float(current_time[0]) * 3600 + float(current_time[1]) * 60 + float(current_time[2])

                lat, lon = float(line[2]), float(line[3])

                if not (down_border < lat < up_border):
                    continue

                if left_border < right_border:
                    if not (left_border < lon < right_border):
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

            current_date = current_date + datetime.timedelta(days=1)

        if not thunderbolt_detected_flag:
            print("Lightning discharges not detected\n")
            return

        cell_size_list = []
        number_of_cells_with_object_list = []
        current_cell_size = 1

        while current_cell_size <= max_cell_size:
            counter = 0
            for y in range(0, height, current_cell_size):
                for x in range(0, width, current_cell_size):
                    cell_result = False
                    for yy in range(y, y + current_cell_size):
                        for xx in range(x, x + current_cell_size):
                            if xx < width and yy < height:
                                cell_result |= zone[yy][xx]

                    counter += cell_result

            number_of_cells_with_object_list.append(counter)
            cell_size_list.append(current_cell_size)
            current_cell_size *= progression_step

        cell_size_list.reverse()
        number_of_cells_with_object_list.reverse()

        for i in range(len(cell_size_list)):
            cell_size_list[i] = math.log(1 / cell_size_list[i], 10)
            number_of_cells_with_object_list[i] = math.log(number_of_cells_with_object_list[i], 10)

        output = open(file_template + '_' + str((time_step_cycle_counter + 1) * time_step_size) + "_days.txt", 'w')
        output.write("cell size: \n")
        output.write(str(cell_size_list))
        output.write('\n')
        output.write("cell with charge amount: \n")
        output.write(str(number_of_cells_with_object_list))
        output.write('\n')

    log_text_box.insert(END, "Data collection completed successfully\n")
    # linear_coefficients = pf(cell_size_list, number_of_cells_with_object_list, deg=1)
    # x = cell_size_list
    # y = []
    # for i in x:
    #    y.append(linear_coefficients[0] * i + linear_coefficients[1])
    # fig = plt.figure(figsize=(20, 10))
    # plt.scatter(cell_size_list, number_of_cells_with_object_list, color='orange', s=40, marker='x')
    # plt.plot(x, y)
    # plt.show()

#print("Fractal dimension = " + str(linear_coefficients[0]))


data_collection_window = Tk()
data_collection_window.title("collect data")
data_collection_window.geometry('770x770')

label_start_date = Label(data_collection_window, text="Start date:")
label_start_date.grid(column=0, row=0)

input_text_box_start_date = Entry(data_collection_window, justify=CENTER)
input_text_box_start_date.grid(column=1, row=0)

label_time_step_size = Label(data_collection_window, text="Size of time steps:")
label_time_step_size.grid(column=0, row=1)

input_text_box_time_step_size = Entry(data_collection_window, justify=CENTER)
input_text_box_time_step_size.grid(column=1, row=1)

label_time_step_count = Label(data_collection_window, text="Amount of time steps:")
label_time_step_count.grid(column=0, row=2)

input_text_box_time_step_count = Entry(data_collection_window, justify=CENTER)
input_text_box_time_step_count.grid(column=1, row=2)

label_file_template_name = Label(data_collection_window, text="File template name:")
label_file_template_name.grid(column=0, row=3)

input_text_box_file_template_name = Entry(data_collection_window, justify=CENTER)
input_text_box_file_template_name.grid(column=1, row=3)

label_up_boarder = Label(data_collection_window, text="Up border:")
label_up_boarder.grid(column=0, row=4)

input_text_box_up_border = Entry(data_collection_window, justify=CENTER)
input_text_box_up_border.grid(column=1, row=4)

label_down_border = Label(data_collection_window, text="Down border:")
label_down_border.grid(column=0, row=5)

input_text_box_down_border = Entry(data_collection_window, justify=CENTER)
input_text_box_down_border.grid(column=1, row=5)

label_left_boarder = Label(data_collection_window, text="Left border:")
label_left_boarder.grid(column=0, row=6)

input_text_box_left_border = Entry(data_collection_window, justify=CENTER)
input_text_box_left_border.grid(column=1, row=6)

label_right_border = Label(data_collection_window, text="Right border:")
label_right_border.grid(column=0, row=7)

input_text_box_right_border = Entry(data_collection_window, justify=CENTER)
input_text_box_right_border.grid(column=1, row=7)

label_width = Label(data_collection_window, text="Horizontal resolution:")
label_width.grid(column=0, row=8)

input_width = Entry(data_collection_window, justify=CENTER)
input_width.grid(column=1, row=8)

label_height = Label(data_collection_window, text="Vertical resolution:")
label_height.grid(column=0, row=9)

input_height = Entry(data_collection_window, justify=CENTER)
input_height.grid(column=1, row=9)

label_max_cell_size = Label(data_collection_window, text="Maximum cell size:")
label_max_cell_size.grid(column=0, row=10)

input_max_cell_size = Entry(data_collection_window, justify=CENTER)
input_max_cell_size.grid(column=1, row=10)

label_progression_step = Label(data_collection_window, text="Step of the geometric progression:")
label_progression_step.grid(column=0, row=11)

input_progression_step = Entry(data_collection_window, justify=CENTER)
input_progression_step.grid(column=1, row=11)

log_text_box = scrolledtext.ScrolledText(data_collection_window, width=90)
log_text_box.grid(column=0, columnspan=5, row=13, rowspan=10, sticky=S+W+E)

start_collection_button = Button(data_collection_window, text="Start collection", command=data_collection)
start_collection_button.grid(column=0, row=12)

data_collection_window.mainloop()
