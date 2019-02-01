""" Dependencies """
import paho.mqtt.subscribe as subscribe
# Using the thread class to use threads and prevent the subscribe call from blocking.
from threading import Thread
# Client class
import paho.mqtt.client as mqtt

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


# Default callback function for subscriptions to use if none given during subscription
def new_Msg(client, userdata, message):
    """ Arguements passed in by the subscription service:
        client: The MQTT client object
        user_data: User data that was included in the message payload
        message: The message that was received
    """
    # print("%s : %s" % (message.topic, message.payload))
    print(client)
    print(userdata)
    print(message.payload)  # Just print out the message body


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
    # Put the blocking subscribe action into a daemonic thread based loop and return control to the main thread.
    client.loop_start()
    # Debug statement.
    print("Subscribed to topic: ", topic)


if __name__ == "__main__":
    # If module called as standalone module, run the example code below to demonstrate this MQTT client lib
    import time

    # Set topic for subscription
    set_topic('IOTP/grp4/channel/')
    # Subscribe to the above topic
    sub()

    """ Inner functions like this can also be used as the callback function for a subscription.
    Note that if you are defining your own callback functions, make sure it accepts the same input parameters
    as the parameters shown in the example and default subscription on_message callback function, 'new_Msg' """
    def new_Msg2(client, userdata, message):
        print('This is the new handler, msg is: ', message.payload)

    # Set new topic for subscription
    set_topic('IOTP/grp4/channel/hellow')
    # Subscribe to te newly set topic
    sub(new_Msg2)

    # Threading library used to wait for daemons
    from Jevents import wait_for_daemons

    wait_for_daemons()

    # while True:
    #     # Print statement to emulate the process/main thread doing something else.
    #     print('chicken')
    #     time.sleep(0.8)
