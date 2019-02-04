""" Dependencies """
import paho.mqtt.client as mqtt


class Subscriber:
    """ Class to create a Publisher to a given topic, to allow user to create some sort of
        data output pipe/stream to the MQTT Broker. """

    def __init__(self, topic, qos=1, broker="m2m.eclipse.org", port=1833, retry_timeout=10, on_connect=None, on_publish=None):
        # Set the topic that this publisher publishes to, not directly accessible to user
        self._topic = topic
        # Set the QoS this publisher uses, not directly accessible to user
        self._qos = qos
        self._broker = broker
        self._port = port

        # Create a new mqtt client with input arguements and connect asynchrounously on a daemonic thread
        self._client = mqtt.Client(broker, port, retry_timeout)
        self._client.on_message = self.new_Msg

        def subed():
            print('Subed')

        self._client.on_subscribe = subed
        
        self._client.subscribe('IOTP/')
        print('The cb is')
        print(self._client.on_message)

        self._client.connect_async(broker, port)
        self._client.loop_start()

        # Set the retry timeout to be 5 seconds instead of the default 20 seconds
        self._client.message_retry_set(retry_timeout)
        # self._client.on_disconnect = on_disconnect

        # if on_connect == True:
        #     # If User wants a on_connect callback but did not pass in any, use the default handler
        #     self._client.on_connect = connected
        # elif on_connect != None:
        #     # If user passed in their own callback to run when data is published
        #     self._client.on_connect = on_connect

        # if on_publish == True:
        #     # If User wants a on_publish callback but did not pass in any, use the default handler
        #     self._client.on_publish = published
        # elif on_publish != None:
        #     # If user passed in their own callback to run when data is published
        #     self._client.on_publish = on_publish


    # Default callback function for subscriptions to use if none given during subscription
    def new_Msg(self, client, userdata, message):
        """ Arguements passed in by the subscription service:
            client: The MQTT client object
            user_data: User data that was included in the message payload
            message: The message that was received
        """
        print('MEssg receisved')
        # print("%s : %s" % (message.topic, message.payload))
        print(client)
        print(userdata)
        print(str(message.payload))  # Just print out the message body

    def sub(self, topic):
        self._client.subscribe(topic, qos=1)
        # Return self reference to allow method call chainings.
        return self

    def unsub(self, topic):
        self._client.unsubscribe(topic)
        # Return self reference to allow method call chainings.
        return self

    # @property # See if this works
    def qos(self, qos=1):
        if qos < 0 or qos > 2:
            raise AttributeError
        self._qos = qos
        # Return self reference to allow method call chainings.
        return self

    def disconnect(self):
        self._client.disconnect()
        # Return self reference to allow method call chainings.
        return self

    def connect(self):
        self._client.connect(self._broker, self._port)
        # Return self reference to allow method call chainings.
        return self

    def reconnect(self):
        self._client.reconnect()
        # Return self reference to allow method call chainings.
        return self


def onMessage(client, userdata, message):
    print("%s %s" % (message.topic, message.payload))


if __name__ == "__main__":
    # If module called as standalone module, run the example code below to demonstrate this MQTT client lib
    import time

    # Change subscriber to subscription name

    # Create a publisher, request for default handlers for on_connect and on_publish events.
    mSub = Subscriber('IOTP/', on_connect=True, on_publish=True)
    mSub.sub('IOTP/grp4/channel/')

    # Infinite publish loop
    while True:
        time.sleep(2)
        print('Chicken')
