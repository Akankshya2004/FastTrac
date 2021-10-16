#from typing_extensions import Literal

# The following lines are for importing the relevant python libraries 
# The main interface for the app will be designed and created using the tkinter module 

from tkinter import ttk
import tkinter as tk
from tkinter import *  
from tkinter import filedialog as fd
from tkinter import messagebox
from tkinter.messagebox import showinfo
from tkinter import font, colorchooser
from tkinter.filedialog import SaveFileDialog, askopenfilename
import os
import glob
from glob import glob
import speech_recognition as sr 
from pygame.locals import *
from moviepy.editor import *
from moviepy.editor import VideoFileClip
from moviepy.editor import AudioFileClip
import moviepy.editor as me
from pydub import AudioSegment
from pydub.utils import make_chunks
import threading  # For running multiple functions simultaneously 


main_application = tk.Tk()
# This is to set the window size for the application
main_application.geometry('1200x1000')
# This is to add a title to the application file
main_application.title('FastTrac....')
# This is to set the icon for the min window 
main_application.wm_iconbitmap('mainicon.ico')
# This is to completely restrict any resizing of the app window
main_application.resizable(0,0)

# The purpose of the PanedWindow widget is to give the application's user some control over how space is divided up within the application.
window=ttk.Panedwindow(main_application, orient=VERTICAL)  
window.pack(fill=BOTH, expand=True)

# Create Frames
# The Frame widget is very important for the process of grouping and organizing other widgets in a somehow friendly way. 
# It works like a container, which is responsible for arranging the position of other widgets  

fram4=ttk.Frame(window,width=500,height=125)
window.add(fram4)
panedwindow=ttk.Panedwindow(main_application, orient=HORIZONTAL)  
panedwindow.pack(fill=BOTH, expand=True)  

fram1=ttk.Frame(panedwindow,width=200,height=325)
fram3=ttk.Frame(panedwindow,width=300,height=325)
panedwindow.add(fram1, weight=1)
panedwindow.add(fram3, weight=8)


label = ttk.Label(fram4)
image1 = PhotoImage(file='icons2/Banner2.png')

label['image'] = image1
label.grid(column=0, row=0)


pw_5=ttk.PanedWindow(fram3, orient=VERTICAL)
pw_5.pack(fill=BOTH, expand=True)

frame_8 = ttk.Frame(pw_5,width=500,height=100, relief=SUNKEN)
pw_5.add(frame_8)

# This is to create a "text box" where the transcript of the video will appear 
text_box = tk.Text(frame_8, height=10, width=130)
text_box.insert(1.0, "Transcription will appear here!")
text_box.tag_configure("center", justify="left")
text_box.tag_add("center", 1.0, "end")
text_box.pack(expand=True)
open("my_result.txt", "w").close()

# This function is to create the buttons in the transcript space
# It has 4 buttons: Open, save, transcribe any ideo, transcribe selected video 
# This function will be called later and the buttons will appear together 
def transcriptButton():
    left_small1=ttk.Button(frame_8,text='Open Transcription',  command=open_file_trans, width=40)
    left_small=ttk.Button(frame_8,text='Save Transcription', command=t3, width=40)
    center_small=ttk.Button(frame_8,text='Transcribe Any Video', command=t2, width=40)
    right_small=ttk.Button(frame_8,text='Transcribe Opened Video', command=t2, width=40)
    
    left_small.pack(side = RIGHT,expand=True)
    center_small.pack(side=RIGHT, expand=True )
    left_small1.pack(side = LEFT,expand=True)
    right_small.pack(side = LEFT,expand=True)
  
# This function is to add the text that is given as the input parameter into the transcription space.
# The function calls on transcriptButton() at the end because everything in that frame was deleted at the start of the function.
def put(text):
    #text box
    clear_frame(frame_8)
    text_box = tk.Text(frame_8, height=10, width=130)
    text_box.insert(1.0, text)
    text_box.tag_configure("center", justify="center", wrap=WORD, font="Arial")
    text_box.tag_add("center", 1.0, "end")
    text_box.pack(expand=True)
    scroll_bar = tk.Scrollbar(text_box)
    text_box.focus_set()
    scroll_bar.pack(side = tk.RIGHT,fill=tk.Y)
    text_box.pack(fill=tk.BOTH, expand=True)
    scroll_bar.config(command=text_box.yview)
    text_box.config(yscrollcommand= scroll_bar.set)
    transcriptButton()

