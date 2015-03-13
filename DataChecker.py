#encoding:utf-8
import threading
import re

SQLInjection_feature = r'''([\W][uU][nN][iI][oO][nN][\W])|(^[uU][nN][iI][oO][nN][\W])|([\W][sS][eE][lL][eE][cC][tT][\W][\s\S]+[\W][fF][rR][oO][mM][\W])|(^[sS][eE][lL][eE][cC][tT][\W][\s\S]+[\W][fF][rR][oO][mM][\W])|(^[aA][nN][dD][\W])|([\W][aA][nN][dD][\W])|(^[oO][rR][\W])|([\W][oO][rR][\W])|(^[eE][xX][eE][cC][\W])|([\W][eE][xX][eE][cC][\W])|(^[dD][rR][oO][pP][\W])|([\W][dD][rR][oO][pP][\W])|([\W][iI][nN][sS][eE][rR][tT] [iI][nN][tT][oO][\W])|(^[iI][nN][sS][eE][rR][tT] [iI][nN][tT][oO][\W])|([dD][bB][oO][\.])|([\W][\*][\W])|(')|(")|(--[\S]*)'''
XSS_feature = r""
dangerous_file_feature = r""


class PackageChecker:
    def __init__(self, data_list, report_list, SQLInjection_feature, XSS_feature ):
        self.data_list = data_list
        self.report_list = report_list
        self.SQLInjection_regex = re.compile(SQLInjection_feature)
        self.XSS_regex = re.compile(XSS_feature)

    def work(self):
        while True:
            data = self.data_list.dequeue()
            ct = PackageCheckingThread(data, self.report_list, self.SQLInjection_regex, self.XSS_regex)
            ct.start()


class PackageCheckingThread(threading.Thread):
    def __init__(self, data, report_list, sr, xr):
            self.data = data
            self.report_list = report_list
            self.SQLInjection_regex = sr
            self.XSS_regex = xr

    def run(self):
        if "GET" == self.data[1]:
            checking_data = self.data[3]
        elif "POST" == self.data[1]:
            checking_data = self.data[4]

        if self.SQLInjection_regex.match(checking_data):
            pass
        
        
def check(str):
    a = re.compile(SQLInjection_feature)
    if a.match(str):
        print True
    else:
        print False


if __name__ == '__main__':
    pass
