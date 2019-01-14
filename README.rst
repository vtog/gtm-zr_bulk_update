F5 - GTM / ZoneRunner Bulk Update
=================================

#. makerecordfile.py

   - Simple script that creates a txt file containing dns records.
   - /test/mkrecords.txt
   - "name.test1.local. A 1.1.1.1"

#. importrecords.py

   1. Grabs the list of zones from “/var/named/config/named.conf”
   #. Grabs the list of records from a txt file. (see below for file sample)
   #. Stops “zrd” and “named”
   #. Adds the record to the proper db.external file by parsing the list and
      matching it to a valid domain.
      
      a.	If domain doesn’t exist it adds the record to a log and skips it.
         (Can’t add it to a db file that doesn’t exist.)

   #. Starts “zrd” and “named”

#. makezone.py

   - 
