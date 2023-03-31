# Class in this file is used to create a new connection to the
# HiveMQ server and publish into it
from typing import Callable
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

    def publish(self, topic : str, payload, qos = 0) -> None:
        self.client.publish(topic, payload, qos)