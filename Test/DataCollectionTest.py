import DataCollection
import DataStructure
import threading

class SniffingThread(threading.Thread):
    def __init__(self, dc):
        self.dc = dc
        super(SniffingThread, self).__init__()
    
    def run(self):
        self.dc.work()

class ReadThread(threading.Thread):
    def __init__(self, data_queue):
        self.data_queue = data_queue
        super(ReadThread, self).__init__() 

    def run(self):
        while(1):
            var = self.data_queue.dequeue()
            print var

class NotifyThread(threading.Thread):
    def __init__(self, fn):
        self.fn = fn
        super(NotifyThread, self).__init__()
    
    def run(self):
        self.fn.work()
         
    

if __name__ == '__main__':
    package_list = DataStructure.DataList()
    file_list = DataStructure.DataList()
    dc = DataCollection.PackageSniffer('wlan0', 'tcp port 80', package_list)
    fn = DataCollection.FileNotifier('/var/www',r'\S+\.php|\S+\.inc|\S+\.php5',file_list)
    st = SniffingThread(dc)
    nt = NotifyThread(fn)
    rt1 = ReadThread(package_list)
    rt2 = ReadThread(file_list)
  
    rt1.start()
    rt2.start()
    nt.start()
    st.start()
    
