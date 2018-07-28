import socket
import re
'''
创建WEB服务器，返回给浏览器固定的页面
'''


class HttpServer(object):
    def __init__(self):  # 定义初始化函数，创建套接字，端口重用，绑定监听端口，定义属性（全局被使用）
        tcp_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        tcp_server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, True)
        tcp_server_socket.bind(('192.168.100.129', 8080))
        tcp_server_socket.listen(128)
        self.tcp_server_socket = tcp_server_socket

    def start(self):  # 不断接受连接
        while True:
            tcp_client_socket, ip_port = self.tcp_server_socket.accept()
            print('有新客户端连接', ip_port)
            self.request_hander(tcp_client_socket)

    def request_hander(self, tcp_client_socket):  # 判断请求url目录，并返回响应
        recv_data = tcp_client_socket.recv(1024)
        if not recv_data:
            print('浏览器断开连接')
            return
        recv_text = recv_data.decode()
        request_list = recv_text.split("\r\n")
        ret = re.search(r"\s(.*)\s", request_list[0])
        path_info = ret.group(1)
        if path_info == '/':
            path_info = '/index.html'

        response_line = 'HTTP/1.1 200 OK\r\n'
        response_header = 'Server:PythonWeb v1.0\r\n'
        response_blank = '\r\n'

        try:
            with open('./static' + path_info, 'rb') as file:
                response_content = file.read()
        except Exception as e:
            response_line = 'HTTP/1.1 404 Not Found\r\n'
            response_content = 'Error!!!~ %s'% str(e)
            response_content = response_content.encode()
        response_data = (response_line + response_header + response_blank).encode() + response_content
        tcp_client_socket.send(response_data)


if __name__ == '__main__':
    httpserver = HttpServer()
    httpserver.start()

