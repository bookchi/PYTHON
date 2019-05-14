import zipfile
import optparse
from threading import Thread

def extractFile(zFile, passwd):
    try:
        zFile.extractall(pwd=passwd.encode())
        print('[+] Found password: %s' %passwd)
    except Exception as e:
        pass

def main():
    # construct command
    parser = optparse.OptionParser('usage%prog -f <zipfile> -d <dictionary>')
    parser.add_option('-f', dest='zname',type='string',help='specify zip file')
    parser.add_option('-d', dest='dname',type='string',help='specify dictionary file')
    (options, args) = parser.parse_args()
    if options.zname==None or options.dname==None:
        print(parser.usage)
        exit(0)
    else:
        zname = options.zname
        dname = options.dname
    zFile = zipfile.ZipFile(zname)
    passFile = open(dname,'r')
    for line in passFile.readlines():
        passwd = line.strip('\n')
        # a thread for each passwd
        t = Thread(target=extractFile,args=(zFile,passwd))
        t.start()
if __name__ == '__main__':
    main()

