#!/bin/bash
chengxu='k'
arr=${1}  #注意这个地方用花括号.就自动把穿进去的参数当成数组了.
for i in $arr  #这里面不用谢[@]这个了.
do        #注意pycharm书写shell脚本的回车设置.https://blog.51cto.com/yuanji6699/1929286
    echo ${chengxu}
    echo ${i}
    jieguo=`lsof -i:$i |awk  '{print $2}' |head -2|tail -1`   #用``来把结果变成
    #对jieguo这个pid号进行杀死
    echo ${jieguo}
    #注意逻辑,如果没被占用直接启动
    if [ -n "$jieguo" ]; then
    jieguo=`kill -9 ${jieguo}`
    jieguo=`kill -KILL ${jieguo}`
    `kill -9 ${jieguo}`
    kill -9 ${jieguo}
    `kill -KILL ${jieguo}`
    kill -KILL ${jieguo}
    echo KILLed ${i}
    fi
    #下面houtai运行程序到这个端口
    jieguo=nohup python manage.py runserver 0:${i} & >>laji
#    jieguo=nohup python manage.py runserver 0:${i} &   这一行目前最好的方法,但是关闭xshell就会关闭所有服务.
    #这里面有问题,现在是关闭终端服务就停了..为什么写了nohup也不起作用?bao IO错误.
    #打印到终端就会报错.不打印到终端即可,用logging记录到文件rizhi.log即可.
    #nohup python manage.py runserver 0:8082& >laji
jieguo=''
echo {$jieguo}
#https://www.jianshu.com/p/0f72afb513ab 同时运行多个python脚本的问题. 就是每一个命令后面都袈裟&
done
: << !

上面已经实现了同时启动3个相同的服务到8082,8083,8084的端口.提前用kill保证了端口的呗占用kill刁情况.

下面要做一个轮训,让每一个请求过来,经过一个计数器mod3之后的结果给对应端口进行处理.
开一个8081端口的应用,他来控制8082-8084的应用.
为了方便就让8081的代码和其他代码都一样.只是8081多写一个控制器来调用其他端口程序.


还需要高并发,来测试数据库的读写是否并发有错误.


!



