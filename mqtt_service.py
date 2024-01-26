import paho.mqtt.client as mqtt
import mysql.connector
import json

# MySQL数据库配置
DB_CONFIG = {
    "user": "root",
    "password": "your_mysql_password",
    "host": "localhost",
    "database": "mqtt_data",
}

# MQTT配置
MQTT_BROKER = "localhost"
MQTT_TOPIC = "your/mqtt/topic"

# 连接到MySQL数据库
db = mysql.connector.connect(
    host=DB_CONFIG["host"],
    user=DB_CONFIG["user"],
    password=DB_CONFIG["password"],
    database=DB_CONFIG["database"],
)
cursor = db.cursor()


# MQTT回调函数
def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")
    client.subscribe(MQTT_TOPIC)


def on_message(client, userdata, msg):
    print(f"Received message '{msg.payload}' on topic '{msg.topic}' with QoS {msg.qos}")

    # 将消息存储到MySQL数据库
    insert_stmt = "INSERT INTO messages (topic, payload, qos, retain) " "VALUES (%s, %s, %s, %s)"
    data = (msg.topic, msg.payload, msg.qos, msg.retain)
    cursor.execute(insert_stmt, data)
    db.commit()


# 创建MQTT客户端
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

# 连接到MQTT代理
client.connect(MQTT_BROKER, 1883, 60)

# 开始循环处理网络事件
client.loop_forever()
