#!/usr/bin/env python3
import socket
from threading import Thread
from loguru import logger as log
from time import sleep


def thread_command():
    while True:
        log.info(Thread.name)


class Server:
    """
    内网穿透工具服务端程序（接受客户端程序的连接，并在服务端开通端口映射）
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
        #  wait for client connections
        #
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((self.Config.SERVER_HOST, self.Config.SERVER_PORT))
            s.listen(0)  # 2 connections max ?
            log.info('Waiting for client connection ...')
            conn, addr = s.accept()
            log.info('Connected from: ', addr)
            self.cmd_sock = conn
            # s.close()
        #
        # startup command thread
        #
        self.cmd_thread = Thread(thread_command, args=(), name='Thread-CMD')
        self.cmd_thread.start()
        while True:
            self.cmd_sock.send(b'from server.')
            sleep(2)






if __name__ == '__main__':
    server = Server()
    server.start()
