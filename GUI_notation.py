import re
from tkinter import *
from tkinter import ttk
import pandas as pd
import time
import os

##################################################
# change the data name here!
origin_data = "test03"
##################################################
origin_datafile = f"{origin_data}.pkl"
problem_file = f"{origin_data}_test_problems.txt"


# problem_file is used to store the bug info, details in problem_sentence()


def display_sentence(event=None):
    global data
    global current_sentence_index
    global len_data
    global len_person

    ##################################################################
    # choose whether to jump the labelled ones
    if data.iloc[current_sentence_index]['raw_label'][3] == "1" or data.iloc[current_sentence_index]['raw_label'][
        3] == "0" or data.iloc[current_sentence_index]['raw_label'][3] == "5":
        # display_next_sentence()
        1
    ###################################################################

    # --------------------------------------------------------------------------#
    """Pre_handling the origin data."""
    sentence = data.iloc[current_sentence_index]['sent_list'][0]
    information = f"Person:{data.iloc[current_sentence_index]['sample_source']}, label: {data.iloc[current_sentence_index]['raw_label'][3]} \n"
    if data.iloc[current_sentence_index]['raw_label'][5] == "full":
        temp_name = data.iloc[current_sentence_index]['raw_label'][0]
    else:
        temp_name = data.iloc[current_sentence_index]['sample_source']
    temp_time = data.iloc[current_sentence_index]['raw_label'][1]
    temp_loc = data.iloc[current_sentence_index]['raw_label'][2]
    rule = f"姓名:{temp_name},时间:{temp_time},地点:{temp_loc}。"
    # --------------------------------------------------------------------------#

    # --------------------------------------------------------------------------#
    """Separate the layout of the data."""
    text_area.delete("1.0", END)
    text_area.insert("1.0",
                     f"Person: {data.iloc[current_sentence_index]['person_index']}/{len_person}, index: {current_sentence_index + 1}/{len_data}\n")
    text_area.insert("2.0", information)
    text_area.insert("3.0", f"{sentence}\n")
    text_area.insert("4.0", f"\n")
    text_area.insert("5.0", f"{rule}")
    # --------------------------------------------------------------------------#

    # --------------------------------------------------------------------------#
    """Highlight the part of the data."""
    if data.iloc[current_sentence_index]['raw_label'][5] == "full":
        text_area.tag_add("person", f"3.{data.iloc[current_sentence_index]['raw_label'][6][0][0]}",
                          f"3.{data.iloc[current_sentence_index]['raw_label'][6][0][1]}")
    else:
        text_area.tag_add("person", f"2.7", f"2.{7 + len(data.iloc[current_sentence_index]['sample_source'])}")
    if data.iloc[current_sentence_index]['raw_label'][3] == "5":
        text_area.tag_add("error", "2.0", "3.0")
    text_area.tag_add("time", f"3.{data.iloc[current_sentence_index]['raw_label'][6][1][0]}",
                      f"3.{data.iloc[current_sentence_index]['raw_label'][6][1][1]}")
    text_area.tag_add("location", f"3.{data.iloc[current_sentence_index]['raw_label'][6][2][0]}",
                      f"3.{data.iloc[current_sentence_index]['raw_label'][6][2][1]}")
    text_area.tag_add("person", f"5.3", f"5.{3 + len(temp_name)}")
    text_area.tag_add("time", f"5.{7 + len(temp_name)}", f"5.{7 + len(temp_name) + len(temp_time)}")
    text_area.tag_add("location", f"5.{11 + len(temp_name) + len(temp_time)}",
                      f"5.{11 + len(temp_name) + len(temp_time) + len(temp_loc)}")
    # --------------------------------------------------------------------------#

    # --------------------------------------------------------------------------#
    """Set the style of the font."""
    text_area.configure(font=("楷体", 30))
    text_area.tag_config('person', font=('楷体', 30, 'bold'), background="bisque", foreground="red", underline=0)
    text_area.tag_config('time', font=('楷体', 30, 'bold'), background="lightgreen", foreground="red", underline=0)
    text_area.tag_config('location', font=('楷体', 30, 'bold'), background="khaki", foreground="red", underline=0)
    text_area.tag_config('error', font=('楷体', 30, 'bold'), background="yellow", foreground="red", underline=1)
    # --------------------------------------------------------------------------#

