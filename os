fconfig eth0 | awk '/RX p/{print $3}'

ifconfig eth0 | awk '/RX p/{print $6}' | sed  s/\(//

发送数据包数量的接收流量

ifconfig eth0 | awk '/TX p/{print $3}'

ifconfig eth0 | awk '/TX p/{print $6}' | sed  s/\(//

     Cpu 占用:top  -n 1 | awk '/id/{print $8}'

     内存使用/空余内存:

free -m | awk 'NR==2{print $3}'

     free -m | awk 'NR==2{print $4}'

     硬盘使用情况(已用/可用)

df -h | awk '/sda1/{print $3}'

df -h | awk '/sda1/{print $4}'

平均负载(1/5/15min)

uptime | awk '{print $8}' | sed s/,//

uptime | awk '{print $9}' | sed s/,//

uptime | awk '{print $10}'
