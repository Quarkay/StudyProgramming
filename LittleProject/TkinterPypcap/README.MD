### TkinterPypcap

基于tkinter和pypcap、dpkt的嗅探器(python2.7)

----

为了将网络设备设置为混合模式所以需要在root下执行，然后按照提示输入网络设备名称即可。

sudo tkinterpypcap.py

![运行截图][1]

（测试环境:ubuntu 14.04.4，Python2.7.6）

----

写的比较匆忙，代码较为混乱。

##### Task List
- [ ] 改善代码组织结构
- [ ] 友好的Dump格式
- [ ] GUI亟待改善
- [ ] 筛选条件支持BPF
- [ ] 解析更多的数据包格式
- [ ] 支持pcap文件解析、文件输出

[1]: https://o2ok64blz.qnssl.com/2016/04/1695856389.png