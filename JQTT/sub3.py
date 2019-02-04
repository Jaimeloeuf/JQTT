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
    print(str(message.payload))  # Just print out the message body


subscriptions = []

sub_thread = []

# Subscribe to topic from broker in this module and use callback function provided or default new_Msg function.
def sub(cb=new_Msg):
    # Inner function that will utilize the values form outer functions just fine thanks to closure
    def sub_wrapper():
        subscribe.callback(cb, topic, qos=1, hostname=broker)
    
    # # Create a unique ID for the thread
    # thread_name = None
    # while thread_name == None:
    #     # Create a random ID
    #     thread_name = ''.join(random.choices(string.ascii_uppercase + string.digits, k=3))
    #     # thread_name should be the topic instead which makes it easier to unsub
    #     # Check if the ID is unique
    #     for name in sub_thread:
    #         # If not unique, reset the thread name to None
    #         if thread_name == name:
    #             thread_name = None

    # # Create the thread name with the wrapper function and the 'thread_name' UID
    # thread = Thread(target=sub_wrapper, name=thread_name)
    # # Append this thread to the array of threads, to allow subscription to more than one topic.
    # sub_thread.append(thread)
    # # Allow the thread to auto terminate when the main thread/process is killed.
    # thread.daemon = True
    # # Start the thread after appending the thread to the array
    # thread.start()
    # # Return the thread created
    # return thread

    # sub_thread.append(Thread(target=sub_wrapper, daemon=True).start())

    thread = Thread(target=sub_wrapper, daemon=True)
    sub_thread.append(thread)
    thread.start()


# Function to unsubscribe to a topic, by killing the thread stored in the sub_thread array
def unsub(thread_name):
    # Check for the name in the array
    for name in sub_thread:
        if thread_name == name:
            # Stop the thread when found
            sub_thread[name]._stop()
            # Return true to indicate operation successful.
            return True
    # If no such thread with the given thread name is found, return false to indicate failure
    return False # Should I raise and exception instead?



if __name__ == "__main__":
    # If module called as standalone module, run the example code below to demonstrate this MQTT client lib
    from time import sleep
    # Threading library used to wait for daemons
    from Jevents import wait_for_daemons
    from threading import enumerate

    # Set topic for subscription
    set_topic('IOTP/grp4/channel/')
    # Subscribe to the above topic
    sub()

    """ Inner functions like this can also be used as the callback function for a subscription.
    Note that if you are defining your own callback functions, make sure it accepts the same input parameters
    as the parameters shown in the example and default subscription on_message callback function, 'new_Msg' """
    def new_Msg2(client, userdata, message):
        print('This is the new handler, msg is: ', str(message.payload))

    # Set new topic for subscription
    set_topic('IOTP/grp4/channel/hellow')
    # Subscribe to te newly set topic
    sub(new_Msg2)

    print(sub_thread)

    print(enumerate())

    """ Blocking call on the main thread to prevent it from ending when there are still Daemonic
        threads running in the background such as the subscription services which are daemons. """
    # wait_for_daemons()

    """ Below is an alternative to using wait_for_daemons by keeping the main thread busy with an
        infinite loop printing out stuff to simulate other actions that can happen in the main thread """
    # while True:
    #     # Print something to emulate the main thread doing something.
    #     print('chicken')
    #     sleep(0.8) # Blocking wait call.
