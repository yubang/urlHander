#coding:UTF-8

"""
一个demo
"""

from urlHander import UrlHander

def index():
    dao=UrlHander()
    dao.dealAccess("/ui/ui/__init__(None,None)")
    
if __name__ == "__main__":
    index()