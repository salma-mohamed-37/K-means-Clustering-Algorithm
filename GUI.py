from tkinter import *
from tkinter import filedialog
import os
import pandas as pd
from algorithm import kmeans

file=""

def open_file_dialog():
    file_path = filedialog.askopenfilename()
    if file_path:
        global file
        file = file_path
        file_name = os.path.basename(file_path)
        label1.config(text=f"{file_name}")

def submit():
    percentage = float(txt1.get())
    k = int(txt2.get())
    
    global file
    result1, result2=kmeans (file, k, percentage)
    view_results(result1, result2)  

def view_results(result1, result2):
    result = "Clusters \n"+result1+"\n"+result2+"\n \n \n \n"
    text_widget1 = Text(frame, wrap=WORD, font=('Arial', 16)) 
    text_widget1.grid(row=6, column=0, columnspan=10)
    text_widget1.insert(END, result)

# Create root window
root = Tk()
root.configure(bg="white")
root.title("Data Mining Assignment 2")

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

root.geometry(f"{screen_width}x{screen_height}")

# Create a frame to hold the widgets
frame = Frame(root, bg="white")
frame.pack()  # Expand to fill the window


# Create widgets inside the frame
title = Label(frame, text="Problem 1", font=('Arial', 16, 'bold'), fg="pink", bg="white")
title.grid(row=0, column=1)

btn1 = Button(frame, text="Upload File", command=open_file_dialog, fg="white", bg="pink", font=('Arial', 16))
btn1.grid(row=1, column=1)
  
label1 =Label(frame, text="", font=('Arial', 16), fg="pink", bg="white")  
label1.grid(row=2, column=1)

label2 = Label(frame, text="Percentage of the file to use: ", font=('Arial', 16), fg="pink", bg="white")
label2.grid(row=3, column=0)

txt1 = Entry(frame, width=20, fg="white", bg="pink", font=('Arial', 16))
txt1.grid(row=3, column=2)

label3 = Label(frame, text="K: ", font=('Arial', 16), fg="pink", bg="white")
label3.grid(row=4, column=0)

txt2 = Entry(frame, width=20,font=('Arial', 16), fg="white", bg="pink")
txt2.grid(row=4, column=2)

btn2 = Button(frame, text="Submit",font=('Arial', 16), fg="white", bg="pink", command=submit)
btn2.grid(row=5, column=1)

root.mainloop()
