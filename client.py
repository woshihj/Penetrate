#!/usr/bin/env python3
import socket
from time import sleep
from threading import Thread, current_thread, Lock
from common import Protocol, ProtocolError
from loguru import logger as log


def thread_command():
    """
    客户端与服务端的通信服务线程函数：处理服务端的请求
    :return:
    """
    client.thread_lock_cmd.acquire(blocking=True)
    log.info('%s started.' % current_thread().name)
    try:
        while not client.thread_lock_cmd.acquire(blocking=False):
            cmd, data = client.protocol.wait_request()
            #
            #
            #
            if cmd == Protocol.get_name(Protocol.Server.ADD_NEW_CONNECTION):
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


class Client:
    """
    内网穿透工具客户端程序（主动连接服务端进行端口映射）
    """
    protocol = Protocol(False, None)    # 通信协议接口
    thread_cmd = None                   # 通信服务：线程
    thread_lock_cmd = Lock()            # 通信服务线程：线程控制锁
    # thread_list = []                  # 线程列表
    # sock_list = []                    # 服务通信连接列表

    class Config:
        # Public configurations
        SERVER_HOST = '127.0.0.1'
        SERVER_PORT = 10000
        MAX_CONNECTIONS = 1000          # unix limits 1024
        MAX_PORT_MAP = 100              # S{MAX_PORT_MAP}=MAX_CONNECTIONS
        # client side configurations
        PORT_MAP_LIST = [80, 8080, 8081, 8082]

    def __init__(self):
        pass

    def start(self):
        #
        # connect to server
        #
        try:
            s_in = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s_in.connect((self.Config.SERVER_HOST, self.Config.SERVER_PORT))
            sleep(3)
            s_out = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s_out.connect((self.Config.SERVER_HOST, self.Config.SERVER_PORT))
            log.info('Connected to: %s:%d' % (self.Config.SERVER_HOST, self.Config.SERVER_PORT))
            self.protocol.set_socket(sock_in=s_in, sock_out=s_out)
        except ConnectionError as e:
            log.error('Failed to connect the server: %s' % e)
            return False
        #
        # synchronize config settings
        #
        try:
            self.protocol.execute(Protocol.Client.UPLOAD_MAPPING_PORTS,
                                  ','.join(str(x) for x in Client.Config.PORT_MAP_LIST))
        except ProtocolError as e:
            log.info(e)
            return False
        #
        # startup command thread
        #
        self.thread_cmd = Thread(thread_command, args=(), name='Thread-CMD')
        self.thread_cmd.start()
        while True:
            log.info('local alive!')
            sleep(10)

    def restart(self):
        pass


client = Client()

if __name__ == '__main__':
    client.start()
