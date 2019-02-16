import AnyToJson
import time
import socket

class SyslogRun(AnyToJson.AnyToJson):
    def __init__(self, ):
        super().__init__()

        in_host = self.conf.get('connection', 'input_host')
        in_port = self.conf.getint('connection', 'input_port')

        self.listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.listen_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.listen_socket.bind(( in_host, in_port ))
        self.listen_socket.listen(1)

    def run(self):
        while True:
            conn, addr = self.listen_socket.accept()
            data = ''

            while True:
                try:
                    chunk = conn.recv(1024).decode('utf-8', 'ignore')
                except UnicodeDecodeError:
                    continue

                data = data + chunk
                rows = data.split("\n")
                if chunk != '':
                    data = rows.pop()
                for row in rows:
                    jsonvals = self.parse(row.strip("\r\n"))
                    for jsonval in jsonvals:
                        self.send(jsonval)

                if chunk == '':
                    break

            time.sleep(0.05)

        pass
