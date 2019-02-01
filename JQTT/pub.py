""" Dependencies """
import paho.mqtt.publish as publish
from threading import Thread

# Global variable to store the topic name, default broker is here too
broker = "m2m.eclipse.org"
# Global variable to store the topic name, default topic is here too
topic = ""
# Global variable to store the transaction QoS, default value here.
qos = 1


def set_broker(data):
    # Function exposed to the other modules to set their own topics to publish to.
    global broker
    broker = data


def set_topic(data=None):
    # Function exposed to the other modules to set their own topics to publish to.
    global topic
    topic = data


def set_qos(data=None):
    # Function exposed to the other modules to set their own topics to publish to.
    global qos
    qos = data


# Function to just publish one message/payload at a time to the specified topic on the broker
def pub(payload):
    def publish_wrapper():
        publish.single(topic, payload, qos, hostname=broker)
    # Publish in a non-deamonic thread to finnish publish even if the main thread dies midway.
    Thread(target=publish_wrapper).start()


if __name__ == "__main__":
    # If module called as standalone module, run the example code below to demonstrate this MQTT client lib
    pub('helifgjs')  # Publish payload in seperate thread
	# Publish will continue in the background even as the main thread exits.