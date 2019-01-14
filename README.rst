F5 - GTM / ZoneRunner Bulk Update
=================================

#. makerecordfile.py

   - Simple script that creates a txt file containing dns records.
     "name.test1.local. A 1.1.1.1" (/test/mkrecords.txt)

#. makezone.py

   - Simple script that creates/adds test zones to the named.conf with
     corresponding db file

#. importrecords.py

   - Grabs the list of zones from “/var/named/config/named.conf”
   - Grabs the list of records from a txt file. (see makerecordfile.py)
   - bigstart stop “zrd” and “named”
   - Adds the record to the proper db.external file by parsing the list and
     matching it to a valid domain. (If domain doesn’t exist it adds the
     record to a log and skips it. Can’t add it to a db file that doesn’t
     exist.)
   - bigstart start “zrd” and “named”
