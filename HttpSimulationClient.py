
# -*- coding: utf-8 -*-

import urllib
import urllib.request

 
from PyQt5.QtWidgets import QApplication, QWidget, QMessageBox,QMainWindow
from PyQt5 import uic

from HttpSimulationClient_ui import *
import numpy as np
import sys
import json


class ClientMainWin(Ui_MainWindow):
   def __init__(self,mainWin):
        super(Ui_MainWindow, self).__init__()
        self.setupUi(mainWin)
        self.GetBtn.clicked.connect(self.get)
        self.PostBtn.clicked.connect(self.post)
        self.GetUrlText.setPlainText("http://192.168.1.33:8888/getShape")
        self.PostUrlText.setPlainText("http://192.168.1.33:8888/")
        
        jsondata = {'ssid':'xxxx','password':'xxxxxxxx','server_ip':'xxx.xxx.xxx.xxx'}
        jstr = json.dumps(jsondata)
        self.PostDataText.setPlainText(jstr)
        
   def get(self):
        geturl = self.GetUrlText.toPlainText();
        print(geturl)
        req = urllib.request.Request(geturl)
        print(req)

        try:
            res_data = urllib.request.urlopen(req)
            res = res_data.read()
            print(res)
        except IOError:
            print('http get error')
   def post(self):
        
        posturl = self.PostUrlText.toPlainText();
        jsondata = self.PostDataText.toPlainText();
        jsondata=bytes(jsondata,'utf8')
        try:
            req = urllib.request.Request(posturl)
            req.add_header('Content-Type', 'application/json')
       
            res_data = urllib.request.urlopen(req,jsondata)
            res = res_data.read()
            print(res)
        except IOError:
            print('http post error')
def main():
    app = QApplication(sys.argv)
    mainWin = QMainWindow()
    #win = uic.loadUi("HttpSimulationClient_ui.ui")
    win = ClientMainWin(mainWin)
    mainWin.show()
    
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()