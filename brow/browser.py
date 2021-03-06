
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtCore import Qt
import configparser
from libs.ui import CiSetting

import libs.sock as sock
import os
import sys
from urllib import request


def getCent(url):
    with request.urlopen(url) as f:
        data = f.read()
        txt = data.decode('utf-8')
        return txt

class MainWindow(QMainWindow):
    # noinspection PyUnresolvedReferences
    def __init__(self,_config):
        super().__init__()
        # 设置窗口标题
        self.setWindowTitle('My Browser')
        # 设置窗口图标
        self.setWindowIcon(QIcon('icons/penguin.png'))
        # 设置窗口大小900*600
        self.resize(900, 600)
        self.config = _config
        self.show()
        self.initui()
        self.initdata()

        # 指定打开界面的 URL
        self.open()

    def open(self):
        url = self.config.get("mainurl")
        if url.startswith('file:///'):
            url = os.getcwd() + url.replace('file:///', '')
        elif url.startswith('file:'):
            url='file:///'+url.replace('file:','')
        self.browser.setUrl(QUrl(url))

    def initui(self):
        # 设置浏览器
        self.browser = QWebEngineView()
        # 添加浏览器到窗口中
        self.setCentralWidget(self.browser)

        ###使用QToolBar创建导航栏，并使用QAction创建按钮
        # 添加导航栏
        navigation_bar = QToolBar('Navigation')
        # 设定图标的大小
        navigation_bar.setIconSize(QSize(16, 16))
        # 添加导航栏到窗口中
        self.addToolBar(navigation_bar)

        menubar = self.menuBar()
        menubar.setNativeMenuBar(False)
        fileMenu = menubar.addMenu('menu')
        exitAction = QAction(QIcon('icons/penguin.png'), 'setting', self)
        exitAction.setStatusTip('setting')
        exitAction.triggered.connect(self.menu_setting)

        # 将这个Action添加到fileMenu上
        fileMenu.addAction(exitAction)

        # QAction类提供了抽象的用户界面action，这些action可以被放置在窗口部件中
        # 添加前进、后退、停止加载和刷新的按钮
        back_button = QAction(QIcon('icons/back.png'), 'Back', self)
        next_button = QAction(QIcon('icons/next.png'), 'Forward', self)
        stop_button = QAction(QIcon('icons/cross.png'), 'stop', self)
        reload_button = QAction(QIcon('icons/renew.png'), 'reload', self)
        open_dialog = QAction(QIcon('icons/clipboard.png'), 'dialog', self)

        # setting_bar.addAction(set_btn)
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

        # 添加URL地址栏
        self.urlbar = QLineEdit()
        # 让地址栏能响应回车按键信号
        self.urlbar.returnPressed.connect(self.navigate_to_url)

        navigation_bar.addSeparator()
        navigation_bar.addWidget(self.urlbar)

        # 让浏览器相应url地址的变化
        self.browser.urlChanged.connect(self.renew_urlbar)
        # self.browser.page().loadFinished.connect(self.get_html)

    def initdata(self):

        (self.server,self.obj)= sock.buildSocket(app)
        # self.proxy= ser.ServerProxy()
        # self.proxy.globalProxy({'ip':'211.159.177.212','port':'3128'})
        # self.proxy.localProxy(self.browser)


    def menu_setting(self):

        # if self.dia is None:
        self.dia = CiSetting(self, self.config)
        self.dia.show()
        self.dia.on('close',self.refresh)

    def refresh(self):
        # self.initdata()
        self.open()


    def get_html(self):

        plug = self.config.get('plug')
        if plug is not '':
            self.browser.page().runJavaScript(open(plug,'r').read())

        if self.config.get('pathtxt') is not '':
            txt = getCent()
            for t in txt.split("\r\n"):
                if t != '':
                    js =getCent(t)
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



class CiConfig():

    def __init__(self):
        self.__change = False
        self.default="setting"
        self.file='ci.ini'
        self.config = configparser.ConfigParser()
        self.config.read(self.file)

        if self.config.has_section(self.default) is False:
            self.config.add_section(self.default)
            self.set("model", '2')
            # self.set("pathadd", 'http://www.baidu.com')
            self.set("pathtxt", 'http://www.baidu.com/t.txt')
            # self.set("path", 'f/t.txt')
            self.set("mainurl", 'http://www.1688.com')
            # self.set("times", '0')

    def set(self,key,val):
        self.__change=True
        self.config.set(self.default,key,val)

    def get(self,key):
        return self.config.get(self.default,key)

    def save(self):
        if self.__change:
            self.config.write(open(self.file, "w"))
            self.__change=False


if __name__ =="__main__":
    #创建应用

    #建主窗口
    app = QApplication(sys.argv)
    window = MainWindow(CiConfig())
    window.show()
    sys.exit(app.exec_())
    # 显示窗口


    # 运行应用，并监听事件

    # saveConfig([["setting",'notify','d'],["setting",'nem','fdgd']])
