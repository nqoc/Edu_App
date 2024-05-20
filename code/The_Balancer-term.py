import datetime
import time
import chemparse
import periodictable
from colorama import Fore, Back, Style,init

#init(convert=True)

def count_elements(element):
    items=chemparse.parse_formula(element)
    for key in chemparse.parse_formula(element).keys():
        items[key]=int(items[key])
    return items
def total(lst, materials, products):
    x={str(periodictable.elements[i]) : 0 for i in range(1,119)}
    
    for i in range(len(materials)):
        v=count_elements("(" + materials[i] + ")" + str(lst[i]))
        for j in v.keys():
            try:
                x[j] += v[j]
            except KeyError:
                return False 
    for i in range(len(products)):
        v=count_elements("(" + products[i] + ")" + str(lst[len(materials)+i]))
        for j in v.keys():
            x[j] -= v[j]           
    return x

def equal(l,r):
    if l==False:
        return None  
    for key in l.keys():
        if l[key]!=r[key]:
            return False            
    return True
def printc(content,co,se=" ",en="\n"):
    if co=="g":
        print(Fore.GREEN + content + Style.RESET_ALL,sep=se,end=en)
    if co=="b":
        print(Fore.BLUE + content + Style.RESET_ALL,sep=se,end=en)
    if co=="c":
        print(Fore.CYAN+ content + Style.RESET_ALL,sep=se,end=en)
    if co=="r":
        print(Fore.RED+ content + Style.RESET_ALL,sep=se,end=en)
    if co=="y":
        print(Fore.YELLOW+ content + Style.RESET_ALL,sep=se,end=en)
    if co=="m":
        print(Fore.MAGENTA+ content + Style.RESET_ALL,sep=se,end=en)
def ctime(t1,t2):
    t1=time.mktime(t1)
    t2=time.mktime(t2)

    t1=datetime.datetime.fromtimestamp(t1)
    t2=datetime.datetime.fromtimestamp(t2)
    return t2-t1
def openkey():
    with open("_key.txt","r") as file:
        return [str(x.strip()) for x in file.readlines()]
def filter_mat_pro(s):
    mid=s.index("-")
    mat=s[:mid].split(",")
    pro=s[mid+1:].split(",")
    return mat,pro
def openbalance():
    with open("_balanced.txt","r") as file:
        return [str(x.strip()) for x in file.readlines()]
def write_key_balance(mat,pro,balance):
    with open("_key.txt","a") as filey:
        print(file=filey)
        print(*mat,sep=",",end="",file=filey)
        print("-",end="",file=filey)
        print(*pro,sep=",",end="",file=filey)
    with open("_balanced.txt","a") as filez:
        print(*balance,sep=",",file=filez)
        
        
while True:
    print(25*"-",sep="",end="")
    print(Fore.MAGENTA+Style.BRIGHT+ "TRÌNH CÂN BẰNG PHẢN ỨNG HÓA HỌC"+ Style.RESET_ALL,end="")
    print(25*"-",sep="",end="")
    print()
    kq=openkey()
    hs=openbalance()
    materials = input("Nhập các chất đầu (phân tách bằng dấu phẩy): ").split(",")
    products = input("Nhập các chất sản phẩm (phân tách bằng dấu phẩy): ").split(",")

    try:
        limit= int(input("Gợi ý giá trị hệ số lớn nhất (càng nhỏ càng tốt, có thể bỏ qua): "))
        if limit>120: limit=25
    except ValueError:
        print("--Mặc định: 25--")
        limit=25
    printc("Các chất tham gia: ","b",se="",en="");print(*materials,sep=",")
    printc("Các chất sản phẩm: ","b",se="",en="");print(*products,sep=",")
    print(20*"-",sep="")
    printc("Calculating...","y")
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
                printc("Hệ số cân bằng là: ","r",en="")
                print(*lst,sep=":")
                for i in range(len(materials)):
                    if i!=len(materials)-1:
                        printc(str(lst[i]),"g",se="",en="")
                        print(materials[i],end=" + ")
                    else:
                        printc(str(lst[i]),"g",se="",en="")
                        print(materials[i],sep="",end=" ==> ")
                for i in range(len(products)):
                    if i!=len(products)-1:
                        printc(str(lst[len(materials)+i]),"g",se="",en="")
                        print(products[i],sep="",end=" + ")
                    else:
                        printc(str(lst[len(materials)+i]),"g",se="",en="")
                        print(products[i],sep="")         
                initialized=False
    else:
        initialized=False
        for i in range(1,13):
            printc("Error <x00>","r")
    def all_cases(n, materials, products, lst=[]):
        global initialized, count, limit
        if len(lst) == n:
            count+=1
            if count>limit**(len(materials)+len(products)):
                print("Can't solve")
                initialized=False
                return
            if equal(total(lst, materials, products), {str(periodictable.elements[i]):0 for i in range(1,119)}):
                printc("Hệ số cân bằng là: ","r",en="");print(*lst,sep=":")
                for i in range(len(materials)):
                    if i!=len(materials)-1:
                        printc(str(lst[i]),"g",se="",en="")
                        print(materials[i],end=" + ")
                    else:
                        printc(str(lst[i]),"g",se="",en="")
                        print(materials[i],sep="",end=" ==> ")
                for i in range(len(products)):
                    if i!=len(products)-1:
                        printc(str(lst[len(materials)+i]),"g",se="",en="")
                        print(products[i],sep="",end=" + ")
                    else:
                        printc(str(lst[len(materials)+i]),"g",se="",en="")
                        print(products[i],sep="",end="")
                write_key_balance(materials,products,lst)
                initialized=False
                print()
                return
            elif equal(total(lst, materials, products), {str(periodictable.elements[i]):0 for i in range(1,119)})==None:
                initialized=False
                printc("Error <x00>","r")
                return
        else:
            if initialized:
                for i in range(1, limit):
                    all_cases(n, materials, products, lst + [i])
    all_cases(len(materials)+len(products), materials, products)
    timeed=time.localtime()
    print("Started at: ",time.strftime("%H:%M:%S",timest))
    print("Finished at: ",time.strftime("%H:%M:%S",timeed))
    print(ctime(timest,timeed))