import iptc
import threading

def release_ip(chain, rule):
    chain.delete_rule(rule)

class Executioner():
    def __init__(self, alarm_list, interface, punish_time):
        self.alarm_list = alarm_list
        self.interface = interface
        self.punish_time = punish_time
    
    def work(self):
        table = iptc.Table(iptc.Table.FILTER)
        chain = iptc.Chain(table, "INPUT")
        print "Executioner ready!"
        while True:
            alarm = self.alarm_list.dequeue()
            if alarm[0] == 0:
                pass
            elif alarm[0] == 1 or alarm[0] == 2:
                rule = iptc.Rule()
                rule.src = alarm[2]
                rule.in_interface = self.interface
                rule.protocol = "tcp"
                rule.target = rule.create_target("DROP")
                chain.append_rule(rule)
                threading.Timer(self.punish_time, release_ip, (chain, rule,)).start()
            else:
                pass

if __name__ == "__main__":
  table = iptc.Table(iptc.Table.FILTER)
  chain = iptc.Chain(table, "INPUT")
  for rule in chain.rules:
    chain.delete_rule(rule)
     
