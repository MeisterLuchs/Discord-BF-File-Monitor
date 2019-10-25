from os import getenv, walk
from time import localtime, strftime

from tkinter import Tk, StringVar, Label, Button, DISABLED, NORMAL

discord_path = getenv("APPDATA")
discord_path += "\\discord\\"

top = Tk()
top.title("Discord BF File Monitor")
top.resizable(0, 0)


def get_discord_version():
    dirlist = []
    for (_, dirs, _) in walk(discord_path):
        for dir in dirs:
            if dir not in ["blob_storage", "Cache", "GPUCache",
                           "Local Storage", "logs", "VideoDecodeStats"]:
                dirlist.append(dir)
        break
    return dirlist[-1]


discord_version = get_discord_version()

discord_path += discord_version
file1_path = discord_path + "\\modules\\discord_modules\\index.js"
file2_path = discord_path + "\\modules\\discord_desktop_core\\index.js"

time_checked1 = StringVar()
time_checked2 = StringVar()


def check_file1():
    global time_checked1
    with open(file1_path, "r") as file:
        time_checked1.set(strftime("%Y-%m-%d %H:%M:%S", localtime()))
        return file.readline() == "module.exports = require('./discord_modules.node');\n"


def check_file2():
    global time_checked2
    with open(file2_path, "r") as file:
        time_checked2.set(strftime("%Y-%m-%d %H:%M:%S", localtime()))
        return file.readline() == "module.exports = require('./core.asar');"


def cleanse1():
    with open(file1_path, "w") as file:
        file.write("module.exports = require('./discord_modules.node');\n")


def cleanse2():
    with open(file2_path, "w") as file:
        file.write("module.exports = require('./core.asar');")


file1_okay = StringVar()
file2_okay = StringVar()


def check_files():
    global file1_okay
    global file2_okay
    global status1
    global status2
    global cleanse1q
    global cleanse2q
    if check_file1():
        file1_okay.set("clean")
        status1.configure(fg="green")
        cleanse1q.configure(state=DISABLED)
    else:
        file1_okay.set("INFECTED")
        status1.configure(fg="red")
        cleanse1q.configure(state=NORMAL)
    if check_file2():
        file2_okay.set("clean")
        status2.configure(fg="green")
        cleanse2q.configure(state=DISABLED)
    else:
        file2_okay.set("INFECTED")
        status2.configure(fg="red")
        cleanse2q.configure(state=NORMAL)


show_Dv_T = Label(top, text="current Discord version",
                          font=("", 7, ""))
show_Dv_T.grid(row=0, column=0, sticky="NW")
show_Dv = Label(top, text=discord_version, font=("", 7, ""))
show_Dv.grid(row=0, column=3, sticky="NE")

table_head1 = Label(top, text="module", font=("", 9, "bold"))
table_head1.grid(row=1, column=0)
table_head2 = Label(top, text="last checked", font=("", 9, "bold"))
table_head2.grid(row=1, column=1)
table_head3 = Label(top, text="status", font=("", 9, "bold"))
table_head3.grid(row=1, column=2)

file1 = Label(top, text="discord_modules")
file1.grid(row=2, column=0)
checked1 = Label(top, textvariable=time_checked1)
checked1.grid(row=2, column=1)
status1 = Label(top, textvariable=file1_okay)
status1.grid(row=2, column=2)

file2 = Label(top, text="discord_desktop_core")
file2.grid(row=3, column=0)
checked2 = Label(top, textvariable=time_checked2)
checked2.grid(row=3, column=1)
status2 = Label(top, textvariable=file2_okay)
status2.grid(row=3, column=2)

cleanse1q = Button(text="CLEANSE", command=cleanse1, state=DISABLED)
cleanse1q.grid(row=2, column=3)
cleanse2q = Button(text="CLEANSE", command=cleanse2, state=DISABLED)
cleanse2q.grid(row=3, column=3)


def mainloop():
    check_files()
    top.after(300000, mainloop)


top.after(0, mainloop)
top.mainloop()
