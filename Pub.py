import paho.mqtt.client as mqtt

broker_address = "192.168.0.103"
broker_portno = 1883

client = mqtt.Client("Python")
client.username_pw_set(username="username", password="password")
client.connect(broker_address, broker_portno)
client.publish(topic = "set/Temp", payload = "sdssdsf")