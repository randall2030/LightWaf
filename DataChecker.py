#encoding:utf-8
import threading
import re

SQLInjection_feature = r'''(\bunion\b)|(\bselect\b[\s\S]+\bfrom\b)|(\band\b)|(\bor\b)|(\bexec\b)|(\bdrop\b)|(\binsert into\b)|(dbo\.)|(\b\*\b)|(')|(")|(--[\S]*)'''

XSS_feature = r'''([\w\W]*<[\w\W]*)|([\w\W]*\\u003C[\w\W]*)|([\w\W]*\\U0000003C[\w\W]*)|([\w\W]*&#60;[\w\W]*)|([\w\W]*&#x3C;[\w\W]*)|([\w\W]*\\x3C[\w\W]*)|([\w\W]*\\074[\w\W]*)|([\w\W]*%3C[\w\W]*)|(>)|([\w\W]*\\u003E[\w\W]*)|([\w\W]*\\U0000003E[\w\W]*)|([\w\W]*&#62;[\w\W]*)|([\w\W]*&#x3E;[\w\W]*)|([\w\W]*\\x3E[\w\W]*)|([\w\W]*\\076[\w\W]*)|([\w\W]*%3E[\w\W]*)|([\w\W]*\\u0022[\w\W]*)|([\w\W]*\\U00000022[\w\W]*)|([\w\W]*&#34;[\w\W]*)|([\w\W]*&#x22;[\w\W]*)|([\w\W]*\\x22[\w\W]*)|([\w\W]*\\042[\w\W]*)|([\w\W]*%22[\w\W]*)'''

PHP_shell_feature = r'''(\bexec\b)|(\bsystem\b)|(\bcreate_function\b)|(\bpassthru\b)|(\bshell_exec\b)|(\bproc_open\b)|(\bpopen\b)|(\bsurl_exec\b)|(\bshow_source\b)|(\bassert\b)|(\bfile_put_contents\b)|(\bcall_user_func_array\b)|(\bpreg_replace\b)|(\binclude\b)|(\binclude\b)|(\beval\b)|(\bputenv\b)|(\bsymlink\b)|(\bdl\b)'''

JSP_shell_feature = r'''\bexec\b'''


class PackageChecker:
    def __init__(self, data_list, alarm_list):
        self.data_list = data_list
        self.alarm_list = alarm_list
        self.SQLInjection_regex = re.compile(SQLInjection_feature, re.I)
        self.XSS_regex = re.compile(XSS_feature, re.I)

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
        else:
            checking_data = self.data[4]
        
        while True:
            if self.SQLInjection_regex.search(checking_data):
                alarm_type = 1
                break
            if self.XSS_regex.search(checking_data):
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


class FileChecker():
    def __init__(self, data_list, alarm_list):
        self.data_list = data_list
        self.alarm_list = alarm_list
        self.php_regex = re.compile(PHP_shell_feature, re.I)
        self.jsp_regex = re.compile(JSP_shell_feature, re.I)

    def work(self):
        php_suffix_regex = re.compile(r'''(\S+\.php)|(\S+\.inc)|(\S+\.php5)''', re.I)
        jsp_suffix_regex = re.compile(r'''\S+\.jsp''', re.I)
        while True:
            data = self.data_list.dequeue()
            if php_suffix_regex.search(data[3]):
                regex = self.php_regex
            elif jsp_suffix_regex.search(data[3]):  
                regex = self.jsp_regex
            else:
                continue
            ct = FileCheckingThread(data, self.alarm_list, regex)
            ct.start()

class FileCheckingThread(threading.Thread):
    def __init__(self, data, alarm_list, regex):
        self.data = data
        self.alarm_list = alarm_list
        self.regex = regex
        super(FileCheckingThread, self).__init__()

    def run(self):
        try:
            file_obj = open(self.data[3])
            file_str = file_obj.read()
        except:
            return
        m = self.regex.search(file_str)
        if m:
            new_element = []
            new_element.append(0)
            new_element.append(self.data[0])
            new_element.append(self.data[3])
            new_element.append(self.data[3])
            new_element.append(m)
            self.alarm_list.enqueue(new_element)
        file_obj.close()
        return


def check(str):
    a = re.compile(JSP_shell_feature, re.I)
    m = a.search(str)
    if m:
        print m.group() 
    else:
        print False

if __name__ == '__main__':
    f = open("/var/www/PhpShell.php")
    a = f.read()
    print a
    check("union")
