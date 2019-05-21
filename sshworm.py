import pexpect

PROMPT = ['# ', '>>> ', '> ', '\$ ','~']

# ssh连接成功后，执行并打印命令
def send_command(child, cmd):
    child.sendline(cmd)
    child.expect(PROMPT)
    print(child.before.decode())

# ssh连接     - 少了端口，如果改掉了端口，则不能进行有效连接。最好和端口扫描结合起来
def connect(user, host, passwd):
    ssh_newkey = 'Are you sure you want to continue connecting'
    connStr = 'ssh '+user+'@'+host
    # 产生一个新的进/线程
    child = pexpect.spawn(connStr)
    # 预测提示
    ret = child.expect([pexpect.TIMEOUT, ssh_newkey,
                         "password:",'Connection refused'])
    # 根据提示发送命令
    if ret == 0:
        print('[-] Error Connecting')
        return
    if ret == 1:
        child.sendline('yes')
        ret = child.expect([pexpect.TIMEOUT,  'password:'])
        if ret==0:
            print('[-] Error Connecting')
            return
        child.sendline(passwd)
        child.expect(PROMPT)
        return child
    if ret == 2:
        print('trying...')
        child.sendline(passwd)
        child.expect(PROMPT)
        return child
    else:
        print('Connection refused')
        exit(0)

def main():
    host,user,passwd = input('Enter host,user,passwd split by space:').split(' ')
    child = connect(user, host, passwd)
    send_command(child, 'pwd')

if __name__ == '__main__':
    main()
