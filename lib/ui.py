from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi

class CiQDialog(QDialog):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        # self.ci_init(*arg,**karg)

    def ci_init(self,*args,**kwargs):
        pass

    def __ci_show(self):
        pass

    def ci_show(self,ui):
        loadUi(ui,self)
        super().show()
        self.__ci_show()


class CiLogin(CiQDialog):

    def __init__(self):
        super().__init__()

    def __ci_show(self):
        pass


class CiRegister(CiQDialog):

    def __init__(self):
        super().__init__()


class CiSetting(CiQDialog):

    def ci_init(self,con):
        self.config = con
        self.setWindowTitle("配置数据")
        self.setModal(True)
        self.ci_show('ui/setting.ui')

    def __ci_show(self):
        self.findChild(QLineEdit, "mainurl").setText(self.config.get('mainurl'))
        self.findChild(QLineEdit, "remote").setText(self.config.get('pathadd'))
        self.findChild(QLineEdit, "local").setText(self.config.get('path'))
        self.findChild(QLineEdit, "script").setText(self.config.get('pathtxt'))
        self.findChild(QRadioButton, "remotebtn").toggled.connect(self.changeRadio1)

    def closeEvent(self, QCloseEvent):
        self.config.save()

    def changeRadio1(self):
        bool=self.findChild(QRadioButton, "remotebtn").isChecked()
        if bool:
            self.config.set('model','2')
        else:
            self.config.set('model', '1')


if __name__ =="__main__":
    CiSetting().ci_show("/ui/setting.ui")