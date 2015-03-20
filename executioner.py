#encoding:utf-8
import iptc
import threading
import shutil
import random
import string
import smtplib
from email.mime.text import MIMEText

def release_ip(chain, rule):
    chain.delete_rule(rule)

alarm_type_description = ["Dangergous File upload!","SQL injection","XSS"]

class Executioner():
    def __init__(self, alarm_list, interface, punish_time, doubtful_dir):
        self.alarm_list = alarm_list
        self.interface = interface
        self.punish_time = punish_time
        self.doubtful_dir = doubtful_dir
    
    def work(self):
        table = iptc.Table(iptc.Table.FILTER)
        chain = iptc.Chain(table, "INPUT")
        exec '''print "Executioner ready!"'''
        while True:
            alarm = self.alarm_list.dequeue()
            new_file_name = ""
            if alarm[0] == 0:
                try:
                    new_file_name = self.doubtful_dir + alarm[1] + "_" + string.join(random.sample(['z','y','x','w','v','u','t','s','r','q','p','o','n','m','l','k','j','i','h','g','f','e','d','c','b','a'], 20)).replace(' ','') + "_" + alarm[3].replace("/","_")
                    shutil.move(alarm[3],new_file_name)
                    self.sendMail(alarm, new_file_name)
                except IOError:
                    pass
            elif alarm[0] == 1 or alarm[0] == 2:
                rule = iptc.Rule()
                rule.src = alarm[2]
                rule.in_interface = self.interface
                rule.protocol = "tcp"
                rule.target = rule.create_target("DROP")
                chain.append_rule(rule)
                threading.Timer(self.punish_time, release_ip, (chain, rule,)).start()
                self.sendMail(alarm, "")
            else:
                pass
            
    def sendMail(self, alarm, file_name):
        mailto_list=["laiqing3321568@qq.com"]
        mail_host="smtp.163.com"
        mail_user="laiqingquan.110@163.com"
        mail_pass="laiqingquan"
        mail_postfix="163.com"
        content = alarm_type_description[alarm[0]]+"\n"
        content = content + alarm[1] + "\n"
        if alarm[0] != 0:
            content = content + "From: " + alarm[2] + "\n"
        else:
            content = content + "Moved in:" + file_name + "\n"
        content = content + "Vulnerability: " + alarm[3] + "\n"
        content = content + "Vertor: " + alarm[4] + "\n" 
        me=mail_user+"<"+mail_user+"@"+mail_postfix+">"
        msg = MIMEText(content,_charset='utf-8')
        msg['Subject'] = "Server Alarm!"
        msg['From'] = me
        msg['To'] = ";".join(mailto_list)
        try:
            s = smtplib.SMTP()
            s.connect(mail_host)
            s.login(mail_user,mail_pass)
            s.sendmail(me, mailto_list, msg.as_string())
            s.close()
        except Exception, e:
            print str(e)

if __name__ == "__main__":
  table = iptc.Table(iptc.Table.FILTER)
  chain = iptc.Chain(table, "INPUT")
  for rule in chain.rules:
    chain.delete_rule(rule)