# This function is to open/select file for transcription.
def open_file_trans(event=None):
    global url
    url = fd.askopenfilename(initialdir= os.getcwd(), title ='Select File',filetypes=(('Text File','*.txt'),('All files','*.*')))
    try:
        with open(url, 'r') as fr:
            text_box.delete(1.0,tk.END)
            text_box.insert(1.0,fr.read())
    except FileNotFoundError:
        return 
    


#---------------------------------------------loadingvideo--------------------------------------------------------

# This is a temeporary class created to save the name of the selected video files.
# This was done as the file name had to be used multiple times this proved as an efficient way of saving the name.
class temp():
    def __init__(self):
        self.name = " "

    def assignName(self, newname):
        self.name = newname
    
    def getName(self):
        return self.name

one = temp()
# The class was assigned a temporary name to ensure that other functions would not open a non-existant video 
one.assignName("NoVideoActuallyADDED")

filetypes = (
        ('Video files', '*.mp4'),
        ('All files', '*.*')
    )

# This is to select the file.
def select_file():
    
    filename = fd.askopenfilename(
        title='Open a file',
        initialdir='/',
        filetypes=filetypes)
    
    one.assignName(filename)

    showinfo(
        title='Selected File',
        message=filename
    )
    
# Call Silence file and start Threading process to commence parallel processing
def process_file():

    t1=threading.Thread(target=Thread_Process)
    t1.start()

# The following thread processes allow for all the widgets in different windows to work simultaneously.    
def Thread_Process():
    #T.insert(tk.END, "Video Processing..........")
    os.system("python Silence_Final.py " + one.getName())
    #T.insert(tk.END, None)   
    #T.insert(tk.END, "Video Processing Completed !!")
    quit()
# Parallel processing ends here for module

# Start Thread for MediaPLayer Parallel process
    
#-------------------------------------------------------------------Video Player------------------------------------------------------
def launch():
    t2=threading.Thread(target=Thread_Process_Player)
    t2.start()
    
    
    

def Thread_Process_Player():
    
    os.system("python MediaPlayer.py")
    

# # End of Thread for MediaPLayer Parallel process

# This class was created to store the result of transcript created as that result will be used by multip,e methods. 
class temp2:
    def __init__(self):
        self.content = " "
    def getContent(self):
        return self.content
    def writeContent(self, result):
        self.content = result

intermediary = temp2()
#---------------------------------------------------------------transcript---------------------------------------------------------

# This function deals with transcription. The result of that transcription is saved in the class instantance "intermediary"
def t2():
    global whole_text
    global VIDEO_FILE
    VIDEO_FILE = ""
    OUTPUT_AUDIO_FILE = "converted.wav"
    OUTPUT_TEXT_FILE = "recognized.txt"

    #"""Open the audio (*.mp4) file."""

    #Tk().withdraw() # we don't want a full GUI, so keep the root window from appearing
    if(one.getName() == "NoVideoActuallyADDED"):
        # show an "Open" dialog box and return the path to the selected file
        VIDEO_FILE = fd.askopenfilename( title='Open a file', initialdir='/', filetypes=filetypes)
        one.assignName(VIDEO_FILE)
    else:
        VIDEO_FILE = one.getName()

    

    video_clip = me.VideoFileClip(r"{}".format(VIDEO_FILE))
    video_clip.audio.write_audiofile(r"{}".format(OUTPUT_AUDIO_FILE))

    myaudio = AudioSegment.from_file(OUTPUT_AUDIO_FILE , "wav") 
    chunk_length_ms = 10000 # pydub calculates in millisec
    chunks = make_chunks(myaudio, chunk_length_ms) #Make chunks of one sec

    #Export all of the individual chunks as wav files

    folder_name = "audio-chunks"
        # create a directory to store the audio chunks
    if not os.path.isdir(folder_name):
            os.mkdir(folder_name)
    whole_text = ""        
    r = sr.Recognizer()
        # process each chunk     
    for i, chunk in enumerate(chunks):
            chunk_name = "chunk{0}.wav".format(i)
            #print ("exporting", chunk_name)
            #chunk = os.path.join(folder_name, chunk_name)
            chunk.export(chunk_name, format="wav")
            # export audio chunk and save it in
            # the `folder_name` directory.
                
            #audio_chunk.export(chunk_filename, format="wav")
            # recognize the chunk
            with sr.AudioFile(chunk_name) as source:
                audio_listened = r.record(source)
                # try converting it to text
                try:
                    text = r.recognize_google(audio_listened)
                except sr.UnknownValueError as e:
                    print("Error:", str(e))
                else:
                    text = f"{text.capitalize()}. "
                    print(chunks, ":", text)
                    whole_text += text
                    #os.remove('chunk{0}.wav')
        
    # Get a list of all the file paths that ends with .txt from in specified directory
    fileList = glob(os.path.join(os.path.dirname(__file__), 'chunk*.*'))
    # Iterate over the list of filepaths & remove each file.
    for filePath in fileList:
        try:
            os.remove(filePath)
        except:
            print("Error while deleting file : ", filePath)


    result1 = whole_text
    put(result1)
    intermediary.writeContent(result1)
    

    
