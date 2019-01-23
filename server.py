#!/usr/bin/env python3
import socket
from time import sleep
from threading import Thread, current_thread, Lock
from common import Protocol, ProtocolError
from loguru import logger as log


def thread_command():
    """
    客户端与服务端的通信服务线程函数：处理客户端的请求
    :return:
    """
    server.thread_lock_cmd.acquire(blocking=True)
    log.info('%s started.' % current_thread().name)
    try:
        while not server.thread_lock_cmd.acquire(blocking=False):
            cmd, data = server.protocol.wait_request()
            #
            # 上传被映射的端口列表
            #
            if cmd == Protocol.get_name(Protocol.Client.UPLOAD_MAPPING_PORTS):
                pass
            #
            # 空闲情况下
            #
            else:
                pass
    except ConnectionError as e:
        log.error(e)
        pass
    except Exception as e:
        log.error(e)
    finally:
        log.info('%s exited' % current_thread().name)


class Server:
    """
    内网穿透工具服务端程序（接受客户端程序的连接，并在服务端开通端口映射）
    """
    protocol = Protocol(True, None)     # 通信协议接口
    thread_cmd = None                   # 通信服务：线程
    thread_lock_cmd = Lock()            # 通信服务线程：线程控制锁
    # thread_list = []                  # 线程列表
    # sock_list = []                    # 服务通信连接列表

    class Config:
        # public configurations
        SERVER_HOST = '127.0.0.1'
        SERVER_PORT = 10000
        MAX_CONNECTIONS = 1000          # unix limits 1024
        MAX_PORT_MAP = 100              # S{MAX_PORT_MAP}=MAX_CONNECTIONS
        # server side configurations
        PORT_MAP_INDEX = 10000          # SERVER_PORT = PORT_MAP_INDEX + CLIENT_PORT
        PORT_MAP_LIST = []              # Accepts from client_request & user_update

    def __init__(self):
        pass

    def start(self):
        #
        #  wait for client connections
        #
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((self.Config.SERVER_HOST, self.Config.SERVER_PORT))
            s.listen(2)  # 2 connections max ?
            log.info('Waiting for client connection ...')
            conn1, addr1 = s.accept()
            conn2, addr2 = s.accept()
            log.info('Connected from: %s and %s' % (addr1, addr2))
            self.protocol.set_socket(sock_in=conn2, sock_out=conn1)
        #
        # startup command thread
        #
        self.thread_cmd = Thread(thread_command, args=(), name='Thread-CMD')
        self.thread_cmd.start()
        while True:
            log.info('server alive!')
            sleep(10)

    def restart(self):
        pass


server = Server()

if __name__ == '__main__':
    server.start()
