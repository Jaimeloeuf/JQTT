""" Dependencies """
import paho.mqtt.subscribe as subscribe
# Using the thread class to use threads and prevent the subscribe call from blocking.
from threading import Thread
# Random module used to generate the random and unique ID for the different threads
import random

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


def new_Msg(client, userdata, message):
    print("%s : %s" % (message.topic, message.payload))

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

""" Below is code to subscribe to multiple topics """
# topics = ['#']
# m = subscribe.simple(topics, hostname="iot.eclipse.org", retained=False, msg_count=2)
# for a in m:
#     print(a.topic)
#     print(a.payload)