# This function deals with saving the transcript in a file.
def t3():
    global url
    try :
        url = fd.asksaveasfile(mode = 'w' ,defaultextension = '.txt',filetypes=(('Text File','*.txt'),('All files','*.*')))
        print(url)
        content=whole_text
        #url.write.t2()
        url.write(content)
        url.close()

    except:
        return

#------------------------------------------------------------------Buttons------------------------------------------------------------
    
#Header Lable -----------------------
label6 = ttk.Label(fram1)
image16 = PhotoImage(file='icons2/vidmenu.png')

label6['image'] = image16

# HeaderLabel End---------------------

process_button = ttk.Button(
    fram1,
    text=None,
    command=process_file 
)
photo = tk.PhotoImage(file="icons2/open&pro.png", master=fram1)
process_button.config(image=photo, compound=tk.CENTER)

#T = tk.Text(fram1, height=2, width=30)
#T.insert(tk.END, "")

play_any_button = ttk.Button(
    fram1,
    text=None,
    command=launch
)
photo1 = tk.PhotoImage(file="icons2/Playvidfin.png", master=fram1)
play_any_button.config(image=photo1, compound=tk.CENTER)
#style = ttk.Style()
#style.configure("BW.TLabel", foreground="white", background="#20bebe")
label6.pack()
process_button.pack(expand=True)
#T.pack(expand=True)
play_any_button.pack(expand=True)

transcriptButton()

#This functions is delete all the widgets in a given window.
def clear_frame(frame):
   for widgets in frame.winfo_children():
      widgets.destroy()

# This master menu is for the entire app.
master_menu = tk.Menu()
# This will act as a sub-menu for the master menu. This gives option for the video 
video_menu = tk.Menu()
# This will act as a sub-menu for the master menu. This gives option for the transcript
transcript_menu = tk.Menu()
# This function is for notepad menu 
main_menu = tk.Menu()

#-----------The following code deals with assigning images to options in the notepad menu--------------------
#File icons

new_icon =tk.PhotoImage(file='icons2/new.png')
open_icon =tk.PhotoImage(file='icons2/open.png')
save_icon =tk.PhotoImage(file='icons2/save.png')
save_as_icon =tk.PhotoImage(file='icons2/save_as.png')
exit_icon = tk.PhotoImage(file='icons2/exit.png')

file = tk.Menu(main_menu,tearoff=False)


####edit 
#edit icons

copy_icon = tk.PhotoImage(file='icons2/copy.png')
paste_icon = tk.PhotoImage(file='icons2/paste.png')
cut_icon = tk.PhotoImage(file='icons2/cut.png')
clear_all_icon = tk.PhotoImage(file='icons2/clear_all.png')
find_icon = tk.PhotoImage(file='icons2/find.png')

edit= tk.Menu(main_menu,tearoff=False)
##commands are added after edit menu


####view
#view icons

tool_bar_icon = tk.PhotoImage(file='icons2/tool_bar.png')
status_bar_icon = tk.PhotoImage(file='icons2/status_bar.png')

view = tk.Menu(main_menu,tearoff=False)


###color theme
light_default_icon=tk.PhotoImage(file='icons2/light_default.png')
light_plus_icon=tk.PhotoImage(file='icons2/light_plus.png')
dark_icon=tk.PhotoImage(file='icons2/dark.png')
red_icon=tk.PhotoImage(file='icons2/red.png')
monokai_icon=tk.PhotoImage(file='icons2/monokai.png')
night_blue_icon=tk.PhotoImage(file='icons2/night_blue.png')

