# Default callback function for subscriptions to use if none given during subscription
import psutil
import paho.mqtt.client as mqtt
import time


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


"""
Random and string module used to generate the random and unique ID for the different threads
import random
import string

# Below is the code for multithreaded subscription

sub_thread = []

# Subscribe to topic from broker in this module and use callback function provided or default new_Msg function.
def sub(cb=new_Msg):
    # Inner function that will utilize the values form outer functions just fine thanks to closure
    def sub_wrapper():
        subscribe.callback(cb, topic, qos=1, hostname=broker)
    
    # Create a unique ID for the thread
    thread_name = None
    while thread_name == None:
        # Create a random ID
        thread_name = ''.join(random.choices(string.ascii_uppercase + string.digits, k=3))
        # thread_name should be the topic instead which makes it easier to unsub
        # Check if the ID is unique
        for name in sub_thread:
            # If not unique, reset the thread name to None
            if thread_name == name:
                thread_name = None

    # Create the thread name with the wrapper function and the 'thread_name' UID
    thread = Thread(target=sub_wrapper, name=thread_name)
    # Append this thread to the array of threads, to allow subscription to more than one topic.
    sub_thread.append(thread)
    # Allow the thread to auto terminate when the main thread/process is killed.
    thread.daemon = True
    # Start the thread after appending the thread to the array
    thread.start()
    # Return the thread created
    return thread
    # QUes: How would I stop the thread? Or how or when do I call the thread.join method?

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
"""

if __name__ == "__main__":

    my_mqtt = mqtt.Client()
    
    my_mqtt.connect("m2m.eclipse.org", port=1883)
    my_mqtt.loop_start()
    
    my_mqtt.on_message = new_Msg

    my_mqtt.subscribe('IOTP/', qos=1)
    print("Subscribed to topic")

    while True:
        time.sleep(2)
