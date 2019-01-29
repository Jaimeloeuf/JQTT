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



class Publisher:
	def __init__(self):
		self._client = mqtt.Client()
		# self._client.connect
		self._client.connect_async(broker, port)
		self._client.loop_start()
		self._client.message_callback_add()
		# Set the retry timeout to be 5 seconds instead of the default 20 seconds
		self._client.message_retry_set(5)
		self._client.on_connect
		self._client.on_disconnect
		self._client.on_message
		self._client.on_publish
		self._client.on_subscribe
		self._client.on_unsubscribe
		self._client.publish()
		self._client.qos
		self._client.rc
		# What is the below one for?
		self._client.state
		self._client.subscribe()
		self._client.unsubscribe()
		self._client.user_data_set()
		self._client._do_on_publish
		self._client._handle_connack
		self._client._handle_on_message
		self._client._handle_publish
	
	# Method to publish data
	def push(self):
		pass

def pub(payload):
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
# def on_connect(client, userdata, rc):
#     print("Connected with result code "+str(rc))
#     # Subscribing in on_connect() means that if we lose the connection and
#     # reconnect then subscriptions will be renewed.
#     client.subscribe("$SYS/#")

# client = mqtt.Client()
# client.on_connect = on_connect
# client.on_message = on_message

# client.connect("iot.eclipse.org", 1883, 60)

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
# client.loop_forever()
# client.loop_start()


if __name__ == "__main__":
    import time
    while True:
        # If module called as standalone module, run the example code below to demonstrate this MQTT client lib
        pub2('HELLOW')
        # print('published')
        # raise EnvironmentError
        time.sleep(3)
