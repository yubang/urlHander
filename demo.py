#coding:UTF-8

"""
一个demo
"""

from urlHander import UrlHander

def index():
    dao=UrlHander()
    result=dao.dealAccess("/ui/ui/hello")
    print result.DATA
    
    result=dao.dealAccess("/ui/ui/__index")
    print result.DATA
    
if __name__ == "__main__":
    index()