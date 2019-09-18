
# -*- coding: utf-8 -*-

import urllib
 
from PyQt5.QtWidgets import QApplication, QWidget, QMessageBox,QMainWindow
from PyQt5 import uic

from HttpSimulationClient_ui import *
import numpy as np
import sys
import json


def HttpGet():
    url = "http://192.168.81.16/cgi-bin/python_test/test.py?ServiceCode=aaaa"

    req = urllib.request.Request(url)
    print(req)

    res_data = urllib.request.urlopen(req)
    res = res_data.read()
    print(res)

def HttpPost():
    jsondata = {'ssid':'xxxx','password':'xxxxxxxx',"server_ip":"xxx.xxx.xxx.xxx"}
    jsondata_urlencode = urllib.urlencode(jsondata)

    requrl = "http://192.168.81.16/cgi-bin/python_test/test.py"

    req = urllib.request.Request(url = requrl,data =jsondata_urlencode)
    print(req)

    res_data = urllib.request.urlopen(req)
    res = res_data.read()
    print(res)


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

        res_data = urllib.request.urlopen(req)
        res = res_data.read()
        print(res)
   def post(self):
        
        posturl = self.PostUrlText.toPlainText();
        jsondata = self.PostDataText.toPlainText();
        jsondata=bytes(jsondata,'utf8')

        req = urllib.request.Request(posturl)
        req.add_header('Content-Type', 'application/json')
       
        res_data = urllib.request.urlopen(req,jsondata)
        res = res_data.read()
        print(res)
def main():
    app = QApplication(sys.argv)
    mainWin = QMainWindow()
    #win = uic.loadUi("HttpSimulationClient_ui.ui")
    win = ClientMainWin(mainWin)
    mainWin.show()
    
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()