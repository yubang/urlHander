#coding:UTF-8

from urlHander import Action

class Ui(Action):
    def __init__(self,request,data):
        Action.__init__(self,request,data)
        self.__data=data
    def index(self):
        self._write(u"测试")
        return self
    def hello(self):
        print "hello"
        self._display()
        return self
        