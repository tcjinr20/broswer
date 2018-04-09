
from urllib import request

import os
def getAPNIC():
    url="http://ftp.apnic.net/apnic/stats/apnic/delegated-apnic-latest"
    request2 = request.Request(url)
    request2.add_header('user-agent', 'Mozilla/5.0')
    response2 = request.urlopen(request2)
    html2 = response2.read()
    mystr2 = html2.decode("utf8")
    response2.close()
    with open('apnic.txt','w') as f:
        f.write(mystr2)
        f.close()
    return mystr2

def praseApnic():
    try:
        fl=open("apnic.txt",'r')
    except Exception as e:
        getAPNIC()
        return praseApnic()
    ipvpack=[]
    while True:
        line=fl.readline(10240)
        arr = line.split('|')
        if len(arr)>5 and arr[2]=="ipv4" and arr[3] != "*":
            ipvpack.append([arr[3],arr[4],arr[1]])
        if not line:
            break
    return ipvpack

def ip4Section(start,num):

    # start = start.split('.')
    # start_a = dec2bin80(start[0])
    # start_b = dec2bin80(start[1])
    # start_c = dec2bin80(start[2])
    # start_d = dec2bin80(start[3])
    # start_bin = start_a + start_b + start_c + start_d
    # # 将二进制代码转化为十进制
    # start_dec = bin2dec(start_bin)
    # end_dec=int(start_dec)+num
    # address_bin = dec2bin320(end_dec)
    # # # 分割IP，转化为十进制
    # address_a = bin2dec(address_bin[0:8])
    # address_b = bin2dec(address_bin[8:16])
    # address_c = bin2dec(address_bin[16:24])
    # address_d = bin2dec(address_bin[24:32])
    # address = address_a + '.' + address_b + '.' + address_c + '.' + address_d
    # return address
    ips = start.split('.')
    if len(ips)!=4:
        return 0
    for i in range(len(ips)):
        ips[i]=int(ips[i])

    while num>0:
        num-=1
        if ips[3]>255:
            ips[2]+=1
            ips[3]=0

        ips[3] += 1
        if ips[3]>255:
            ips[2]+=1
            ips[3]=0
        if ips[2]>255:
            ips[1]+=1
            ips[2]=0
        if ips[1]>255:
            ips[0]+=1
            ips[1]=0

        if ips[0]>255 :raise AttributeError("the num is wrong")
    return '.'.join(str(i) for i in ips)

def saveIpsection():
    apnic=praseApnic()
    for m in apnic:
        n=ip4Section(m[0],int(m[1]))
        txt=m[0]+"-"+n
        saveIP(m[2],txt)
    return foldnum

foldnum={}
def saveIP(name,txt):
    fold='ip'
    if not os.path.exists(fold):
        os.makedirs(fold)
    if name not in foldnum:
        foldnum[name]=0
    else:
        foldnum[name]+=1
    fn = fold + "/" + name + ".txt"
    ff = open(fn, 'a',encoding="utf-8")
    ff.writelines([txt,'\r'])
    ff.flush()
    ff.close()

if __name__ == '__main__':
    # saveIpsection()
    ff = open("t.txt", 'a', encoding="utf-8")
    ff.writelines(['123', '\n\r'])
    ff.flush()
    ff.close()




