import paho.mqtt.client as mqtt
import time


def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")
    client.publish("ABC", "什么", qos=0)


def on_message(client, userdata, msg):
    print(f"Received message '{msg.payload}' on topic '{msg.topic}' with QoS {msg.qos}")


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("localhost", 1883, 60)  # 连接到本地的Mosquitto代理
i = 0
while True:
    i = i + 1
    print(i)
    client.loop(5)  # 每5秒处理一次网络事件
    client.publish("ABC", "KISS", qos=0)  # 发送消息到ABC主题
    time.sleep(5)  # 等待5秒
