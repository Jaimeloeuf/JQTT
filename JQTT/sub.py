""" Dependencies """
import paho.mqtt.subscribe as subscribe
# Using the thread class to use threads and prevent the subscribe call from blocking.
from threading import Thread
# Client class
import paho.mqtt.client as mqtt

# This is the prefix for all the topics.
topic_prefix = "IOTP/grp4/channel/"
# Global variable to store the topic name, default topic is here too
topic = ""
# Global variable to store the topic name, default broker is here too
broker = "m2m.eclipse.org"


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


# Call to set topic function to create the default topic combining the prefix.
topic = set_topic(topic)


def new_Msg(client, userdata, message):
    # print("%s : %s" % (message.topic, message.payload))
    # Just print out the message body
    print(message.payload)

subscriptions = []

def sub(cb=new_Msg):
    # Create a new client
    client = mqtt.Client()
        # Append the subscription to the array to allow more than one subscription.
        # subscriptions.append(client)
    # Add event handler /  callback function when there is a new incoming message.
    client.on_message = cb
    # Establish a connection with the broker using the default port. Note that this call is blocking
    client.connect(broker, port=1883)
    # After a successful connection, establish a subscription pipe with the broker to the specified topic
    # Qos is currently 1, will create another function to allow overiding this.
    client.subscribe(topic, qos=1)
    # Put the blocking subscribe action into another thread based loop and return control to the main thread.
    client.loop_start()
    # Debug statement.
    print("Subscribed to topic: ", topic)


if __name__ == "__main__":
    # If module called as standalone module, run the example code below to demonstrate this MQTT client lib
    import time

    # Subscribe to the default topic
    sub()
    # Set new topic for subscription
    set_topic('hellow')
    # Subscribe to te newly set topic
    sub()

    while True:
        # Print statement to emulate the process/main thread doing something else.
        print('chicken')
        time.sleep(0.5)