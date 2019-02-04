from time import sleep
import paho.mqtt.client as mqtt

mqtt_broker = "m2m.eclipse.org"
topic_cpu = "IOTP/"

my_mqtt = None
def onMessage(client, userdata, message):
    print("%s %s" % (message.topic, message.payload))
def startMQTT():
    my_mqtt = mqtt.Client()
    my_mqtt.on_message = onMessage
    # my_mqtt.on_message = (lambda _ : print('hello'))
    my_mqtt.connect(mqtt_broker, port=1883)
    my_mqtt.subscribe(topic_cpu, qos=1)
    my_mqtt.loop_start()
    print("Subscribed to topic")
def main():
    startMQTT()
    while True:
        sleep(2)


class Subscriber:
    """ Class to create a Publisher to a given topic, to allow user to create some sort of
        data output pipe/stream to the MQTT Broker. """

    """ Subscriber should only be subscriber to a single topic, but allow multiple callbacks
        to be ran when a new payload comes """
        

    def __init__(self, topic, cb=None, qos=1, broker="m2m.eclipse.org", port=1833, retry_timeout=10, on_disconnect=None, on_connect=None, on_publish=None):
        # # Set the topic that this publisher publishes to, not directly accessible to user
        # self._topic = topic
        # # Set the QoS this publisher uses, not directly accessible to user
        # self._qos = qos
        # self._broker = broker
        # self._port = port

        
        self._client = mqtt.Client()

        if cb != None:
            self._client.on_message = cb
        else:
            self._client.on_message = onMessage

        self._client.connect(broker, port)
        self._client.subscribe(topic, qos)
        self._client.loop_start()
        print("Subscribed to topic")
        


if __name__ == "__main__":
    main()
    # subeddd = Subscriber('IOTP/')
    # while True:
    #     sleep(1)