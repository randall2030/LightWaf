#encoding:utf-8
from Tkinter import *
import tkFont
import sys
import threading
import DataStructure
import patrol
import executioner
import judge
import time

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


class WorkerThread(threading.Thread):
    def __init__(self, t):
        self.t = t
        super(WorkerThread, self).__init__()
    
    def run(self):
        self.t.work()


class listBox_stdout():
    def __init__(self, list_box):
        self.list_box = list_box
    
    def write(self, string):
        if (len(string) != 1):
            self.list_box.insert(0, string)
class UI():
    def __init__(self, root):
        self.root = root
        self.frame = Frame(root)
        self.default_font = tkFont.Font(family="Helvetica",size=12,weight="bold")
        self.bg_color = "#888888"
        self.out = sys.stdout

    
    def show_stop_frame(self):
        self.frame.destroy()
        self.frame = Frame(self.root, height=399, width=599, bg = self.bg_color)
        self.frame.grid_propagate(False)
        self.frame.grid()

        l_web_root = Label(self.frame, text = "Web Root:", bg = self.bg_color, font = self.default_font)
        l_web_root.grid(row = 0, column = 1, sticky = "e")
        e_web_root = Entry(self.frame, bd = 5, text = "abc")
        e_web_root.grid(row = 0, column = 2)

        l_interface = Label(self.frame, text = "Interface:", bg = self.bg_color, font = self.default_font )
        l_interface.grid(row = 1, column = 1, sticky = "e")
        e_interface = Entry(self.frame, bd = 5)
        e_interface.grid(row = 1, column = 2)
    
        l_filter = Label(self.frame, text = "Filter:", bg = self.bg_color, font = self.default_font)
        l_filter.grid(row = 2, column = 1, sticky = "e")
        e_filter = Entry(self.frame, bd = 5)
        e_filter.grid(row = 2, column = 2)

        l_file_suffix = Label(self.frame, text = "File Suffix:", bg = self.bg_color, font = self.default_font)
        l_file_suffix .grid(row = 3, column = 1, sticky = "e")
        e_file_suffix  = Entry(self.frame, bd = 5)
        e_file_suffix .grid(row = 3, column = 2)

   
        l_punish_time = Label(self.frame, text = "Punish Time:", bg = self.bg_color, font = self.default_font)
        l_punish_time.grid(row = 4, column = 1, sticky = "e")
        e_punish_time = Entry(self.frame, bd = 5)
        e_punish_time.grid(row = 4, column = 2)

        l_file_prison = Label(self.frame, text = "File Prison:", bg = self.bg_color, font = self.default_font)
        l_file_prison.grid(row = 5, column = 1, sticky = "e")
        e_file_prison = Entry(self.frame, bd = 5)
        e_file_prison.grid(row = 5, column = 2)

        l_gap = Label(self.frame, text = "                  ", bg = self.bg_color, font = self.default_font)
        l_gap.grid(row = 0, column = 3)    

        l_mail_host = Label(self.frame, text = "Mail Host;", bg = self.bg_color, font = self.default_font)
        l_mail_host.grid(row = 0, column = 4, sticky = "e")
        e_mail_host = Entry(self.frame, bd = 5)
        e_mail_host.grid(row = 0, column = 5)

        l_mail_user = Label(self.frame, text = "Mail User:", bg = self.bg_color, font = self.default_font)
        l_mail_user.grid(row = 1, column = 4, sticky = "e")
        e_mail_user = Entry(self.frame, bd = 5)
        e_mail_user.grid(row = 1, column = 5)

        l_mail_pass = Label(self.frame, text = "Mail Pass:", bg = self.bg_color, font = self.default_font)
        l_mail_pass.grid(row = 2, column = 4, sticky = "e")
        e_mail_pass = Entry(self.frame, bd = 5)
        e_mail_pass.grid(row = 2, column = 5)

        l_mail_postfix = Label(self.frame, text = "Mail Postfix:", bg = self.bg_color, font = self.default_font)
        l_mail_postfix.grid(row = 3, column = 4, sticky = "e")
        e_mail_postfix= Entry(self.frame, bd = 5)
        e_mail_postfix.grid(row = 3, column = 5)

        l_mailto = Label(self.frame, text = "Mail To:", bg = self.bg_color, font = self.default_font)
        l_mailto.grid(row = 4, column = 4, sticky = "e")
        e_mailto = Entry(self.frame, bd = 5)
        e_mailto.grid(row = 4, column = 5)
    
        is_definse_dos = IntVar()
        cb_definse_dos = Checkbutton(self.frame, text = "  Definse  Dos  ", font = self.default_font, bg = self.bg_color, variable = is_definse_dos, onvalue = 1, offvalue = 0, bd = 5)
        cb_definse_dos.grid(row = 5, column = 5)

        l_gap.grid(row = 6, column = 3) 
        b_start = Button(self.frame, text ="Start", command = self.start, font = tkFont.Font(family="Helvetica",size=26,weight="bold"), bg = self.bg_color, bd = 5)
        b_start.grid(row = 7, column = 2) 

        root.mainloop()


    def show_start_frame(self):
        self.frame.destroy()
        self.frame = Frame(root, height=399, width=599, bg = self.bg_color)
        self.frame.grid_propagate(False)
        self.frame.grid()

        list_box = Listbox(self.frame, height = 23, width = 60)
        list_box.grid(row = 0, column = 0, columnspan=3, rowspan=5)
        rso = listBox_stdout(list_box)
        sys.stdout = rso

        l_gap = Label(self.frame, text = "       ", bg = self.bg_color, font = self.default_font)
        l_gap.grid(row = 0, column = 4)        

        b_stop = Button(self.frame, text ="Stop", command = self.stop, font = tkFont.Font(family="Helvetica",size=26,weight="bold"), bg = self.bg_color, bd = 5)
        b_stop.grid(row = 0, column = 5) 
            

    def start(self):
        self.show_start_frame()
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
        root.mainloop()

    
    def stop(self):
        sys.stdout = self.out
        self.root.destroy()
        

if __name__ == "__main__":
    root = Tk()
    root.title("WAF")
    gui = UI(root)
    gui.show_stop_frame()
    
