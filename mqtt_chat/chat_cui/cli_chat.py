# -*- coding: utf-8 -*-

from mqtt_chat.mqtt_client.mqtt_client import client as mqtt
import curses, locale
import uuid, json
import sys

class CUIChatClient:

    def __init__(self, host='', username=''):
        locale.setlocale(locale.LC_ALL, '')
        self.client_id = str(uuid.uuid1())
        self.user_name = username
        curses.wrapper(self.loop, host)

    def loop(self, scr, host):
        self.init_colors()
        self.init_window(scr)

        def on_message(client, userdata, message):
            # callback for recieve message.
            payload = self._loads_payload(message.payload)
            if payload['client_id'] != self.client_id:
                self.message(payload['username']+':'+payload['message'],color=2)

        #initialize mqtt client
        mqtt_client = mqtt('chat/room1')
        mqtt_client.set_callback_on_message(on_message)
        mqtt_client.connect(host)
        mqtt_client.subscribe()

        self.message("こんにちは")
        self.message("Type 'quit' to exit.", 1)
        self.message("",)

        while True:
            input = self.ask('type message')
            self.message('own:'+input, 3)
            payload = self._dump_payload(input)
            mqtt_client.publish(payload)
            #self.chat.send(input)
            if input == 'quit':
                mqtt_client.disconnect()
                break

    def init_window(self, scr):
        self.cmd_window = scr.subwin(3,79,22,0)
        self.cmd_window.box()
        self.msg_window = scr.subwin(20,79,0,0)
        self.msg_window.box()
        self.msg_window.scrollok(True)
        self.msg_window.move(1,1)

    def init_colors(self):
        curses.start_color()
        curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
        curses.init_pair(3, curses.COLOR_CYAN, curses.COLOR_BLACK)
        curses.init_pair(4, curses.COLOR_YELLOW, curses.COLOR_BLACK)

    def ask(self, word):
        self.cmd_window.erase()
        self.cmd_window.box()
        self.cmd_window.move(1,1)
        self.cmd_window.addstr(word + ' >> ')
        self.cmd_window.refresh()
        curses.echo()
        input = self.cmd_window.getstr()
        curses.noecho()
        return input

    def message(self, msg, color=0):
        msg = " " + msg + "\n"
        if color:
            self.msg_window.addstr(msg,curses.color_pair(color))
        else:
            self.msg_window.addstr(msg)
        self.msg_window.box()
        self.msg_window.refresh()

    def _dump_payload(self,message):
        payload = {'client_id':self.client_id, 'username':self.user_name, 'message':message}
        return json.dumps(payload)

    def _loads_payload(self,payload):
        return json.loads(payload)



if __name__ == "__main__":

    args = sys.argv

    view = CUIChatClient("192.168.211.164", args[1])