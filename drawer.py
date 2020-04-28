import matplotlib.pyplot as plt
from tkinter import *
from PIL import Image
from tkinter import scrolledtext

input_text_box_time_step_size = 1
input_text_box_time_step_count = 1
input_text_box_file_template_name = 1
log_text_box = 1
color_coefficient = 5


def draw_start():
    global input_text_box_time_step_size
    global input_text_box_time_step_count
    global input_text_box_file_template_name
    global log_text_box

    file_template = input_text_box_file_template_name.get()
    step_count = input_text_box_time_step_count.get()
    step_size = input_text_box_time_step_size.get()

    if "" in (file_template, step_count, step_size):
        log_text_box.insert(END, "Error: Empty field detected\n")
        return

    try:
        step_size = int(step_size)
        step_count = int(step_count)
    except Exception:
        log_text_box.insert(END, "Error: Wrong size or count format\n")
        return

    for time_step_cycle_counter in range(step_count):
        try:
            input_file = open(file_template + '_' + str((time_step_cycle_counter + 1) * step_size) + "_days.txt", 'r')
            input_string = input_file.readline()  # reading of human-readable string
            input_string = input_file.readline()  # reading string of cell sizes
            cell_size_list = input_string[1:-2:].split(', ')
            for i in range(len(cell_size_list)):
                cell_size_list[i] = float(cell_size_list[i])
            input_string = input_file.readline()  # reading of human-readable string
            input_string = input_file.readline()  # reading string of number of cells with object list
            number_of_cells_with_object_list = input_string[1:-2:].split(', ')
            for i in range(len(number_of_cells_with_object_list)):
                number_of_cells_with_object_list[i] = float(number_of_cells_with_object_list[i])

            plt.plot(cell_size_list, number_of_cells_with_object_list, marker='x',
                     label=str((time_step_cycle_counter + 1) * step_size) + " days")

            input_file.close()
        except FileNotFoundError:
            log_text_box.insert(END, "File " + file_template + '_' +
                                str((time_step_cycle_counter + 1) * step_size) + "_days.txt" + " not found\n")
        except Exception:
            log_text_box.insert(END, "File " + file_template + '_' +
                                str((time_step_cycle_counter + 1) * step_size) + "_days.txt" + "corrupted error\n")

    plt.legend()
    plt.show()

    try:
        input_file = open(file_template + '_table.txt', 'r')
        height = int(input_file.readline()[:-1:])
        width = int(input_file.readline()[:-1:])

        draw_table = []
        for i in range(height):
            draw_table.append(input_file.readline()[:-1:].split(' '))

        maximum = -1
        for i in range(height):
            for j in range(width):
                draw_table[i][j] = int(draw_table[i][j])
                if draw_table[i][j] > maximum:
                    maximum = draw_table[i][j]

        img = Image.new('RGB', (height * 4, width * 4), (0, 0, 150))
        gradient_picture = Image.open("gradient.jpg")

        for i in range(height):
            for j in range(width):
                for bonus_x in range(4):
                    for bonus_y in range(4):
                        color_coefficient = int(gradient_picture.size[0] * float(draw_table[i][j] / maximum))
                        color = gradient_picture.getpixel((min(color_coefficient + 1, gradient_picture.size[0] - 1), 1))
                        img.putpixel((i * 4 + bonus_x, j * 4 + bonus_y), color)
        d = 1
        img.show()
        #img.save(file_template + "_picture.jpg", "JPEG")
        img.save(file_template + "_picture.jpg", "JPEG")
        log_text_box.insert(END, "File " + file_template + '_picture.jpg' + " saved1\n")
    except FileNotFoundError:
        log_text_box.insert(END, "File " + file_template + '_table.txt' " wasn't found\n")
    except Exception:
        log_text_box.insert(END, "Unexpected error\n")


drawer_window = Tk()
drawer_window.title("drawer")
drawer_window.geometry('770x770')

label_time_step_size = Label(drawer_window, text="Size of time steps:")
label_time_step_size.grid(column=0, row=1)

input_text_box_time_step_size = Entry(drawer_window, justify=CENTER)
input_text_box_time_step_size.grid(column=1, row=1)

label_time_step_count = Label(drawer_window, text="Amount of time steps:")
label_time_step_count.grid(column=0, row=2)

input_text_box_time_step_count = Entry(drawer_window, justify=CENTER)
input_text_box_time_step_count.grid(column=1, row=2)

label_file_template_name = Label(drawer_window, text="File template name:")
label_file_template_name.grid(column=0, row=3)

input_text_box_file_template_name = Entry(drawer_window, justify=CENTER)
input_text_box_file_template_name.grid(column=1, row=3)

log_text_box = scrolledtext.ScrolledText(drawer_window, width=90)
log_text_box.grid(column=0, columnspan=5, row=13, rowspan=10, sticky=S+W+E)

start_collection_button = Button(drawer_window, text="Draw", command=draw_start)
start_collection_button.grid(column=0, row=12)

drawer_window.mainloop()
