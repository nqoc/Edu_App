import matplotlib.pyplot as plt
from matplotlib.patches import Circle
import numpy as np
import re
from turtle import *
import tkinter as tk
from math import *
import io
import sys
import builtins
import pygame

pygame.init()

screen_info = pygame.display.Info()
screen_width, screen_height = screen_info.current_w, screen_info.current_h

setup(510,510,(screen_width-510)/2,(screen_height-510)/2)
screensize(500,500)
setworldcoordinates(0,500,500,0)
colormode(255)
Screen()._root.iconbitmap('icons/function_icon.ico')
title("Function drawer")


addshape("tools/resources/mathbg.gif")
t=Turtle()
t.ht()
t.speed(90)
t.pu()
p=t.clone()
t.goto(250,250)
t.shape("tools/resources/mathbg.gif")
t.stamp()
del(t)
use_color=False

nor_funcs=[]
cir_funcs=[]
def printc(*args,co="black",se=" ",en="\n",pos=(0,0),fon="Consolas",typ="normal",size=12):
    def print2(*args, s=' ', e='\n', file=None):
        if file is None:
            file = io.StringIO()
        builtins.print(*args, sep=s, end=e, file=file)
        file.seek(0)
        output = file.read()
        file.seek(0)
        file.truncate(0)
        return output
    global p
    tracer(0)
    p.color(co)
    p.pu()
    p.goto(pos)
    p.pd()
    p.seth(0)
    p.write(print2(*args,s=se,e=en),font=(fon,size, typ))
    update()
def math_convert(expr):
    d=[]
    for i  in expr:
        i = re.sub(r'(\d)([a-zA-Z])', r'\1*\2', i)
        i = i.replace('^', '**')
        d.append(i)
    return d
def math_caution(content,icon="caution.ico"):
    root = tk.Tk()
    root.iconbitmap(icon)
    root.title("Thông báo")
    root.lift()
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    x = (screen_width - 300) // 2
    y = (screen_height - 150) // 2
    root.geometry("400x100+{}+{}".format(x, y))
    label = tk.Label(root, text=content, font=("Arial", 14))
    label.pack(pady=20)
    button = tk.Button(root, text="Đóng", command=root.destroy)
    button.pack()
def draw_circle(a, b, r):
    theta = np.linspace(0, 2*np.pi, 100)
    x_circle = r * np.cos(theta) + a
    y_circle = r * np.sin(theta) + b
    return x_circle, y_circle

def add_func(typ=1):
    global nor_funcs,cir_funcs,if_use_color
    if typ==1:
        if len(nor_funcs)+len(cir_funcs)<5:
            f=textinput("Normal function","Nhập hàm số f(x):(VD: x^3+2x+2)")
            if f!=None:
                nor_funcs.append(f)
                printc("y=",f,fon="Consolas",co=colo[len(nor_funcs)+len(cir_funcs)-1],pos=(80,(len(cir_funcs)+len(nor_funcs))*30+300),typ="bold")
        else:
            math_caution("Tối đa 5 phương trình!")
        return
    if typ==2:
        if len(nor_funcs)+len(cir_funcs)<5:
            f=textinput("Circle function","Nhập tọa độ tâm và bán kính,\nPhân tách bằng dấu phẩy (VD:2.5,2.5,3): ")
            if f!=None:
                try:
                    cir_funcs.append(draw_circle([int(x) for x in f.split(",")][0],[int(x) for x in f.split(",")][1],[int(x) for x in f.split(",")][2]))
                    printc("(x-",f.split(",")[0],")^2 + (y-",f.split(",")[1],")^2 =",f.split(",")[2],"^2",fon="Consolas",co=colo[len(nor_funcs)+len(cir_funcs)-1],pos=(80,(len(nor_funcs)+len(cir_funcs))*30+300),typ="bold")
                except:
                    printc("Error <xx00>",fon="Consolas",co=colo[len(nor_funcs)+len(cir_funcs)],pos=(80,(len(nor_funcs)+len(cir_funcs)+1)*30+300),typ="bold")
                    cir_funcs.append(None)
        else:
            math_caution("Tối đa 5 phương trình!")
        return

def plot_function(nor,cir,if_use_color):
    global colo,nor_funcs
    fig, ax = plt.subplots()
    cont=True
    for i in range(len(nor)):
        if cont!=True:
            break 
        x=np.linspace(-1000,1000,100000)
        try:
            y=eval(nor[i])
            if if_use_color:
                ax.plot(x, y, linewidth=2, color=colo[i])
            else:
                ax.plot(x, y, linewidth=2,color="black")
        except :
            math_caution("Lỗi phương trình, vui lòng kiểm tra!")
            cont=False
            
    for i in range(len(cir)):
        if cont!=True:
            break 
        if cir[i]!=None:
            if if_use_color:
                ax.plot(cir[i][0], cir[i][1], linewidth=2, color=colo[i+len(nor_funcs)])
            else:
                ax.plot(cir[i][0], cir[i][1], linewidth=2,color="black")
        else:
            math_caution("Lỗi phương trình, vui lòng kiểm tra!")
            cont=False
    ax.axhline(y=0, color='black', linewidth=1)
    ax.axvline(x=0, color='black', linewidth=1)
    ax.set_aspect('equal')
    ax.set_xlim(-10000000,10000000)
    ax.axis([-20, 20, -20, 20])
    ax.grid(which='both', linestyle=':', linewidth='0.5', color='gray')

    plt.xlabel('Hoành độ-X')
    plt.ylabel('Tung độ-Y')
    if nor_funcs!=[] and cir_funcs!=[]:
        plt.title("Đồ thị phương trình {} ".format("L&C type"))
    else:
        plt.title("Đồ thị phương trình {} ".format("L type"))
    plt.show()
def on_closing():
    plt.close("all") 
    Screen().bye()
colo=('#ff0000','#1e90ff','#ff99cc','#a0522d','#00ee00')
def draw_funcs():
    global if_use_color
    plot_function(math_convert(nor_funcs),cir_funcs,if_use_color.get())
def clear_all():
    global p,nor_funcs,cir_funcs
    p.clear()
    nor_funcs=[]
    cir_funcs=[]

button = tk.Button(Screen()._root, text="Thêm hàm số", command=add_func,height=2)
button.place(x=55,y=237)
button2 = tk.Button(Screen()._root, text="Vẽ hàm số", command=draw_funcs,height=2)
button2.place(x=350,y=431)
button3 = tk.Button(Screen()._root, text="Xóa tất cả", command=clear_all,height=2)
button3.place(x=138,y=237)
button4 = tk.Button(Screen()._root, text="PT đường tròn", command=lambda: add_func(typ=2),height=2)
button4.place(x=200,y=237)

if_use_color = tk.BooleanVar()
use_color = tk.Checkbutton(Screen()._root, text="Dùng nhiều màu sắc để phân biệt hàm số", variable=if_use_color)
use_color.place(x=82,y=437)
use_color.select()


Screen().getcanvas().master.protocol("WM_DELETE_WINDOW", on_closing)

mainloop()