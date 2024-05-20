import datetime
import time
import chemparse
import periodictable
from turtle import *
import io
import builtins
import tkinter as tk
import pygame

pygame.init()

screen_info = pygame.display.Info()
screen_width, screen_height = screen_info.current_w, screen_info.current_h

setup(510,510,(screen_width-510)/2,(screen_height-510)/2)

screensize(500,500)
setworldcoordinates(0,500,500,0)
colormode(255)
Screen()._root.iconbitmap('icons/balancer_icon.ico')
title("The Balancer")

addshape("tools/resources/balancer_bg.gif")
addshape("tools/resources/instructions.gif")
t=Turtle()

t.ht()
t.speed(90)
t.pu()
t.goto(250,250)
t.shape("tools/resources/balancer_bg.gif")
t.stamp()
t.shape("tools/resources/instructions.gif")
t.goto(250,350)
idst=t.stamp()

def count_elements(element):
    items=chemparse.parse_formula(element)
    for key in chemparse.parse_formula(element).keys():
        items[key]=int(items[key])
    return items
def total(lst, materials, products):
    v={str(periodictable.elements[i]) : 0 for i in range(1,119)}
    
    tol_result={str(periodictable.elements[i]) : 0 for i in range(1,119)}
    for i in range(len(materials)):
        v=count_elements(materials[i])
        for key in v:
            v[key] = v[key] * lst[i]
        try:
            for key in v:
                tol_result[key] = tol_result[key] + v[key]
        except KeyError:
            return False
            
    v={str(periodictable.elements[i]) : 0 for i in range(1,119)}
    for i in range(len(products)):
        v=count_elements(products[i])
        for key in v:
            v[key] = v[key] * lst[len(materials)+i]
        try:
            for key in v:
                tol_result[key] = tol_result[key] - v[key]
        except KeyError:
            return False
        
    return tol_result

def equal(l,r):
    if l==False:
        return None  
    for key in l.keys():
        if l[key]!=r[key]:
            return False            
    return True
def ctime(t1,t2):
    t1=time.mktime(t1)
    t1=datetime.datetime.fromtimestamp(t1)
    t2=datetime.datetime.fromtimestamp(t2)
    return t2-t1
def openkey():
    with open("tools/resources/_key.txt","r") as file:
        return [str(x.strip()) for x in file.readlines()]
def filter_mat_pro(s):
    mid=s.index("-")
    mat=s[:mid].split(",")
    pro=s[mid+1:].split(",")
    return mat,pro
def openbalance():
    with open("tools/resources/_balanced.txt","r") as file:
        return [str(x.strip()) for x in file.readlines()]
def write_key_balance(mat,pro,balance):
    with open("_key.txt","a") as filey:
        print(file=filey)
        print(*mat,sep=",",end="",file=filey)
        print("-",end="",file=filey)
        print(*pro,sep=",",end="",file=filey)
    with open("_balanced.txt","a") as filez:
        print(*balance,sep=",",file=filez)
        
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

def caution(content,icon="appicon.ico"):
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
    if icon=="caution.ico":
        printc("Error <x00>",pos=(170,400),co="red",typ="bold",size=20)
def convert(lst,mat,pro):
    t=""
    for i in range(len(materials)):
        if i!=len(materials)-1:
            t=t+(str(lst[i])+materials[i]+" + ")
        else:
            t=t+str(lst[i])+materials[i]+" ==> "
    for i in range(len(products)):
        if i!=len(products)-1:
            t=t+str(lst[len(materials)+i])
            t=t+products[i]+" + "
        else:
            t=t+str(lst[len(materials)+i])
            t=t+products[i]
    return t

p=Turtle()
p.speed(90)
p.ht()

kq=openkey()
hs=openbalance()

