""" Dependencies """
import paho.mqtt.client as mqtt

# This is the prefix for all the topics.
topic_prefix = "IOTP/grp4/channel/"
# Global variable to store the topic name, default topic is here too
topic = ""
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
    # Why when I use payload and broker here I dont need to use the global keyword??
    # ^ Learn more about the global keyword usage.
    print(broker, port, topic) # Try to see what is the port and broker used heres
    publish.single(topic, payload, 1, hostname=broker) # Publish with a QoS of 1


def pub2(payload):
    client = mqtt.Client()
    print(broker, port) # Try to see what is the port and broker used here
    client.connect(broker, port)
    try:
        client.publish(topic, payload)
    except:
        print("Publish Error!")
    else:
        client.disconnect()

if __name__ == "__main__":
	# If module called as standalone module, run the example code below to demonstrate this MQTT client lib
    pub2('HELLOW')
    # raise EnvironmentError