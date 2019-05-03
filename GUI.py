from tkinter import *
import paho.mqtt.client as mqtt
import asyncio

window = Tk()

window.title("SmartHome")

window.geometry('480x320')

tempDef = 20

def on_connect(client, userdata, flags, rc):
    print("Connected with result code {0}".format(str(rc)))
    client.subscribe("get/Temp")

def on_message(client, userdata, msg):
    print("Message received-> " + msg.topic + " " + str(msg.payload))
    lblTemp.configure(text = msg.payload)

async def getdata():
    client = mqtt.Client("digi_mqtt_test")
    client.username_pw_set(username="username", password="password")
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect('192.168.1.103', 1883)
    client.loop_start()

def senddata(data):
    clientSend = mqtt.Client("Python")
    clientSend.username_pw_set(username="username", password="password")
    clientSend.connect('192.168.1.103', 1883)
    clientSend.publish(topic="set/Temp", payload=data)
    clientSend.disconnect()

def sel():
    global selection
    scaleData = str(var.get())
    radioData = var2.get()
    selection = scaleData + "   " + str(radioData)
    senddata(selection)


switchMode1 = Button(window, text="Set Scale Value", background="#555", foreground="#ccc",
              padx="5", pady="5", font="Arial 18",command = sel)
switchMode1.place(x = 165, y = 220)

lblTemp = Label(window, font="Arial 25", text = tempDef)
lblTemp.place(x = 210, y = 130)


var2 = IntVar()
R1 = Radiobutton(window, text="Default", variable=var2, value=1)
R1.place(x = 140, y = 50)
R2 = Radiobutton(window, text="Night", variable=var2, value=2)
R2.place(x = 240, y = 50)

var = DoubleVar()
scale = Scale( window, variable = var,length = 300, orient = HORIZONTAL, resolution=0.5, from_ = 15, to = 40)
scale.place(x = 90, y = 180)

loop = asyncio.get_event_loop()
loop.run_until_complete(getdata())
R1.select()
loop.close()
window.mainloop()
