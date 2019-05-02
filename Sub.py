import paho.mqtt.client as mqtt


def on_connect(client, userdata, flags, rc):  # The callback for when the client connects to the broker
    print("Connected with result code {0}".format(str(rc)))  # Print result of connection attempt
    client.subscribe("set/Temp")  # Subscribe to the topic “digitest/test1”, receive any messages published on it


def on_message(client, userdata, msg):  # The callback for when a PUBLISH message is received from the server.
    print("Message received-> " + msg.topic + " " + str(msg.payload))


client = mqtt.Client("digi_mqtt_test")
client.username_pw_set(username="username", password="password")
client.on_connect = on_connect
client.on_message = on_message
client.connect('192.168.0.103', 1883)
client.loop_forever()