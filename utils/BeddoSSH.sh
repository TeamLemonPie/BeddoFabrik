SERVERLIST=serverlist.txt
ICMD=$1

while read SERVERNAME
do
   echo "Run $ICMD Command on $SERVERNAME"
   ssh -n pi@$SERVERNAME $ICMD
done < "$SERVERLIST"
