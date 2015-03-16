#coding:UTF-8

"""
一个demo
"""

from urlHander import UrlHander
from test import Test

def index():
    dao=UrlHander()
    
    dao.setClassPath("classes")
    #dao.setDebug(False)
    dao.addBeforeExecute(Test(None).index)
    dao.load()
    
    result=dao.dealAccess("/ui/ui/hello")
    print result.DATA
    
    result=dao.dealAccess("/ui/ui/__index")
    print result.DATA
    
if __name__ == "__main__":
    index()
