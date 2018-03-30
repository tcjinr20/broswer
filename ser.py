from PyQt5 import QtCore, QtWebSockets,  QtNetwork, QtWidgets
import requests
import threading
import json

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

    def onNewConnection(self):
        self.clientConnection = self.server.nextPendingConnection()
        self.clientConnection.textMessageReceived.connect(self.processTextMessage)

        self.clientConnection.binaryMessageReceived.connect(self.processBinaryMessage)
        self.clientConnection.disconnected.connect(self.socketDisconnected)

        self.clients.append(self.clientConnection)

    def processTextMessage(self,  message):
        back= sendTo(message)
        if (self.clientConnection):
            self.clientConnection.sendTextMessage(back)

    # def threadback(self,str):
    #     if (self.clientConnection):
    #         self.clientConnection.sendTextMessage("1")

    def processBinaryMessage(self,  message):
        if (self.clientConnection):
            self.clientConnection.sendBinaryMessage(message)

    def socketDisconnected(self):
        print("close")
        if (self.clientConnection):
            self.clients.remove(self.clientConnection)
            self.clientConnection.deleteLater()


class WorkerThread(threading.Thread):

    def __init__(self, callback,param):
        super(WorkerThread, self).__init__()
        self.callback = callback
        self.param=param

    def run(self):
        url = u"http://47.254.42.59/api/addgood.php"
        try:
            req = requests.post(url=url, data=self.param.encode('utf-8'))
        except Exception as e:
            self.callback(0)
        finally:
            if self.callback: self.callback(req.content.decode('utf-8'))


def sendTo(arg):

    par=json.loads(arg)
    url = u"http://47.254.42.59/api/addgood.php"
    try:
        req = requests.post(url=url, data=par)
        return req.content.decode('utf-8')
    except Exception as e:
        print(e)
    finally:
        print(2)


if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    serverObject = QtWebSockets.QWebSocketServer('My Socket', QtWebSockets.QWebSocketServer.NonSecureMode)
    server = MyServer(serverObject)

    serverObject.closed.connect(app.quit)
    app.exec_()