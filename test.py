#encoding:utf-8
import judge
import DataStructure
import patrol
import executioner

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

    package_patrol = patrol.PackagePatrol('wlan0', 'tcp port 80', package_list)
    file_patrol = patrol.FilePatrol('/var/www',r'(\S+\.php)|(\S+\.inc)|(\S+\.php5)|(\S+\.jsp)',file_list)
    package_judge = judge.PackageJudge(package_list, alarm_list)
    file_judge = judge.FileJudge(file_list, alarm_list)
    execution = executioner.Executioner(alarm_list, "wlan0", 20, "/home/qero/毕设/attack_vertor/")
    
    package_patrol_thread = WorkerThread(package_patrol)
    file_patrol_thread = WorkerThread(file_patrol)
    package_judge_thread = WorkerThread(package_judge)
    file_judge_thread = WorkerThread(file_judge)
    executioner_thread = WorkerThread(execution)

    rt1 = ReadThread(alarm_list)
    rt2 = ReadThread(file_list)
    rt3 = ReadThread(package_list)
    
    file_patrol_thread.start()
    time.sleep(1)
    package_patrol_thread.start()

    package_judge_thread.start()
    file_judge_thread.start()

    #rt1.start()
    executioner_thread.start()
