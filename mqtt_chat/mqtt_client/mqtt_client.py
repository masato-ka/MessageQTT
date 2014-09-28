# -*- coding: utf-8 -*-

from paho.mqtt import client as mqtt



class client(object):

    def __init__(self, _topic, clean_session=True, user_data=None, _protocol=mqtt.MQTTv31):

        self.topic = _topic
        self.QoS_level = 0
        self.clean_session = clean_session

        self.client = mqtt.Client(protocol=_protocol)
        self.connect_result = []
        self.disconnect_result = []
        self.messages = []

        self.client.on_connect = lambda client, user_data, flg, return_code : \
                self.connect_result.append((client, user_data, flg, return_code))

        self.client.on_message = lambda client, user_data, message : \
                self.messages.append((client, user_data, message))

        self.client.on_disconnect = lambda client, user_data, return_code : self.disconnect_result.append((client, user_data, return_code))



    def set_QoS(self,qos_level):
        pass

    def set_callback_connect(self,on_connect):
        self.client.on_connect = on_connect

    def set_callback_on_message(self,on_connect):
        self.client.on_message = on_connect

    def set_topic(self, _topic):
        self.topic = _topic

    def subscribe(self):
        self.client.subscribe(self.topic)

    def set_username_pw(self, username, password=None):
        self.client.username_pw_set(username, password)

    def connect(self, host, port=1883, keep_alive=60, only_publish=False):
        #Connect to broker and start Network loop.
        self.client.connect(host, port, keep_alive)
        if not only_publish:
            self.client.loop_start()

    def disconnect(self,):
        self.client.disconnect()

    def loop_start(self):
        self.client.loop_start()

    def loop_stop(self, force=False):
        self.client.loop_stop(force)

    def publish(self, _message):
        self.client.publish(self.topic, _message)