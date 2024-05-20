import tkinter as tk
import loading
import sys
import os
from tkinter import ttk
from tkinter import messagebox
from PIL import Image,ImageTk,ImageDraw,ImageFont
from turtle import *
import ctypes
import requests
import webbrowser
import run_tools
import ast
import io
import cv2
import face_recognition
import numpy as np
import win10toast
import datetime
import re
from random import shuffle
import pygame
import threading


user32 = ctypes.windll.user32
screen_width,screen_height = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
APIurl = 'http://127.0.0.1:8000'
SERVERurl = 'http://127.0.0.1:3003'
Toaster = win10toast.ToastNotifier()
pygame.mixer.init()
try:
    USER_ID = sys.argv[1]
except:
    USER_ID = '39478646' 
    # 10957288# '82654793
    #http://127.0.0.1:3076/GUI/guii.png
    
USERINFO:str = requests.get(APIurl+'/userIn4',params={'getIn4By':'user_ID',
                                            'where':USER_ID,
                                            'wantToGet':'*'}).text

USERINFO:dict = ast.literal_eval(USERINFO)
if USERINFO['account_TYPE']=='ADMIN':
    loading.loadADMIN()
    face_detection = loading.face_detection
    allFaces = loading.allFaces
else:
    face_detection = None
    allFaces = None
    loading.loadSTDENT()

