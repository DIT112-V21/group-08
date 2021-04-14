from tkinter import *
from tkinter import ttk
from PIL import Image , ImageTk
from tkinter import messagebox
import paho.mqtt.client as mqtt

#MQTT Stuff
broker_address = "localhost"
manualClient = mqtt.Client("Manual-Control")
manualClient.connect(broker_address)
manualClient.subscribe("smartcar")

def publish(a):
    print(manualClient.publish("smartcar", a))

#Tkinter Stuff
mainpage = Tk()
mainpage.title("Pathfinder")
# Adjust size
mainpage.geometry('800x700')
mainpage.iconbitmap("images\car.ico")

backGround_img = ImageTk.PhotoImage(Image.open("images\star.png"))
label_img = Label(image=backGround_img)
label_img.pack()

#bg = PhotoImage(file=r'C:\Users\Admin\Downloads\wallpaper.png')
#my_canvas = Canvas(mainpage, width=800, height=700)
#my_canvas.pack(fill="both", expand=True)
#my_canvas.create_image(0,0,image=bg,anchor="nw")


# Adding buttons
btnB = Button(mainpage,text="Backward",width=15,height=3,fg="blue", command=lambda: publish("b"))
btnB.place(x=300, y=300)


btnF = Button(mainpage,text="Forward",width=15,height=3,fg="blue", command=lambda: publish("f"))
btnF.place(x=300, y=100)


btnL = Button(mainpage, text="Left",width=15,height=3,fg="blue", command=lambda: publish("l"))
btnL.place(x=150, y=200)


btnR = Button(mainpage,text="Right",width=15,height=3,fg="blue", command=lambda: publish("r"))
btnR.place(x=450, y=200)


btnBrakes = Button(mainpage,text="Brakes", width=15,height=3,fg="black",bg="darkred", command=lambda: publish("stop"))
btnBrakes.place(x=50, y=350)


btnA = Button(mainpage, text="Accelerate", width=15,height=3,fg="black",bg="darkgreen", command=lambda: publish("e"))
btnA.place(x=575, y=350)

btnMap = Button(mainpage, text="Map", width=15,height=3,fg="brown",bg="white")
btnMap.place(x=20, y=80)

btnDecelerate = Button(mainpage, text="Decelerate", width=15,height=3,fg="black",bg="yellow", command=lambda: publish("q"))
btnDecelerate.place(x=300, y=400)


def clicked():
    messagebox.showinfo('Help', 'Instructions on How to use PathFinder')

btnHelp = Button(mainpage, text="Help&Info", width=15,height=3,fg="black",bg="pink",command=clicked)
btnHelp.place(x=650, y=20)


btnHelp = Button(mainpage, text="Help&Info", width=15,height=3,fg="black",bg="pink", command=clicked)
btnHelp.place(x=650, y=20)


btnQuit = Button(mainpage,text="Exit",width=15,height=2,fg="red",command=mainpage.quit)
btnQuit.place(x=600, y=600)


def second_win():
    mainpage2=Tk()
    mainpage2.title("Voice-Control")
    mainpage2.geometry('800x700')
    btnVoice = Button(mainpage2, text="Hold To Command", width=20, height=3, fg="black",bg="blue")
    btnVoice.place(x=300, y=300)
    btnHelp = Button(mainpage2, text="Help&Info", width=15, height=3, fg="black", bg="yellow", command=clicked)
    btnHelp.place(x=650, y=20)
    btnQuit = Button(mainpage2,text="Exit",width=15,height=2,fg="red",command=mainpage.quit)
    btnQuit.place(x=600, y=600)

    backGround_img2 = ImageTk.PhotoImage(Image.open(r'C:\Users\Admin\Downloads\forest.png'))
    label_img2 = Label(mainpage2, image=backGround_img2)
    label_img2.pack()

btnNext= Button(mainpage,text="Voice-Control",width=20,height=3,fg="red",command=second_win)
btnNext.place(x=50, y=600)


lblM = Label(mainpage, text='Welcome to PathFinder Smart Car',fg="black",bg="blue",font="TimesNewRoman")
lblM.place(x=20,y=20)


mainpage.mainloop()