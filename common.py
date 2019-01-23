from threading import Lock


class AppConfig:
    SOCKET_BUFFER_SIZE = 1024


class ProtocolError(Exception):
    pass


class Protocol:
    """
    内网穿透客户端与服务端通信协议：命令接口、工具函数等
    """
    class Client:
        UPLOAD_MAPPING_PORTS = {'name': 'UploadMappingPorts'}

    class Server:
        ADD_NEW_CONNECTION = {'name': 'AddNewConnection'}

    def __init__(self, is_server=False, sock_in=None, sock_out=None):
        self._is_server = is_server
        self._sock_in = sock_in
        self._sock_out = sock_out

    def set_socket(self, sock_in, sock_out):
        self._sock_in = sock_in
        self._sock_out = sock_out

    @staticmethod
    def get_name(cmd):
        return cmd['name']

    @staticmethod
    def req_str(cmd, val):
        return '<' + cmd['name'] + '>' + val + '</' + cmd['name'] + '>'

    @staticmethod
    def resp_str(cmd, val):
        return '<Response>' + cmd['name'] + ':' + val + '</Response>'

    def wait_request(self):
        req = self._sock_in.recv(AppConfig.SOCKET_BUFFER_SIZE)
        p1 = req.find('>', 0, -1)
        p2 = req.find('<', 1)
        if req[0] == '<' and req[-1] == '>' and 0 < p1 < p2:
            req_cmd = req[1:p1] if req[1:p1] == req[p2+2:-1] else None
            if req_cmd:
                return req_cmd, req[p1+1:p2]
        raise ProtocolError('Invalid request format: %s', req)

    def send_response(self, cmd, data):
        self._sock_in.send(self.resp_str(cmd, data))

    def send_request(self, cmd, data):
        self._sock_out.send(self.req_str(cmd, data))

    def wait_response(self):
        resp = self._sock_out.recv(AppConfig.SOCKET_BUFFER_SIZE)
        if len(resp) > 22 and resp[:10] == '<Response>' and resp[-11:] == '</Response>' and resp.find(':') > 0:
            cmd, data = resp[10:-11].split(':', 1)
            return cmd.strip(), data.strip()
        raise ProtocolError('Invalid response format: %s', resp)

    def execute(self, cmd, data):
        self.send_request(cmd, data)
        resp_cmd, resp_data = self.wait_response()
        if cmd == resp_cmd:
            return resp_data
        else:
            raise ProtocolError('Error while execute <%s>, received response for <%s>.' % cmd, resp_cmd)
