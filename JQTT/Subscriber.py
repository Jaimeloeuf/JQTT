""" Dependencies """
import paho.mqtt.client as mqtt
from Jevents import Watch


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


# Default callback function for new message event
# def print_msg(client, userdata, message):
def print_msg(message):
    """ Arguements passed in by the subscription service:
        client: The MQTT client object
        user_data: User data that was included in the message payload
        message: The message that was received
    """
    # print("%s : %s" % (message.topic, message.payload))
    # Just print out the message body
    print(message.payload.decode())


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


class Subscription:
    """ Class to make a Subscription to a topic, allowing user to create some sort of
        data input pipe/stream from the MQTT Broker.
        The only actions allowed on the subscription after subscribing is add or delete callbacks.
        After the subscription is established, the topic, broker, port, QOS cannot, CANNOT be changed.
    """

    def __init__(self, topic, qos=1, broker="m2m.eclipse.org", port=1883, retry_timeout=10, on_message=None, on_disconnect=disconnected, on_connect=None):
        # Store the topic of this subscription. Topic should not be changed by user.
        self._topic = topic

        # Create a new mqtt client with input arguements and connect asynchrounously on a daemonic thread
        self._client = mqtt.Client()
        # Connect to the broker with the blocking connect method, as connect_async does not work properly
        self._client.connect(broker, port)
        # Start the sub loop
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

        # # Create a watched variable to store the incoming message in
        self.msg = Watch()
        # Create a magic Method/Property binder to add callbacks to run on new message
        self.on_message = self.msg.on_set

        if on_message == True:
            # If User wants a on_message callback but did not pass in any, use the default handler
            self.msg.on_set += print_msg
        elif on_message != None:
            # If user passed in their own callback to run when data is received
            self.msg.on_set += on_message

        # The callback function of the Client used to trigger other User set callback functions.
        def new_Msg(client, userdata, message):
            """ This is the only 'real' on_message callback.
                This callback itself will set the message, which is a Watched variable.
                Upon setting a value all the other callbacks will be ran.
            """
            # Set the message and let the Callback functions run
            self.msg(message)
            # Fix the Watch class to allow passing in more than one arguement to the Callbacks
            # (client, userdata, message)

        # # Pass the 'Callback calling method' as the Callback function to the Client object
        self._client.on_message = new_Msg

        # To test the line below.
        # self._client.on_message = new_Msg if on_message == True else on_message if on_message != None else None

        # Default callback function for on_subscribe event
        def subscribed(*args):
            print(f'Successfully subscribed to: "{self._topic}"')

        # Add the callback function for the subscribed event
        self._client.on_subscribe = subscribed

        # Default callback function for on_subscribe event
        def unsubscribed(*args):
            print(f'Successfully unsubscribed from: "{self._topic}"')

        # Add the callback function for the unsubscribed event
        self._client.on_unsubscribe = unsubscribed

        # After setting up everything, subscribe to the topic
        self._client.subscribe(topic, qos=qos)

    # @property # See if this works
    def qos(self, qos=1):
        if qos < 0 or qos > 2:
            raise AttributeError
        self._qos = qos
        # Return self reference to allow method call chainings.
        return self

    # Method to unsub from the Broker's Topic.
    def unsub(self):
        self._client.unsubscribe(self._topic)
        # Return self reference to allow method call chainings.
        return self

    # Method to disconnect from the Broker
    def disconnect(self):
        # Unsubscribe first before disconnecting.
        self.unsub()
        self._client.disconnect()
        # Return self reference to allow method call chainings.
        return self

    # Method to reconnect to the Broker
    def reconnect(self):
        self._client.reconnect()
        # Return self reference to allow method call chainings.
        return self


if __name__ == "__main__":
    # If module called as standalone module, run the example code below to demonstrate this MQTT client lib
    from time import sleep
    from Jevents import wait_for_daemons
    import signal

    # Make a new Subscription, request for default handlers for on_connect and on_message events.
    my_Subscription = Subscription('IOTP/', on_connect=True, on_message=True)

    # Define a inner Callback function
    def onMessage2(message):
        print("This is the second cb %s" % (message.payload.decode()))
    
    # Define a inner Callback function
    def onMessage3(message):
        print("This is the third cb %s" % (message.payload.decode()))

    # Pass the callback functions to the Subscriber to use for the subscription
    # Pass the callback functions using the method call. Pass in one by one
    my_Subscription.on_message(onMessage2)
    my_Subscription.on_message(onMessage3)
    # Pass the callback functions as a tuple using the magic method binding
    my_Subscription.on_message += onMessage2, onMessage3

    def signal_handler(signal, frame):
        print("Program interrupted!")
        # Disconnect
        my_Subscription.disconnect()
        # Blocking call on main thread to wait for the disconnect to finnish first
        wait_for_daemons()
        exit(0)

    # Pass in the signal_handler to run when the INTerrupt signal is received
    signal.signal(signal.SIGINT, signal_handler)

    # infinite loop printing out stuff to simulate actions happening in the main thread
    while True:
        # Print something to emulate the main thread doing something.
        print('chicken')
        sleep(1)  # Blocking wait call.
