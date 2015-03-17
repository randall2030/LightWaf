import DataChecker
import DataStructure
import DataCollection
import threading
import time

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
    notifier = DataCollection.FileNotifier('/var/www',r'(\S+\.php)|(\S+\.inc)|(\S+\.php5)|(\S+\.jsp)',file_list)
    pack_checker = DataChecker.PackageChecker(package_list, alarm_list)
    file_checker = DataChecker.FileChecker(file_list, alarm_list)
    
    sniff_thread = WorkerThread(sniffer)
    notify_thread = WorkerThread(notifier)
    pack_check_thread = WorkerThread(pack_checker)
    file_check_thread = WorkerThread(file_checker)
    rt1 = ReadThread(alarm_list)
    rt2 = ReadThread(file_list)
    rt3 = ReadThread(package_list)
  
    rt1.start()
    notify_thread.start()
    time.sleep(1)
    sniff_thread.start()
    pack_check_thread.start()
    file_check_thread.start()
