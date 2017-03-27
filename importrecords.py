#!/usr/bin/env python

import os
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

def getrecords(zones):
    i = 0
    records = {}
    try:
        os.remove('/test/import-error.log')
    except OSError:
        pass
    try:
        data = open('/test/mkrecords.txt', 'r').read().splitlines()
    except OSError:
        print "/test/mkrecords.txt does not exist"
        quit()

    for line in data:
        j = 0
        k = 0
        if line != "":
            fqdn = line.split()[0].split('.')
            for j in range(-len(fqdn), 0):
                last_j_elements = fqdn[j:]
                candidate = ".".join(last_j_elements)
                if candidate in zones:
                    records[i] = line.split(candidate)[0].rstrip('.'), \
                                 candidate, line.split()[1], line.split()[2]
                    i += 1
                    break
                elif k == (len(fqdn) - 1):
                    importerrorlog = open('/test/import-error.log', 'a')
                    importerrorlog.write(line + '\n')
                    importerrorlog.close()                    
                k += 1 #track iterations for NO zone match
    return records

def addrecords(records):
    for record in records:
        zonedb = open('/test/db.external.' + records[record][1], 'a')
        #zonedb = open('/var/named/config/namedb/db.external.' + records[record][1], 'a')
        zonedb.write(records[record][0] + '\t\t' +  \
                     records[record][2] + '\t' + \
                     records[record][3] + '\n')
        zonedb.close()

zones = getzones()
records = getrecords(zones)
#cmdline("bigstart stop zrd")
#cmdline("bigstart stop named")
addrecords(records)
#cmdline("bigstart start named")
#cmdline("bigstart start zrd")
