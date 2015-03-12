import sys
import time
import threading
class Thread1(threading.Thread):
    def run(self):
        print "Thread 1 before sleep: %s" % time.strftime('%Y-%m-%d %H:%M:%S')
        time.sleep(3)
        print "End thread 1: %s" %  time.strftime('%Y-%m-%d %H:%M:%S')
class Thread2(threading.Thread):
    def run(self):
        print "Thread 2 before sleep: %s" % time.strftime('%Y-%m-%d %H:%M:%S')
        time.sleep(3)
        print "End thread 2: %s" %  time.strftime('%Y-%m-%d %H:%M:%S')


if __name__ == "__main__":
    t1 = Thread1()
    t2 = Thread2()
    t1.start()
    t2.start()
    t2.join()
    print "End main thread!"