color_theme = tk.Menu(main_menu,tearoff=False)
#all icons saved in a tuple
theme_choice = tk.StringVar()
color_icons = (light_default_icon ,light_plus_icon,dark_icon,red_icon,monokai_icon,night_blue_icon)
## text  ,background 
#  
color_dict = {
    'Light Default' :('#000000','fffffff'),
    'Light Plus' :('#474747','#e0e0e0'),
    'Dark' : ('#c4c4c4', '#2d2d2d'),
    'Red' : ('#2d2d2d','#ffe8e8'),
    'Monokai' : ('#d3b774','#474747'),
    'Night Blue' :('#ededed','#6b9dc2')
}

#---------------------------------------------END--------------------------------------------------

# The following lines add the options of video and transcript to the master menu
master_menu.add_cascade(label='Video',menu=video_menu)
master_menu.add_cascade(label='Transcript',menu=transcript_menu)

# The following add all the options relating to notepad in the notepad menu
main_menu.add_cascade(label='File',menu=file)
main_menu.add_cascade(label='Edit',menu=edit)
main_menu.add_cascade(label='View',menu=view)
main_menu.add_cascade(label='Color Theme',menu=color_theme)
# This line adds the notepad option to the master menu. 
master_menu.add_cascade(label='Notepad',menu=main_menu)

########## toolbar  #############

tool_bar = ttk.Label(main_application)
tool_bar.pack(side=tk.TOP,fill=tk.X)

##font box
font_tuple = tk.font.families()
font_family = tk.StringVar()
font_box=ttk.Combobox(tool_bar, width=30 ,textvariable=font_family,state='readonly' )
font_box['values']=font_tuple
font_box.current(font_tuple.index('Arial'))
font_box.grid(row=0,column=0,padx=5)

##size box
size_var = tk.IntVar()
font_size=ttk.Combobox(tool_bar,width=14,textvariable = size_var,state='readonly')
font_size['values']=tuple(range(8,80,2))
font_size.current(4)
font_size.grid(row=0,column=1,padx=5)


##bold button
bold_icon = tk.PhotoImage(file='icons2/bold.png')
bold_btn  =ttk.Button(tool_bar ,image=bold_icon)
bold_btn.grid(row=0, column=2, padx=5)


 ##italic button
italic_icon = tk.PhotoImage(file='icons2/italic.png')
italic_btn=ttk.Button(tool_bar,image=italic_icon)
italic_btn.grid(row=0, column=3,padx=5)


##underline button
underline_icon = tk.PhotoImage(file='icons2/underline.png')
underline_btn=ttk.Button(tool_bar,image=underline_icon)
underline_btn.grid(row=0, column=4,padx=5)


##font color button
font_icon = tk.PhotoImage(file='icons2/font_color.png')
font_color_btn = ttk.Button(tool_bar,image=font_icon)
font_color_btn.grid(row=0, column=5,padx=5)

##font Microphone button
mic_icon = tk.PhotoImage(file='icons2/mic.png')
mic_color_btn = ttk.Button(tool_bar,image=mic_icon)
mic_color_btn.grid(row=0, column=6,padx=5)

##add Save button to the toolbar
save_icon = tk.PhotoImage(file='icons2/save_as.png')
save_color_btn = ttk.Button(tool_bar,image=save_icon)
save_color_btn.grid(row=0, column=7,padx=5)

exit_icon = tk.PhotoImage(file='icons2/exit.png')  ## adding Exit button on the toolbar
exit_btn = ttk.Button(tool_bar,image=exit_icon)
exit_btn.grid(row=0, column=8,padx=5)



#----------&&&&& End toolbar &&&&&----------#


########## text editor  #############

text_editor = tk.Text(main_application)
text_editor.config(wrap = 'word', relief=tk.FLAT)


scroll_bar = tk.Scrollbar(main_application)
text_editor.focus_set()
scroll_bar.pack(side = tk.RIGHT,fill=tk.Y)
text_editor.pack(fill=tk.BOTH, expand=True)
scroll_bar.config(command=text_editor.yview)
text_editor.config(yscrollcommand= scroll_bar.set)


