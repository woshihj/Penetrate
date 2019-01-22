#!/usr/bin/env python3
import socket
from threading import Thread
from loguru import logger as log


def thread_command():
    while True:
        log.info(Thread.name)


class Client:
    """
    内网穿透工具客户端程序（主动连接服务端进行端口映射）
    """
    class Config:
        SERVER_HOST = '127.0.0.1'
        SERVER_PORT = 10000
        PORT_MAP_INDEX = 10000
        PORT_MAP_LIST = []
        MAX_PORT_MAP = 100
        MAX_CONNECTIONS = 1000

    def __init__(self):
        self.cmd_sock = None            # 主通信服务连接
        self.cmd_thread = None          # 主通信服务线程
        self.sock_list = []             # 服务通信连接列表
        self.thread_list = []           # 线程列表

    def start(self):
        #
        # connect to server
        #
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((self.Config.SERVER_HOST, self.Config.SERVER_PORT))
            log.info('Connected to: %s:%d', self.Config.SERVER_HOST, self.Config.SERVER_PORT)
            self.cmd_sock = s
        except ConnectionError as e:
            log.error('Failed to connect the server: %s' % e)
            return False
        #
        # startup command thread
        #
        self.cmd_thread = Thread(thread_command, args=(), name='Thread-CMD')
        self.cmd_thread.start()
        while True:
            data = self.cmd_sock.recv(1024)
            print(bytes.decode(data))





if __name__ == '__main__':
    client = Client()
    client.start()
