postman发送请求的例子.:

http://116.196.87.166:8082/test/  post方法
body form-data里面用
url -------/data/zb/policy_files/txt/（东营）综合保税区及相关优惠政策.txt



eval('print(1)')
xuyao :

python-docx  yong pip anzhuang

用配置文件来控制里面的一些参数配置.

调用pytesseract来做ocr

所以目前支持 pdf doc docx txt png jpg
下一步可以继续做支持语音.



搭建:

1.建立python环境,安装requirement.txt
2.建立mongodb数据库,用腾讯16gb分词写入mongodb.py文件写入mongodb数据库.
3.安装https://www.rarlab.com/rar/rarlinux-x64-5.5.0.tar.gz
说明:https://blog.csdn.net/lyliyongblue/article/details/48519261
4.建立mysql数据库.
5.配置2个数据库的参数.


腾讯800万词
https://ai.tencent.com/ailab/nlp/embedding.html




ocr相关安装:


2019-08-08,21点55
linux上teseract安装:
tesseract 3.04在centos6上安装
https://blog.csdn.net/kfzx3427/article/details/88690195








整:

http://www.liangchan.net/soft/softdown.asp?softid=11126
把下载好的zip里面的chi_sim开头的贴到liux系统对应的目录下面即可.

tesseract 3.png 3.txt -l chi_sim


这时候会遇到:
 No module named ‘_lzma
使用这个来做:
 https://blog.csdn.net/sangfei18829896970/article/details/97754635


访问例子:
post请求
url:file:///data/zb/1.html
url:https://www.cnblogs.com/mfryf/p/3691563.html
url:data/zb/1.txt
url:data/zb/1.jpg
url:data/zb/1.png
url:data/zb/1.pdf
url:data/zb/1.doc
url:data/zb/1.docx



https://nanjing.s3.cn-north-1.jdcloud-oss.com/nanjing/济南市政府门户网站 政策文件 关于印发《济南市科技金融风险补偿金管理办法》的通知.pdf



https://nanjing.s3.cn-north-1.jdcloud-oss.com/nanjing/济南新政策.docx











2019-08-11,12点32
用shell对启动进行自动化处理.



结果总结:

配置文件里面默认写开3个端口8082,8083,8084
随便用哪个端口发送下面的post请求

http://116.196.87.166:8082/master
http://116.196.87.166:8083/master
http://116.196.87.166:8084/master

请求体
url:file:///data/zb/1.html
url:https://www.cnblogs.com/mfryf/p/3691563.html
url:data/zb/1.txt
url:data/zb/1.jpg
url:https://www.runoob.com/wp-content/themes/runoob/assets/images/qrcode.png
url:https://nanjing.s3.cn-north-1.jdcloud-oss.com/nanjing/济南市政府门户网站 政策文件 关于印发《济南市科技金融风险补偿金管理办法》的通知.pdf
url:data/zb/1.doc
url:https://nanjing.s3.cn-north-1.jdcloud-oss.com/nanjing/济南新政策.docx

都会进行分布式轮询.即3个服务轮岗服务.

运行项目的方法:

如果要改端口在properties.conf里面修改即可.

然后运行python自动化运行.py 即可.他会自动把参数传给shell自动化运行.


如果返回的json格式里面有中文显示成了/uxxxx形式,改变代码里面编码都为utf8即可.












nohup python manage.py runserver 0:8082 &  nohup python manage.py runserver 0:8088 &
为什么终端闭了,程序就闭了??

有时候会发生进程杀不干净.总发生在启动的最后一个端口身上.








