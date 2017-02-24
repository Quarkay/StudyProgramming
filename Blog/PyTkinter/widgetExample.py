#coding: utf-8
#Date: 2016.03
#Author: PigKnife blog: https://www.mierhuo.com

from Tkinter import *

root = Tk()
root.title('觅而获')

t = Label(root, bg="blue", fg="white", text="www.mierhuo.com", width=40, height=2)
t.pack(fill='x')

p = PhotoImage(file="./baifeng.gif")
w = Label(root, image=p)
w.pack()

class Blink():

    flag = 1

    @staticmethod
    def changeColor():
        if Blink.flag:
            t.config(fg='red', bg='green')
            Blink.flag = 0
        else:
            t.config(fg="white", bg="blue")
            Blink.flag = 1

bt_blink = Button(root, text="Blink", fg="green", command=Blink.changeColor)
bt_blink.place(relx=0.7, rely=0.7)

bt_quit = Button(root, text="Quit", fg="red", command=root.quit)
bt_quit.pack()


root.mainloop()
