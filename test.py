# -*- coding: utf-8 -*-
import threading
import time
import DataStructure

class WriteThread(threading.Thread):
    def __init__(self, data_queue):
        self.data_queue = data_queue
        super(WriteThread, self).__init__() 
    def run(self):
        n = 100
        while n != 0:
            var = []
            n = n - 1;
            var.append(n)
            var.append("get")
            var.append("127.0.0.1")
            var.append("www.baidu.com")
            var.append("password = ASDASDASDSAFFWEFWEFRV")
            self.data_queue.enqueue(var)
            print "push Id = %d" %n		
			
class readThread(threading.Thread):
    def __init__(self, n, data_queue):
        self.data_queue = data_queue
        self.n = n
        super(readThread, self).__init__() 

    def run(self):
        while(1):
            var = self.data_queue.dequeue()
            print "\npop id = %d" %var[0] + " by reader %d" %self.n

if __name__ == '__main__':
    data_queue = DataStructure.DataList()
    a = WriteThread(data_queue)
    b = readThread(1, data_queue)
    c = readThread(2, data_queue)
    dd = DataStructure.DataDictionary()
    

    b.start()
    a.start()
    c.start()
    dd.setDictionaryFromFile("WhiteList/WhiteList")
    print dd.data
    
