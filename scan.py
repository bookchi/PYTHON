import optparse
from socket import *
from threading import *

# 输出信号量
screenLock = Semaphore(value=1)

# 判断端口开闭and判断服务，通过tcp全连接
def connScan(tgtHost, tgtPort):
    try:
        connSkt = socket(AF_INET,SOCK_STREAM)
        connSkt.connect((tgtHost,tgtPort))
        connSkt.send(b'ViolentPython\r\n')
        results = connSkt.recv(100)
        # 输出时加锁
        screenLock.acquire()
        print('[+] %d/tcp open'%tgtPort)
        print('[+] %s'%str(results))
    except:
        screenLock.acquire()
        print('[-] %d/tcp closed'%tgtPort)
    finally:
        screenLock.release()
        connSkt.close()

# 特定主机的端口们扫描
def portScan(tgtHost, tgtPorts):
    # 域名解析为IP
    try:
        tgtIP = gethostbyname(tgtHost)
    except:
        print("[-] Cannot resolve '%s': Unknown host" %tgtHost)
        return
    # IP获取主机名
    try:
        tgtName = gethostbyaddr(tgtIP)
        print('\n[+] Scan Results for: '+tgtName[0])
    except:
        print('\n[+] Scan Results for: '+tgtIP)
    # 设置超时时间？
    setdefaulttimeout(1)
    # 遍历所有端口
    for tgtPort in tgtPorts:
        # print('Scanning port: '+tgtPort)
        # connScan(tgtHost, int(tgtPort))
        # 多线程，每个端口创建一个线程
        '''
            如果0-65535这么多端口，意味着我要创建这么多的线程，能不能我创建10个线程，然后这10个线程并发执行呢？
            难点在于这些线程如何分配任务
        '''
        t = Thread(target=connScan, args=(tgtHost, int(tgtPort)))
        t.start()

def main():
    # 输入命令
    parser = optparse.OptionParser('usage%prog -H <target host> -p <target prot>')
    parser.add_option('-H', dest='tgtHost', type='string', help='specify taget host')
    parser.add_option('-p', dest='tgtPort', type='string', help='specify target port[s] seperated by comma')
    (options, args) = parser.parse_args()
    if options.tgtHost == None or options.tgtPort == None:
        print('[-] You must specify a target host and port[s].\n%s'%parser.usage)
        exit(0)
    tgtHost = options.tgtHost
    tgtPorts = options.tgtPort.split(',')
    # 端口扫描
    portScan(tgtHost, tgtPorts)

if __name__ == '__main__':
    main()


















