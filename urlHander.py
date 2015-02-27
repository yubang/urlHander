#coding:UTF-8

"""
url自动化映射函数
@author:yubang
"""


import os,re,inspect,urllib,traceback


class ClearPycFile():
    def __init__(self,debug,path):
        self.__debug=debug
        self.__index(path)
    def __index(self,path):
        if(os.path.exists(path) and os.path.isdir(path)):
            fps=os.listdir(path)
            for fp in fps:
                filePath=path+'/'+fp
                if(os.path.isfile(filePath)):
                    if(re.search(r'.pyc$',filePath)):
                        os.remove(filePath)
                        if(self.__debug):
                            print 'delete:'+filePath
                else:
                    self.__index(filePath)

class Action():
    "action类"
    def __init__(self,request,data):
        self.__templatePath=request['templatePath']
        self.__debug=request['debug']
        self.__actionPath=request['actionPath']
        self.DATA=""
        self.STATUS=['200','ok']
        if(self.__debug):
            print "load class Action"
    def __getContentFromFile(self,actionPath=None):
        "从文件读取内容"
        if(actionPath==None):
            actionPath=self.__actionPath
        fp=open(self.__templatePath+actionPath,'r')
        text=fp.read()
        fp.close()
        return text
    def __render(self,data):
        "渲染模板"
        return data
    def _write(self,data):
        if(type(data).__name__=="unicode"):
            data=data.encode("UTF-8")
        self.DATA=self.DATA+data
    def _display(self,path=None):
        text=self.__getContentFromFile(path)
        self.DATA=self.__render(text)
        
class UrlHander():
    "url自动化映射类"
    def __init__(self):
        self.__setDefaultConfig()
        temp=ClearPycFile(self.__debug,self.__classPath)
        self.__loadAllClass()
    def __log(self,data):
        "调试信息输出"
        if(self.__debug):
            print data
    def __notFoundMethod(self):
        self.__log("404 not found!")
        return "404"
    def __serviceErrorMethod(self):
        self.__log("server error!")
        return "500"
    def __setDefaultConfig(self):
        "设置默认"
        nowPath=os.path.dirname(os.path.realpath(__file__))+"/"
        self.__classPath=nowPath+"lib"
        self.__templatePath=nowPath+"template"
        self.__debug=True
        self.__urlObjMap={}
        self.__notFound=self.__notFoundMethod
        self.__serviceError=self.__serviceErrorMethod
        self.__beforeExecuteMethod=[]
        self.__afterExecuteMethod=[]
    def __getObjFromModule(self,module,className):
        "从模块获取类"
        for temp in dir(module):
            if(inspect.isclass(getattr(module,temp))):
                if(temp==className):
                    return getattr(module,temp)
            elif(inspect.ismodule(getattr(module,temp))):
                return self.__getObjFromModule(getattr(module,temp),className)
    def __loadClassInFile(self,fpPath):
        "从文件加载类"
        tempPath=fpPath.replace(self.__classPath,"")
        tempPath=tempPath[0:len(tempPath)-3]
        tempPath=tempPath.replace("/",".")
        
        libNames=re.split(r'[\\\/]',self.__classPath)
        libName=libNames[len(libNames)-1]
        
        modulePath=libName+tempPath
        tempClassNames=modulePath.split(".")
        className=tempClassNames[len(tempClassNames)-1]
        dirName=tempClassNames[len(tempClassNames)-2]
        
        index=0
        newClassName=""
        for temp in className:
            if(index==0):
                newClassName=temp.upper()
            else:
                newClassName=newClassName+temp
            index=index+1
        
        #加载模块
        m=__import__(modulePath)
        m=getattr(m,dirName)
        #获取类
        obj=self.__getObjFromModule(m,newClassName)
        
        #保存对象
        if(obj!=None):
            urlKey=tempPath.replace(".","/")
            self.__urlObjMap[urlKey]=obj
            #输出调试
            self.__log(u"加载类："+modulePath+"."+newClassName)
        else:
            self.__log(u"无法加载类："+modulePath+"."+newClassName)
    def __loadAllClassInAllDirs(self,dirPath):
        "加载文件夹下的所有py文件"
        fps=os.listdir(dirPath)
        for fp in fps:
            fpPath=dirPath+"/"+fp
            if(re.search(r'\.py$',fp)):#获取py文件
                if(fp!="__init__.py"):#过滤__init__.py文件
                    self.__loadClassInFile(fpPath)
    def __loadAllClass(self):
        "加载所有的类"
        fps=os.listdir(self.__classPath)
        for temp in fps:#获取类目录下的所有文件夹
            dirPath=self.__classPath+"/"+temp
            if(os.path.isdir(dirPath)):
                self.__loadAllClassInAllDirs(dirPath)
    def __useMethodFromUrl(self,method,data):
        "根据url调用函数"
        try:
            
            for temp in self.__beforeExecuteMethod:
                result=temp(data)
                if(result!=None):
                    return result
            
            result=method()
            
            for temp in self.__afterExecuteMethod:
                result=temp(data,result)
            
            return result
        except:
            if(self.__debug):
                print traceback.format_exc()
            return self.__serviceError()
    def __dealBadFunction(self,methodName):
        "防止调用特别函数"
        if(methodName=="__init__"):
            return "index"
        elif(methodName=="__del__"):
            return "index"
        else:
            return methodName
    def addBeforeExceute(self,method):
        "添加中间方法，在函数执行前"
        self.__beforeExecuteMethod.append(method)
    def addAfterExceute(self,method):
        "添加中间方法，在函数执行后"
        self.__afterExecuteMethod.append(method)
    def dealAccess(self,fullUrl,data=None):
        "处理访问"
        url=fullUrl
        urls=url.split("/")
        if(len(urls)==2):
            key="/index/index"
            methodName=urls[1]
        elif(len(urls)==3):
            key="/index/"+urls[1]
            methodName=urls[2]
        elif(len(urls)==4):
            key="/"+urls[1]+"/"+urls[2]
            methodName=urls[3]
        else:
            key="/"+urls[1]+"/"+urls[2]
            methodName=urls[3]
            index=0
            i=4
            while(i<len(urls)):
                getArgv[index]=urls[i]
                index=index+1
                i=i+1
        
        methodName=self.__dealBadFunction(methodName)
        
        if(methodName==""):
            methodName="index"
        
        #输出执行结果
        if(self.__debug):
            self.__log(u"要访问的路径："+fullUrl)
            self.__log(u"映射函数："+key+"/"+methodName)
        
        if(self.__urlObjMap.has_key(key)):
            obj=self.__urlObjMap[key]
            templatePath=self.__templatePath
            debug=self.__debug
            actionPath=key+"/"+methodName+".html"
            request={'templatePath':self.__templatePath,"debug":debug,'actionPath':actionPath}
            try:
                dao=obj(request,data)
                method=getattr(dao,methodName)
                return self.__useMethodFromUrl(method,data)
            except:
                "触发404"
                return self.__notFound()
        else:
            return self.__notFound()