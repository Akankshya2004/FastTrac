import tkinter as tk
from tkinter import * 
from tkinter import messagebox
from tkinter import filedialog as fd
from PIL import ImageTk, Image
import moviepy.editor  
import os


mp4_file_name = ""
mp4_file_name = fd.askopenfile()
only_name = str(mp4_file_name).split("/")
only_name=only_name[-1]
only_name = only_name.split("'")
only_name=only_name[0]
mp4_file_name = only_name


os.system("python video_remove_silence.py "+ mp4_file_name)



# Create an object by passing the location as a string
Original_video = moviepy.editor.VideoFileClip(mp4_file_name)
# Contains the duration of the video in terms of seconds
new_file=mp4_file_name[0:len(mp4_file_name)-4]+"_result.mp4"
d=(Original_video.duration)/60
Processed_video = moviepy.editor.VideoFileClip(new_file)
# Contains the duration of the video in terms of seconds
p=(Processed_video.duration)/60
Per= (d-p)/d*100
p="{:.2f}".format(p)
d="{:.2f}".format(d)
Per="{:.2f}".format(Per)
root = tk.Toplevel()
root.title("Video Repocessed Successfully.....")
img1=tk.PhotoImage(file="roll.png")

l = "\nVideo Proccessing Statistics, \n\nOriginal Video Duration (min) = "+ str(d) + "\n\nProcessed Video Duration (min) = "+str(p)+"\n\nTotal Time Saved (min) = "+str(Per)+"%"
w = Label(root, text =l, font = ("Lucida Calligraphy", 16), justify=LEFT, image=img1, compound=CENTER) 
w.pack(side=LEFT)
root.mainloop() 




