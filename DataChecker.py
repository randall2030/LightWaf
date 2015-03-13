#encoding:utf-8
import threading
import re

SQLInjection_feature = r'''([\W][uU][nN][iI][oO][nN][\W])|(^[uU][nN][iI][oO][nN][\W])|([\W][sS][eE][lL][eE][cC][tT][\W][\s\S]+[\W][fF][rR][oO][mM][\W])|(^[sS][eE][lL][eE][cC][tT][\W][\s\S]+[\W][fF][rR][oO][mM][\W])|(^[aA][nN][dD][\W])|([\W][aA][nN][dD][\W])|(^[oO][rR][\W])|([\W][oO][rR][\W])|(^[eE][xX][eE][cC][\W])|([\W][eE][xX][eE][cC][\W])|(^[dD][rR][oO][pP][\W])|([\W][dD][rR][oO][pP][\W])|([\W][iI][nN][sS][eE][rR][tT] [iI][nN][tT][oO][\W])|(^[iI][nN][sS][eE][rR][tT] [iI][nN][tT][oO][\W])|([dD][bB][oO][\.])|([\W][\*][\W])|(')|(")|(--[\S]*)'''

XSS_feature = r'''([\w\W]*<[\w\W]*)|([\w\W]*\\u003C[\w\W]*)|([\w\W]*\\U0000003C[\w\W]*)|([\w\W]*&#60;[\w\W]*)|([\w\W]*&#x3C;[\w\W]*)|([\w\W]*\\x3C[\w\W]*)|([\w\W]*\\074[\w\W]*)|([\w\W]*%3C[\w\W]*)|(>)|([\w\W]*\\u003E[\w\W]*)|([\w\W]*\\U0000003E[\w\W]*)|([\w\W]*&#62;[\w\W]*)|([\w\W]*&#x3E;[\w\W]*)|([\w\W]*\\x3E[\w\W]*)|([\w\W]*\\076[\w\W]*)|([\w\W]*%3E[\w\W]*)|([\w\W]*\\u0022[\w\W]*)|([\w\W]*\\U00000022[\w\W]*)|([\w\W]*&#34;[\w\W]*)|([\w\W]*&#x22;[\w\W]*)|([\w\W]*\\x22[\w\W]*)|([\w\W]*\\042[\w\W]*)|([\w\W]*%22[\w\W]*)'''

dangerous_file_feature = r''''''

class PackageChecker:
    def __init__(self, data_list, alarm_list, SQLInjection_feature, XSS_feature ):
        self.data_list = data_list
        self.alarm_list = alarm_list
        self.SQLInjection_regex = re.compile(SQLInjection_feature)
        self.XSS_regex = re.compile(XSS_feature)

    def work(self):
        while True:
            data = self.data_list.dequeue()
            ct = PackageCheckingThread(data, self.alarm_list, self.SQLInjection_regex, self.XSS_regex)
            ct.start()


class PackageCheckingThread(threading.Thread):
    def __init__(self, data, alarm_list, sr, xr):
            self.data = data
            self.alarm_list = alarm_list
            self.SQLInjection_regex = sr
            self.XSS_regex = xr
            super(PackageCheckingThread, self).__init__()

    def run(self):
        if "GET" == self.data[1]:
            checking_data = self.data[3]
        elif "POST" == self.data[1]:
            checking_data = self.data[4]
        
        while True:
            if self.SQLInjection_regex.match(checking_data):
                alarm_type = 1
                break
            if self.XSS_regex.match(checking_data):
                alarm_type = 2
                break
            return

        new_element = []
        new_element.append(alarm_type)
        new_element.append(self.data[0])
        new_element.append(self.data[2])
        new_element.append(self.data[3])
        new_element.append(checking_data)
        self.alarm_list.enqueue(new_element) 
        return 
        
def check(str):
    a = re.compile(XSS_feature)
    if a.match(str):
        print True
    else:
        print False


if __name__ == '__main__':
    check("http://172.21.20.160/webbookshare/views/vmain.php?%3C")
