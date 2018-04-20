from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi

class CiQDialog(QDialog):
    def __init__(self,parent=None,config=None):
        super().__init__(parent)
        self.ci_init(config)
        pass

    def ci_init(self,config):
        pass

    def ci_show(self,ui):
        loadUi(ui,self)
        self.show()
        self._ci_show()

    def _ci_show(self):
        print('__ci_show')
        pass

    dispach={}
    def on(self,estr,back):
        self.dispach[estr]=back;

    def emit(self,estr):
        self.dispach[estr]()


class CiLogin(CiQDialog):

    def __init__(self):
        super().__init__()

    def __ci_show(self):
        pass


class CiRegister(CiQDialog):

    def __init__(self):
        super(CiRegister,self).__init__()


class CiSetting(CiQDialog):
    def __init__(self,parent=None,config=None):
        CiQDialog.__init__(self,parent,config)

    def ci_init(self,con):
        self.config = con
        self.setWindowTitle("配置数据")
        self.setModal(True)
        self.ci_show('./ui/setting.ui')

    def _ci_show(self):
        print(self.config.get('mainurl'))
        self.findChild(QLineEdit, "mainurl").setText(self.config.get('mainurl'))
        self.findChild(QLineEdit, "remote").setText(self.config.get('pathadd'))
        self.findChild(QLineEdit, "local").setText(self.config.get('path'))
        self.findChild(QLineEdit, "script").setText(self.config.get('pathtxt'))
        self.findChild(QRadioButton, "remotebtn").toggled.connect(self.changeRadio1)


    def closeEvent(self, QCloseEvent):
        self.config.set('mainurl',self.findChild(QLineEdit, "mainurl").text())
        self.config.set('pathadd',self.findChild(QLineEdit, "remote").text())
        self.config.set('path',self.findChild(QLineEdit, "local").text())
        self.config.set('pathtxt',self.findChild(QLineEdit, "script").text())

        self.config.save()
        self.emit('close')

    def changeRadio1(self):
        bool=self.findChild(QRadioButton, "remotebtn").isChecked()
        if bool:
            self.config.set('model','2')
        else:
            self.config.set('model', '1')


if __name__ =="__main__":
    import sys
    app = QApplication(sys.argv)
    window = QMainWindow()
    window.setWindowTitle('main')
    m=CiSetting(window,{1:23})
    m.show()
    # print(m.config)
    window.show()

    sys.exit(app.exec_())
    # CiSetting().ci_show("../ui/setting.ui")