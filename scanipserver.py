from ipspy import ipspy
from scans import base
import os
import time

class ScanServer:
    def __init__(self):
        self.fold = ipspy.saveIpsection()
        self.fold={'CN': 15, 'HK': 3, 'PK': 0, 'AU': 0, 'JP': 2, 'IN': 0}
        self.keys = list(self.fold.keys())
        self.cur = ''
        # pass

    def getFile(self):
        if self.cur != '':
            path = "ip/" + self.cur + "-" + str(self.fold[self.cur]) + ".txt"
            if os.path.exists(path):os.remove(path)
            self.fold[self.cur] -= 1
            if self.fold[self.cur]<=-1:
                self.fold.pop(self.cur)
            self.keys = list(self.fold.keys())
            print(path)
        if len(self.keys) <= 0:
            return None

        self.cur = self.keys[0]
        path="ip/" + self.cur + "-" + str(self.fold.get(self.cur)) + ".txt"
        if os.path.exists(path):
            file = open(path, 'r')
            return file.readline()
        else:
            return self.getFile()

    def goOn(self):
        path='ip'
        for f in os.listdir('ip'):
            with open(path+"/"+f) as fk:
                pl=fk.readline(1024)
                while pl:
                    pl = fk.readline(1024)
                    pl=pl.strip("\n")
                    self.sartScan(pl,f)
            os.remove(path+"/"+f)


    def sartScan(self,line,name):
        opts = {}
        opts['-p'] = 8080
        opts['-i'] = line
        opts['-t'] = 50
        opts['-s'] = "re/"+name
        if not os.path.exists("re"):os.makedirs('re')
        sc = base.Scans(opts)
        sc.setB(self.scanBack)
        sc.start()


    def scanBack(self,savefile):
        if len(self.keys) <= 0:
            return None
        self.begin()

    def begin(self):
        line = self.getFile()
        if line is not None: self.sartScan(line)

if __name__ == '__main__':
    ScanServer().goOn()
    # ScanServer().begin()
#
# fold=ipspy.saveIpsection()
# # fold={'CN': 10, 'HK': 1, 'PK': 0, 'AU': 0, 'JP': 2, 'IN': 0}
# keys = list(fold.keys())
# cur=''
#
# def getFile(cur):
#     if cur != '':
#         path="ip/" + cur + "-" + str(fold[cur]) + ".txt"
#         os.remove(path)
#     if len(keys)<=0 :
#         return 0
#     cur = keys.pop()
#     file = open("ip/" + cur + "-" + str(fold[cur]) + ".txt", 'r')
#     return file.readline()
#
# def sartScan(line):
#     opts = {}
#     opts['-p'] = 8080
#     opts['-i'] = line
#     opts['-t'] = 50
#     opts['-s'] = 'te.txt'
#     sc = base.Scans(opts)
#     sc.setB(scanBack)
#     sc.start()
#
# def scanBack(savefile):
#     if len(keys)<=0 :
#         return 0
#     line = getFile(cur)
#     if line != 0: scanBack(line)
#
# def begin():
#     line=getFile(cur)
#     if line !=0:scanBack(line)
