#!/usr/bin/python3

import sys
import re
import requests
import time
import argparse
import threading
import random
from queue import Queue
from bs4 import BeautifulSoup
from requests.exceptions import RequestException

class SpiderUniprot(threading.Thread):
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36'
    }
    proxy_target = 'http://www.xicidaili.com/nn/' + str(random.randint(2, 20))
    ip_list = []
    def __init__(self):
        self.proxy_queue = Queue()
        self.thread_num = 50
        self.proxies = {}
        self.infile = sys.argv[1]
        self.dict = {}
        self.line_queue = Queue()

    def get_proxies(self):
        response = requests.get(self.proxy_target, headers = self.headers).text
        tr = BeautifulSoup(response, 'lxml').find_all('tr')
        for i in range(1, len(tr)):
            ip_info = tr[i]
            tds = ip_info.find_all('td')
            ip = tds[1].text + ':' + tds[2].text
            self.proxy_queue.put(ip)

    def try_proxies(self):
        while not self.proxy_queue.empty():
            ip = self.proxy_queue.get()
            try:
                proxy_host = "https://" + ip
                proxy_temp = {"https": proxy_host}
                requests.get('https://www.uniprot.org', headers = self.headers, proxies=proxy_temp,timeout = 3)
                SpiderUniprot.ip_list.append(ip)
            except RequestException:
                continue
    
    def run_proxy(self):
        sys.stderr.write("Start to get proxies...\n")
        while(len(self.ip_list) < 5):
            length = len(SpiderUniprot.ip_list)
            sys.stderr.write("Current avaliable proxies:%d The program will continue until there are 5 proxies...\n" %length)
            self.get_proxies()
            ths = []
            for _ in range(self.thread_num):
                th = threading.Thread(target=self.try_proxies)
                th.start()
                ths.append(th)
            for th in ths:
                th.join()
        length = len(SpiderUniprot.ip_list)
        sys.stderr.write("Testing over, Proxies number:%d...\n" %length) 
    
    def get_random_ip(self):
        proxy_list = []
        for ip in SpiderUniprot.ip_list:
            proxy_list.append('http://' +  ip)
        proxy_ip = random.choice(proxy_list)
        self.proxies = {'http:':proxy_ip}
    
    def read_file(self):
        if not self.infile:
            sys.stderr.write("Input the file!\n")
            sys.exit()
        with open(self.infile, 'r') as file_obj:
            for line in file_obj:
                line = line.strip()
                a = line.split("\t")
                self.dict[a[1]] = a[0]
                self.line_queue.put(a[1])

    def get_page(self, url):
        self.get_random_ip()
        try:
            response = requests.get(url, headers = self.headers, proxies = self.proxies)
            if response.status_code == 200:
                return response.text
            return None
        except RequestException:
            return None
    
    def step_one(self, text):
        text = str(text)
        pattern = re.compile('<tr id="(.*?)" class=" entry selected-row">|</td><td class="entryID"><a href="/uniprot/.*?">(.*?)</a>')
        items = re.findall(pattern, text)
        if items:
            entry = items[0][0]
            return entry

    def step_two(self, text):
        pattern1 = re.compile('<div id="content-gene" class="entry-overview-content"><h2>(.*?)</h2></div>|<div id="content-gene" class="entry-overview-content"><h2>(.*?)</h2> <a href="#gene_name_table">')
        text = str(text)
        item1 = re.findall(pattern1, text)
        gene = '-'
        if  len(item1) != 0:
            gene = item1[0][0]
        pattern2 = re.compile('</script><meta content="(.*?)" name="description"/>')
        item2 = re.findall(pattern2, text)
        func = '-'
        if len(item2) != 0:
            func = item2[0]
        info = [gene, func]
        return info
    
    def change_form(self):
        self.read_file()
        while not self.line_queue.empty():
            name = self.line_queue.get()
            url1 = "https://www.uniprot.org/uniprot/?query=" + name + "&sort=score"
            content1 = self.get_page(url1)
            entry = self.step_one(content1)
            if not entry:
                res = "-"
                func = "-"
                entry = ''
            url2 = "https://www.uniprot.org/uniprot/" + entry
            content2 = self.get_page(url2)
            info = self.step_two(content2)
            res = "-"
            func = "-"
            if info[0]:
                res = info[0]
            if info[1]:
                func = info[1]
            print(self.dict[name] + "\t" + str(name) + "\t" + str(res) + "\t" + str(func))
    
    def run_function(self):
        sys.stderr.write("Start to search function...\n")
        ths = []
        for _ in range(self.thread_num):
            th = threading.Thread(target=self.change_form)
            th.start()
            ths.append(th)
        for th in ths:
            th.join()
        sys.stderr.write("Function searching over...\n")

if __name__ == '__main__':
    SpiderUniprot().run_proxy()
    SpiderUniprot().run_function()