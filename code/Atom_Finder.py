from turtle import*
import pygame
import periodictable
import re
import tkinter as tk
import io
import builtins
from plyer import notification

pygame.init()

screen_info = pygame.display.Info()
screen_width, screen_height = screen_info.current_w, screen_info.current_h

setup(510,510,(screen_width-510)/2,(screen_height-510)/2)
screensize(500,500)
setworldcoordinates(0,500,500,0)
colormode(255)
Screen()._root.iconbitmap('icons/atom_icon.ico')
title("Atom Finder")

addshape("tools/resources/atom_bg.gif")
t=Turtle()
t.ht()
t.pu()
t.speed(90)
p=t.clone()
t.goto(250,250)
t.shape("tools/resources/atom_bg.gif")
t.stamp()

elements = {
    'H': [1],
    'He': [3, 4],
    'Li': [6, 7],
    'Be': [7, 9],
    'B': [10, 11],
    'C': [11, 12, 13, 14],
    'N': [13, 14, 15],
    'O': [15, 16, 17, 18],
    'F': [18, 19],
    'Ne': [20, 21, 22, 23, 24, 25, 26, 27],
    'Na': [22, 23, 24, 25, 26],
    'Mg': [23, 24, 25, 26, 27, 28, 29, 30],
    'Al': [26, 27, 28, 29, 30, 31],
    'Si': [27, 28, 29, 30, 31, 32, 33, 34],
    'P': [30, 31, 32, 33, 34, 35, 36],
    'S': [31, 32, 33, 34, 35, 36, 37, 38],
    'Cl': [34, 35, 36, 37, 38, 39, 40],
    'Ar': [36, 37, 38, 39, 40, 41, 42, 43, 44, 45],
    'K': [39, 40, 41, 42, 43, 44, 45, 46, 47],
    'Ca': [40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51],
    'Sc': [44, 45, 46, 47, 48, 49, 50, 51, 52, 53],
    'Ti': [45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56],
    'V': [48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58],
    'Cr': [49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60],
    'Mn': [51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61],
    'Fe': [52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64],
    'Co': [56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66],
    'Ni': [58, 60, 61, 62, 64],
    'Cu': [63, 64],
    'Zn': [64, 66, 67, 68, 70],
    'Ga': [69, 71],
    'Ge': [70, 72, 73, 74, 76],
    'As': [75, 77],
    'Se': [74, 76, 77, 78, 80, 82],
    'Br': [79, 81],
    'Kr': [78, 80, 82, 83, 84, 86],
    'Rb': [85, 87],
    'Sr': [84, 86, 87, 88],
    'Y': [89],
    'Zr': [90, 91, 92, 94, 96],
    'Nb': [93],
    'Mo': [92, 94, 95, 96, 97, 98, 100],
    'Tc': [98],
    'Ru': [96, 98, 99, 100, 101, 102, 104],
    'Rh': [103],
    'Pd': [102, 104, 105, 106, 108, 110],
    'Ag': [107, 109],
    'Cd': [106, 108, 110, 111, 112, 113, 114, 116],
    'In': [113, 115],
    'Sn': [112, 114, 115, 116, 117, 118, 119, 120, 122, 124],
    'Sb': [121, 123],
    'Te': [120, 122, 123, 124, 125, 126, 128, 130],
    'I': [127],
    'Xe': [124, 126, 128, 129, 130, 131, 132, 134, 136],
    'Cs': [133],
    'Ba': [130, 132, 134, 135, 136, 137, 138],
    'La': [138, 139],
    'Ce': [136, 138, 140, 142],
    'Pr': [141],
    'Nd': [142, 143, 144, 145, 146, 148, 150],
    'Pm': [145],
    'Sm': [144, 147, 148, 149, 150, 152, 154],
    'Eu': [151, 153],
    'Gd': [152, 154, 155, 156, 157, 158, 160],
    'Tb': [159],
    'Dy': [156, 158, 160, 161, 162, 163, 164],
    'Ho': [165],
    'Er': [162, 164, 166, 167, 168, 170],
    'Tm': [169],
    'Yb': [168, 170, 171, 172, 173, 174, 176],
    'Lu': [175, 176],
    'Hf': [168, 170, 171, 172, 173, 174],
    'Ta': [177, 178],
    'W': [180, 182, 183, 184, 186],
    'Re': [185, 187],
    'Os': [184, 186, 187, 188, 189, 190, 192],
    'Ir': [191, 193],
    'Pt': [190, 192, 194, 195, 196, 198],
    'Au': [197],
    'Hg': [196, 198, 199, 200, 201, 202, 204],
    'Tl': [176, 177, 178, 179, 180, 181, 182, 183, 184, 185, 186, 187, 188, 189, 190, 191, 192],
    'Pb': [204, 206, 207, 208],
    'Bi': [209],
    'Po': [209, 210, 211, 212, 213, 214, 215, 216, 218, 219, 220],
    'At': [210, 211, 212, 213, 214, 215, 216, 217, 218, 219, 220, 222],
    'Rn': [211, 220, 222, 224, 226, 228],
    'Fr': [223],
    'Ra': [223, 224, 225, 226, 228, 229, 230, 231],
    'Ac': [227, 228, 229, 230, 231, 232, 233, 234],
    'Th': [232],
    'Pa': [231],
    'U': [233, 234, 235, 238],
    'Np': [237],
    'Pu': [244, 246, 247, 248, 249, 250, 252],
    'Am': [243, 244, 245, 246, 247, 248, 249, 250, 252],
    'Cm': [247, 248, 249, 250, 251, 252, 253, 254],
    'Bk': [247, 249, 250, 251, 252, 253, 254],
    'Cf': [251, 252, 253, 254, 255, 256],
    'Es': [252, 253, 254, 255, 256, 257, 258],
    'Fm': [253, 254, 255, 256, 257, 258, 259, 260],
    'Md': [256, 257, 258, 259, 260, 261, 262],
    'No': [259, 260, 261, 262, 263, 264, 265, 266],
    'Lr': [262, 263, 264, 265, 266, 267, 268, 269, 270]
}

