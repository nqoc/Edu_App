import H3D
import time
from turtle import*
import pygame
import psutil
import tkinter as tk
import subprocess
import os

pygame.init()

screen_info = pygame.display.Info()
screen_width, screen_height = screen_info.current_w, screen_info.current_h

H3D.main()
time.sleep(1)

setup(500,500,(screen_width-510)/2,(screen_height-510)/2)
screensize(500,500)
setworldcoordinates(0,500,500,0)
colormode(255)
Screen()._root.iconbitmap('appicon.ico')
title("EQN+")


addshape("mainbg.gif")
addshape("mainbg2.gif")
addshape("control.gif")
addshape("ce.gif")
t=Turtle()
t.speed(90)
t.ht()
t.pu()
p=t.clone()
t.shape("mainbg.gif")
t.goto(250,250)
t.stamp()

myapp=["Function","Balancer","Atom"]
button=[]
ok=False
def printc(*args,co="black",se=" ",en="\n",pos=(0,0),fon="Consolas",typ="normal",size=12):
    global p
    tracer(0)
    p.color(co)
    p.pu()
    p.goto(pos)
    p.pd()
    p.seth(0)
    p.write(*args,font=(fon,size, typ))
    update()
def printc2(pos):
    h=Turtle()
    h.speed(90)
    h.ht()
    h.pu()
    h.shape("ce.gif")
    h.goto(pos)
    h.stamp()
    del(h)
def check_status():
    status={"Function":"Power off","Balancer":"Power off","Atom":"Power off"}
    for proc in psutil.process_iter():
        try:
            name = proc.name()
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
        else:
            if name in [x+".exe" for x in myapp]:
                status[name[:-4:]]="Running"
    return status
def print_status():
    global myapp
    cs=check_status()
    for i in range(len(myapp)):
        printc(myapp[i],co=(160,82,45),typ="bold",pos=(50,30*i+220))
        if cs[myapp[i]]=="Running":
            printc2((313,30*i+216))
            printc("Running",co=((0,255,0)),typ="bold",pos=(271,30*i+220))
        elif cs[myapp[i]]=="Power off":
            printc2((313,30*i+216))
            printc("Power off",co=((255,0,0)),typ="bold",pos=(271,30*i+220))
def run_func():
    path_to_exe = r'cd {}'.format(os.getcwd())
    subprocess.run(path_to_exe, shell=True)
    subprocess.Popen(['Function.exe'])
    print_status()
def run_baln():
    path_to_exe = r'cd {}'.format(os.getcwd())
    subprocess.run(path_to_exe, shell=True)
    subprocess.Popen(['Balancer.exe'])
def run_atom():
    path_to_exe = r'cd {}'.format(os.getcwd())
    subprocess.run(path_to_exe, shell=True)
    subprocess.Popen(['Atom.exe'])
def clk(x,y):
    global ok,t
    x,y=int(x),int(y)
    print_status()
    if (x in range(205,319)) and (y in range(205,310)) and (ok==False):
        t.pu()
        t.shape("mainbg2.gif")
        t.goto(250,250)
        t.stamp()
        time.sleep(0.5)
        t.shape("mainbg.gif")
        t.goto(250,250)
        t.stamp()
        ok=True
        time.sleep(0.3)
        t.clear()
        t.shape("control.gif")
        t.goto(250,250)
        t.stamp()
        del(t)
        print_status()
        button_func= tk.Button(Screen()._root, text="Chạy", command=run_func,height=1)
        button_func.place(x=400,y=30*0+200)
        
        button_baln= tk.Button(Screen()._root, text="Chạy", command=run_baln,height=1)
        button_baln.place(x=400,y=30*1+200)
        
        button_atom= tk.Button(Screen()._root, text="Chạy", command=run_atom,height=1)
        button_atom.place(x=400,y=30*2+200)

onscreenclick(clk)

mainloop()