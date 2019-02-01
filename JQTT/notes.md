All the MQTT client object methods

self._client = mqtt.Client()
self._client.connect
self._client.connect_async(broker, port)
self._client.loop_start()
self._client.message_callback_add()


# Set the retry timeout to be 5 seconds instead of the default 20 seconds
self._client.message_retry_set(5)
self._client.on_connect
self._client.on_disconnect
self._client.on_message
self._client.on_publish
self._client.on_subscribe
self._client.on_unsubscribe
self._client.publish()
self._client.qos
self._client.rc
# What is the below one for?
self._client.state
self._client.subscribe()
self._client.unsubscribe()
self._client.user_data_set()
self._client._do_on_publish
self._client._handle_connack
self._client._handle_on_message
self._client._handle_publish
