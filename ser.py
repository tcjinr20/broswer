from PyQt5 import QtCore, QtWebSockets,  QtNetwork, QtWidgets
# import requests
from urllib import request
import json
import os

def buildSocket(app):
    serverObject = QtWebSockets.QWebSocketServer('My Socket', QtWebSockets.QWebSocketServer.NonSecureMode)
    server = MyServer(serverObject)
    serverObject.closed.connect(app.quit)
    return (server,serverObject)

class MyServer(QtCore.QObject):

    def __init__(self, parent):
        super(QtCore.QObject, self).__init__(parent)
        self.clients = []
        self.server = QtWebSockets.QWebSocketServer(parent.serverName(), parent.secureMode(), parent)
        if self.server.listen(QtNetwork.QHostAddress.LocalHost, 1302):
            print('Connected: '+self.server.serverName()+' : '+self.server.serverAddress().toString()+':'+str(self.server.serverPort()))
        else:
            print('error')
        self.server.newConnection.connect(self.onNewConnection)
        print(self.server.isListening())

    def setConfig(self,_config):
        self.config=_config

    def onNewConnection(self):
        self.clientConnection = self.server.nextPendingConnection()
        self.clientConnection.textMessageReceived.connect(self.processTextMessage)

        self.clientConnection.binaryMessageReceived.connect(self.processBinaryMessage)
        self.clientConnection.disconnected.connect(self.socketDisconnected)

        self.clients.append(self.clientConnection)

    def processTextMessage(self,  message):
        back= self.sendTo(message)
        if (self.clientConnection):
            self.clientConnection.sendTextMessage(back)

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

    def sendTo(self,arg):
        if self.config.get('model')==2:
            return self.onSaveLocal(arg)
        else:
            return self.onSaveRomote(arg)

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