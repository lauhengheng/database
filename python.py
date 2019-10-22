#############################################################################################
# 1.监控 web 服务是否正常,不低于 3 种监控策略。要求间隔 1 分钟,持续监控。
#!/root/nsd1905/bin/python3

import subprocess
import time
import socket
# import urllib
import urllib.request
import urllib.error


import psutil   # 真机中使用不了这个模块,虚拟机可以使用


if __name__ == '__main__':
    while True:
        # 监听80端口
        sk = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # 第一个参数是满足IP地址协议，第一个参数创建的socket完成TCP协议
        # sk = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # 第一个参数是满足IP地址协议，第一个参数创建的socket完成UDP协议
        sk.settimeout(1) # 通俗的解释为：比如数据库连接时，有时候会因为网络原因造成一直连不上，如果没有去手动停止，socket可能会一直尝试重连，造成资源的浪费。
        try:
            sk.connect(('192.168.4.1', 80))     #使用域名也可以
            print('Server port 80 OK!')
        except Exception:
            print('Server port 80 not connect!')
        sk.close()


        # 查看是否有http进程
        def judgeprocess(processname):
            pl = psutil.pids()
            for pid in pl:
                if psutil.Process(pid).name() == processname:
                    print(pid)
                    return 0
                    # break

        result = judgeprocess('nginx')  # nginx进程
        if result == 0:
            print('web status OK ps')
        else:
            print('web services disable')


        # 使用curl工具查看状态码
        html = urllib.request.urlopen('http://192.168.4.1')
        # print(list(html))
        html_contents = []
        for i in list(html):
            html_contents.append(str(i, encoding="utf-8").strip())

        # print(str(html_contents[3]).find('Welcome to nginx'))
        result = str(html_contents[3]).find('Welcome to nginx')   # find找到的是int类型
        if result == 7:
            print('web status OK curl')
        else:
            print('web services disable')

        time.sleep(60)


#############################################################################################
# 2.监控 db 服务是否正常,不低于 3 种监控策略。要求间隔 1 分钟,持续监控。
#!/root/nsd1905/bin/python3

import subprocess
import time
import socket
import pymysql
import psutil   # 真机中使用不了这个模块,虚拟机可以使用


if __name__ == '__main__':
    # 监听3306端口
    sk = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # 第一个参数是满足IP地址协议，第一个参数创建的socket完成TCP协议
    # sk = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)   # 第一个参数是满足IP地址协议，第一个参数创建的socket完成UDP协议
    sk.settimeout(1) # 通俗的解释为：比如数据库连接时，有时候会因为网络原因造成一直连不上，如果没有去手动停止，socket可能会一直尝试重连，造成资源的浪费。
    try:
        sk.connect(('192.168.4.2', 3306))  # 使用域名也可以
        print('Server port 3306 OK!')
    except Exception:
        print('Server port 3306 not connect!')
    sk.close()


    # 查看是否有mysql进程

    def judgeprocess(processname):
        pl = psutil.pids()
        for pid in pl:
            if psutil.Process(pid).name() == processname:
                print(pid)
                return 0
                # break
    result = judgeprocess('mysql')  # nginx进程
    if result == 0:
        print('mysql status OK ps')
    else:
        print('mysql services disable')

    # 是否可以登录数据库,并显示数据库
    # 链接从数据库
    conn = pymysql.connect(
        host='192.168.4.2',
        port=3306,
        user='root',
        passwd='123qqq...A',
        # db='mysql',
        charset='utf8'
    )
    cursor = conn.cursor()
    cursor.execute("show databases")  # execute执行sql语句
    list_db_name = []

    db_status = False
    for db_name in cursor.fetchall():
        list_db_name.append(db_name[0])
        if db_name[0] == 'mysql':
            db_status = True

    # 关闭数据库链接
    conn.commit()
    cursor.close()
    conn.close()

    if db_status:
        print('db status OK ps')
    else:
        print('db services disable')

#############################################################################################
# 3.监控 web 站点目录(/var/html/www)下所有文件是否被恶意篡改(文件内容被改了),
# 如果有就打印改动的文件名(发邮件),定时任务每 3 分钟执行一次(10 分钟时间完成)。
#!/root/nsd1905/bin/python3


import os
import hashlib
import time
import subprocess



# 获取文件md5值函数
def md5sum(filename, blocksize=65536):
    hash = hashlib.md5()
    with open(filename, "rb") as f:
        #必须是rb形式打开的，否则的两次出来的结果不一致
        for block in iter(lambda: f.read(blocksize), b""):
            hash.update(block)
    return hash.hexdigest()

# print(md5sum('/root/result.txt'))


