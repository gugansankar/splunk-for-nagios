#!/bin/bash
echo "host_name,name,state,num,servicegroup"
/usr/bin/nc 127.0.0.1 6557 < nagios-servicegroupmembers |sed 's/,/\n/g'|sed 's/|/,/g'|while read line
do
COUNT=`echo $line|grep -c ","`

if [ $COUNT -eq 0 ]
 then
     SG=$line
 else
     echo $line","$SG
fi

done

