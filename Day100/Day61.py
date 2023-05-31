# 网络数据采集概述
import whois as whois

if __name__ == '__main__':
    w = whois.whois('https://www.bootcss.com')
    print(w)
