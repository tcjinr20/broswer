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
        while os.path.exists(self.config['path']):
            self.config['times'] += 1
            self.config['path'] = 'f/t' + str(self.config['times']) + ".txt"

        with open(self.config['path'], 'w',encoding='utf-8') as cf:
            cf.writelines(arg)
            cf.close()
        return 'ok'

    def onSaveRomote(self,arg):
        par = json.loads(arg)
        url = self.config['pathadd']
        try:
            # req = requests.post(url=url, data=par)
            # return req.content.decode('utf-8')
            textmod = json.dumps(par).encode(encoding='utf-8')
            req = request.Request(url=url, data=textmod)
            res = request.urlopen(req)
            res = res.read().encode(encoding='utf-8')
            print(res)
            return res
        except Exception as e:
            print(e)
            return 'error'
        finally:
            return 'error'

    def sendTo(self,arg):
        if self.config['model']==2:
            return self.onSaveLocal(arg)
        else:
            return self.onSaveRomote(arg)



if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    serverObject = QtWebSockets.QWebSocketServer('My Socket', QtWebSockets.QWebSocketServer.NonSecureMode)
    server = MyServer(serverObject)
    server.onSave("fsfds")
    # serverObject.closed.connect(app.quit)
    app.exec_()