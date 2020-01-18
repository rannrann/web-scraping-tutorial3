import requests
from bs4 import BeautifulSoup
import random
import urllib
import urllib3

headers = {
        "Proxy-Connection": "keep-alive",
        "Pragma": "no-cache",
        "Cache-Control": "no-cache",
        "User-Agent": "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "DNT": "1",
        "Accept-Encoding": "gzip, deflate, sdch",
        "Accept-Language": "zh-CN,zh;q=0.8,en-US;q=0.6,en;q=0.4",
        "Referer": "https://www.baidu.com/s?wd=%BC%96%E7%A0%81&rsv_spt=1&rsv_iqid=0x9fcbc99a0000b5d7&issp=1&f=8&rsv_bp=1&rsv_idx=2&ie=utf-8&rqlang=cn&tn=baiduhome_pg&rsv_enter=0&oq=If-None-Match&inputT=7282&rsv_t=3001MlX2aUzape9perXDW%2FezcxiDTWU4Bt%2FciwbikdOLQHYY98rhPyD2LDNevDKyLLg2&rsv_pq=c4163a510000b68a&rsv_sug3=24&rsv_sug1=14&rsv_sug7=100&rsv_sug2=0&rsv_sug4=7283",
        "Accept-Charset": "gb2312,gbk;q=0.7,utf-8;q=0.7,*;q=0.7",
    }


def get_ip_HTMLText(url,proxies):
    try:
        r = requests.get(url,proxies=proxies)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
    except:
        return 0
    else:
        return r.text

def get_ip_list(url):
    web_data = requests.get(url,headers=headers,verify=False).content.decode('utf-8')
    soup = BeautifulSoup(web_data, "html.parser")
    ips = soup.find_all('tr')
    ip_list = []
    for i in range(1, len(ips)):
        ip_info = ips[i]
        tds = ip_info.find_all('td')
        ip_list.append(tds[1].text + ':' + tds[2].text)
#检测ip可用性，移除不可用ip：（这里其实总会出问题，你移除的ip可能只是暂时不能用，剩下的ip使用一次后可能之后也未必能用）
    for ip in ip_list:
        try:
          proxy_host = "http://" + ip
          proxy_temp = {"http": proxy_host}
          res = urllib.urlopen(url, proxies=proxy_temp).read()
        except Exception as e:
          ip_list.remove(ip)
          continue
    return ip_list

def get_random_ip(ip_list):
    proxy_list = []
    for ip in ip_list:
        proxy_list.append('http://' + ip)
    proxy_ip = random.choice(proxy_list)
    proxies = {'http': proxy_ip}
    return proxies


def get_information(url,proxies):
    try:
        html = requests.get(my_url, headers=headers, verify=False,proxies=proxies).content.decode('utf-8')
    except urllib3.exceptions.NewConnectionError:
        print("由于连接方在一段时间后没有正确答复或连接的主机没有反应，连接尝试失败。——urllib3")
    except requests.exceptions.ProxyError:
        print("由于连接方在一段时间后没有正确答复或连接的主机没有反应，连接尝试失败。——request")


    page_soup = BeautifulSoup(html, "html.parser")
    phonetic_symbols = page_soup.find_all("bdo")
    return [phonetic_symbols[0].string, phonetic_symbols[1].string]

if __name__ == '__main__':
    ip_url = 'http://www.xicidaili.com/nn/'
    my_url = 'http://dict.cn/word'
    ip_list = get_ip_list(ip_url)
    proxies = get_random_ip(ip_list)
    print(get_information(my_url,proxies))