def display_previous_sentence(event=None):
    global current_sentence_index
    if current_sentence_index > 0:
        current_sentence_index = current_sentence_index - 1
    display_sentence(current_sentence_index)


def display_next_sentence(event=None):
    global current_sentence_index
    global len_data
    if current_sentence_index < len_data - 1:
        current_sentence_index = current_sentence_index + 1
    display_sentence(current_sentence_index)


def label_sentence_true():
    global current_sentence_index
    global data
    temp_list = list(data.iloc[current_sentence_index]['raw_label'])
    temp_list[3] = '1'
    new_raw_label = tuple(temp_list)
    data.at[current_sentence_index, 'raw_label'] = new_raw_label


def label_sentence_false():
    global current_sentence_index
    global data
    temp_list = list(data.iloc[current_sentence_index]['raw_label'])
    temp_list[3] = '0'
    new_raw_label = tuple(temp_list)
    data.at[current_sentence_index, 'raw_label'] = new_raw_label


def problem_sentence():
    global current_sentence_index
    global data
    global len_data
    global len_person

    # --------------------------------------------------------------------------#
    "label!"
    temp_list = list(data.iloc[current_sentence_index]['raw_label'])
    temp_list[3] = '5'
    new_raw_label = tuple(temp_list)
    data.at[current_sentence_index, 'raw_label'] = new_raw_label
    # --------------------------------------------------------------------------#

    if data.iloc[current_sentence_index]['raw_label'][5] == "full":
        temp_name = data.iloc[current_sentence_index]['raw_label'][0]
    else:
        temp_name = data.iloc[current_sentence_index]['sample_source']
    temp_time = data.iloc[current_sentence_index]['raw_label'][1]
    temp_loc = data.iloc[current_sentence_index]['raw_label'][2]
    # --------------------------------------------------------------------------#
    "Write the bug file!"
    with open(problem_file, "a") as f:
        f.write(
            f"The problem lines on: Person: {data.iloc[current_sentence_index]['person_index']}/{len_person}, index: {current_sentence_index + 1}/{len_data}.\n")
        f.write(f"姓名:{temp_name},时间:{temp_time},地点:{temp_loc}。\n")


def save():
    global temp_save_time
    global data
    temp_save_time = 0  # reset the save time
    data.to_pickle(origin_datafile)
    print("Saved!")


def keyBack(evt):
    global current_sentence_index
    global temp_save_time
    global save_time
    global len_data
    # --------------------------------------------------------------------------#
    """The data is labeled false!"""
    if evt.char == '0':
        label_sentence_false()
        if current_sentence_index < len_data - 1:
            current_sentence_index += 1
        temp_save_time += 1
    # --------------------------------------------------------------------------#
    """The data is labeled true!"""
    if evt.char == '1':
        label_sentence_true()
        if current_sentence_index < len_data - 1:
            current_sentence_index += 1
        temp_save_time += 1
    # --------------------------------------------------------------------------#
    """The data has problem!"""
    if evt.char == '5':
        problem_sentence()
        if current_sentence_index < len_data - 1:
            current_sentence_index += 1
        temp_save_time += 1
    # --------------------------------------------------------------------------#
    """It is time to save the data!"""
    if temp_save_time == save_time:
        save()
    # --------------------------------------------------------------------------#
    """Go to the next data!"""
    display_sentence(current_sentence_index)


#############################################################################
"""This is used for the GUI"""

root = Tk()
root.title("Notation tool")
root.bind("<Left>", display_previous_sentence)
root.bind("<Right>", display_next_sentence)
root.bind("<Key>", keyBack)
# Create the text area and label input
text_area = Text(root, width=50, height=20)
text_area.grid(row=0, column=0, columnspan=3, padx=10, pady=10)
#############################################################################


#############################################################################
"""This is used for the data loading"""

data = pd.read_pickle(origin_datafile)
save_time = 1  # the time before data will be saved
temp_save_time = 0
current_sentence_index = 0
len_data = len(data)  # the length of the whole data pieces
len_person = data.at[len_data - 1, 'person_index']  # the length of the whole people in the data file

# to find the first unlabelled data, set the idx as the current_sentence_index
for idx in range(len_data):
    if data.iloc[idx]['raw_label'][3] != "1" and data.iloc[idx]['raw_label'][3] != "0":
        current_sentence_index = idx + 1
        print(data.iloc[idx]['raw_label'][3])
        break
#############################################################################
"""GUI start here"""
display_sentence()
root.mainloop()