symbols={"<a>":"\u03B1", "<b+>":"\u03B2+", "<b->":"\u03B2-", "<g>":"\u03B3","<p>":"p","<n>":"n"}
special_atom={"<a>":[4,2],"<b+>":[0,1],"<b->":[0,-1],"<g>":[0,0],"<p>":[1,1],"<n>":[1,0]}
show=True

def _notification(title,message,app_name,app_icon):
    notification.notify(
        title=title,
        message=message,
        app_name=app_name,
        app_icon=app_icon,
        timeout=5)
def caution(content,icon="caution.ico"):
    _notification("Thông báo",content,"Atom Finder",'atom_icon.ico')
    root = tk.Tk()
    root.iconbitmap(icon)
    root.title("Thông báo")
    root.lift()
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    x = (screen_width - 300) // 2
    y = (screen_height - 150) // 2
    root.geometry("420x100+{}+{}".format(x, y))
    label = tk.Label(root, text=content, font=("Arial", 14))
    label.pack(pady=20)
    button = tk.Button(root, text="Đóng", command=root.destroy)
    button.pack()
def print_out(*args, s=' ', e='\n', file=None):
        if file is None:
            file = io.StringIO()
        builtins.print(*args, sep=s, end=e, file=file)
        file.seek(0)
        output = file.read()
        file.seek(0)
        file.truncate(0)
        return output
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

def instruction():
    def rdestroy():
        nonlocal root2
        global show
        root2.destroy()
        show=True
    global symbols,show
    content="\nHạt Alpha ({}): <a>\nHạt Beta âm ({}): <b->\nHạt Beta dương ({}):<b+>\nHạt Gamma ({}):<g>\nHạt Neutron ({}):<n>".format(symbols["<a>"],symbols["<b->"],symbols["<b+>"],symbols["<g>"],symbols["<n>"])
    root2=tk.Tk()
    root2.iconbitmap("atom_icon.ico")
    root2.title("Hướng dẫn nhập các hạt đặt biệt")
    root2.lift()
    screen_width = Screen()._root.winfo_screenwidth()
    screen_height = Screen()._root.winfo_screenheight()

    x = (screen_width - 300) // 2+400
    y = (screen_height - 150) // 2-180
    root2.geometry("400x200+{}+{}".format(x, y))
    label = tk.Label(root2, text=content, font=("Arial", 14),anchor="w")
    label.pack(pady=20)
    button = tk.Button(root2, text="Đóng", command=rdestroy)
    button.pack()
    show=False
