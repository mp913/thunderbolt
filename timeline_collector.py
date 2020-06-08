import datetime
import matplotlib.pyplot as plt
from tkinter import *
from tkinter import scrolledtext


input_text_box_start_date = 1
label_start_time = 1
input_text_box_start_time = 1
input_text_box_time_step_size = 1
input_text_box_time_step_count = 1
input_text_box_file_template_name = 1
log_text_box = 1


def data_collection():
    global input_text_box_start_date
    global label_start_time
    global input_text_box_start_time
    global input_text_box_time_step_size
    global input_text_box_time_step_count
    global input_text_box_file_template_name
    global log_text_box

    try:
        first_date = input_text_box_start_date.get()
        if first_date == '':
            first_date = "2016/06/01"

        first_time = input_text_box_start_time.get()
        if first_time == '':
            first_time = "00:00:00.0"
        first_time += ".0"
        
        time_step_size = input_text_box_time_step_size.get()
        if time_step_size == '':
            time_step_size = 1000000
        else:
            time_step_size = int(time_step_size)

        time_step_count = input_text_box_time_step_count.get()
        if time_step_count == '':
            time_step_count = 50
        else:
            time_step_count = int(time_step_count)

        file_template = input_text_box_file_template_name.get()
        if file_template == '':
            file_template = 'central_America_1month'

        meta_data = "first_date:" + str(first_date) + " time_step_size:" + str(time_step_size) \
                + " time_step_count:" + str(time_step_count) + " file_template:" + str(file_template) \

        first_date = first_date.split('/')
        first_time = first_time.split(':')

        left_border_datetime = datetime.datetime(int(first_date[0]), int(first_date[1]), int(first_date[2]),
                                                 int(first_time[0]), int(first_time[1]),
                                                 int(first_time[2].split('.')[0]), int(first_time[2].split('.')[1]))
        right_border_datetime = left_border_datetime + datetime.timedelta(microseconds=time_step_size * time_step_count)

        current_datetime = datetime.datetime(left_border_datetime.year,
                                             left_border_datetime.month,
                                             left_border_datetime.day,
                                             0, 0, 0, 0)

        fig, ax = plt.subplots()
        ax.set_xlabel('Steps')
        ax.set_ylabel('Number of events')
        event_count_list = [0] * time_step_count
    except Exception:
        log_text_box.insert(END, "Input error\n")
        return

    while current_datetime <= right_border_datetime:
        path_to_data = "../thunderbolt_data/" + '0' * (2 - len(str(current_datetime.month))) \
                       + str(current_datetime.month) + '/'
        file = open(path_to_data + "A" + str(current_datetime.year) + (('0' + str(current_datetime.month))[-2::])
                    + (('0' + str(current_datetime.day))[-2::]) + ".loc")
        for line in file:
            line = line.split(',')
            line_date = line[0].split('/')
            line_time = line[1].split(':')
            line_datetime = datetime.datetime(int(line_date[0]), int(line_date[1]), int(line_date[2]),
                                              int(line_time[0]), int(line_time[1]),
                                              int(line_time[2].split('.')[0]), int(line_time[2].split('.')[1]))

            if left_border_datetime <= line_datetime < right_border_datetime:
                timedelta = (line_datetime - left_border_datetime).total_seconds() * 1e6
                event_count_list[int(timedelta / time_step_size)] += 1

        current_datetime = datetime.datetime(current_datetime.year, current_datetime.month,
                                             current_datetime.day + 1,
                                             0, 0, 0, 0)

    output = open(file_template + '_timeline.txt', 'w')
    output.write(str(len(event_count_list)) + '\n')
    output.write(str(event_count_list) + '\n')
    output.write(meta_data)
    output.close()
    log_text_box.insert(END, file_template + '_timeline.txt saved successfully\n')

    plt.plot(range(len(event_count_list)), event_count_list)
    log_text_box.insert(END, "Timeline collection completed successfully\n")
    plt.legend()
    plt.show()


timeline_analysis_window = Tk()
timeline_analysis_window.title("collect data")
timeline_analysis_window.geometry('770x770')

label_start_date = Label(timeline_analysis_window, text="Start date:")
label_start_date.grid(column=0, row=0)

input_text_box_start_date = Entry(timeline_analysis_window, justify=CENTER)
input_text_box_start_date.grid(column=1, row=0)

label_start_time = Label(timeline_analysis_window, text="Start time:")
label_start_time.grid(column=0, row=1)

input_text_box_start_time = Entry(timeline_analysis_window, justify=CENTER)
input_text_box_start_time.grid(column=1, row=1)

label_time_step_size = Label(timeline_analysis_window, text="Size of time steps:")
label_time_step_size.grid(column=0, row=2)

input_text_box_time_step_size = Entry(timeline_analysis_window, justify=CENTER)
input_text_box_time_step_size.grid(column=1, row=2)

label_time_step_count = Label(timeline_analysis_window, text="Amount of time steps:")
label_time_step_count.grid(column=0, row=3)

input_text_box_time_step_count = Entry(timeline_analysis_window, justify=CENTER)
input_text_box_time_step_count.grid(column=1, row=3)

label_file_template_name = Label(timeline_analysis_window, text="File template name:")
label_file_template_name.grid(column=0, row=4)

input_text_box_file_template_name = Entry(timeline_analysis_window, justify=CENTER)
input_text_box_file_template_name.grid(column=1, row=4)

log_text_box = scrolledtext.ScrolledText(timeline_analysis_window, width=90)
log_text_box.grid(column=0, columnspan=5, row=6, rowspan=10, sticky=S+W+E)

start_collection_button = Button(timeline_analysis_window, text="Start analysis", command=data_collection)
start_collection_button.grid(column=0, row=5)

timeline_analysis_window.mainloop()
