# v1.2
# created
#   by Roger
# in 2017.1.3

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtWebChannel import QWebChannel
import threading

from PyQt5 import QtCore, QtWebSockets

from ser import MyServer

import sys
from urllib import request


def getCent(url):
    with request.urlopen(url) as f:
        data = f.read()
        txt = data.decode('utf-8')
        return txt


class CallHandler(QObject):

    @pyqtSlot()
    def myHello(self):
        print('call received')



class MainWindow(QMainWindow):
    # noinspection PyUnresolvedReferences
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 设置窗口标题
        self.setWindowTitle('My Browser')
        # 设置窗口图标
        self.setWindowIcon(QIcon('icons/penguin.png'))
        # 设置窗口大小900*600
        self.resize(900, 600)

        self.show()
		
        # 设置浏览器
        self.browser = QWebEngineView()


        # 添加浏览器到窗口中
        self.setCentralWidget(self.browser)

        ###使用QToolBar创建导航栏，并使用QAction创建按钮
        # 添加导航栏
        navigation_bar = QToolBar('Navigation')
        # 设定图标的大小
        navigation_bar.setIconSize(QSize(16, 16))
        #添加导航栏到窗口中
        self.addToolBar(navigation_bar)

        #QAction类提供了抽象的用户界面action，这些action可以被放置在窗口部件中
        # 添加前进、后退、停止加载和刷新的按钮
        back_button = QAction(QIcon('icons/back.png'), 'Back', self)
        next_button = QAction(QIcon('icons/next.png'), 'Forward', self)
        stop_button = QAction(QIcon('icons/cross.png'), 'stop', self)
        reload_button = QAction(QIcon('icons/renew.png'), 'reload', self)
        open_dialog = QAction(QIcon('icons/renew.png'), 'dialog', self)

        back_button.triggered.connect(self.browser.back)
        next_button.triggered.connect(self.browser.forward)
        stop_button.triggered.connect(self.browser.stop)
        reload_button.triggered.connect(self.browser.reload)
        open_dialog.triggered.connect(self.get_html)

        # 将按钮添加到导航栏上
        navigation_bar.addAction(back_button)
        navigation_bar.addAction(next_button)
        navigation_bar.addAction(stop_button)
        navigation_bar.addAction(reload_button)
        navigation_bar.addAction(open_dialog)

        #添加URL地址栏
        self.urlbar = QLineEdit()
        # 让地址栏能响应回车按键信号
        self.urlbar.returnPressed.connect(self.navigate_to_url)

        navigation_bar.addSeparator()
        navigation_bar.addWidget(self.urlbar)

        #让浏览器相应url地址的变化
        self.browser.urlChanged.connect(self.renew_urlbar)
        # self.browser.page().loadFinished.connect(self.get_html)

        # 指定打开界面的 URL
        url = 'http://www.1688.com'
        self.browser.setUrl(QUrl(url))


    def get_html(self):
        txt = getCent("http://47.254.42.59/admin/js/layer/t.txt")
        # js = ''
        for t in txt.split("\r\n"):
            if t != '':
                js =getCent(t)
                print(t)
                r=self.browser.page().runJavaScript(js)


    def navigate_to_url(self):
        q = QUrl(self.urlbar.text())
        if q.scheme() == '':
            q.setScheme('http')
        self.browser.setUrl(q)

    def renew_urlbar(self, q):
        # 将当前网页的链接更新到地址栏
        self.urlbar.setText(q.toString())
        self.urlbar.setCursorPosition(0)

def buildSocket(app):
    serverObject = QtWebSockets.QWebSocketServer('My Socket', QtWebSockets.QWebSocketServer.NonSecureMode)
    server = MyServer(serverObject)
    serverObject.closed.connect(app.quit)
    return (serverObject,server)

# 创建应用
app = QApplication(sys.argv)
# 创建主窗口
window = MainWindow()
t=buildSocket(app)
# 显示窗口
window.show()
# 运行应用，并监听事件
app.exec_()