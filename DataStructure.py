# -*- coding: utf-8 -*-
import threading
import hashlib

#可线程并发列表类DataList：
#	互斥锁lock，
#	同步锁semaphore,
#		数据data，
#	入列方法enqueue（）
#	出列方法dequeue（）
class DataList:
    def __init__(self):
        self.lock = threading.Lock()
        self.semaphore = threading.Semaphore(0)
        self.data = []
    def dequeue(self):
        if  self.semaphore.acquire():
            if self.lock.acquire():
                res = self.data[0]
                del self.data[0]
                self.lock.release()
                return res
    def enqueue(self, var):
        if self.lock.acquire():
            self.data.append(var)
            self.semaphore.release()
            self.lock.release()

#可线程并发字典类 DataDictionary：
#	互斥锁lock，
#	数据data,
#	从文件读字典方法setDictionary（）
#	添加元素方法set（）
#	查看元素的值对方法get（）
#	删除指定元素方法delete（）
#	清空字典方法clear（）
class DataDictionary:
    def __init__(self):
        self.data = {}
        self.lock = threading.Lock()
   
    def setDictionaryFromFile(self, path):
        f = open(path)
        while True:
            lines = f.readlines(100000)
            if not lines:
                break
            for line in lines:
                self.data[hashlib.md5(line.strip().encode('utf-8')).hexdigest()] = True
 
    def set(self, key):
        if self.lock.acquire():
            self.data.setdefault(key,1)
            self.lock.release()
    
    def get(self, key):
        if self.lock.acquire():
            if self.data.has_key(key):
                return self.data[key]
            self.data.release()
    
    def delete(self, key):
        if self.lock.acquire():
            self.data.pop(key)
            self.data.release()

    def clear(self, key):
        if self.lock.acquire():
            self.data.clear()
            self.lock.release()