# 获取制定目录全部文件函数
def all_path(dirname):

    result = []#所有的文件

    for maindir, subdir, file_name_list in os.walk(dirname):
        # print("1:",maindir) #当前主目录
        # print("2:",subdir) #当前主目录下的所有目录
        # print("3:",file_name_list)  #当前主目录下的所有文件
        for filename in file_name_list:
            apath = os.path.join(maindir, filename)#合并成一个完整路径
            result.append(apath)

    return result


if __name__ == '__main__':
    while True:
        # 事先先保存各个文件的md5值
        file_md5sum = {} # 使用字典类型存储

        for filename in all_path("/root/httpDir"):
            file_md5sum[filename] = md5sum(filename)


        # 打印各个文件对应的md5值,保存到文件中/root/fileMD5sum.txt(只操作一次,保存原始的MD5值)
        # save_file_md5sum_contents = []
        #
        # for iii in file_md5sum:
        #     save_file_md5sum_contents.append('%s %s\n'% (iii,file_md5sum[iii]))
        #
        # with open('/root/fileMD5sum.txt', 'w') as fobjs:
        #     fobjs.writelines(save_file_md5sum_contents)

        # 根据时间文件名
        tmp_md5sum_contents = []
        for iii in file_md5sum:
            tmp_md5sum_contents.append('%s %s\n'% (iii,file_md5sum[iii]))

        tmpFileName = '/root/tmpFileMD5sum-' + str(time.time())
        with open(tmpFileName, 'w') as fobjs:
            fobjs.writelines(tmp_md5sum_contents)

        # 检查变化的MD5值
        with open('/root/fileMD5sum.txt') as fobj1:
            set111 = set(fobj1)

        with open(tmpFileName) as fobj2:
            set222 = set(fobj2)
        # 讲临时文件删除
        os.remove(tmpFileName)

        with open('/root/fileMD5Result.txt', 'w') as fResult:
                fResult.writelines(set111 - set222)

        # 将变化的文件名和Md5的值存放的指定文件中
        var_file = []
        with open('/root/fileMD5Result.txt') as fResult1:
            var_file = fResult1.readlines()


        # 打印被修改的文件,连同md5的值一起打印
        if len(var_file) > 0:
            # 将临时文件内容清空,
            with open('/root/fileMD5Result.txt', 'w') as fResult:
                fResult.write(' ')
            # 将变化的文件 发邮件
            results = ''
            for line in var_file:
                results += line
                # print(line, end='')

            mds = str("echo -e '%s' | mail -s 'md5 changed' root" % results) # 发送邮件
            subprocess.run(mds, shell=True)

        time.sleep(180)     # 间隔3分钟检查一次

#############################################################################################
# 4.nginx 实现日志按天切割
#!/root/nsd1905/bin/python3

import time
import subprocess
import shutil

import schedule     # 需要安装模块pip install schedule
# import sqlalchemy   # 本真机需要安装这个版本 pip install SQLAlchemy  华为云主机安装pip3 install sqlalchemy

