# Class in this file is used to create a new connection to the
# HiveMQ server and publish into it
from typing import Callable, Union, Any
import time
import paho.mqtt.client as paho
from paho import mqtt

class HiveClient:

    default_host = "41c1ed9ae7f140168d7f1515d3eb3fab.s2.eu.hivemq.cloud"
    default_port = 8883

    default_username = "UGAMQTT"
    default_password = "STEM2023"

    def __init__(self, host : str = default_host, port : int = default_port, username : str = default_username, password : str = default_password):
        self.client = paho.Client(client_id="", userdata=None, protocol=paho.MQTTv5)
        self.client.tls_set(tls_version=mqtt.client.ssl.PROTOCOL_TLS)
        self.client.username_pw_set(username, password)

        self.host = host
        self.port = port


    def connect(self) -> None:
        self.client.connect(self.host, self.port)


    def loop_start(self) -> None:
        self.client.loop_start()


    def connect_and_loop_start(self) -> None:
        self.connect()
        self.loop_start()


    def loop_stop(self) -> None:
        self.client.loop_stop()


    def disconnect(self) -> None:
        self.client.disconnect()


    def loop_stop_and_disconnect(self) -> None:
        self.loop_stop()
        self.disconnect()
        print("Disconnected from HiveMQ.")


    def publish(self, topic : str, payload, qos = 0) -> None:
        self.client.publish(topic, payload, qos)


    def publish_dict(self, base_topic : str, payload_dict : dict, qos = 0) -> None:
        for key, value in payload_dict.items():
            try:
                self.publish(base_topic + "/" + key, value, qos)
            except TypeError as e:
                if type(value) == dict:
                    self.publish_dict(base_topic + "/" + key, value, qos)
                if type(value) == list:
                    self.publish_dict(base_topic + "/" + key, {str(i): val for i, val in enumerate(value)}, qos)
                else:
                    raise e


    def subscribe(self, topic : str, qos : int = 0, callback : Union[Callable[[str], Any], None] = None):
        self.client.subscribe(topic, qos)
        if callback:
            self.client.message_callback_add(topic, callback)


    def set_topic_callback(self, topic : str, callback : Callable[[str], Any]):
        self.client.message_callback_add(topic, callback)
    

    def remove_topic_callback(self, topic : str):
        self.client.message_callback_remove(topic)


    def set_all_subscribed_topics_callback(self, callback):
        """calback(client, userdata, msg)"""
        self.client.on_message = callback

