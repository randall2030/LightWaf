import pcap
import dpkt
import sys
import re
import DataStructure
import threading
import datetime
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import time

class PackageSniffer:
    def __init__(self, interface, package_filter, package_data_list):
        self.interface = interface
        self.package_filter = package_filter
        self.package_data_list = package_data_list

    def work(self) :
        sniffer = pcap.pcapObject()
        net, mask = pcap.lookupnet(self.interface)
        sniffer.open_live(self.interface, 1600, 0, 100)
        sniffer.setfilter(self.package_filter, 0, 0)
        try:
            while True:
                temp = sniffer.next()
                if temp:
                    ht = HandlePackageDataThread(temp[0],temp[1],temp[2],self.package_data_list)
                    ht.start()
                time.sleep(0.001)
        except KeyboardInterrupt:
            print '%s' % sys.exc_type
            print 'shutting down'
            print '%d packets received, %d packets dropped, %d packets dropped by interface' % sniffer.stats()
    

class HandlePackageDataThread(threading.Thread):
    def __init__(self, pktlen, data, timestamp, package_data_list):
        self.pktlen = pktlen
        self.data = data
        self.timestamp = timestamp
        self.package_data_list = package_data_list
        super(HandlePackageDataThread, self).__init__()

    def run(self):
        if not self.data:
            return
        ether_package = dpkt.ethernet.Ethernet(self.data)
        package_time = datetime.datetime.utcfromtimestamp(self.timestamp)
        package_time = package_time.strftime("%Y-%m-%d %H:%M:%S")
        if ether_package.data.__class__.__name__ == "IP":
            ip_package = ether_package.data
            src_ip = '%d.%d.%d.%d' % tuple(map(ord,list(ip_package.src)))
            if ether_package.data.data.__class__.__name__ == 'TCP':
                tcp_package = ether_package.data.data
                if tcp_package.dport == 80:
                    if tcp_package.data:
                        http_package = dpkt.http.Request(tcp_package.data)
                        pre = "^/.*$"
                        if re.match(pre, http_package.uri):
                            http_method = http_package.method
                            http_url = "http://" + http_package.headers["host"] + http_package.uri
                            http_body = http_package.body
                            new_element = []
                            new_element.append(package_time)
                            new_element.append(http_method)
                            new_element.append(src_ip)
                            new_element.append(http_url)
                            new_element.append(http_body)
                            self.package_data_list.enqueue(new_element)

class FileNotifier():
    def __init__(self, path, suffix, file_data_list):
        self.path = path
        self.suffix = suffix
        self.file_data_list = file_data_list

    def work(self):
        event_handler = FileEventHandler(self.suffix, self.file_data_list)
        observer = Observer()
        observer.schedule(event_handler, self.path,recursive=True)
        observer.start()
        #try:
        #    while True:
        #        pass
        #except KeyboardInterrupt:
        #    observer.stop()
        #observer.join()

    
class FileEventHandler(FileSystemEventHandler):
    def __init__(self, suffix, file_data_list):
        self.file_data_list = file_data_list
        self.pattern = re.compile(suffix)
        super(FileEventHandler, self).__init__()

    def on_modified(self, event):
        (event_type, src_path, is_dir) = event.key
        if not is_dir:
            if self.pattern.match(src_path):
                temp = HandleFileDataThread(event_type, src_path, is_dir, time.strftime('%Y-%m-%d %H:%M:%S'), self.file_data_list)
                temp.start()
               
 
    def on_moved(self, event):
        (event_type, src_path, is_dir) = event.key
        if not is_dir:
            if self.pattern.match(src_path):
                temp = HandleFileDataThread(event_type, src_path, is_dir, time.strftime('%Y-%m-%d %H:%M:%S'), self.file_data_list)
                temp.start()

    
    def on_created(self, event):
        (event_type, src_path, is_dir) = event.key
        if not is_dir:
            if self.pattern.match(src_path):
                temp = HandleFileDataThread(event_type, src_path, is_dir, time.strftime('%Y-%m-%d %H:%M:%S'), self.file_data_list)
                temp.start()

    
    def on_deleted(self, event):
        (event_type, src_path, is_dir) = event.key

class HandleFileDataThread(threading.Thread):
    def __init__(self, event_type, src_path, is_dir, time, file_data_list):
        self.event_type = event_type
        self.src_path = src_path
        self.is_dir = is_dir
        self.time = time
        self.file_data_list = file_data_list
        super(HandleFileDataThread, self).__init__()

    def run(self):
        new_element = []
        new_element.append(self.time)
        new_element.append(self.is_dir)
        new_element.append(self.event_type)
        new_element.append(self.src_path)
        self.file_data_list.enqueue(new_element)



if __name__ == '__main__':
    #package_list = DataStructure.DataList()
    #dc = PackageSniffer('wlan0', 'tcp port 80', package_list)    
    #dc.work()
    
    file_data_list = DataStructure.DataList()
    fn = FileNotifier('/var/www',r'\S+\.php|\S+\.inc|\S+\.php5',file_data_list)
    fn.work()