##  font family and font size functionality

current_font_family= 'Arial'
current_font_size= 12

def change_font(event=None):
    global current_font_family
    current_font_family = font_family.get()
    text_editor.config(font=(current_font_family,current_font_size))


def change_size(event=None):
    global current_font_size
    current_font_size = size_var.get()
    text_editor.config(font=(current_font_family,current_font_size))


##binding combobox with function
font_box.bind("<<ComboboxSelected>>",change_font)
font_size.bind("<<ComboboxSelected>>",change_size)


####### buttons functionality


#bold buttton functionality

def change_bold():
    text_property=tk.font.Font(font=text_editor['font'])
##upper line gives a dictionary whose attributes we are changing
    if text_property.actual()['weight']=='normal' :
        text_editor.configure(font=(current_font_family,current_font_size,'bold'))
    if text_property.actual()['weight']=='bold' :
        text_editor.configure(font=(current_font_family,current_font_size,'normal'))

bold_btn.configure(command=change_bold)


#italic button functionality

def change_italic():
    text_property=tk.font.Font(font=text_editor['font'])
##upper line gives a dictionary whose attributes we are changing
    if text_property.actual()['slant']=='roman' :
        text_editor.configure(font=(current_font_family,current_font_size,'italic'))
    if text_property.actual()['slant']=='italic' :
        text_editor.configure(font=(current_font_family,current_font_size,'normal'))

italic_btn.configure(command=change_italic)

##underline button functionality
def underline():
    text_property=tk.font.Font(font=text_editor['font'])
##upper line gives a dictionary whose attributes we are changing
    if text_property.actual()['underline']==0 :
        text_editor.configure(font=(current_font_family,current_font_size,'underline'))
    if text_property.actual()['underline']==1 :
        text_editor.configure(font=(current_font_family,current_font_size,'normal'))

underline_btn.configure(command=underline)


##font color functionality
def change_font_color():
    color_var = tk.colorchooser.askcolor()
##ask color asks for a color and stores into the color_var      
##text color is called foreground color also abbrivated as fg
## a tuple in which 0th ondex shows the RGB values where as 1st index shows hexa value for color
    text_editor.configure(fg=color_var[1])

font_color_btn.configure(command=change_font_color)
text_editor.configure(font=('Arial',12))


#----------&&&&& End text editor  &&&&&----------#
##  Speech to Text
def Speech2text():
    
    # Reading Microphone as source
    # listening the speech and store in audio_text variable
    # obtain audio from the microphone
    
                    r = sr.Recognizer()
                    try:
                        with sr.Microphone() as source:                # use the default microphone as the audio source
                        
                            r = sr.Recognizer()
                        with sr.Microphone() as source:                # use the default microphone as the audio source
                            r.adjust_for_ambient_noise(source)  # here
                            print ("say something")
                            audio = r.listen(source, timeout=10)
                            try:
                                text_editor.delete(1.0,tk.END)
                                # using google speech recognition
                                page_content=r.recognize_google(audio)
                                with open('my_result.txt',mode ='a') as file: 
                                    file.write(". ") 
                                    file.write(page_content) 
                                    file1 = open("my_result.txt","r+") 
                                #text_editor.insert(1.0, "\n" )
                                text_editor.insert(1.0, file1.read())
                                text_editor.tag_configure("center", justify="left")
                                text_editor.tag_add("center", 1.0, "end")
                            except:
                                print("Sorry, I did not get that")
                    except KeyboardInterrupt:
                        pass
                    
mic_color_btn.configure(command=lambda:Speech2text())

#########    status bar #############

status_bar = ttk.Label(main_application, text ='Status Bar')
status_bar.pack(side=tk.BOTTOM)

text_changed = False

def changed(event=None):
    global text_changed
    if text_editor.edit_modified():###checks if any character is added or not
        text_changed= True
        words = len(text_editor.get(1.0, 'end-1c').split()) ##it even counts new line character so end-1c subtracts one char
        characters = len(text_editor.get(1.0,'end-1c'))
        status_bar.config(text=f' Words: {words} Characters : {characters}')
    text_editor.edit_modified(False)
text_editor.bind('<<Modified>>',changed)


#----------&&&&& End main status bar &&&&&----------#



########## main menu functinality #############

##file commands


##variable 
url = ''

##new functionality

