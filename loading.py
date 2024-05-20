from tkinter import *
from tkinter.ttk import Progressbar
from threading import Thread
from random import randint
import face_recognition
import dlib
import os
from ast import literal_eval


with open('resources/listFFace.txt','r') as file:
    fake_FACES = file.read().split('\n')
finished = False
def loadMP():
    import mediapipe as mp
    global face_detection,allFaces,finished
    allFaces = {}
    face_detection = mp.solutions.face_detection.FaceDetection()
    dlib.shape_predictor(rf'{os.getcwd()}\resources\shape_predictor_68_face_landmarks.dat')
    for img in fake_FACES:
        try:
            allFaces[img] = face_recognition.face_encodings(face_recognition.load_image_file(f'database/user_avatar/{img}'))[0]
        except IndexError:
            print(img)
            pass
    finished = True
def load():
    global image
    root = Tk()
    image = PhotoImage(file='resources/miLoading2.png')
    height = 653
    width = 736
    x = (root.winfo_screenwidth()//2)-(width//2)
    y = (root.winfo_screenheight()//2)-(height//2)
    root.geometry('{}x{}+{}+{}'.format(width, height, x, y))
    root.overrideredirect(1)
 
    root.wm_attributes('-topmost', True)
    root.lift()
    root.wm_attributes("-topmost", True)
    root.wm_attributes("-disabled", True)
    root.wm_attributes("-transparentcolor", "dark blue")
 
    bg_label = Label(root, image=image, bg='dark blue')
    bg_label.place(x=0, y=0)
 
    progress_label = Label(root, text="Please Wait...", font=('Comic Sans MS', 13, 'bold'), fg='#14183e', bg='#71b3ef')
    progress_label.place(x=160, y=475)
    progress = Progressbar(root, orient=HORIZONTAL, length=360, mode='determinate')
    progress.place(x=160, y=505)
 
    def top():
        root.withdraw()
        root.destroy()
    i = 0
    value = 1
    def waitTensorFlow():
        nonlocal i,value
        if (not finished) and (i==69):
            value = 0
        else:
            value = 1
        if not finished:
            return randint(700,1000)
        else: return 10
    def load():
        nonlocal i
        if i in range(0,30):
            txt = 'Loading database...  ' + (str(1*i)+'%')
            progress_label.config(text=txt)
            progress_label.after(60, load)
            progress['value'] = 1*i
            i += randint(1,4)
        elif i in range(30,70):
            txt = 'Creating TensorFlow Lite XNNPACK...  ' + (str(1*i)+'%')
            progress_label.config(text=txt)
            progress_label.after(waitTensorFlow(), load)
            progress['value'] = 1*i
            i += value
        elif i in range(70,101):
            txt = 'Loading theme...  ' + (str(1*i)+'%')
            progress_label.config(text=txt)
            progress_label.after(40, load)
            progress['value'] = 1*i
            i += 3
        else:
            top()
    load()
    root.mainloop()
def loadADMIN():
    Thread(target=loadMP).start()
    global finished
    load()
def loadSTDENT():
    global finished
    finished = True
    load()
if __name__ == '__main__':
    loadADMIN()