def key_pos(key):
    global elements
    if key in elements:
        pos = list(elements.keys()).index(key)
        return pos+1
    else:
        return False
def value_pos(dictionary, value):
    for i, v in enumerate(dictionary.values()):
        if v == value:
            return i
    return False 
def spl(s):
    global special_atom
    if s in special_atom.keys():
        return special_atom[s]
    else:
        match = re.match(r'(\d+)([A-Za-z]+)', s)
        if match:
            number = int(match.group(1))
            letter = match.group(2)
            if letter not in elements.keys():
                return "Không có nguyên tố {}".format(letter)
            if number in elements[letter]:
                return [number,letter]
            else:
                return "Không có đồng vị {} của {}!".format(number,str(periodictable.elements.symbol(letter).name).title())
        else:
            return "Nguyên tố không đúng biểu thức chính quy!"
def check_result(result):
    for i in range(len(result)):
        if type(result[i])==type("a"):
            return result[i]
    return True
def check_radiation(list_element):
    if (len(list_element)==1) and (pos_x=="right"):
        for i in range(len(list_element)):
            try:
                if key_pos(list_element[i][1])>82:
                    return True
            except IndexError:
                pass
        return False
    elif (len(list_element)>1) or ((len(list_element)==1) and (pos_x=="left")) :
        return True

def check(lst):
    result=[]
    atom=[]
    
    for i in range(len(lst)):
        result.append(spl(lst[i]))
    if check_result(result)==True:
        return result
    else:
        return check_result(result)

def print_key(dictionary, n):
    keys = list(dictionary.keys())
    if n < 0 or n >= len(keys):
        return False
    else:
        return keys[n]

def find_atom(atom_left,atom_right,pos_x):
    global special_atom
    
    total_proton_left=0
    total_proton_right=0
    total_mass_left=0
    total_mass_right=0
    
    find_Z=0
    find_A=0
    
    for i in range(len(atom_left)):
        if type(atom_left[i][1])==type(""):
            total_proton_left=total_proton_left+key_pos(atom_left[i][1])
        elif type(atom_left[i][1])==type(0):
            total_proton_left=total_proton_left+atom_left[i][1]
    for i in range(len(atom_right)):
        if type(atom_right[i][1])==type(""):
            total_proton_right=total_proton_right+key_pos(atom_right[i][1])
        elif type(atom_right[i][1])==type(0):
            total_proton_right=total_proton_right+atom_right[i][1]
            
            
    for i in range(len(atom_left)):
        total_mass_left=total_mass_left+atom_left[i][0]
    for i in range(len(atom_right)):
        total_mass_right=total_mass_right+atom_right[i][0]
    print("Total proton: left",total_proton_left,"right",total_proton_right)
    print("Total mass: left",total_mass_left,"right",total_mass_right)
    if pos_x=="left":
        find_Z=total_proton_right-total_proton_left
        find_A=total_mass_right-total_mass_left
    if pos_x=="right":
        find_Z=total_proton_left-total_proton_right
        find_A=total_mass_left-total_mass_right
    print("Z",find_Z)
    print("A",find_A)
    if value_pos(special_atom,[find_A,find_Z])!=False:
        return [str(print_key(special_atom,value_pos(special_atom,[find_A,find_Z])))]
    else:
        try:
            if find_A in elements[print_key(elements,find_Z-1)]:
                return [str(find_A)+str(print_key(elements,find_Z-1))]
        except:
            return False

def reload(b):
    global atom_left,atom_right,pos_x,p
    if b==1:
        atom_left=[]
        atom_right=[]
        pos_x=None
    p.clear()
