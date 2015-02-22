#coding:UTF-8

class Ui():
    def __init__(self,request,data):
        self.__request=request
    def index(self):
        print '123',self.__request['getArgv'].get(2,"unknow")
    def hello(self):
        print "hello"
        