def new_file(event=None):
    global url 
    url = ''
    text_editor.delete(1.0,tk.END)
file.add_command(label='new', image=new_icon ,compound=tk.LEFT, accelerator ='Ctrl+N',command=new_file )


##open functionality
## it is coppying the data from the desired file into the working file
def open_file(event=None):
    global url
    url = fd.askopenfilename(initialdir= os.getcwd(), title ='Select File',filetypes=(('Text File','*.txt'),('All files','*.*')))
    try:
        with open(url, 'r') as fr:
            text_editor.delete(1.0,tk.END)
            text_editor.insert(1.0,fr.read())
    except FileNotFoundError:
        return 
    except :
        return
    main_application.title(os.path.basename(url))

file.add_command(label='Open', image=open_icon ,compound=tk.LEFT, accelerator ='Ctrl+O',command =open_file )

##save functionality

def save_file(event=None):
    global url
    try:
        if url :
            content = str(text_editor.get(1.0,tk.END))
            with open(url,'w',encoding= 'utf-8') as fw:
                fw.write(content)
        else :
            url = fd.asksaveasfile(mode = 'w' ,defaultextension = '.txt',filetypes=(('Text File','*.txt'),('All files','*.*')))
            content = text_editor.get(1.0,tk.END)
            url.write(content)
            url.close()
    except :
        return 


file.add_command(label='Save', image=save_icon ,compound=tk.LEFT, accelerator ='Ctrl+S',command= save_file )
save_color_btn.configure(command=save_file)

###save as functionality
def save_as(event=None):
    global url
    try :
        content=str(text_editor.get(1.0,tk.END))
        url = fd.asksaveasfile(mode = 'w' ,defaultextension = '.txt',filetypes=(('Text File','*.txt'),('All files','*.*')))
        url.write(content)
        url.close()
    except :
        return


file.add_command(label='Save As', image=save_as_icon ,compound=tk.LEFT, accelerator ='Ctrl+Alt+S',command =save_as )

##exit functionality

def exit_func(event=None):
    global url, text_changed
    try:
        if text_changed:
            mbox = messagebox.askyesnocancel('Warning','Do you want to save the file')
            if mbox is True :
##if user wants to save the file and it already exists
                if url:
                    content = text_editor.get(1.0,tk.END)
                    with open(url,'w',encoding='utf-8') as fw:
                        fw.write(content)
                        main_application.destroy()
                else:
                    content2 = str(text_editor.get(1.0,tk.END))
                    url = fd.asksaveasfile(mode = 'w' ,defaultextension = '.txt',filetypes=(('Text File','*.txt'),('All files','*.*')))
                    url.write(content2)
                    url.close()
                    main_application.destroy()
            elif mbox is False:
                main_application.destroy()
        else:
            main_application.destroy()
    except:
        return 


file.add_command(label='Exit', image=exit_icon ,compound=tk.LEFT, accelerator ='Ctrl+Q',command=exit_func )
exit_btn.configure(command=exit_func)
###edit commands
### find functionality

def find_func(event=None):
##using tag inbuilt function
    def find():
        word = find_input.get()
        text_editor.tag_remove('match','1.0',tk.END)
        matches = 0
        if word :
            start_pos = '1.0'
            while True :
                start_pos = text_editor.search(word,start_pos,stopindex=tk.END)
                if(not start_pos):
                    break
                end_pos = f'{start_pos}+{len(word)}c'
                text_editor.tag_add('match',start_pos,end_pos)
                matches +=1
                start_pos=end_pos
                text_editor.tag_config('match',foreground='red',background='')

    def replace():
        word = find_input.get()
        replace_text = replace_input.get()
        content = text_editor.get(1.0,tk.END)
        new_content = content.replace(word,replace_text)
        text_editor.delete(1.0,tk.END)
        text_editor.insert(1.0,new_content)


    find_dialogue = tk.Toplevel()
    find_dialogue.geometry('450x250+500+200')
    find_dialogue.resizable(0,0)

    ## frame
    find_frame = ttk.LabelFrame(find_dialogue, text ='Find/Replace')
    find_frame.pack(pady=20)

    ## labels 
    text_find_label = ttk.Label(find_frame,text ='Find :')
    text_replace_label = ttk.Label(find_frame,text ='Replace')

    ##entry boxes 
    find_input = ttk.Entry(find_frame,width=30)
    replace_input = ttk.Entry(find_frame,width=30)


    ## Button
    find_button = ttk.Button(find_frame,text ='Find',command=find)
    replace_button = ttk.Button(find_frame,text ='Replace',command=replace)

    ##label grid
    text_find_label.grid(row=0,column=0,padx=4,pady=4)
    text_replace_label.grid(row=1,column=0,padx=4,pady=4)

    ##entry grid
    find_input.grid(row=0, column=1,padx=4,pady=4)
    replace_input.grid(row=1, column=1,padx=4,pady=4)

    ##button grid
    find_button.grid(row=2 ,column=0 ,padx=8,pady=4)
    replace_button.grid(row=2 ,column=1 ,padx=8,pady=4)

    find_dialogue.mainloop()

