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

#you can change the default config at here
config = {"web_root":"/var/www",
          "interface":"wlan0",
          "filter":"tcp port 80",
          "file_suffix":r"(\S+\.php)|(\S+\.inc)|(\S+\.php5)|(\S+\.jsp)",
          "punish_time":30,
          "file_prison":"/home/qero/毕设/attack_vertor/",
          "mail_host":"smtp.163.com",
          "mail_user":"laiqingquan.110@163.com",
          "mail_pass":"laiqingquan",
          "mail_postfix":"163.com",
          "mailto_list":["laiqing3321568@qq.com"],
         }

if __name__ == '__main__':
    package_list = DataStructure.DataList()
    file_list = DataStructure.DataList()
    alarm_list = DataStructure.DataList()

    package_patrol = patrol.PackagePatrol(config['interface'], config['filter'], package_list)
    file_patrol = patrol.FilePatrol(config['web_root'], config['file_suffix'],file_list)
    package_judge = judge.PackageJudge(package_list, alarm_list)
    file_judge = judge.FileJudge(file_list, alarm_list)
    execution = executioner.Executioner(alarm_list, config['interface'], config['punish_time'], config['file_prison'], config['mail_host'], config['mail_user'], config['mail_pass'], config['mail_postfix'], config['mailto_list'], True)
    
    package_patrol_thread = WorkerThread(package_patrol)
    file_patrol_thread = WorkerThread(file_patrol)
    package_judge_thread = WorkerThread(package_judge)
    file_judge_thread = WorkerThread(file_judge)
    executioner_thread = WorkerThread(execution)

   
    file_patrol_thread.start()
    time.sleep(1)
    package_patrol_thread.start()
    package_judge_thread.start()
    file_judge_thread.start()
    executioner_thread.start()
    
