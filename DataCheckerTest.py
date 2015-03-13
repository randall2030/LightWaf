import DataChecker
import DataStructure
import DataCollection
import threading

class WorkerThread(threading.Thread):
    def __init__(self, t):
        self.t = t
        super(WorkerThread, self).__init__()
    
    def run(self):
        self.t.work()

class ReadThread(threading.Thread):
    def __init__(self, data_queue):
        self.data_queue = data_queue
        super(ReadThread, self).__init__() 

    def run(self):
        while(1):
            var = self.data_queue.dequeue()
            print var

if __name__ == '__main__':
    package_list = DataStructure.DataList()
    file_list = DataStructure.DataList()
    alarm_list = DataStructure.DataList()
    sniffer = DataCollection.PackageSniffer('wlan0', 'tcp port 80', package_list)
    notifier = DataCollection.FileNotifier('/var/www',r'\S+\.php|\S+\.inc|\S+\.php5',file_list)
    checker = DataChecker.PackageChecker(package_list, alarm_list, DataChecker.SQLInjection_feature, DataChecker.XSS_feature)
    
    sniff_thread = WorkerThread(sniffer)
    notify_thread = WorkerThread(notifier)
    check_thread = WorkerThread(checker)
    rt1 = ReadThread(alarm_list)
    rt2 = ReadThread(file_list)
    rt3 = ReadThread(package_list)
  
    rt1.start()
    rt2.start()
    sniff_thread.start()
    notify_thread.start()
    check_thread.start()
