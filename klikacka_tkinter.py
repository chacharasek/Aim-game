import random
from tkinter import *
import math
import time
root = Tk()
root.geometry('700x500')

canvas = Canvas(root, width=700, height = 500, bg='white')
canvas.pack()
canvas.create_line(530,0,530,500,fill='blue', width = 5)

colors = ['red' , 'orange' , 'yellow']
count = [1, 2]
body = 0



def score():
    global body
    body = body + 1

def buttons():
    x1 = random.randint(1, 470)
    y1 = random.randint(1, 470)
    c = Button(root ,  background = "blue", activebackground = "blue", width=3,command=lambda:[score(), buttons(), c.destroy()])
    c.pack()
    c.place(x=x1,y=y1)
    canvas.create_rectangle(541,20,700,200,fill='white',outline='white')
    canvas.create_text(600, 40, text='body = '+ str(body))

def b():

    x2 = random.randint(1, 470)
    y2 = random.randint(1, 470)

    b = Button(root ,  background = "red", activebackground = "red", width=3,command=lambda:[score(), buttons(), b.destroy()])
    b.pack()
    b.place(x=x2,y=y2)

b()



root.mainloop()