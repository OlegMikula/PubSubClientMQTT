from tkinter import *
import paho.mqtt.client as mqtt
import asyncio
import time

window = Tk()
window.title("SmartHome")
window.geometry('480x320')
tempDef = 20
batteryStatus = ""
temperatureInRoom = 0
scaleData = 15
max = 2

def on_connect(client, userdata, flags, rc):
    print("Connected with result code {0}".format(str(rc)))
    client.subscribe("get/Temp")
    # client.subscribe("get/Status")

def on_message(client, userdata, msg):
    print("Message received-> " + msg.topic + " " + str(msg.payload))
    global scaleData
    if msg.topic == "get/Temp":
        lblTemp.configure(text = msg.payload)
        temp = str(msg.payload)
        temperatureInRoom = temp[3:8]
        print(temperatureInRoom)
        if scaleData - max >= float(temperatureInRoom):
            data = "on"
            sendData("set/Status", data)
        elif scaleData + max <= float(temperatureInRoom):
            data = "off"
            sendData("set/Status", data)

    if msg.topic == "get/Status":
        global batteryStatus
        batteryStatus = msg.payload

async def getData():
    client = mqtt.Client("digi_mqtt_test")
    client.username_pw_set(username="username", password="password")
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect('192.168.1.103', 1883)
    client.loop_start()

def sendData(topic, data):
    clientSend = mqtt.Client("set/Temperature")
    clientSend.username_pw_set(username="username", password="password")
    clientSend.connect('192.168.1.103', 1883)
    time.sleep(1)
    if topic == "set/Temp":
        clientSend.publish(topic="set/Temp", payload=data)
        clientSend.disconnect()
    elif topic == "set/Status":
        clientSend.publish(topic="set/Status", payload=data)
        clientSend.disconnect()


def sel():
    global selection
    global scaleData
    scaleData = int(var.get())
    lblNameSetTempLbl.configure(text = scaleData)
    radioData = var2.get()
    selection = str(scaleData) + "   " + str(radioData)
    sendData("set/Temp", selection)


switchMode1 = Button(window, text="Set Scale Value", background="#555", foreground="#ccc",
              padx="5", pady="5", font="Arial 18",command = sel)
switchMode1.place(x = 165, y = 220)

lblTemp = Label(window, font="Arial 20", text = tempDef)
lblTemp.place(x = 210, y = 130)

lblNameCurTemp = Label(window, font="Arial 20", text = "Current: ")
lblNameCurTemp.place(x = 120, y = 130)


lblNameSetTemp = Label(window, font="Arial 20", text = "Set: ")
lblNameSetTemp.place(x = 140, y = 90)

lblNameSetTempLbl = Label(window, font="Arial 20", text = scaleData)
lblNameSetTempLbl.place(x = 210, y = 90)

var2 = IntVar()
R1 = Radiobutton(window, text="Manual", variable=var2, value=1)
R1.place(x = 140, y = 50)
R2 = Radiobutton(window, text="Auto", variable=var2, value=2)
R2.place(x = 240, y = 50)

var = DoubleVar()
scale = Scale( window, variable = var,length = 300, orient = HORIZONTAL, resolution=0.5, from_ = 15, to = 40)
scale.place(x = 90, y = 180)



loop = asyncio.get_event_loop()
loop.run_until_complete(getData())
R1.select()
loop.close()
window.mainloop()
