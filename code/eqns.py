import webbrowser
import qrcode
from PIL import ImageTk
import tkinter as tk
from tkinter import ttk
import ctypes


user32 = ctypes.windll.user32
screen_width,screen_height = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
run = True
def op():
    webbrowser.open('https://h-designerit-miapp-hpt-4w0uh7.streamlit.app/')
        
root = tk.Tk()

root.geometry(f'259x280+{(screen_width-259)//2}+{(screen_height-279)//2}')
root.iconbitmap('icons/icon.ico')
root.title('Scan to open')
root.configure(background='#26A69A')

img = qrcode.make('https://h-designerit-miapp-hpt-4w0uh7.streamlit.app/').resize((250,250))
imgtk = ImageTk.PhotoImage(img)

tk.Label(root,width=250,height=250,image=imgtk).place(x=3,y=3)
ttk.Button(root,text='Follow link',command=op).place(x=100,y=255)
root.mainloop()