materials,products=[],[]
initialized=True
materials,products,limit,count=None,None,25,0
timest,timeed=0,0
def goc(x,y):
    x=int(x)
    y=int(y)
    
    global  materials,products,kq,hs,initialized,timest,timeed,idst,limit
    if x in range(47,132) and y in range(229,254):
        try:
            materials = textinput("Trình cân bằng phản ứng hóa học","Nhập các chất đầu (phân tách bằng dấu phẩy): ").split(",")
        except AttributeError:
            pass
    if x in range(135,220) and y in range(229,254):
        try:
            products = textinput("Trình cân bằng phản ứng hóa học","Nhập các chất sản phẩm (phân tách bằng dấu phẩy): ").split(",")
        except AttributeError:
            pass
    if x in range(223,308) and y in range(229,254):
        try:
            limit=int(textinput("Trình cân bằng phản ứng hóa học","Gợi ý giá trị hệ số lớn nhất (càng nhỏ càng tốt, có thể bỏ qua): "))+1
            if limit>120: limit=25
        except ValueError:
            limit=25
        except TypeError:
            pass
        
    if x in range(310,396) and y in range(229,254):
        if (materials==None) or (products==None):
            if (materials==None) and (products==None): caution("Bạn chưa nhập chất đầu và sản phẩm!")
            elif materials==None: caution("Bạn chưa nhập chất đầu!")
            elif products==None: caution("Bạn chưa nhập sản phẩm!")
        else:
            count=0
            p.clear()
            t.clearstamp(idst)
            printc("Các chất tham gia: ",co=(238,99,99)	,se="",en="",pos=(70,280))
            printc(*materials,co=((64,224,208)),se=",",pos=(235,300),typ="bold")
            printc("Các chất sản phẩm: ",co=(238,99,99),se="",en="",pos=(70,300))
            printc(*products,co=((64,224,208)),se=",",pos=(235,320),typ="bold")
            printc("       Calculating       ",pos=(110,340),typ="underline")
            initialized=True
            count=0
            timest=time.localtime()

            l=[];r=[]
            for i in materials:
                d=count_elements(i)
                l.extend(list(d.keys()))
            for i in products:
                d=count_elements(i)
                r.extend(list(d.keys()))
            if set(l)==set(r):
                for react in kq:
                    if (set(materials)==set(filter_mat_pro(react)[0])) and (set(products)==set(filter_mat_pro(react)[1])):
                        lst=hs[kq.index(react)].split(",")
                        materials=filter_mat_pro(react)[0]
                        products=filter_mat_pro(react)[1]
                        printc("Hệ số cân bằng là",*lst,se=":",en="",pos=(70,350))
                        printc(convert(lst,materials,products),co=(28,134,238),fon="Patrick Hand",size=14,pos=(70,450))
                        
                        timeed=time.time()
                        printc("Started at: ",time.strftime("%H:%M:%S",timest),pos=(100,385),co=(0,128,128),typ="italic")
                        printc("Finished at: ",time.strftime("%H:%M:%S",time.localtime(timeed)),pos=(100,400),co=(137,104,205),typ="italic")
                        printc("Time: ",ctime(timest,timeed),pos=(100,415),co=(238,154,0),typ="italic")
                        initialized=False
            else:
                initialized=False
                caution("Error <x00>",icon="caution.ico")
            def all_cases(n, materials, products, lst=[]):
                global initialized, count, limit
                if len(lst) == n:
                    count+=1
                    if count>=(limit-1)**(len(materials)+len(products)):
                        printc("<Can't solve>",co="red",size=20,pos=(155,400),typ="bold")
                        initialized=False
                        return
                    if equal(total(lst, materials, products), {str(periodictable.elements[i]):0 for i in range(1,119)}):
                        printc("Hệ số cân bằng là",*lst,se=":",en="",pos=(70,350))
                        printc(convert(lst,materials,products),co=(28,134,238),fon="Patrick Hand",size=14,pos=(70,450))
                        printc("Started at: ",time.strftime("%H:%M:%S",timest),pos=(100,385),co=(0,128,128),typ="italic")
                        timeed=time.time()
                        printc("Finished at: ",time.strftime("%H:%M:%S",time.localtime(timeed)),pos=(100,400),co=(137,104,205),typ="italic")
                        printc("Time: ",ctime(timest,timeed),pos=(100,415),co=(238,154,0),typ="italic")
                        write_key_balance(materials,products,lst)
                        initialized=False
                        return
                    elif equal(total(lst, materials, products), {str(periodictable.elements[i]):0 for i in range(1,119)})==None:
                        initialized=False
                        caution("Error <x00>",icon="caution.ico")
                        return
                else:
                    if initialized:
                        for i in range(1, limit):
                            all_cases(n, materials, products, lst + [i])
            all_cases(len(materials)+len(products), materials, products)
            
onscreenclick(goc)
mainloop()