setup(1251,672,(screen_width-1251)//2,0)
screensize(1251,700)
setworldcoordinates(0,700,1251,0)
colormode(255)

screen = Screen()
screen._root.iconbitmap('icons/icon.ico')
screen._root.resizable(False,False)
screen.center = (772,408)
pygame.mixer.music.load('sounds/background.mp3')
pygame.mixer.music.play(loops=90)
def createButton(mode = 'ADMIN'):
    def enterImg(index):
        nonlocal mode
        if mode == 'ADMIN':
            return buttonImagesADMIN['enter'][index+'2.png']
        elif mode == 'STDENT':
            return buttonImagesSTDENT['enter'][index+'4.png']
    def leaveImg(index):
        if mode == 'ADMIN':
            return buttonImagesADMIN['leave'][index+'1.png']
        elif mode == 'STDENT':
            return buttonImagesSTDENT['leave'][index+'3.png']
    def check(index):
        nonlocal pressed
        if pressed!=index:
            buttons[index].configure(image=leaveImg(index))
    def setLabel(idx):
        nonlocal mode
        txt = {'homepage':'Tổng quan','attendance':'Điểm danh','studentlist':'Danh sách','studentpos':'Sơ đồ lớp',
               'learning':'Học tập','learningresult':'Kết quả','hollandtest':'Hướng nghiệp'}
        label = tk.Label(screen._root,
                 text=txt[idx],
                 font=('SVN-Agency FB',20,'bold'),
                 background='#989898',
                 foreground='#DFDF92',
                 borderwidth=0,
                 width=17,height=1)
        label.place(x=320,y=60)
        label.bind('<Enter>',lambda event :label.configure(background='#000000'))
        label.bind('<Leave>',lambda event :label.configure(background='#989898'))
    def press(idx:str):
        nonlocal pressed
        global COMMANDS
        try: buttons[pressed].configure(image=leaveImg(pressed)) 
        except KeyError: pass
        setLabel(idx)
        pressed = idx
        buttons[idx].configure(image=enterImg(idx))
        COMMANDS[idx]()

    global buttons,screen
    if mode == 'ADMIN':
        buttons = {key.lower():tk.Button for key in allKeysADMIN}
    elif mode == 'STDENT':
        buttons = {key.lower():tk.Button for key in allKeysSTDENT}
    pressed = ''
    for i in buttons.keys():
        buttons[i] = tk.Button(screen._root,
                image=leaveImg(i),
                width=197,height=52,
                highlightthickness=0,
                borderwidth=0,
                cursor='hand2',background='#E0E6EE' if USERINFO['account_TYPE']=='ADMIN' else '#E3EFEB',
                command=lambda idx=i:press(idx))
        buttons[i].place(x=55,y=list(buttons).index(i)*50+270)
        buttons[i].bind('<Enter>',lambda event,idx = i :buttons[idx].configure(image=enterImg(idx)))
        buttons[i].bind('<Leave>',lambda event,idx = i:check(idx))

def setMyTurtle(t:Turtle)->Turtle:
    t.speed(90)
    t.hideturtle()
    t.penup()
    return t
def setBackground(bg:str='resources/MainAppADMIN.gif'):
    t = Turtle(shape=bg,visible=False)
    t = setMyTurtle(t)
    t.goto(650,350)
    return t.stamp()
def setUserInfo():
    def toAvt(image:Image.Image,color):
        draw = ImageDraw.Draw(image)
        i,j = 0,image.size[0]
        while i>-200:
            draw.ellipse((i, i, j, j), outline = color,width=2)
            i-=1
            j+=1
        return image
    global roundAVT
    response = requests.get(url=SERVERurl+f'/database/user_avatar/{USER_ID}.png')
    bytesImg = response.content
    file = io.BytesIO(bytesImg)
    roundAVT = ImageTk.PhotoImage(toAvt(image=Image.open(file),color='#E0E6EE' if USERINFO['account_TYPE']=='ADMIN' else '#E3EFEB').resize((130,130)))
    avt = tk.Label(screen._root,image=roundAVT,borderwidth=0)
    avt.bind(sequence='<Button-1>',func=lambda event:AccountPressed())
    avt.place(x=85,y=50)
    tk.Label(screen._root,text=USERINFO['user_NAME'],
             background='#E0E6EE' if USERINFO['account_TYPE']=='ADMIN' else '#E3EFEB',foreground='#000000',font=('SVN-Amsi Narw Light.ttf',17, 'bold'),anchor='center').place(x=5,y=190,width=300)
    _type = tk.Label(screen._root,text='Giáo viên' if USERINFO['account_TYPE']=='ADMIN' else 'Học sinh',font=('SVN-Amsi Narw Light.ttf',12),
            foreground='#000000',background='#E0E6EE' if USERINFO['account_TYPE']=='ADMIN' else '#E3EFEB',anchor='center')
    _type.place(x=5,y=220,width=300)
def logoutButton():
    logout = tk.Button(screen._root,command=exit,
                       width=164,height=50,
                       image=logoutImg['leave'],
                       background='#FFFFFF',
                       highlightthickness=0,
                       borderwidth=0)
    logout.bind('<Enter>',lambda event:logout.configure(image=logoutImg['enter']))
    logout.bind('<Leave>',lambda event:logout.configure(image=logoutImg['leave']))
    logout.place(x=1050,y=20)
def addAllShapes() -> None:
    shapes = ['resources/MainAppSTDENT.gif',
            'resources/MainAppADMIN.gif']
    for shape in shapes:
        addshape(shape)
    return


allKeysADMIN = ['Homepage','Attendance','StudentList','StudentPos']
allKeysSTDENT = ['Homepage','Learning','LearningResult','HollandTest']

idCancel = 0
idBind = 0

buttonImagesADMIN = {'enter':{name:ImageTk.PhotoImage(Image.open('resources/buttons/'+name)) for name in [x+'2.png' for x in [key.lower() for key in allKeysADMIN]]},
                     'leave':{name:ImageTk.PhotoImage(Image.open('resources/buttons/'+name)) for name in [x+'1.png' for x in [key.lower() for key in allKeysADMIN]]}}
buttonImagesSTDENT = {'enter':{name:ImageTk.PhotoImage(Image.open('resources/buttons/'+name)) for name in [x+'4.png' for x in [key.lower() for key in allKeysSTDENT]]},
                     'leave':{name:ImageTk.PhotoImage(Image.open('resources/buttons/'+name)) for name in [x+'3.png' for x in [key.lower() for key in allKeysSTDENT]]}}

homeImgs = [ImageTk.PhotoImage(Image.open(f'resources/HomepageGif.png'))]

learnImgs = [ImageTk.PhotoImage(Image.open(f'resources/LearningPressed.png')),
             ImageTk.PhotoImage(Image.open(f'resources/buttons/join1.png')),
             ImageTk.PhotoImage(Image.open(f'resources/buttons/join2.png'))]
learnImgs.append({f'start {i}':ImageTk.PhotoImage(Image.open(f'resources/LearningPressed{i}.png')) for i in range(1,5)})
accountImgs = [Image.open('resources/AccountPressed.png')]
resultImgs = [ImageTk.PhotoImage(Image.open('resources/ResultPressed.png'))]
attendanceImgs = [ImageTk.PhotoImage(Image.open('resources/novideoinputavailable.png')),
                  ImageTk.PhotoImage(Image.open('resources/AttendancePressed.png'))]
studentImgs = [ImageTk.PhotoImage(Image.open('resources/StudentListPressed.png')),
               ImageTk.PhotoImage(Image.open('resources/studentResult.png'))]
hollandTestImgs = {'background':[ImageTk.PhotoImage(Image.open(f'resources/HollandTestPressed.png')),
                                 *[ImageTk.PhotoImage(Image.open(f'resources/HollandTest{i}.png')) for i in range(1,6)]],
                   'buttons1':[0,*[ImageTk.PhotoImage(Image.open(f'resources/buttons/hollandbutton{i}1.png')) for i in range(1,6)]],
                   'buttons2':[0,*[ImageTk.PhotoImage(Image.open(f'resources/buttons/hollandbutton{i}2.png')) for i in range(1,6)]],
                   'opening':[ImageTk.PhotoImage(Image.open(f'resources/HollandTestOpening.png')),
                              ImageTk.PhotoImage(Image.open(f'resources/buttons/hollandstartbutton1.png')),
                              ImageTk.PhotoImage(Image.open(f'resources/buttons/hollandstartbutton2.png'))],
                   'result':[ImageTk.PhotoImage(Image.open(f'resources/HollandTestResult.png')),
                             ImageTk.PhotoImage(Image.open(f'resources/buttons/hollandresultbutton1.png')),
                             ImageTk.PhotoImage(Image.open(f'resources/buttons/hollandresultbutton2.png'))]}
studentPosImgs = [ImageTk.PhotoImage(Image.open('resources/StudentPosPressed.png')),0,0]
logoutImg = {'enter':ImageTk.PhotoImage(Image.open('resources/buttons/logoutButton2.png')),
             'leave':ImageTk.PhotoImage(Image.open('resources/buttons/logoutButton1.png'))}

startImg = ImageTk.PhotoImage(Image.open('resources/buttons/startButton.png'))
logImg = ImageTk.PhotoImage(Image.open('resources/buttons/logButton.png'))
infoImgText = Image.open('resources/AttendancePressed.png')

def HomepagePressed() -> None:
    def dec():
        nonlocal idx
        idx-=1
        if idx == 0: idx=3
        readVideo()
    def inc():
        nonlocal idx
        idx+=1
        if idx == 4: idx=1
        readVideo()
    def incordec(event):
        if event.x<=432: dec()
        else: inc()
    def readVideo():
        def setVideo():
            global imagePIL2,imageTK2,l,video
            nonlocal idx
            try:
                ret, frame = video.read()
                frame = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
                imagePIL2 = Image.fromarray(frame)
                imagePIL2 = imagePIL2.resize((854,223))
                imageTK2 = ImageTk.PhotoImage(imagePIL2)
                l.configure(image=imageTK2)
                l.after(1,setVideo)
            except:
                pass
        global l,video
        nonlocal idx
        if idx==4: idx = 1
        video = cv2.VideoCapture(f'resources/HomepageGif{idx}.gif')
        setVideo()
    def makeChart():
        def counter():
            lst = requests.get(APIurl+'/userIn4',params={'getIn4By':'user_CLASS',
                                            'where':USERINFO['user_CLASS'],
                                            'wantToGet':'stdent_ABSENT,stdent_LATENESS',
                                            'account_TYPE':'STDENT'})
            lst = ast.literal_eval(lst.text)
            stdentNumber = len(lst)
            absent = len(list(filter(bool,[x['stdent_ABSENT'] for x in lst])))
            lateness = len(list(filter(bool,[x['stdent_LATENESS'] for x in lst])))
            return stdentNumber,lateness,absent
        def convertT2R(text:str)->dict[str,list[list[float,float]]]:
            def rsFilter(result:str):
                result = result.lstrip('<').rstrip('>')
                type1 = list(map(float,result[result.index('1:')+2:result.index('2:')-1].split(',')))
                type2 = list(map(float,result[result.index('2:')+2:result.index('3:')-1].split(',')))
                type3 = list(map(float,result[result.index('3:')+2:].split(',')))
                return [type1,type2,type3]
            lst = text.split('>,')
            lst = [sj+'>' for idx,sj in enumerate(lst) if idx!=len(lst)-1]
            result = {sj[:sj.index('<')]:rsFilter(sj) for sj in lst}
            result['IT']=rsFilter(text[text.index('IT')+2:len(text)])
            return result
        def rCalculate(result:list[list]):
            total1 = sum(result[0])
            total2 = sum(result[1])*2
            total3 = sum(result[2])*3
            total = (total1+total2+total3)/12
            return round(total,1)
        if USERINFO['account_TYPE']=='ADMIN':
            res = counter()
            r = requests.get(url=f"https://quickchart.io/chart?v=2.9.4&c=%7B%0A%20%20width%3A471%2C%0A%20%20height%3A300%2C%0A%20%20type%3A%20%27doughnut%27%2C%0A%20%20data%3A%20%7B%0A%20%20%20%20labels%3A%20%5B%27%C4%90%C3%BAng%20gi%E1%BB%9D%27%2C%27%C4%90i%20mu%E1%BB%99n%27%2C%27V%E1%BA%AFng%20h%E1%BB%8Dc%27%5D%2C%0A%20%20%20%20datasets%3A%20%5B%7B%20data%3A%20%5B{res[0]-(res[1]+res[2])}%2C%20{res[1]}%2C%20{res[2]}%5D%2C%0A%20%20%20%20backgroundColor%3A%5B%27%236bd089%27%2C%27%23ffb27d%27%2C%27%23f47378%27%5D%7D%5D%2C%0A%20%20%20%20%7D%2C%0A%20%20options%3A%20%7B%0A%20%20%20%20plugins%3A%20%7B%0A%20%20%20%20%20%20datalabels%3A%20%7B%0A%20%20%20%20%20%20%20%20color%3A%20%27%23ffffff%27%2C%0A%20%20%20%20%20%20%20%20anchor%3A%20%27center%27%2C%0A%20%20%20%20%20%20%20%20align%3A%20%27center%27%2C%0A%20%20%20%20%20%20%20%20font%3A%7Bsize%3A18%2Cweight%3A%27bold%27%7D%7D%2C%0A%20%20%20%20%20%20doughnutlabel%3A%20%7B%0A%20%20%20%20%20%20%20%20labels%3A%20%5B%7B%20text%3A%20%27{res[0]}%27%2C%20font%3A%20%7B%20size%3A%2020%20%7D%20%7D%2C%20%7B%20text%3A%20%27L%E1%BB%9Bp%20{USERINFO['user_CLASS']}%27%20%7D%5D%2C%0A%20%20%20%20%20%20%7D%2C%0A%20%20%20%20%7D%2C%0A%20%20%7D%2C%0A%7D")
        else:
            results = requests.get(APIurl+'/userIn4',params={'getIn4By':'user_ID',
                                                     'where':USER_ID,
                                                     'wantToGet':'stdent_SCORE'}).text.strip('''"''')
            cleanResult = convertT2R(results)
            averageResult = {avrg:rCalculate(cleanResult[avrg]) for avrg in cleanResult}
            r = requests.get(url="https://quickchart.io/chart?w=471&h=305&v=2.9.4&c={type:'radar',data:{labels:['Toán','Lý','Hoá','Sinh','Anh','Sử','Địa','GDCD','Côngnghệ','Tinhọc'],datasets:[{label:'Họclực',data:["+\
                             f"{averageResult['Math']},{averageResult['Physics']},{averageResult['Chemistry']},\
                                {averageResult['Biology']},{averageResult['English']},{averageResult['History']},\
                                {averageResult['Geography']},{averageResult['CE']},{averageResult['Technology']},{averageResult['IT']}"+\
                                "]},],},}")
        a = r.content
        file = io.BytesIO(a)
        image = Image.open(file).resize((471,300))
        return ImageTk.PhotoImage(image)
    def makeChart2():
        with open('resources/best.csv','r') as file:
            R,I,A,S,E,C = file.read().split('\n')[1].split(',')
        r = requests.get(url=f'https://quickchart.io/chart?v=2.9.4&c=%7Btype%3A%27doughnut%27%2Cwidth%3A472%2Cheight%3A305%2Cdata%3A%7Bdatasets%3A%5B%7Bdata%3A%5B{R}%2C{I}%2C{A}%2C{S}%2C{E}%2C{C}%5D%2CbackgroundColor%3A%5B%27%23007aae%27%2C%27%23138535%27%2C%27%23bfb500%27%2C%27%23bf5b16%27%2C%27%23b21016%27%2C%27%23660010%27%5D%2Clabel%3A%27Dataset1%27%2CborderWidth%3A0%2C%7D%2C%5D%2Clabels%3A%5B%27R%27%2C%27I%27%2C%27A%27%2C%27S%27%2C%27E%27%2C%27C%27%5D%2C%7D%2Coptions%3A%7Bcircumference%3AMath.PI%2Crotation%3AMath.PI%2CcutoutPercentage%3A75%2Clayout%3A%7Bpadding%3A40%2C%7D%2Clegend%3A%7Bdisplay%3Afalse%2C%7D%2Cplugins%3A%7Bdatalabels%3A%7Bcolor%3A%27%23ffffff%27%2Canchor%3A%27center%27%2Calign%3A%27center%27%2Cfont%3A%7Bsize%3A25%2Cweight%3A%27bold%27%2C%7D%2C%7D%2Cdoughnutlabel%3A%7Blabels%3A%5B%7Btext%3A%27%5CnTh%E1%BB%91ng%20k%C3%AA%20t%C3%ADnh%20c%C3%A1ch%27%2Cfont%3A%7Bsize%3A20%2C%7D%2C%7D%2C%7Btext%3A%27%5CnRIASEC%27%2Ccolor%3A%27%23000%27%2Cfont%3A%7Bsize%3A25%2Cweight%3A%27bold%27%2C%7D%2C%7D%2C%5D%2C%7D%2C%7D%2C%7D%2C%7D').content
        file = io.BytesIO(r)
        image = Image.open(file)
        image = image.resize((472,305))
        return ImageTk.PhotoImage(image)
    global screen,homeImgs,btnImgs,l,useWebcam,camChoosen,idCancel,video,chartimg
    useWebcam = False
    try:
        camChoosen.destroy()
    except: pass
    try:
        screen._root.after_cancel(idCancel)
    except: pass
    try:
        screen._root.unbind('<Key>',idBind)
    except: pass
    try: l.destroy() 
    except:pass
    idx = 1
    l = tk.Label(screen._root,
                 width=864,height=223,image=homeImgs[0],borderwidth=0,highlightthickness=0)
    l.place(x=348,y=144)
    chartimg = [makeChart(),makeChart2()]
    chart = tk.Label(screen._root,width=471,height=305,image=chartimg[0],highlightthickness=0,borderwidth=0)
    chart.place(x=308,y=367)
    chart2 = tk.Label(screen._root,width=472,height=305,image=chartimg[1],highlightthickness=0,borderwidth=0)
    chart2.place(x=779,y=367)
    l.bind('<Button-1>',lambda event:incordec(event))
    readVideo()
def LearningPressed() -> None:
    def check(pos):
        if pos.x in range(210):
            return 1
        elif pos.x in range(235,445):
            return 2
        elif pos.x in range(500,705):
            return 3
        elif pos.x in range(750,925):
            return 4
        return 0
    def effect(pos):
        if pos.y in range(155,315):
            result = check(pos)
            match result:
                case 1:l.configure(image=learnImgs[3]['start 1'])
                case 2:l.configure(image=learnImgs[3]['start 2'])
                case 3:l.configure(image=learnImgs[3]['start 3'])
                case 4:l.configure(image=learnImgs[3]['start 4'])
                case 0:l.configure(image=learnImgs[0])
        else:l.configure(image=learnImgs[0])
    def meetNow():
        def meet(link:str)->None:
            '''Check the link and open it in default browser'''
            nonlocal listRooms
            if (link in listRooms):
                webbrowser.open(link)
            else:
                messagebox.showwarning("Thông báo", "Đường liên kết phòng học không hợp lệ!")
        global screen,screen_width,screen_height,USERINFO
        global APIurl,SERVERurl
        scr = tk.Toplevel(screen._root)
        scr.geometry(f'300x500+{(screen_width-300)//2}+{(screen_height-500)//2}')
        scr.iconbitmap('icons/icon.ico')
        scr.title('Danh sách phòng học')
        scr.resizable(width=False,height=False)
        lb1 = tk.Label(scr,text='DANH SÁCH PHÒNG HỌC\n***',font=('SVN-Amsi Narw',19,'normal'),
                       foreground='#7EC0DC')
        lb1.pack()
        tk.Label(scr,text=f'Trường: {USERINFO["user_schoolNAME"]}',font=('SVN-Comic Sans MS',12,'normal'),
                       foreground='#0000CD').pack(anchor='w')
        tk.Label(scr,text=f'Mã trường: {USERINFO["user_schoolID"]}',font=('SVN-Comic Sans MS',12,'normal'),
                       foreground='#0000CD').pack(anchor='w')
        tk.Label(scr,text=30*'-',font=('Eras Demi ITC',12,'normal'),
                 foreground='#EEB4B4').pack(anchor='center')
        tk.Label(scr,text='*Chọn phòng học bất kỳ bên dưới',font=('Arial',10,'italic'),
                 foreground='#48D1CC').pack(anchor='center')
        
        user_schoolID = requests.get(url=APIurl+'/userIn4',params={'getIn4By':'user_ID',
                                                                   'where':USERINFO['user_ID'],
                                                                   'wantToGet':'user_schoolID'}).text
        img = [ImageTk.PhotoImage(Image.open(f'resources/buttons/meeting_room{i}.png')) for i in range(1,3)]

        listRooms = requests.get(url=APIurl+'/meetlinks',params={'meet_schoolID':user_schoolID}).text
        listRooms = ast.literal_eval(listRooms) # Convert str result to list result
        
        n = tk.StringVar()
        roomChoosen = ttk.Combobox(scr,width=280,textvariable=n)
        roomChoosen['values'] = listRooms
        roomChoosen.pack(side=tk.TOP)
        roomChoosen.current()

        meetButton = tk.Button(scr,image=img[0],
                               width=98,height=24,command=lambda:meet(n.get()),borderwidth=0,highlightthickness=0,
                               background='#FFFFFF')
        meetButton.bind('<Enter>',lambda event:meetButton.configure(image=img[1]))
        meetButton.bind('<Leave>',lambda event:meetButton.configure(image=img[0]))
        meetButton.pack(side=tk.BOTTOM)
        scr.grab_set()
    def press(pos):
        if pos.y in range(155,315):
            l.configure(image=learnImgs[0])
            idx = check(pos)
            match idx:
                case 1: # The Balancer
                    run_tools.call('The Balancer')
                case 2: # Atom Finder
                    run_tools.call('Atom Finder')
                case 3: # Function Drawer
                    run_tools.call('EQNs Solver')
                case 4: # EQNs Solver
                    run_tools.call('Function Drawer')
    global screen,l,learnImgs,idCancel
    try: l.destroy() 
    except:pass
    l = tk.Label(screen._root,image=learnImgs[0],
                 width=943,height=528)
    l.place(x=308,y=144)
    try:
        screen._root.after_cancel(idCancel)
    except: pass
    try:
        screen._root.unbind('<Key>',idBind)
    except: pass
    joinButton = tk.Button(screen._root,image=learnImgs[1],
                           highlightthickness=0,
                           width=164,height=61,cursor='hand2',
                           borderwidth=0,background='#FFFFFF',
                           command=meetNow)
    joinButton.place(x=1050,y=480)
    joinButton.bind('<Enter>',lambda event:joinButton.configure(image=learnImgs[2]))
    joinButton.bind('<Leave>',lambda event:joinButton.configure(image=learnImgs[1]))
    joinButton.bind('<Button>',lambda event:joinButton.configure(image=learnImgs[1]))
    joinButton.bind('<ButtonRelease>',lambda event:joinButton.configure(image=learnImgs[2]))
    l.bind('<Motion>',effect)
    l.bind('<Button-1>',press)
def AccountPressed() -> None:
    def getAvtByID(ID)-> Image.Image:
        response = requests.get(url=SERVERurl+f'/database/user_avatar/{ID}.png')
        bytesImg = response.content
        file = io.BytesIO(bytesImg)
        return Image.open(file)
    def progressBar():
        global screen
        pb = ttk.Progressbar(master=l,length=90,orient='horizontal',mode='indeterminate')
        pb.place(x=680,y=206)
        pb.start(interval=20)
        pb2 = ttk.Progressbar(master=l,length=90,orient='horizontal',mode='indeterminate')
        pb2.place(x=680,y=230)
        pb2.start(interval=15)
    def saveIn4():
        def saveScore(score:str)->str:
            score = score.replace('>,','>\n')
            score = score.replace('<',':')
            score = score.replace('>','')
            score = score.replace(';','')
            score = score.replace('1:','\nHệ số 1:').replace('2:','\nHệ số 2:').replace('3:','\nHệ số 3:')
            return score
        if messagebox.askokcancel('Thông báo',f"Do you want to save {USERINFO['user_NAME']}?"):
            with open(f"savedUsers\{USERINFO['user_NAME']}.txt",'w',encoding='UTF-8') as file:
                for key in USERINFO.keys():
                    if key!='stdent_SCORE':
                        print(f'{key}:{USERINFO[key]}',file=file)
                    else:
                        print(f"{key}:\n{saveScore(USERINFO['stdent_SCORE'])}",file=file)
            messagebox.showinfo('Thông báo',f"{USERINFO['user_NAME']} info saved at:\n{os.getcwd()}\savedUsers")
    def setInfo():
        global accountImgs,USERINFO
        nonlocal accountImgs_copy
        barPosition = {'user_NAME':(405,195),
                       'user_LOGIN':(405,230),
                       'user_EMAIL':(405,265),
                       'user_schoolNAME':(405,300),'user_CLASS':(585,300),
                       'stdent_PHONENUM':(405,337),'user_GENDER':(585,333),
                       'user_BIRTHDAY':(405,370)}
        accountImgs_copy = accountImgs[0].copy()
        Tpen = ImageDraw.Draw(accountImgs_copy)
        Tfont = ImageFont.truetype('requirements/SVN-Aleo Bold.otf',15)
        for p in barPosition.keys():
            if p!='user_schoolNAME':
                Tpen.text(xy=barPosition[p],text=str(USERINFO[p]),fill=(0,0,0),font=Tfont)
            else:
                Tpen.text(xy=barPosition[p],text=USERINFO[p].replace(' HIGH SCHOOL',''),fill=(0,0,0),font=Tfont)
    global screen,l,learnImgs,SERVERurl,avtTK,useWebcam,camChoosen,idCancel

    accountImgs_copy = 0
    useWebcam = False
    try:camChoosen.destroy()
    except: pass
    try:screen._root.after_cancel(idCancel)
    except: pass
    try:screen._root.unbind('<Key>',idBind)
    except: pass
    try: l.destroy() 
    except:pass
    setInfo()
    screen.accountImg = ImageTk.PhotoImage(accountImgs_copy)
    l = tk.Label(screen._root,image=screen.accountImg,
                width=943,height=528)
    l.place(x=308,y=144)
    try:
        screen._root.after_cancel(idCancel)
    except: pass
    avt = getAvtByID(USERINFO['user_ID'])
    avtTK = ImageTk.PhotoImage(avt)
    avtLabel = tk.Label(l,image=avtTK)
    avtLabel.place(x=167,y=205)

    saveButton = ttk.Button(l,text='Save info',command=saveIn4)
    saveButton.place(x=692,y=380)
    progressBar()
def ResultPressed() -> None:
    def convertT2R(text:str)->dict[str,list[list[float,float]]]:
        def rsFilter(result:str):
            result = result.lstrip('<').rstrip('>')
            type1 = list(map(float,result[result.index('1:')+2:result.index('2:')-1].split(',')))
            type2 = list(map(float,result[result.index('2:')+2:result.index('3:')-1].split(',')))
            type3 = list(map(float,result[result.index('3:')+2:].split(',')))
            return [type1,type2,type3]
        lst = text.split('>,')
        lst = [sj+'>' for idx,sj in enumerate(lst) if idx!=len(lst)-1]
        result = {sj[:sj.index('<')]:rsFilter(sj) for sj in lst}
        result['IT']=rsFilter(text[text.index('IT')+2:len(text)])
        return result
    def rCalculate(result:list[list]):
        total1 = sum(result[0])
        total2 = sum(result[1])*2
        total3 = sum(result[2])*3
        total = (total1+total2+total3)/12
        return round(total,1)
    def rank(mark:float):
        if mark>9.0: return 'HSXS'
        elif mark>8: return 'HSG'
        elif mark>6.5:return 'HSTT'
        elif mark>5: return 'HSK'
        else: return 'HSY'
    global screen,l,resultImgs,USER_ID,isLeaveAll
    try: l.destroy() 
    except:pass
    l = tk.Label(screen._root,image=resultImgs[0],
                 width=943,height=528)
    l.place(x=308,y=144)
    try:screen._root.after_cancel(idCancel)
    except: pass
    try:screen._root.unbind('<Key>',idBind)
    except: pass
    subjects = {'n':'Hệ số','Math':'Toán','Physics':'Vật lý',
            'English':'Tiếng Anh','Chemistry':'Hóa học',
            'Literature':'Ngữ văn','History':'Lịch sử',
            'Geography':'Địa lý','Biology':'Sinh học',
            'CE':'GDCD','Technology':'Công nghệ',
            'DE':'GDQP','PE':'Thể dục','IT':'Tin học'}
    results = requests.get(APIurl+'/userIn4',params={'getIn4By':'user_ID',
                                                     'where':USER_ID,
                                                     'wantToGet':'stdent_SCORE'}).text.strip('''"''')
    cleanResult = convertT2R(results)
    averageResult = {avrg:rCalculate(cleanResult[avrg]) for avrg in cleanResult}
    table = ttk.Treeview(l, columns=tuple(subjects.keys()),show='headings')
    table.configure(cursor='crosshair')
    for col in subjects.keys():
        table.heading(col, text=subjects[col])
        table.column(col, width=65)
    for i in range(3): # 3 hệ số
        for j in range(2): # 2 cột điểm
            table.insert("", "end", values=[i+1]+[vls[i][j] for vls in cleanResult.values()])
    table.insert("", "end", values=['TBM:']+list(averageResult.values()))
    table.insert("","end",values=['TBCM:',round(sum(averageResult.values())/13,1)])
    table.insert("","end",values=['XL:',rank(round(sum(averageResult.values())/13,1))])
    table.place(x=9,y=206)
    refresh = ttk.Button(l,text='Refresh',command=ResultPressed)
    refresh.place(x=792,y=388)
def AttendancePressed() -> None:
    def listCAM():
        """
        Test the ports and returns a tuple with the available ports 
        and the ones that are working.
        """
        is_working = True
        dev_port = 0
        working_ports = []
        available_ports = []
        while is_working:
            camera = cv2.VideoCapture(dev_port)
            if not camera.isOpened():
                is_working = False
            else:
                is_reading, img = camera.read()
                w = camera.get(4)
                h = camera.get(3)
                if is_reading:
                    working_ports.append([dev_port,h,w])
                else:
                    available_ports.append(dev_port)
            dev_port +=1
        return available_ports,working_ports
    def showChoosen():
        global n,camChoosen,camInfo
        n = tk.StringVar()
        camInfo = [[cam,w,h] for cam,w,h in listCAM()[1]]
        camChoosen = ttk.Combobox(l,width=280,textvariable=n)
        camChoosen['values'] = [f'Camera {cam} ({round(w)} x {round(h)})' for cam,w,h in camInfo]
        camChoosen.configure(width=120)
        camChoosen.place(x=92,y=56)
        camChoosen.current()
    def faceChecking(frame):
        nonlocal face_match
        try:
            result = face_recognition.face_distance(list(allFaces.values()),face_recognition.face_encodings(frame)[0])
            if result[result.argmin()]<.6:
                face_match = list(allFaces.keys())[result.argmin()].strip('.png')
                # Có gương mặt đúng với độ chính xác .6
            else:
                face_match = False
        except IndexError:
            face_match = False
    def setInfo(user_ID:str):
        if not user_ID:
            return
        def getAvtByID(ID)-> Image.Image:
            response = requests.get(url=SERVERurl+f'/database/user_avatar/{ID}.png')
            bytesImg = response.content
            file = io.BytesIO(bytesImg)
            return Image.open(file)
        def nameShorter(user_NAME: str):
            nameSplit = user_NAME.split()
            return '. '.join([s[0] for s in nameSplit[:len(nameSplit)-1]])+'. '+nameSplit.pop()
        def getTime():
            currentTime = datetime.datetime.now()
            currentTimedict = {}
            currentTimedict['year'] = '-'.join([str(i) for i in [currentTime.day,currentTime.month,currentTime.year]])
            currentTimedict['hour'] = ':'.join([str(i) for i in [currentTime.hour,currentTime.minute,currentTime.second]])
            currentTimedict['all'] = currentTimedict['year']+' '+currentTimedict['hour']
            return currentTimedict
        def noVietnamese(utf8_str):
            utf8_str = re.sub(u'[àáạảãâầấậẩẫăắằặẳẵ]', 'a', utf8_str)
            utf8_str = re.sub(u'[ÀÁẠẢÃĂẰẮẶẲẴÂẦẤẬẨẪ]', 'A', utf8_str)
            utf8_str = re.sub(u'[èéẹẻẽêềếệểễ]', 'e', utf8_str)
            utf8_str = re.sub(u'[ÈÉẸẺẼÊỀẾỆỂỄ]', 'E', utf8_str)
            utf8_str = re.sub(u'[òóọỏõôồốộổỗơờớợởỡ]', 'o', utf8_str)
            utf8_str = re.sub(u'[ÒÓỌỎÕÔỒỐỘỔỖƠỜỚỢỞỠ]', 'O', utf8_str)
            utf8_str = re.sub(u'[ìíịỉĩ]', 'i', utf8_str)
            utf8_str = re.sub(u'[ÌÍỊỈĨ]', 'I', utf8_str)
            utf8_str = re.sub(u'[ùúụủũưừứựửữ]', 'u', utf8_str)
            utf8_str = re.sub(u'[ƯỪỨỰỬỮÙÚỤỦŨ]', 'U', utf8_str)
            utf8_str = re.sub(u'[ýỳỵỷỹ]', 'y', utf8_str)
            utf8_str = re.sub(u'[ÝỲỴỶỸ]', 'Y', utf8_str)
            utf8_str = re.sub(u'Đ', 'D', utf8_str)
            utf8_str = re.sub(u'đ', 'd', utf8_str)
            return utf8_str
        # def checkUserIsAttended(filename:str,user_ID:int):
        #     user_ID = str(user_ID)
        #     with open(filename) as file:
        #         while True:
        #             line = file.readline()
        #             if line == '':
        #                 return False
        #             line = line.split(',')
        #             if user_ID in line:
        #                 return True
        def notifyAndWriteToCSV(user_NAME:str,user_ID:str,user_CLASS:str):
            Toaster.show_toast(title='EduQuest',msg=f"Đã điểm danh: {user_NAME}\nID:{user_ID}\nThời gian: {getTime()['all']}",
                               icon_path='icons/icon.ico',duration=5,threaded=True)
            attendanceFilename = f"attendance.logdir/{getTime()['year']}.csv"
            if os.path.isfile(attendanceFilename):
                # if checkUserIsAttended(attendanceFilename,user_ID): check xem neu da diem danh roi thi ko ghi lai nx, neu # dong nay thi diem danh bao nhieu no cung se luu lai
                #     return
                # else:
                    with open(attendanceFilename,'a',encoding='utf-8') as csvfile:
                        print(f"{getTime()['hour']}",f'{user_ID}',f'{noVietnamese(user_NAME)}',f'{user_CLASS}',sep=',',end='\n',file=csvfile)
            else:
                with open(attendanceFilename,'a',encoding='utf-8') as csvfile:
                    print('Time,ID,Name,Class',end='\n',file=csvfile)
                    print(f"{getTime()['hour']}",f'{user_ID}',f'{noVietnamese(user_NAME)}',f'{user_CLASS}',sep=',',end='\n',file=csvfile)  
        global l,infoImgText,infoImgText_copy,faceNow
        faceNow = user_ID
        infoImgText_copy = infoImgText.copy()
        userinfo = requests.get(APIurl+'/userIn4/',params={'getIn4By':'user_ID','where':str(user_ID),'wantToGet':'*'})
        userinfo:dict = ast.literal_eval(userinfo.text)
        userinfo['user_shortedNAME'] = nameShorter(userinfo['user_NAME'])
        userinfo['user_GENDER'] = userinfo['user_GENDER'].replace('female','Nữ').replace('male','Nam')
        userimage = getAvtByID(user_ID)

        barPosition = {'user_shortedNAME':(800,125),'user_CLASS':(800,150),
                       'user_BIRTHDAY':(850,187),'user_GENDER':(850,220)}
        Tpen = ImageDraw.Draw(infoImgText_copy)
        Tfont = ImageFont.truetype('requirements/SVN-Aleo Bold.otf',18)

        for i in list(barPosition.keys()):
            Tpen.text(xy=barPosition[i],text=userinfo[i],fill=(0,0,0),font=Tfont)
        
        infoImgText_copy.paste(userimage,(587,120))
        infoImgText_copy = ImageTk.PhotoImage(infoImgText_copy)
        l.configure(image=infoImgText_copy)
        notifyAndWriteToCSV(userinfo['user_NAME'],userinfo['user_ID'],userinfo['user_CLASS'])

    def frameProcessor(frame):
        nonlocal counter,face_match
        try:
            result = face_detection.process(frame)
            face = result.detections[0]
            bbox = face.location_data.relative_bounding_box
            x, y, w, h = int(bbox.xmin * frame.shape[1]), int(bbox.ymin * frame.shape[0]), int(bbox.width * frame.shape[1]), int(bbox.height * frame.shape[0])
            if not face_match:
                cv2.rectangle(frame,(x, y),(x+w, y+h),(204,108,108),2)
            else:
                cv2.rectangle(frame,(x, y),(x+w, y+h),(108,204,145),2)
        except:
            pass
        finally:
            counter += 1
            if counter % 60 == 0:
                faceChecking(frame)
                setInfo(face_match)
            return frame
    def getImgFromCAM() -> None:
        '''## getImgFromCAM(): 
        Show an image which captured by webcam number x'''
        def setImgForCAM():
            global imagePIL, imageTK, c, framePrs, video
            if useWebcam:
                ret, frame = video.read()
                frame = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
                frame = framePrs(frame)
                imagePIL = Image.fromarray(frame)
                imagePIL = imagePIL.resize((round((imagePIL.size[0]/imagePIL.size[1])*435),435))
                imageTK = ImageTk.PhotoImage(imagePIL)
                c.configure(image=imageTK)
                screen._root.after(1,setImgForCAM)
            else:
                return
        global c,camChoosen,video
        nonlocal btn
        try:
            port = int(n.get()[7])
        except:
            screen._root.bell()
            messagebox.showerror('EduQuest','Vui lòng chọn một Camera!')
            return
        video = cv2.VideoCapture(port)
        
        l.configure(image=attendanceImgs[1])
        btn.configure(image=logImg,command=lambda: os.startfile('attendance.logdir')) 
        c = tk.Label(l,
                     width=580,
                     height=435)
        # print(round((camInfo[port][1]/camInfo[port][2])*435))
        c.place(x=0,y=46)
        camChoosen.destroy()
        setImgForCAM()
    global screen,l,useWebcam,framePrs,faceNow
    try:
        if useWebcam:
            return
    except NameError:
        pass
    try: l.destroy() 
    except:pass
    faceNow = False
    face_match = False
    useWebcam = True
    counter = np.int64(-1)
    framePrs = frameProcessor
    l = tk.Label(screen._root,image=attendanceImgs[0],
                 width=943,height=528,highlightthickness=0, borderwidth=0)
    l.place(x=308,y=144)
    showChoosen()
    btn = tk.Button(l,command=getImgFromCAM,
                    image=startImg,
                    highlightthickness=0,
                    borderwidth=0,
                    state='active')
    btn.place(x=672,y=481)
def StudentListPressed() -> None:
    def getStudentofClass(_class:str) -> list:
        '''Get all user_ID of students who in class '_class' as a list'''
        allIn4 = requests.get(APIurl+'/userIn4',params={'getIn4By':'user_CLASS','where':_class,'wantToGet':
                                                       'user_ID,user_NAME,stdent_PHONENUM,user_BIRTHDAY,user_GENDER',
                                                       'account_TYPE':'STDENT'}).text
        allIn4:list = ast.literal_eval(allIn4)
        return allIn4
    def showUpdate():
        def convertT2R(text:str)->dict[str,list[list[float,float]]]:
            def rsFilter(result:str):
                result = result.lstrip('<').rstrip('>')
                type1 = list(map(float,result[result.index('1:')+2:result.index('2:')-1].split(',')))
                type2 = list(map(float,result[result.index('2:')+2:result.index('3:')-1].split(',')))
                type3 = list(map(float,result[result.index('3:')+2:].split(',')))
                return [type1,type2,type3]
            lst = text.split('>,')
            lst = [sj+'>' for idx,sj in enumerate(lst) if idx!=len(lst)-1]
            result = {sj[:sj.index('<')]:rsFilter(sj) for sj in lst}
            result['IT']=rsFilter(text[text.index('IT')+2:len(text)])
            return result
        def convertR2T(result:dict) -> str:
            final = ''
            for i, subj in enumerate(result.keys()):
                if i!=0:
                    final+='>,'
                final += str(subj)+'<'
                for hs,mark in enumerate(result[subj]):
                    final+=str(hs+1)+f':{mark[0]},{mark[1]}'
                    if hs!=2:
                        final+=';'
            final+='>'
            return final
        def rCalculate(result:list[list]):
            total1 = sum(result[0])
            total2 = sum(result[1])*2
            total3 = sum(result[2])*3
            total = (total1+total2+total3)/12
            return round(total,1)
        def rank(mark:float):
            if mark>9.0: return 'HSXS'
            elif mark>8: return 'HSG'
            elif mark>6.5:return 'HSTT'
            elif mark>5: return 'HSK'
            else: return 'HSY'
        def doUpdate():
            nonlocal stdentUpdateButton,stdentUpdateEntry,stdentUpdateText,subjects
            global lineEditR, ID_update
            subjectUpdate = list(subjects.keys())[numUpdate]
            new = stdentUpdateEntry.get()
            _type = lineEditR[0]
            _id = ID_update

            result = requests.get(APIurl+'/userIn4',params={'getIn4By':'user_ID','where':_id,'wantToGet':'stdent_SCORE'}).text.strip('''"''')
            cleanedResult = convertT2R(result)
            match _type:
                case 1:
                    m,n = 0,0
                case 2:
                    m,n = 0,1
                case 3:
                    m,n = 1,0
                case 4:
                    m,n = 1,1
                case 5:
                    m,n = 2,0
                case 6:
                    m,n = 2,1
            cleanedResult[subjectUpdate][m][n] = new
            realUpdate = convertR2T(cleanedResult)
            realUpdate = "{'stdent_SCORE':'"+str(realUpdate)+"'}"
            requests.post(APIurl+'/update',params={'updateIn4By':'user_ID','where':_id,'wantToUpdate':realUpdate})
            stdentUpdateButton.configure(state='disable')
            stdentUpdateEntry.delete(0,tk.END)
            stdentUpdateEntry.configure(state='disabled')
        def updateResult(event):
            nonlocal stdentList, STT, stdentUpdateEntry, stdentUpdateButton
            global studentTable, lineEditR, numUpdate,ID_update
            x = event.x
            y = event.y
            if y not in range(26): return
            numUpdate = int(x)//39 # Môn học thứ x
            lineEdit = studentTable.focus() # Mã bài ktra
            ID_update = stdentList[int(STT)-1]['user_ID'] # ID của hs cần update
            try:
                lineEditR = [int(studentTable.focus()[studentTable.focus().rfind('0'):],16), False] # Loại bài ktra
                match lineEditR[0]:
                    case 1:
                        lineEditR[1] = '15p số 1'
                    case 2:
                        lineEditR[1] = '15p số 2'
                    case 3:
                        lineEditR[1] = '45p số 1'
                    case 4:
                        lineEditR[1] = '45p số 2'
                    case 5:
                        lineEditR[1] = 'Học kì 1'
                    case 6:
                        lineEditR[1] = 'Học kì 2'
                    case other:
                        # Trường hợp nhấn > 6
                        lineEditR = False
            except:
                # Trường hợp không nhấn
                lineEditR = False
            
            subjects = {'Math':'Toán','English':'Anh',
            'Physics':'Lý','Chemistry':'Hóa',
            'Literature':'Văn','History':'Sử',
            'Geography':'Địa','Biology':'Sinh',
            'CE':'GDCD','Technology':'CN',
            'DE':'GDQP','PE':'Thể','IT':'Tin'}
            stdentUpdateEntry.delete(0,tk.END)
            stdentUpdateEntry.configure(state='disabled')
            stdentUpdateButton.configure(state='disabled')
            stdentUpdateText.configure(text='Chọn môn học')
            # Trường hợp nhấn đúng 'y' nhưng không đúng hàng ngang và không đúng môn (0~6)
            if lineEditR and numUpdate:
                # Người dùng nhấp đôi, đúng vị trí y, đúng ô (0~6)
                stdentUpdateText.configure(text=list(subjects.values())[numUpdate-1]+f' {lineEditR[1]}')

                stdentUpdateEntry.configure(state='!disabled')
                values = studentTable.item(lineEdit,'values')
                stdentUpdateEntry.insert(0,values[numUpdate])
                stdentUpdateButton.configure(state='!disable')
        def refresh():
            nonlocal top
            top.destroy()
            showUpdate()
        global screen, Ltop, Atop, studentImgs, studentTable
        nonlocal stdentList, table
        STT = table.focus()
        STT = int(STT[STT.rfind('0'):],16)
        r = requests.get(SERVERurl+f"/database/user_avatar/{stdentList[int(STT)-1]['user_ID']}.png").content
        file = io.BytesIO(r)
        img = Image.open(fp=file).resize((135,135))
        img = ImageTk.PhotoImage(img)
 
        top = tk.Toplevel(screen._root,width=700,height=300)
        top.geometry("+32+32")
        top.resizable(False,False)
        top.title('Update student')
        top.iconbitmap('icons/icon.ico')
        top.grab_set()
        Ltop = tk.Label(top,image=studentImgs[1])
        Ltop.place(x=0,y=0)
        Atop = tk.Label(top,image=img,borderwidth=0)
        Atop.place(x=5,y=42)

        subjects = {'n':'Hệ số','Math':'Toán','English':'Anh',
            'Physics':'Lý','Chemistry':'Hóa',
            'Literature':'Văn','History':'Sử',
            'Geography':'Địa','Biology':'Sinh',
            'CE':'GDCD','Technology':'CN',
            'DE':'GDQP','PE':'Thể','IT':'Tin'}
        results = requests.get(APIurl+'/userIn4',params={'getIn4By':'user_ID',
                                                        'where':stdentList[int(STT)-1]['user_ID'],
                                                        'wantToGet':'stdent_SCORE'}).text.strip('''"''')
        cleanResult = convertT2R(results)
        averageResult = {avrg:rCalculate(cleanResult[avrg]) for avrg in cleanResult}
        studentTable = ttk.Treeview(top, columns=tuple(subjects.keys()),show='headings')
        for col in subjects.keys():
            studentTable.heading(col, text=subjects[col])
            studentTable.column(col, width=39)
        for i in range(3): # 3 hệ số
            for j in range(2): # 2 cột điểm
                studentTable.insert("", "end", values=[i+1]+[vls[i][j] for vls in cleanResult.values()])
        studentTable.insert("", "end", values=['TBM:']+list(averageResult.values()))
        studentTable.insert("","end",values=['TBCM:',round(sum(averageResult.values())/13,1)])
        studentTable.insert("","end",values=['XL:',rank(round(sum(averageResult.values())/13,1))])
        studentTable.place(x=142,y=9,height=200)
        studentTable.bind('<Double-Button-1>',updateResult)
        stdentRefresh = ttk.Button(top, text='Làm mới', command=refresh)
        stdentRefresh.place(x=600,y=211)
        stdentUpdateButton = ttk.Button(top, text='Cập nhật', command=doUpdate, state='disable')
        stdentUpdateButton.place(x=500,y=211)
        stdentUpdateText = ttk.Label(top,text='Chọn môn học',width=15)
        stdentUpdateText.place(x=143,y=211)

        ttk.Label(top,text='Điểm:').place(x=256,y=211)
        stdentUpdateEntry = ttk.Entry(top, state='disabled')
        stdentUpdateEntry.place(x=290,y=211)
        top.mainloop()
        return top.grab_release()
    def addEmail():
        items = table.item(table.focus())['values']
        table.item(table.focus(),text="",values=items,tags=('selectedrow',))
        listEmail.append(emailWhat(table.focus()))
        listFocused.append(table.focus())
    def removeEmail():
        if int(table.focus()[table.focus().rfind('0'):],16)%2==0:
            table.item(table.focus(),tags=('oddrow',))
        else:
            table.item(table.focus(),tags=('evenrow',))
        listEmail.remove(emailWhat(table.focus()))
        listFocused.remove(table.focus())
    def emailWhat(focus) -> str:
        items = table.item(focus)
        _id = items['values'][1]
        r = requests.get(APIurl+'/userIn4',params={'getIn4By':'user_ID','where':_id,'wantToGet':'user_EMAIL'})
        r = r.text.strip('''"''')
        return r
    def check():
        nonlocal table,addEmailButton
        if table.focus():
            addEmailButton.configure(state='!disable')
        else:
            addEmailButton.configure(state='disable')

        if table.focus() in listFocused:
            removeEmailButton.configure(state='!disable')
        else:
            removeEmailButton.configure(state='disable')
        if len(listFocused)>0:
            sendEmailButton.configure(state='active')
        else:
            sendEmailButton.configure(state='disable')
        l.after(1,check)
    def send_email():
        threading.Thread(target=lambda:os.system(os.getcwd()+r'\tools\sendEmail.exe '+' '.join([USERINFO['user_EMAIL'],' '.join(listEmail),USERINFO['admin_EMAILPASS']]))).start()

    global screen,l,useWebcam
    useWebcam = False
    try:
        camChoosen.destroy()
    except:
        pass
    try: l.destroy() 
    except:pass
    l = tk.Label(screen._root,image=studentImgs[0],
                 width=943,height=528, highlightthickness=0, borderwidth=0)
    l.place(x=308,y=144)
    collumns = ('STT','ID','Name','Phonenum','Birthday','Gender')
    table = ttk.Treeview(l, columns=collumns,show='headings')
    
    table.heading('STT', text='STT')
    table.column('STT', width=50)
    table.heading('ID', text='ID')
    table.column('ID', width=80)
    table.heading('Name', text='Họ và tên')
    table.column('Name', width=140)
    table.heading('Phonenum', text='Số điện thoại')
    table.column('Phonenum', width=240)
    table.heading('Birthday', text='Ngày sinh')
    table.column('Birthday', width=90)
    table.heading('Gender', text='Giới tính')
    table.column('Gender', width=93)

    table.tag_configure('oddrow', background='#A6A6A6')
    table.tag_configure('evenrow', background='#C8C8C8')
    table.tag_configure('selectedrow', background='#60C5F1')


    stdentList:dict = getStudentofClass(USERINFO['user_CLASS'])
    for stt,student in enumerate(stdentList):
        if stt%2 == 0:
            table.insert("", "end", values=[stt+1,student['user_ID'],student['user_NAME'],student['stdent_PHONENUM'],student['user_BIRTHDAY'],student['user_GENDER'].replace('female','Nữ').replace('male','Nam')], tags=('evenrow',))
        else:
            table.insert("", "end", values=[stt+1,student['user_ID'],student['user_NAME'],student['stdent_PHONENUM'],student['user_BIRTHDAY'],student['user_GENDER'].replace('female','Nữ').replace('male','Nam')], tags=('oddrow',))
    table.place(x=29,y=156,height=296)

    listEmail = []
    listFocused = []

    refresh = ttk.Button(l,text='Làm mới',command=StudentListPressed)
    refresh.place(x=612,y=456)

    updateButton = ttk.Button(l,text='Cập nhật',command=showUpdate)
    updateButton.place(x=522,y=456)

    addEmailButton = ttk.Button(l,text='Thêm Email',command=addEmail,state='disable')
    addEmailButton.place(x=122,y=456)
    removeEmailButton = ttk.Button(l,text='Xoá Email',command=removeEmail,state='disable')
    removeEmailButton.place(x=32,y=456)
    sendEmailButton = ttk.Button(l,text='Gửi',command=send_email,state='disable')
    sendEmailButton.place(x=212,y=456)
    check()    
def HollandTestPressed():
    def showResult():
        def readAFile():
            content = requests.get(SERVERurl+'/resources/AList.txt').content
            content = content.decode(encoding='utf-8')
            content = content.split('<>')
            return {j:content[i+1] for i,j in enumerate('RIASEC')}
        def retry():
            nonlocal retryButton
            retryButton.destroy()
            HollandTestPressed()
        def calculate(answers:list,questionRand:list):
            def theBest(result:dict):
                for i in result:
                    if max(result.values())==result[i]: yield i
            realQuestion = readQFile()[0]
            result = {char:0 for char in 'RIASEC'}
            for question in questionRand:
                for char in 'RIASEC':
                    if question in realQuestion[char]: 
                        result[char]+=4*answers[questionRand.index(question)]
                        break
            bests = list(theBest(result))
            return bests,result
        def openLink(best):
            links = {'R':'https://sites.google.com/view/hollandtest-realistic/trang-ch%E1%BB%A7',
                     'I':'https://sites.google.com/view/hollandtest-investigate/trang-ch%E1%BB%A7',
                     'A':'https://sites.google.com/view/hollandtest-artist/trang-ch%E1%BB%A7',
                     'S':'https://sites.google.com/view/hollandtest-social/trang-ch%E1%BB%A7',
                     'E':'https://sites.google.com/view/hollandtest-social/trang-ch%E1%BB%A7',
                     'C':'https://sites.google.com/view/hollandtest-conventional/trang-ch%E1%BB%A7'}
            for i in best:
                webbrowser.open_new_tab(links[i])
        def saveAFile(best,ratio:dict):
            r1 = requests.post('http://127.0.0.1:8000/save',params={'content':''.join(best),'postType':'best'})
            r2 = requests.post('http://127.0.0.1:8000/save',params={'content':','.join(map(str,ratio.values())),'postType':'ratio'})
            if all(filter(lambda x:bool(x==200),[r1,r2])):
                Toaster.show_toast(title='EduQuest',msg=f"Hoàn thành trắc nghiệm Holland - thuộc nhóm {', '.join(best)}\nĐã lưu kết quả của bạn!",
                                   icon_path='icons/icon.ico',duration=5,threaded=True)
            else:
                Toaster.show_toast(title='EduQuest',msg=f"Đã xảy ra lỗi, hãy thử lại sau!",
                                   icon_path='icons/icon.ico',duration=5,threaded=True)
        nonlocal qesLabel,replyButtons,resultList
        qesLabel.destroy()
        for i in range(1,6):
            replyButtons[i].destroy()
        screen._root.after_cancel(idCancel)
        l.configure(image=hollandTestImgs['result'][0])

        best, ratio = calculate(resultList,questionList)
        saveAFile(best,ratio)

        resultPB = {f'{i}':ttk.Progressbar(screen._root,orient='horizontal',length=240,mode='determinate') for i in 'RIASEC'}
        resultLB = {f'{i}':tk.Label(screen._root,font=('SVN-PF Din Text Pro',8,'bold'),background='#05861A',foreground='#FFFFFF') for i in 'RIASEC'}
        [resultLB[i].configure(foreground='#0200FF') for i in 'RIASEC' if i in best]
        for i,j in enumerate('RIASEC'):
            resultPB[j].configure(value=ratio[j])
            resultPB[j].place(x=438,y=60*i+260)

            resultLB[j].configure(text=f'{ratio[j]}/100')
            resultLB[j].place(x=438,y=60*i+260)

        v = tk.Scrollbar(screen._root,orient='vertical')
        text = tk.Text(screen._root,wrap='word',background='#E4E8EB',font=('SVN-Calling Code',14,'italic'),width=38,borderwidth=0,yscrollcommand=v.set)
        for i in best:
            text.insert(tk.END,readAFile()[i])
        v.configure(command=text.yview)
        v.place(x=1909,y=330,height=170)
        text.place(x=700,y=260,height=240)

        learnMore = tk.Label(screen._root,text='Tìm hiểu thêm',font=(('SVN-Calling Code',12,'italic')),
                             underline=0,background='#E4E8EB',foreground='#4007A2')
        learnMore.bind('<Enter>',lambda event:learnMore.configure(foreground='#8E24AA'))
        learnMore.bind('<Leave>',lambda event:learnMore.configure(foreground='#4007A2'))
        learnMore.bind('<Button>',lambda event:openLink(best))
        learnMore.place(x=950,y=500)

        retryButton = tk.Button(screen._root,image=hollandTestImgs['result'][1],command=retry,borderwidth=0,highlightthickness=0,background='#C2E3F6')
        retryButton.bind('<Enter>',lambda event:retryButton.configure(image=hollandTestImgs['result'][2]))
        retryButton.bind('<Leave>',lambda event:retryButton.configure(image=hollandTestImgs['result'][1]))
        retryButton.place(x=920,y=562)
    def reply(result:int) -> None : 
        nonlocal resultList, qes
        resultList[qes] = result
        if qes<len(questionList)-1:
            qes +=1
            qesLabel.configure(text=f"{qes+1}/{len(questionList)}: {questionList[qes]}")
        if all(resultList):
            nonlocal canSubmit
            canSubmit = False
            showResult()
    def enter(t):
        nonlocal replyButtons
        replyButtons[t].configure(image=hollandTestImgs['buttons2'][t])
        l.configure(image=hollandTestImgs['background'][t])
        isLeaveAll[t] = False
    def leave(t):
        nonlocal replyButtons
        replyButtons[t].configure(image=hollandTestImgs['buttons1'][t])
        isLeaveAll[t] = True
    def leaveAll():
        global idCancel
        if all(isLeaveAll):
            l.configure(image=hollandTestImgs['background'][0])
        idCancel = screen._root.after(1,leaveAll)
    def readQFile()->list:
        question = {}
        content = requests.get(SERVERurl+'/resources/QList.txt').content
        content = content.decode(encoding='utf-8')

        R = content.index('<R>')
        I = content.index('<I>')
        A = content.index('<A>')
        S = content.index('<S>')
        E = content.index('<E>')
        C = content.index('<C>')
        question['R'] = list(filter(lambda x:bool(x),content[R+4:I].split('\n')))
        question['I'] = list(filter(lambda x:bool(x),content[I+4:A].split('\n')))
        question['A'] = list(filter(lambda x:bool(x),content[A+4:S].split('\n')))
        question['S'] = list(filter(lambda x:bool(x),content[S+4:E].split('\n')))
        question['E'] = list(filter(lambda x:bool(x),content[E+4:C].split('\n')))
        question['C'] = list(filter(lambda x:bool(x),content[C+4:].split('\n')))

        nested_list = question.values()
        questionRand = [element for sublist in nested_list for element in sublist]
        shuffle(questionRand)
        return question, questionRand
    def pressKey(event):
        nonlocal replyButtons
        if not canSubmit:
            return
        try:
            for i in range(1,6):
                replyButtons[i].configure(image=hollandTestImgs['buttons1'][i])
        except: pass
        if event.keycode in range(49,54):
            reply(int(event.char))
            try:
                replyButtons[int(event.char)].configure(image=hollandTestImgs['buttons2'][int(event.char)])
                l.configure(image=hollandTestImgs['background'][int(event.char)])
            except: pass
            isLeaveAll[int(event.char)] = False

    def start():
        nonlocal questionList,resultList,qesLabel,replyButtons,qes,isLeaveAll,startButton,canSubmit
        l.configure(image=hollandTestImgs['background'][0])
        startButton.destroy()
        questionList = readQFile()[1]
        resultList = [None]*(len(questionList))
        canSubmit = True
        qesLabel = tk.Label(screen._root,text=f"{qes+1}/{len(questionList)}: {questionList[qes]}",font=('SVN-PF Din Text Pro',14,'normal'),
                            anchor='center',wraplength=580,background='#4681BF',foreground='#FFFFFF') 
        qesLabel.place(x=500,y=200,width=580)
        for i in range(1,6):
            replyButtons[i] = tk.Button(screen._root,image=hollandTestImgs['buttons1'][i],command=lambda t=i:reply(t),highlightthickness=0,borderwidth=0,background='#C2E3F6')
            replyButtons[i].bind('<Enter>',lambda event,u=i:enter(t=u))
            replyButtons[i].bind('<Leave>',lambda event,u=i:leave(t=u))
            replyButtons[i].place(x=495,y=46*i+302)
        leaveAll()
    global screen,l,hollandTestImgs,idBind
    replyButtons:tk.Button = [0]*6
    qes = 0
    canSubmit = False
    isLeaveAll = [True]*6
    questionList,resultList,qesLabel = [None]*3
    try: l.destroy() 
    except:pass
    l = tk.Label(screen._root,image=hollandTestImgs['opening'][0],
                 width=943,height=528, highlightthickness=0, borderwidth=0)
    l.place(x=308,y=144)
    try:
        screen._root.after_cancel(idCancel)
    except: pass
    try:
        screen._root.unbind('<Key>',idBind)
    except:
        pass
    startButton = tk.Button(l,image=hollandTestImgs['opening'][1],command=start,borderwidth=0,highlightthickness=0,background='#E4E3FF')
    startButton.bind('<Enter>',lambda event:startButton.configure(image=hollandTestImgs['opening'][2]))
    startButton.bind('<Leave>',lambda event:startButton.configure(image=hollandTestImgs['opening'][1]))
    startButton.place(x=381,y=401)
    idBind = screen._root.bind('<Key>',pressKey)
    return
def StudentPosPressed():
    def nameFilter(name:str)->str:
        if len(name.split())==2:
            return name.split()[0][0]+'. '+name.split()[1]
        else:
            return name.split()[len(name.split())-2][0]+'. '+name.split()[len(name.split())-1]
    def drawName(name:str,i:int='',color:str="#BFBFBF") -> Image.Image:
        image = Image.new("RGB", (92, 70), color)
        draw = ImageDraw.Draw(image)
        text_color = "black"
        font = ImageFont.truetype('requirements/SVN-Amsi Narw Bold.ttf',15)

        # Tính toán vị trí để đặt chữ ở giữa ảnh
        text_bbox = draw.textbbox((0, 0), name+'\n'+str(i), font=font)
        text_width = text_bbox[2] - text_bbox[0]
        text_height = text_bbox[3] - text_bbox[1]
        text_x = (86 - text_width) // 2
        text_y = (40 - text_height) // 2 + 7

        draw.text((text_x, text_y), name+'\n'+str(i), fill=text_color, font=font,align='center')
        return image
    def showAVT(ID,pos:list):
        try:
            studentPosImgs[1].destroy()
        except:
            pass
        response = requests.get(url=SERVERurl+f'/database/user_avatar/{ID}.png')
        bytesImg = response.content
        file = io.BytesIO(bytesImg)
        image = Image.open(file)
        image = image.resize((100,100))
        imageTK = ImageTk.PhotoImage(image=image)
        studentPosImgs[2] = imageTK
        studentPosImgs[1] = tk.Label(screen._root,image=studentPosImgs[2],width=100,height=100)
        studentPosImgs[1].place(x=pos[0]-40,y=pos[1]-50)
    def readPos():
        _class = USERINFO['user_CLASS']
        with open(f'resources/class/{_class}.txt','r',encoding='utf-8') as file:
            content = file.read()
        lst = content.split('\n')
        IDlst = [l.split(',')[0] for l in lst]
        NAMElst = [l.split(',')[1] for l in lst]
        return IDlst,NAMElst
    def writePos(pos):
        with open(f"resources/class/{USERINFO['user_CLASS']}.txt",'w',encoding='utf-8') as file:
            for i,j in enumerate(pos[0]):
                if i!=len(pos[0])-1:print(f"{j},{pos[1][i]}",file=file)
                else:print(f"{j},{pos[1][i]}",end='',file=file)
    def changePos(pos):
        nonlocal idx,buttons
        buttons[pos].bind('<Leave>',lambda event,m=pos:buttons[m].configure(image=nameImages3[studentsNAME[m]]))
        idx.append(pos)
        if len(idx)==2:
            nowPos = readPos()
            nowPos[0][idx[0]],nowPos[0][idx[1]]=nowPos[0][idx[1]],nowPos[0][idx[0]]
            nowPos[1][idx[0]],nowPos[1][idx[1]]=nowPos[1][idx[1]],nowPos[1][idx[0]]
            writePos(nowPos)
            idx = []
            StudentPosPressed()
    global screen,l,useWebcam,nameImages,nameImages2
    useWebcam = False
    try:
        camChoosen.destroy()
    except:
        pass
    try: l.destroy() 
    except:pass
    l = tk.Label(screen._root,image=studentPosImgs[0],
                 width=943,height=528, highlightthickness=0, borderwidth=0)
    l.place(x=308,y=144)
    studentPosImgs[1] = tk.Label(screen._root,width=100,height=100)
    idx = []

    studentsID,studentsNAME = readPos()
    studentsNAME = list(map(nameFilter,studentsNAME))

    realStudentList:list = ast.literal_eval(requests.get('http://127.0.0.1:8000/userIn4',
                                                    params={'getIn4By':'user_CLASS','where':'11A5','wantToGet':'user_NAME'}).text)
    for i in ast.literal_eval(requests.get('http://127.0.0.1:8000/userIn4',
                                           params={'getIn4By':'account_TYPE','where':'ADMIN','wantToGet':'user_NAME'}).text):
        if i in realStudentList: 
            teacherNAME = realStudentList.pop(realStudentList.index(i))
    realStudentList = list(map(nameFilter,realStudentList))

    nameImages = {name:ImageTk.PhotoImage(drawName(name,i+1)) for i,name in enumerate(realStudentList)}
    nameImages2 = {name:ImageTk.PhotoImage(drawName(name,color='#60C5F1')) for name in realStudentList}
    nameImages3 = {name:ImageTk.PhotoImage(drawName(name,color='#FF7378')) for name in realStudentList}
    pos_x2 = [[220*x+140,220*x+140+86] for x in range(1,5)]
    pos_x = []
    for x in pos_x2:
        pos_x += x
    pos_y = [-82*x+520 for x in range(1,5)]
    buttons = []

    _class = tk.Label(screen._root,text=f"Lớp: {USERINFO['user_CLASS']} - GVCN: {teacherNAME}",font=('SVN-Aleo',12,'bold'))
    _class.place(x=380,y=600)
    _class.bind('<Enter>',lambda event:_class.configure(background='#D9D9D9'))
    _class.bind('<Leave>',lambda event:_class.configure(background='#FFFFFF'))
    
    for i,name in enumerate(studentsNAME):
        buttons.append(0)
        buttons[i] = tk.Button(screen._root,image=nameImages[name],width=86,height=65)
        buttons[i].bind('<Enter>',lambda event,t=i,m=name:buttons[t].configure(image=nameImages2[m]))
        buttons[i].bind('<Leave>',lambda event,t=i,m=name:buttons[t].configure(image=nameImages[m]))
        buttons[i].bind('<Button-1>',lambda event,t=i,p=(pos_x[i%8],pos_y[i//8]):showAVT(studentsID[t],p))
        buttons[i].bind('<Button-3>',lambda event,t=i:changePos(t))
        buttons[i].place(x=pos_x[i%8],y=pos_y[i//8])

COMMANDS = {'homepage': HomepagePressed,
            'learning':LearningPressed,
            'learningresult':ResultPressed,
            'attendance':AttendancePressed,
            'studentlist':StudentListPressed,
            'hollandtest':HollandTestPressed,
            'studentpos':StudentPosPressed}

addAllShapes()
setBackground(bg=f'resources/MainApp{USERINFO["account_TYPE"]}.gif')
createButton(mode=USERINFO['account_TYPE'])
title(f"EduQuest - {USERINFO['account_TYPE']}: {USERINFO['user_NAME']}")
setUserInfo()
logoutButton()
mainloop()