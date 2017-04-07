import os
import time
import MySQLdb
import sys
import math
entrance_x=-1.89
entrance_y=0.769
PID=20170001
while True:
    command=input("Store package input 0  Take package input 1  Quit input 2:")
    if command==2:
    	break
    if command!=0 and command!=1 and command!=2:
        print "Command error!!!"
        continue
    if command==0:
    	conn=MySQLdb.connect(host='localhost',port=3306,user='root',passwd='zls680902',db='realrobot',)
        cur=conn.cursor(MySQLdb.cursors.DictCursor)
        rack_size=cur.execute("select * from rack where ocu = '0'")
        rack_rows=cur.fetchall()
        cur.close()
        conn.commit()
        conn.close()
        if rack_size==0:
            print "Sorry!!! There is no free space for your package!!!"
            continue
        else:
            print "Please wait for the nearest robot come to the entrance to carry your package!"
            conn=MySQLdb.connect(host='localhost',port=3306,user='root',passwd='zls680902',db='realrobot',)
            cur=conn.cursor(MySQLdb.cursors.DictCursor)
            robot_free_number=cur.execute("select * from robot where ocu = '0'")
            robot_rows=cur.fetchall()
            if robot_free_number==0:
            	print "All robots are occupied,please wait!!!"
            	continue
            m=int(robot_rows[0]['id'])
            mindist=1000000.0
            for i in range(robot_free_number):
                temp=math.sqrt(math.pow((entrance_x-float(robot_rows[i]['x'])),2)+math.pow((entrance_y-float(robot_rows[i]['y'])),2))
                if mindist>temp:
                    mindist=temp
                    m=robot_rows[i]['id']
            print '\033[5;36;47m',
            print "Your service robot is robot_"+str(m)
            print '\033[0m',
            cur.execute("update rack set ocu='1' where id='"+str(rack_rows[0]['id'])+"'")
            print '\033[1;31;40m',
            print "Your package ID is "+str(PID)
            print '\033[0m',
            cur.execute("insert into package values('"+str(PID)+"','"+str(rack_rows[0]['id'])+"')")
            t=cur.execute("select * from rack where id='"+str(rack_rows[0]['id'])+"'")
            rows=cur.fetchall()
            cur.execute("update robot set x='"+str(rows[0]['x'])+"',y='"+str(rows[0]['y'])+"' where id='"+str(m)+"'")
            cur.close()
            conn.commit()
            conn.close()
            os.system("gnome-terminal -e 'python client_"+str(m)+'.py '+str(entrance_x)+' '+str(entrance_y)+' '+str(rows[0]['x'])+' '+str(rows[0]['y'])+"'")
            PID+=1
            if PID==20179999:
                print "PID has been used up!!!"
                break
    else:
        p=input("Show your package ID:")
        conn=MySQLdb.connect(host='localhost',port=3306,user='root',passwd='zls680902',db='realrobot',)
        cur=conn.cursor(MySQLdb.cursors.DictCursor)
        t=cur.execute("select * from package where id='"+str(p)+"'")
        rows=cur.fetchall()
        if t==0:
            print "Package ID does not exist,please confirm your Package ID!"
            continue
        n=int(rows[0]['rn'])
        t=cur.execute("select * from rack where id='"+str(n)+"'")
        rows=cur.fetchall()
        storage_rack_x=float(rows[0]['x'])
        storage_rack_y=float(rows[0]['y'])
        cur.execute("delete from package where id = '"+str(p)+"'")
        cur.close()
        conn.commit()
        conn.close()
        conn=MySQLdb.connect(host='localhost',port=3306,user='root',passwd='zls680902',db='realrobot',)
        cur=conn.cursor(MySQLdb.cursors.DictCursor)
        robot_free_number=cur.execute("select * from robot where ocu = '0'")
        robot_rows=cur.fetchall()
        if robot_free_number==0:
            print "All robots are occupied,please wait!!!"
            continue
        m=int(robot_rows[0]['id'])
        mindist=1000000.0
        for i in range(robot_free_number):
            temp=math.sqrt(math.pow((storage_rack_x-float(robot_rows[i]['x'])),2)+math.pow((storage_rack_y-float(robot_rows[i]['y'])),2))
            if mindist>temp:
                mindist=temp
                m=robot_rows[i]['id']
        print '\033[5;36;47m',
        print "Your service robot is robot_"+str(m)
        print '\033[0m',
        cur.execute("update rack set ocu='0' where id='"+str(n)+"'")
        cur.execute("update robot set x='"+str(entrance_x)+"',y='"+str(entrance_y)+"' where id='"+str(m)+"'")
        cur.close()
        conn.commit()
        conn.close()
        os.system("gnome-terminal -e 'python client_"+str(m)+'.py '+str(storage_rack_x)+' '+str(storage_rack_y)+' '+str(entrance_x)+' '+str(entrance_y)+"'")
# os.system('python /home/libliuis/catkin_ws/src/navigation_multi/recovery.py')