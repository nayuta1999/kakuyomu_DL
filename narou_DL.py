#coding:utf-8
import requests

class narou_DL():
    url = ""
    def __init__(self,url):
        self.url = url
    def getURL(self):
        return self.url
    def getContents(self):