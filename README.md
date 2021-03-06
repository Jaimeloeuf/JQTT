### Package name: JQTT
- Author: Jaime Loeuf
- License: MIT
- Package Desciption:
	- This package is a simplified MQTT library based on the paho MQTT library.
	- Currently this package contains the
		1. 'Publisher' Class
		2. 'Subscription' Class
		3. 'Pub' function
		4. 'Sub' function
	- Currently lacking more documentation. For now please view test scripts for the different modules to see how to use this Package.


##### To Publish data to broker:
```python
from JQTT import pub
pub('Chicken Nuggets!')
```

To Subscribe to data:
```python
from JQTT import sub
def onMsg(client, userdata, message):
	print(message) # Callback function to print out the message
sub(onMsg) # Pass the function into the sub function to use it as a callback function
```

* For the above lib usage. The broker and topics are not set, thus the default broker and topics will be used.

To Change broker and topic before publishing data or subscribing to messages:
```python
from JQTT import sub, pub set_broker, set_topic
set_broker('m2m.org', 'p') # Set the broker to publish to
set_topic('MQTT_test', 'p') # Set the topic to publish to
pub('Hello, test 123') # Publish the message to the abv broker's topic
set_broker('m2m.org', 's') # Set the broker to subscribe to
set_topic('MQTT_test', 's') # Set the topic to subscribe to
def onMsg(client, userdata, message):
	print(message) # Callback function to print out the message
sub(onMsg) # Subscribe to the messages from the abv broker's topic using the abv callback function.
```