def rpl(s):
    global symbols
    for i in symbols.keys():
        if i in s:
            s=s.replace(i,symbols[i])
    return s
def convert(s):
    k=[]
    for i in range(len(s)):
        k.append(rpl(s[i]))
    return k
    
button3 = tk.Button(Screen()._root, text="Làm mới", command=lambda : reload(1),height=1,bg="Wheat")
button3.place(x=360,y=440)
atom_left=[]
atom_right=[]
pos_x=None
def clk(x,y):
    def close_lwindow():
        global pos_x
        nonlocal scr
        pos_x="left"
        scr.destroy()
    def close_rwindow():
        global pos_x
        nonlocal scr
        pos_x="right"
        scr.destroy()
    global show,pos_x,atom_left,atom_right
    x,y=int(x),int(y)
    if (x in range(50,250)) and (y in range(229,270)):
        if show==True:
            instruction()
        atom_left=textinput("Atom Finder","Nhập chất đầu\nNhập số khối trước, kí hiệu sau (VD: 238U)")
        if (atom_left==None) or (atom_left==""):
            atom_left=[]
        else:
            atom_left=atom_left.split(",")
    if (x in range(250,450)) and (y in range(229,270)):
        if show==True:
            instruction()
        atom_right=textinput("Atom Finder","Nhập chất sản phẩm\nNhập số khối trước, kí hiệu sau (VD: 95Mo):")
        if (atom_right==None) or (atom_right==""):
            atom_right=[]
        else:
            atom_right=atom_right.split(",")
    if (x in range(50,250)) and (y in range(270,322)):
        scr=tk.Tk()
        screen_width = Screen()._root.winfo_screenwidth()
        screen_height = Screen()._root.winfo_screenheight()

        x = (screen_width - 300) // 2
        y = (screen_height - 150) // 2
        scr.geometry("300x100+{}+{}".format(x, y))
        scr.title("Chọn vị trí chất cần tìm")
        button1 = tk.Button(scr, text="Vế trái ", command=close_lwindow,width=10,height=3,bg="PowderBlue")
        button1.place(x=20,y=20)
        button2 = tk.Button(scr, text="Vế phải", command=close_rwindow,width=10,height=3,bg="PeachPuff1")
        button2.place(x=200,y=20)
        
    if (x in range(250,450)) and (y in range(270,322)):
        if (pos_x==None):
            caution("Hãy chọn vị trí chất cần tìm")
        elif (atom_left!=[]) and (atom_right!=[]):
            if (len(atom_left)==1) and (pos_x=="right") and (check_radiation(atom_left)==False):
                caution("Nhập sai nguyên tố hoặc quy tắc!")
            else:
                reload(2)
                printc("Các chất đầu đã nhập:",co=(255,0,0),fon="Consolas",typ="bold",pos=(70,380))
                printc(*convert(atom_left),se=",",co="SaddleBrown",typ="italic",pos=(280,380))
                
                printc("Các chất sản phẩm đã nhập:",co=(0,0,255),fon="Consolas",typ="bold",pos=(70,400))
                printc(*convert(atom_right),se=",",co="SaddleBrown",typ="italic",pos=(320,400))
                printc("-"*40,co="Sienna",pos=(70,420))
                cont=True
                if type(check(atom_left))==type(""):
                    caution(check(atom_left))
                    cont=False 
                elif type(check(atom_right))==type(""):
                    caution(check(atom_right))
                    cont=False
                if cont:
                    kq=find_atom(check(atom_left),check(atom_right),pos_x)
                    if kq==False:
                        caution("Lỗi phương trình!")
                    else:
                        if pos_x=="left":
                            on_left=kq
                            on_right=""
                        else:
                            on_left=""
                            on_right=kq
                        react=print_out(*convert(atom_left),*convert(on_left),s="+",e="=>")
                        react=react+print_out(*convert(atom_right)+convert(on_right),s="+")
                        printc(react,co="SteelBlue1",typ="bold",pos=(70,480),size=15)
                        
        elif (atom_left==[]) and (atom_right==[]):
            caution("Hãy nhập các chất vào!")
onscreenclick(clk)
mainloop()