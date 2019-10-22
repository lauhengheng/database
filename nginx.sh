#!/bin/bash
Active connections(活跃连接数):
curl http://192.168.1.45/status 2>/dev/null | awk '/^Active/{print $3}'
Server(nginx启动到现在处理的连接数):
curl http://192.168.1.45/status 2>/dev/null | awk 'NR==3{print $1}'
Accepts(nginx启动到现在成功创建的握手次数):
curl http://192.168.1.45/status 2>/dev/null | awk 'NR==3{print $2}'
Handle requests(总共处理的请求数):
curl http://192.168.1.45/status 2>/dev/null | awk 'NR==3{print $3}'
Lose request(请求丢失数)=server-accepts
curl http://192.168.1.45/status 2>/dev/null | awk 'NR==3{print $1-$2}'
Reading(读取到客户端的header信息数):
     curl http://192.168.1.45/status 2>/dev/null | awk 'NR==4{print $2}'
Writing(返回给客户端header信息数):
curl http://192.168.1.45/status 2>/dev/null | awk 'NR==4{print $4}'
Waiting(已经处理完正在等候下一次请求指令的驻留链接（开启keep-alive的情况下，这个值等于 Active - (Reading+Writing)）)
     curl http://192.168.1.45/status 2>/dev/null | awk 'NR==4{print $6}'

