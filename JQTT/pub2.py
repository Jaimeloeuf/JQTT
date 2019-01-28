""" Dependencies """
import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish

# This is the prefix for all the topics.
# topic_prefix = "IOTP/grp4/channel/"
topic_prefix = "IOTP/"
# Global variable to store the topic name, default topic is empty with a prefixed topic_prefix
topic = topic_prefix + ""
# Global variable to store the topic name, default broker is here too
broker = "m2m.eclipse.org"
# Global variable to store the port used, default port is created here
port = 1883


def set_broker(data):
    # Function exposed to the other modules to set their own topics to publish to.
    global broker
    broker = data


def set_topic(data):
    # Function exposed to the other modules to set their own topics to publish to.
    global topic
    # Create the topic by prepending the prefix to the received data and saving inside the global topic variable
    topic = topic_prefix + data
    # Return topic for the function caller to use if needed.
    return topic


def pub(payload):
    # Publish with a QoS of 1
    publish.single(topic, payload, 1, hostname=broker)


def pub2(payload):
    # mqtt.Client
    client = mqtt.Client()
    client.connect(broker, port)
    try:
        client.publish(topic, payload)
    except:
        print("Publish Error!")
    else:
        client.disconnect()


# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, rc):
    print("Connected with result code "+str(rc))
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("$SYS/#")

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print('In msg func')
    print(msg.topic+" "+str(msg.payload))

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("iot.eclipse.org", 1883, 60)

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
# client.loop_forever()
client.loop_start()


if __name__ == "__main__":
    import time
    while True:
        # If module called as standalone module, run the example code below to demonstrate this MQTT client lib
        pub2('HELLOW')
        # print('published')
        # raise EnvironmentError
        time.sleep(3)
