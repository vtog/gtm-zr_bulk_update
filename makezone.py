#!/usr/bin/env python

import time
from subprocess import PIPE, Popen

def cmdline(command):
    process = Popen(
        args=command,
        stdout=PIPE,
        shell=True
    )
    return process.communicate()

def getzones():
    zones = []
    data = open('/test/named.conf', 'r').readlines()
    #data = open('/var/named/config/named.conf', 'r').readlines()
    for zone in data:
        if "zone" in zone:
            zones.append(zone.split()[1].split('"')[1])
    return zones

def makezonedb(n, zones):
    makezone = []
    for i in range(1, n+1):
        makezone.append('test' + str(i) + '.local.')
    for zone in zones:
        for new in makezone:
            if new == zone:
                makezone.remove(new)
    for zone in makezone:
        zonedb = open('/test/db.external.' + zone, 'w')
        #zonedb = open('/var/named/config/namedb/db.external.' + zone, 'w')
        zonedb.write('$ORIGIN .\n')
        zonedb.write('$TTL 604800\t\t; 1 week\n')
        zonedb.write(zone.rstrip('.') + '\t\t\t\tIN SOA  ns.' + zone + ' hostmaster.' + zone + '(\n')
        zonedb.write('\t\t\t\t\t\t\t\t' + time.strftime("%Y%m%d") + '01\t; serial\n')
        zonedb.write('\t\t\t\t\t\t\t\t10800\t\t; refresh (3 hours)\n')
        zonedb.write('\t\t\t\t\t\t\t\t3600\t\t; retry (1 hour)\n')
        zonedb.write('\t\t\t\t\t\t\t\t604800\t\t; expire (1 week)\n')
        zonedb.write('\t\t\t\t\t\t\t\t86400\t\t; minimum (1 day)\n')
        zonedb.write('\t\t\t\t\t\t\t\t)\n')
        zonedb.write('\t\t\t\t\t\tNS\t\tns.' + zone + '\n')
        zonedb.write('$ORIGIN ' + zone + '\n')
        zonedb.write('ns\t\t\t\t\t\tA\t\t192.168.1.245\n')
        zonedb.close()
    return makezone

def appendzonefile(newzones):
    zonefile = open('/test/named.conf', 'r')
    #zonefile = open('/var/named/config/named.conf', 'r')
    lines = zonefile.readlines()
    zonefile.close()
    zonefile = open('/test/named.conf', 'w')
    #zonefile = open('/var/named/config/named.conf', 'w')
    zonefile.writelines([item for item in lines[:-1]])
    zonefile.close()    
    zonefile = open('/test/named.conf', 'a')
    #zonefile = open('/var/named/config/named.conf', 'a')
    for zone in newzones:
        zonefile.write('\tzone "' + zone + '" {\n')
        zonefile.write('\t\ttype master;\n')
        zonefile.write('\t\tfile "db.external.' + zone + '";\n')
        zonefile.write('\t\tallow-update {\n')
        zonefile.write('\t\t\tlocalhost;\n')
        zonefile.write('\t\t};\n')
        zonefile.write('\t};\n')
    zonefile.write('};')
    zonefile.close()

#cmdline("bigstart stop zrd")
#cmdline("bigstart stop named")
total = int(raw_input("How many 'test' zones do you want to create? "))
zones = getzones()
newzones = makezonedb(total, zones)
appendzonefile(newzones)
#cmdline("chown named:named /var/named/config/namedb/*")
#cmdline("bigstart start named")
#cmdline("bigstart start zrd")
