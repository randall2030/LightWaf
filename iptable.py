import iptc
import datetime
import time
#rule = iptc.Rule()
#rule.src = "172.21.20.128"
#rule.in_interface = "wlan0"
#rule.protocol = "tcp"
#t = rule.create_target("DROP")
#rule.target = t


table = iptc.Table(iptc.Table.FILTER)
chain = iptc.Chain(table, "INPUT")
#chain.append_rule(rule)
#chain.delete_rule(rule)
#for chain in table.chains:
#    for rule in chain.rules:
#        chain.delete_rule(rule)
for chain in table.chains:
    chain.flush()


for chain in table.chains:
    print "================================="
    print "chain ", chain.name
    for rule in chain.rules:
        print "Rule", "proto:",rule.protocol,"src:",rule.src,"dst:",\
            rule.dst, "in:", rule.in_interface, "out:", rule.out_interface,
        print "Matches:"
        for match in rule.matches:
            print match.name
        print "Target:",
        print rule.target.name
print "================================="

package_time = datetime.datetime.utcfromtimestamp(time.time())
package_time = package_time.strftime("%Y-%m-%d %H:%M:%S")
print package_time
