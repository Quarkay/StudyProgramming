## PyPScanner
　　使用Python实现的服务扫描、弱密码检测、已知漏洞利用工具

----

#### 使用方式：

 -h　　show help information

 -v　　version of the tool

 -ip　　the ip host(must need)

 -p　　the port of host，eg: -p5555-65535

 　　　　default port value:500-65535

 -s　　service name

 　　　　eg: memcached、mysql

 　　　　default s value:　mysql-server

 -n　　the number of thread that will be actived to scan the host

 　　　　default n value:　666

 -t　　the time (how many seconds) that will be used to judge

 　　　　default t value:　3

 <del>-l　　the file name that will be used to put in the result of scanning.


#### 概要：

实现了插件机制，添加相关的插件即可作对应的扫描服务或exp.

插件例子已经有mysql和redis.

exploit插件已经有一个针对mysql相关版本的例子.


#### 目录说明：

<pre>
----
|PypInit.py -- 初始处理文件
|pypscanner.py -- 入口文件
|config.py -- 配置文件
|Plugins -- 插件目录
----
  |exps -- exploits插件目录
  ----
    |mysqlExampleExp.py -- 漏洞exploit插件例子
  |service -- 扫描服务插件目录
  ----
    |mysql.py -- mysql服务插件
    |redis.py -- redis服务插件
</pre>