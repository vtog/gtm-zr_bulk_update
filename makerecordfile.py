#!/usr/bin/env python

record = open('/test/mkrecords.txt', 'w')
for i in range(1, 11):
    record.write('name.' + 'test' + str(i) + '.local.' + ' A ' + '1.1.1.1' + '\n')
record.close()
        