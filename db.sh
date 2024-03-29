#!/bin/bash 

    MYSQL_SOCK="/var/lib/mysql/mysql.sock"
    MYSQL_USER='db'
    MYSQL_PASSWORD='123qqq...A'
    MYSQL_HOST='localhost'
    MYSQL_PORT='3306'
    MYSQL_Connect="/usr/bin/mysqladmin -u$MYSQL_USER -p$MYSQL_PASSWORD -h$MYSQL_HOST -P$MYSQL_PORT -S$MYSQL_SOCK"


#数据库自定义监控模板:


if  [ $# -ne 1 ];then

        echo "please input one arguement"

    fi



    case $1 in



        Uptime)             #查询当前MySQL本次启动后的运行统计时间

            result=`${MYSQL_Connect} status 2>/dev/null | cut -d ":" -f 2 | cut -d " " -f 2`

            echo $result

            ;;



        Slow_queries)       #查看当前慢查询语句的个数

            result=`${MYSQL_Connect} extended-status 2>/dev/null | grep -w "Slow_queries" | cut -d "|" -f 3`

            echo $result

            ;;



        Com_rollback)       #执行回滚的个数

            result=`${MYSQL_Connect} extended-status 2>/dev/null | grep -w "Com_rollback" | cut -d "|" -f 3`

            echo $result

            ;;



        Questions)

            result=`${MYSQL_Connect} extended-status 2>/dev/null | grep -w "Questions" | cut -d "|" -f 3`

            echo $result

            ;;



        Com_commit)

            result=`${MYSQL_Connect} extended-status 2>/dev/null | grep -w "Com_commit" | cut -d "|" -f 3`

            echo $result

            ;;



        Bytes_sent)       #发送的字节数

            result=`${MYSQL_Connect} extended-status 2>/dev/null | grep -w "Bytes_sent" | cut -d "|" -f 3`

            echo $result

            ;;



        Bytes_received)   #接受的字节数

            result=`${MYSQL_Connect} extended-status 2>/dev/null | grep -w "Bytes_received" | cut -d "|" -f 3`

            echo $result

            ;;

        Com_begin)

            result=`${MYSQL_Connect} extended-status 2>/dev/null | grep -w "Com_begin" | cut -d "|" -f 3`

            echo $result

            ;;



        Open_tables)        #查看当前打开的表数量

            result=`${MYSQL_Connect} status 2>/dev/null | cut -d ":" -f 5 | cut -d " " -f 2`

            echo $result

            ;;



        Threads_connected)  #查看当前打开的连接数量

            result=`${MYSQL_Connect} extended-status 2>/dev/null | grep -w  "Threads_connected" | cut -d "|" -f 3`

            echo $result

            ;;



        Threads_cached)     #查看线程缓存内的线程数量

            result=`${MYSQL_Connect} extended-status 2>/dev/null | grep -w  "Threads_cached" | cut -d "|" -f 3`

            echo $result

            ;;



        Threads_created)   #查看创建用来处理连接的线程数。如果Threads_created较大，可能要增加thread_cache_size值。

            result=`${MYSQL_Connect} extended-status 2>/dev/null | grep -w  "Threads_created"  | cut -d "|" -f 3`

            echo $result

            ;;



        Threads_running)   #查看激活的(非睡眠状态)线程数

            result=`${MYSQL_Connect} extended-status 2>/dev/null | grep -w "Threads_running"  | cut -d "|" -f 3`

            echo $result

            ;;



        Slow_launch_threads) #查看创建时间超过slow_launch_time秒的线程数

            result=`${MYSQL_Connect} extended-status 2>/dev/null | grep -w "Slow_launch_threads" | cut -d "|" -f 3`

            echo $result

            ;;



        Com_select)        #查看select语句的执行数

            result=`${MYSQL_Connect} extended-status 2>/dev/null | grep -w "Com_select"  |cut -d "|" -f 3`

            echo $result

            ;;



        Com_insert)        #查看insert语句的执行数

         result=`${MYSQL_Connect} extended-status 2>/dev/null | grep -w "Com_insert" |cut -d "|" -f 3`

            echo $result

            ;;



        Com_update)        #查看update语句的执行数

            result=`${MYSQL_Connect} extended-status 2>/dev/null | grep -w "Com_update" | cut -d "|" -f 3`

            echo $result

            ;;



        Com_delete)        #查看delete语句的执行数

            result=`${MYSQL_Connect} extended-status 2>/dev/null | grep -w "Com_delete" | cut -d "|" -f 3`

            echo $result

            ;;



        Connections)       #查看试图连接到MySQL(不管是否连接成功)的连接数

            result=`${MYSQL_Connect} extended-status 2>/dev/null | grep -w "Connections"  | cut -d "|" -f 3`

            echo $result

            ;;



        Table_locks_immediate)  #查看立即获得的表的锁的次数

            result=`${MYSQL_Connect} extended-status 2>/dev/null | grep -w "Table_locks_immediate"  | cut -d "|" -f 3`

            echo $result

            ;;



        Table_locks_waited)     #查看不能立即获得的表的锁的次数。如果该值较高，并且有性能问题，你应首先优化查询，然后拆分表或使用复制

            result=`${MYSQL_Connect} extended-status 2>/dev/null | grep -w "Table_locks_waited" | cut -d "|" -f 3`

            echo $result

            ;;



        *)

            echo "Usage:$0(Uptime|Com_update|Slow_queries|Com_select|Com_rollback|Questions|Com_insert|Com_delete|Com_commit|Bytes_sent|Bytes_received|Com_begin)" 

            ;;

        esac


