import socket
from sys import argv
import MySQLdb
scripts,robot_x1,robot_y1,robot_x2,robot_y2=argv
conn=MySQLdb.connect(host='localhost',port=3306,user='root',passwd='zls680902',db='realrobot',)
cur=conn.cursor(MySQLdb.cursors.DictCursor)
cur.execute("update robot set ocu=1 where id=0")
cur.close()
conn.commit()
conn.close()
address = ('172.16.42.6', 31500)
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
msg = str(robot_x1)+' '+str(robot_y1)+' '+str(robot_x2)+' '+str(robot_y2)
s.sendto(msg, address)
data,addr=s.recvfrom(2048)
if data=='success':
    conn=MySQLdb.connect(host='localhost',port=3306,user='root',passwd='zls680902',db='realrobot',)
    cur=conn.cursor(MySQLdb.cursors.DictCursor)
    cur.execute("update robot set ocu=0 where id=0")
    cur.close()
    conn.commit()
    conn.close()
else:
	while True:
	    print "error!!!"
s.close()