edit.add_command(label='Copy',image=copy_icon,compound=tk.LEFT, accelerator='Ctrl+C',command=lambda:text_editor.event_generate("<Control c>"))
edit.add_command(label='Paste',image=paste_icon,compound=tk.LEFT, accelerator='Ctrl+V',command=lambda:text_editor.event_generate("<Control v>"))
edit.add_command(label='Cut',image=cut_icon,compound=tk.LEFT, accelerator='Ctrl+X',command=lambda:text_editor.event_generate("<Control x>"))
edit.add_command(label='Clear All',image=clear_all_icon,compound=tk.LEFT, accelerator='Ctrl+ALt+X',command=lambda:text_editor.delete(1.0,tk.END))


edit.add_command(label='Find',image=find_icon,compound=tk.LEFT, accelerator='Ctrl+F',command=find_func)

#view check button
##it will have check button

show_statusbar = tk.BooleanVar()
show_statusbar.set(True)
show_toolbar = tk.BooleanVar()
show_toolbar.set(True)

def hide_toolbar():
    global show_toolbar
    if show_toolbar:
        tool_bar.pack_forget()
        show_toolbar =False

    else:
        text_editor.pack_forget()
        status_bar.pack_forget()
        tool_bar.pack(side=tk.TOP,fill=tk.X)
        text_editor.pack(fill=tk.BOTH,expand =True)
        status_bar.pack(side=tk.BOTTOM)
        show_toolbar = True

def hide_statusbar():
    global show_statusbar
    if show_statusbar:
        status_bar.pack_forget()
        show_statusbar =False
    else:
        status_bar.pack(side=tk.BOTTOM)
        show_statusbar=True

view.add_checkbutton(label='Tool Bar',onvalue =True,offvalue=0,variable =show_toolbar,image=tool_bar_icon, compound=tk.LEFT,command=hide_toolbar)
view.add_checkbutton(label='Status Bar',onvalue =1,offvalue=False,variable =show_statusbar,image=status_bar_icon, compound=tk.LEFT,command=hide_statusbar)

###color theme
def change_theme():
    choose_theme = theme_choice.get()
    color_tuple =color_dict.get(choose_theme)
    fg_color,bg_color =color_tuple[0], color_tuple[1]
    text_editor.config(background=bg_color,fg=fg_color)

count = 0
for i in color_dict :
    color_theme.add_radiobutton(label = i,image=color_icons[count],variable=theme_choice,compound=tk.LEFT,command =change_theme)
    count+=1

#--------------Main Menu Additional------------
main_menu.add_command(label = 'Voice Notes', command=Speech2text)
#--------------Video Menu----------------------

video_menu.add_command(label='Open & Process Video', command=process_file)
video_menu.add_command(label='Play any video', command=launch)

#-------------Transcript Menu------------------
transcript_menu.add_command(label='Open Transcription', command=open_file_trans)
transcript_menu.add_command(label='Transcribe Opened Video', command=t2)
transcript_menu.add_command(label="Transcribe any video", command=t2)
transcript_menu.add_command(label='Save Transcript', command=t3)

#----------&&&&& End main menu functinality &&&&&----------#

main_application.bind("<Control-n>", new_file)
main_application.bind("<Control-o>", open_file)
main_application.bind("<Control-s>", save_file)
main_application.bind("<Control-Alt-s>", save_as)
main_application.bind("<Control-q>", exit_func)
main_application.bind("<Control-q>", exit_func)
main_application.bind("<Control-f>", find_func)
main_application.config(menu=master_menu)
main_application.mainloop()
