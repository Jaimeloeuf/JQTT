""" Dependencies """
import paho.mqtt.client as mqtt


# Default function to run on disconnect from the Broker
def disconnected(self, user_data, rc):
    """ The value of 'rc' determines success or not:
        0: Connection successful
        1: Connection refused - incorrect protocol version
        2: Connection refused - invalid client identifier
        3: Connection refused - server unavailable
        4: Connection refused - bad username or password
        5: Connection refused - not authorised
        6-255: Currently unused.
    """
    print('Disconnected from MQTT broker')


# Default function to run everytime message is published to Broker
def published(self, user_data, published_packet_num):
    """ Arguements passed in by the on_publish event emitter:
        Self: The MQTT client object
        user_data: User data that was included when creating the client object
        published_packet_num: The number 'ID' of the payload just published out.
    """
    print(f'Package {published_packet_num} published to the MQTT broker')


# The default callback for when the client receives a CONACK response from the server.
def connected(self, user_data, flags_dict, rc):
    """ Arguements passed in by the on_connect event emitter:
        Self: The MQTT client object
        user_data: User data that was included when creating the client object
        flags_dict: A dict that contains response flags from the broker, useful for clients that are using
                    clean session set to 0 only. more info in mqtt.Client().on_connect's implementation
        rc: result code of the connection, look at doc for 'disconnected' function.

        *Note:  Subscribing to on_connect means that if we lose the connection
                and reconnect then subscriptions will be renewed.
    """
    print(f'Client successfully connected to the Broker "{self._host}" with result code {str(rc)}')


class Publisher:
    """ Class to create a Publisher to a given topic, to allow user to create some sort of
        data output pipe/stream to the MQTT Broker. """
        
    def __init__(self, topic, qos=1, broker="m2m.eclipse.org", port=1883, retry_timeout=10, on_disconnect=disconnected, on_connect=None, on_publish=None):
        # Set the topic that this publisher publishes to, not directly accessible to user
        self._topic = topic
        # Set the QoS this publisher uses, not directly accessible to user
        self._qos = qos
        self._broker = broker
        self._port = port

        # Create a new mqtt client with input arguements and connect asynchrounously on a daemonic thread
        self._client = mqtt.Client()
        # Connect to the broker in a seperate thread asynchronously
        self._client.connect_async(broker, port)
        # Start a loop to allow some sort of 'message queue'
        self._client.loop_start()

        # Set the retry timeout to be 5 seconds instead of the default 20 seconds
        self._client.message_retry_set(retry_timeout)

        # Set all the callback functions for the different events
        self._client.on_disconnect = on_disconnect

        if on_connect == True:
            # If User wants a on_connect callback but did not pass in any, use the default handler
            self._client.on_connect = connected
        elif on_connect != None:
            # If user passed in their own callback to run when data is published
            self._client.on_connect = on_connect

        if on_publish == True:
            # If User wants a on_publish callback but did not pass in any, use the default handler
            self._client.on_publish = published
        elif on_publish != None:
            # If user passed in their own callback to run when data is published
            self._client.on_publish = on_publish

    # Method to publish data
    def pub(self, payload, topic=None):
        try:
            # If the user did not call method with a topic, then use pre-defined topic
            if topic == None:
                topic = self._topic
            self._client.publish(topic=topic, payload=payload, qos=self._qos)
        except:
            print('ERR: Publish Error')
        # Return self reference to allow method call chainings.
        return self

    @property
    def qos(self, qos=1):
        if qos < 0 or qos > 2:
            raise AttributeError
        self._qos = qos
        # Return self reference to allow method call chainings.
        return self

    # Method to disconnect Publisher client from the broker
    def disconnect(self):
        self._client.disconnect()
        # Return self reference to allow method call chainings.
        return self

	# Method to reconnect to the Broker
    def reconnect(self):
        self._client.reconnect()
        # Return self reference to allow method call chainings.
        return self


    # Allow user to do Publisher(msg) to publish msg, where Publisher = Publisher('topic')
    __call__ = pub
    # Allow user to use < to publish   ==>  Publisher < 'msg'
    __lt__ = pub


if __name__ == "__main__":
    # If module called as standalone module, run the example code below to demonstrate this MQTT client lib
    from time import sleep
    
    # Create a publisher, request for default handlers for on_connect and on_publish events.
    dataPublisher = Publisher('IOTP/', on_connect=True, on_publish=True)

    # Infinite publish loop
    while True:
        # Publish the message with the 'pub' method
		# The topic passed in as arguement is a one of Topic change.
        dataPublisher.pub('Hi', 'IOTP/test')
        sleep(1)
		# Subsequent publishes uses the same default topic set at Publisher creation
        # Publish the message with the magic method __call__
        dataPublisher('Hello')
        sleep(1)
        # Publish the message with the magic method __lt__
        dataPublisher < 'world'
        sleep(1)