def job():
    # print("I'm working...")

    logs_path='/usr/local/nginx/logs/'
    pid_path='/usr/local/nginx/logs/nginx.pid'

    accesslog_path = logs_path + 'access.log'
    renamelog_path = accesslog_path + time.strftime("-%Y-%m-%d-%X")

    shutil.move(accesslog_path, renamelog_path)

    pid = ''
    with open(pid_path) as fobjs:
        pid=fobjs.read().strip()
    cmds = 'kill -USR1 ' + pid
    # print(cmds)

    result = subprocess.run(cmds, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

# schedule.every().seconds.do(job)
# schedule.every().minutes.do(job)          # 每分钟执行
# schedule.every().hour.do(job)
schedule.every().day.at("00:00").do(job)    #  每天凌晨开始切割文件
# schedule.every(5).to(10).days.do(job)
# schedule.every().monday.do(job)
# schedule.every().wednesday.at("13:15").do(job)

# print(renamelog_path)
if __name__ == '__main__':
    schedule.run_pending()
    time.sleep(1)


#############################################################################################
# 5.监控 MySQL 主从同步是否异常,如果异常,则发送短信或者邮件给管理员。
#!/root/nsd1905/bin/python3

import pymysql
import subprocess
import time



if __name__ == '__main__':
    while True:
        # 链接从数据库
        conn = pymysql.connect(
            host='192.168.4.2',
            port=3306,
            user='root',
            passwd='123qqq...A',
            # db='mysql',
            charset='utf8'
        )
        cursor = conn.cursor()
        cursor.execute("show slave status")        # execute执行SQL语句
        # print(cursor.fetchone())

        i = 0
        list_info = []
        error_code = [0, 1158, 1159, 1008, 1007, 1062] # 同步错误代号是1158,1159,1008,1007,1062,就跳过
        for slave_status in cursor.fetchone():
            # print(i, slave_status)
            if i == 10:
                list_info.append(slave_status) # Slave_IO_Running
            elif i == 11:
                list_info.append(slave_status) # Slave_SQL_Running
            elif i == 34:
                list_info.append(slave_status) # Last_IO_Errno
            elif i == 36:
                list_info.append(slave_status) # Last_SQL_Errno
            else:
                pass
            i += 1

        Last_IO_Errno = int(list_info[2])
        Last_SQL_Errno = int(list_info[3])


        # 如果IO线程有错误就发送邮件
        if Last_IO_Errno not in error_code:
            print('IO_ERRORno',Last_IO_Errno)
            mds = str("echo -e 'error_no:%s' | mail -s 'sync_IO_ERRORn0' root" % Last_IO_Errno)  # 发送邮件
            subprocess.run(mds, shell=True)

        # 如果SQL线程有错误就发送邮件
        if Last_SQL_Errno not in error_code:
            print('SQL_ERRORno',Last_SQL_Errno)
            mds = str("echo -e 'error_no:%s' | mail -s 'sync_SQL_ERRORn0' root" % Last_SQL_Errno)  # 发送邮件
            subprocess.run(mds, shell=True)

        # 关闭数据库链接
        conn.commit()
        cursor.close()
        conn.close()

        time.sleep(30)  # 30秒检查一次


#############################################################################################
# 6.请用至少两种方法实现!写一个脚本解决 DOS 攻击生产案例
#!/root/nsd1905/bin/python3

import time
import datetime
import iptc
import psutil


if __name__ == '__main__':
    ipdict = {}

    if 0:   # 方便测试,如果是0,不执行下面的程序
    # ---------------------------------------------------------------------------------------------
    # (一)nginx日志访问量
        start_time = time.time()    #值是秒
        str_date = datetime.datetime.now().strftime("%Y-%m-%d")
        log_Path1 = '/root/access.log'
        log_Path2 = '/usr/local/nginx/logs/access.log'
        ##

        with open(log_Path2) as fobj:           # 日志文件路径
            log_contents = fobj.readlines()

        for line in log_contents:
            # print(line.split()[3])
            cut_time = line.split()[3]
            cut_time = cut_time[-8:]
            str_datetime = str_date + ' ' + cut_time
            end_datatime = time.strptime(str_datetime, "%Y-%m-%d %H:%M:%S")
            # print(time.time() - time.mktime(end_datatime))  #相差180秒
            if (start_time - time.mktime(end_datatime)) < 180:   # 判断是否为3分钟(180秒)以为的
                ip = line.split()[0]
                if ip in ipdict:
                    ipdict[ip] = ipdict[ip] + 1
                else:
                    ipdict[ip] = 1

        data = sorted(list(ipdict.items()), key=lambda x: x[1], reverse=True)  # IP访问量排名

        for d in data:
            if int(d[1]) > 100:     # 次数超过100次的IP,用iptables禁掉
                print(d[1], ":\t", d[0], sep="")
                print(int(d[1]))
                # 设置iptables规则
                chain = iptc.Chain(iptc.Table(iptc.Table.FILTER), "INPUT")
                rule = iptc.Rule()
                rule.in_interface = "eth0"
                # rule.src = "192.168.4.5"  # 192.168.4.0/255.255.255.0 是网段
                rule.src = str(d[0])
                target = iptc.Target(rule, "DROP")
                rule.target = target
                chain.insert_rule(rule)


    if 1: # 方便测试,如果是0,不执行下面的程序
    # ---------------------------------------------------------------------------------------------
    # (二)网络连接数量
        while True:
            time.sleep(180)  # 时隔3分钟之后再检查一次
            for t_connects in psutil.net_connections():
                str_tcp_connects = str(t_connects)
                if str_tcp_connects.find('ESTABLISHED') > 0:     # 判断是否有ESTABLISHED
                    raddr_addr = str_tcp_connects.split(',')[5]  # 以,为分隔符号,第五位置是
                    # print(raddr_addr)                          # raddr=addr(ip='192.168.4.254'
                    # print(raddr_addr[(raddr_addr.find("'") + 1):-1])  # 截取IP'192.168.4.254'
                    ip = raddr_addr[(raddr_addr.find("'") + 1):-1]
                    if ip in ipdict:
                        ipdict[ip] = ipdict[ip] + 1
                    else:
                        ipdict[ip] = 1

            data = sorted(list(ipdict.items()), key=lambda x: x[1], reverse=True)  # IP访问量排名

            for d in data:
                if int(d[1]) > 100:  # 次数超过100次的IP,用iptables禁掉
                    # print(d[1], ":\t", d[0], sep="")
                    # 设置iptables规则
                    chain = iptc.Chain(iptc.Table(iptc.Table.FILTER), "INPUT")
                    rule = iptc.Rule()
                    rule.in_interface = "eth0"
                    # rule.src = "192.168.4.5"  # 192.168.4.0/255.255.255.0 是网段
                    rule.src = str(d[0])
                    target = iptc.Target(rule, "DROP")
                    rule.target = target
                    chain.insert_rule(rule)



#############################################################################################
# 7.如何实现对 MySQL 数据库进行分库备份,请用脚本实现
#!/root/nsd1905/bin/python3

import pymysql
import os


if __name__ == '__main__':
    # 链接从数据库
    conn = pymysql.connect(
        host='192.168.4.2',
        port=3306,
        user='root',
        passwd='123qqq...A',
        # db='mysql',
        charset='utf8'
    )
    cursor = conn.cursor()
    cursor.execute("show databases")  # execute执行sql语句
    # cursor.fetchall()    # 获取所有查询的结果行
    # cursor.fetchone()    # 获取一行
    # cursor.fetchmany(3)  # 获取前三行
    list_db_name = []
    for db_name in cursor.fetchall():
        list_db_name.append(db_name[0])
        # print(db_name[0])

    # 关闭数据库链接
    conn.commit()
    cursor.close()
    conn.close()

    # 根据数据库名称备份数据库
    sock_path = '/var/lib/mysql/mysql.sock'
    save_path = '/root/'
    for db_name in list_db_name:
        str_db_name = str("mysqldump -h192.168.4.2 -uroot -p123qqq...A -S%s -x -F -R -B %s > %s%s" % (sock_path, db_name, save_path, db_name) + '.sql')
        os.system(str_db_name) # 执行mysqldump备份数据

#############################################################################################
# 8.如何实现对 MySQL 数据库进行分库加分表备份,请用脚本实现
#!/root/nsd1905/bin/python3

import pymysql
import os


if __name__ == '__main__':
    # 链接从数据库
    conn = pymysql.connect(
        host='192.168.4.2',
        port=3306,
        user='root',
        passwd='123qqq...A',
        # db='mysql',
        charset='utf8'
    )
    cursor = conn.cursor()
    cursor.execute("show databases")  # execute执行sql语句
    # cursor.fetchall()    # 获取所有查询的结果行
    # cursor.fetchone()    # 获取一行
    # cursor.fetchmany(3)  # 获取前三行

    sock_path = '/var/lib/mysql/mysql.sock'
    save_path = '/root/mysql_DB/'
    str_public_path = str("mysqldump -h192.168.4.2 -uroot -p123qqq...A -S%s -x -F -R " % (sock_path))
    # print(str_pub_path)

    # 获取数据库的名称,每个库的表
    list_db_name = []
    db_name_new = ['db1', 'db2']            # 数据库的表太多,这里只备份自己新建的db1和db2库
    for db_name in cursor.fetchall():
        list_db_name.append(db_name[0])

        if db_name[0] in db_name_new:
            sql_cmd = 'use ' + db_name[0]

            cursor.execute(sql_cmd)         # 切换到制定的库中
            cursor.execute("show tables")   # 获取表名
            # print(cursor.fetchall())

            for table_name in cursor.fetchall():
                back_db_table_path = str_public_path
                back_db_table_path += str("%s %s > %s%s_%s" % (db_name[0], table_name[0], save_path, db_name[0], table_name[0]) + '.sql')
                # print(back_db_table_path)
                os.system(back_db_table_path) # 执行mysqldump备份数据

    # 关闭数据库链接
    conn.commit()
    cursor.close()
    conn.close()

#############################################################################################
# 9.监控 memcache 服务是否正常,模拟用户(web 客户端)检测。

#!/root/nsd1905/bin/python3

import subprocess
import time
import memcache     # pip install python-memcached  在终端可以使用,但是pycharm不可用



if __name__ == '__main__':
    # 检查memcache状态

    checks = 0        # 总检测次数
    get_hits = 0    # 检测命中次数
    begin_time = time.time()    # 记录开始时间

    mc = memcache.Client(['192.168.4.1:11211'], debug=1)  # 连接memcache开启debug模式
    while True:
        begin_time = time.time()
        set_value = mc.set("foo", "bar")    #判断是否set成功
        if set_value:
            checks += 1
            print('memcache status ok')
            get_hits = mc.stats         # 查看set次数
            get_hits = get_hits['set']  # 取set的次数(字典类型取值)
            # print(int(get_hits))
            print('the memcache hit is {:.2%}'.format(int(get_hits)/checks))
        else:
            print('memcache status disable')

        run_time = time.time() - begin_time
        print('用时:', run_time)



        time.sleep(5)

