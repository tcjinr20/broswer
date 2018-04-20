from PyQt5 import QtCore, QtWebSockets,  QtNetwork, QtWidgets
# import requests
from urllib import request
import json
import os
import configparser

def buildSocket(app):
    serverObject = QtWebSockets.QWebSocketServer('My Socket', QtWebSockets.QWebSocketServer.NonSecureMode)
    server = MyServer(serverObject)
    serverObject.closed.connect(app.quit)
    return (server,serverObject)
#
#code:1 保存临时数据 cookie 必须name
#code:2 获取临时数据 cookie
#code:3 保存永久数据
#code:4 获取永久数据
#code:0
#

class Cookie():
    lib={}
    def set(self,key,value):
        self.lib[key]=value
    def get(self,key):
        if self.lib[key] is not None:
            return self.lib[key]

class Session():

    def __init__(self):
        self.default = "setting"
        self.file = 'session.ini'
        self.config = configparser.ConfigParser()
        self.config.read(self.file)
        if self.config.has_section(self.default) is False:
            self.config.add_section(self.default)

    def set(self,key,val):
        self.config.set(self.default,key,json.dumps(val))
        self.config.write(open(self.file, "w"))
        pass

    def get(self,key):
        return json.loads(self.config.get(self.default,key))


class MyServer(QtCore.QObject):

    cookie = Cookie()
    session = Session()

    def __init__(self, parent):
        super(QtCore.QObject, self).__init__(parent)
        self.clients = []
        self.server = QtWebSockets.QWebSocketServer(parent.serverName(), parent.secureMode(), parent)
        if self.server.listen(QtNetwork.QHostAddress.LocalHost, 1302):
            print('Connected: '+self.server.serverName()+' : '+self.server.serverAddress().toString()+':'+str(self.server.serverPort()))
        else:
            print('error')
        self.server.newConnection.connect(self.onNewConnection)


    def setConfig(self,_config):
        self.config=_config

    def onNewConnection(self):
        self.clientConnection = self.server.nextPendingConnection()
        self.clientConnection.textMessageReceived.connect(self.processTextMessage)
        self.clientConnection.binaryMessageReceived.connect(self.processBinaryMessage)
        self.clientConnection.disconnected.connect(self.socketDisconnected)
        self.clients.append(self.clientConnection)

    def processTextMessage(self,  message):
        self.receive(message)

    def processBinaryMessage(self,  message):
        if (self.clientConnection):
            self.clientConnection.sendBinaryMessage(message)

    def socketDisconnected(self):
        print("close")
        if (self.clientConnection):
            self.clients.remove(self.clientConnection)
            self.clientConnection.deleteLater()

    def onSaveLocal(self,arg):

        path=self.config.get('path')
        times=int(self.config.get('times'))
        while os.path.exists(path):
            times+=1
            path.replace(os.path.basename(path),'t'+times)

        with open(path, 'w',encoding='utf-8') as cf:
            cf.writelines(arg)
            cf.close()
        return 'ok'

    def onSaveRomote(self,arg):
        par = json.loads(arg)
        url = self.config.get('pathadd')
        try:
            # req = requests.post(url=url, data=par)
            # return req.content.decode('utf-8')
            textmod = json.dumps(par).encode(encoding='utf-8')
            req = request.Request(url=url, data=textmod)
            res = request.urlopen(req)
            res = res.read().encode(encoding='utf-8')
            return res
        except Exception as e:
            return 'error'
        finally:
            return 'error'

    def sendto(self,arg):
        if (self.clientConnection):
            self.clientConnection.sendTextMessage(json.dumps(arg))

    def receive(self,arg):
        param=json.loads(arg)
        code = param['code'];
        mess =json.loads(param['mess'])
        if code==1:
            if mess['name'] is None:
                self.sendto({'code':0,'mess':"缺少name"})
                return
            self.cookie.set(mess['name'],mess)
        elif code==2:
            if mess['name'] is None:
                self.sendto({'code':0,'mess':"缺少name"})
            self.sendto(self.cookie.get(mess['name']))
        elif code==3:
            if mess['key'] is None:
                self.sendto({'code':0,'mess':"缺少key"})
                return
            self.session.set(str(mess['key']),mess)
        elif code == 4:
            if mess['key'] is None:
                self.sendto({'code':0,'mess':"缺少key"})
                return
            self.sendto(self.session.get(str(mess['key'])))
        elif code ==5:
            if mess['file'] is None:
                self.sendto({'code':0,'mess':u"缺少file"})
                return

            mess['content'] = open(mess['file'],'a+').write(mess['content'])
            self.sendto(mess['file'])

        elif code == 6:
            if mess['file'] is None:
                self.sendto({'code':0,'mess':"缺少file"})
                return
            if os.path.exists(mess['file']):
                mess['content'] = open(mess['file'],'r').read(1024)
                self.sendto(mess)
            else:
                self.sendto({'code': 0, 'mess': "文件不存在"+mess['file']})


class ServerProxy:

    def globalProxy(self,pro):
        proxy = QtNetwork.QNetworkProxy()
        # Http访问代理
        proxy.setType(QtNetwork.QNetworkProxy.HttpProxy)
        # 代理ip地址HttpProxy
        # proxy.setHostName("211.159.177.212")
        proxy.setHostName(pro['ip'])
        # 端口号
        # proxy.setPort(3128)
        proxy.setPort(int(pro['port']))

        if 'username' in pro and pro['username']!= None:
            proxy.setUser(pro['username'])
            proxy.setPassword(pro['password'])

        QtNetwork.QNetworkProxy.setApplicationProxy(proxy)


    # def localProxy(self,webview):
    #         webview.page().proxyAuthenticationRequired.connect(self.__handleProxyAuthReq)
    #
    # def __handleProxyAuthReq(url, auth, proxyhost):
    #     print(url, auth, proxyhost)
        # auth.setUser('4')
        # auth.setPassword('1')

if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    serverObject = QtWebSockets.QWebSocketServer('My Socket', QtWebSockets.QWebSocketServer.NonSecureMode)
    server = MyServer(serverObject)

    # serverObject.closed.connect(app.quit)
    app.exec_()