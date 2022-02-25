import os
import random
from selenium import webdriver
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from time import sleep

PURPLE = '\033[95m'
CYAN = '\033[36m'
BLUE = '\033[34m'
GREEN = '\033[32m'
YELLOW = '\033[93m'
RED = '\033[91m'
BROWN = "\033[33m"
END = '\033[0m'

def banner():
	os.system('cls && title [YT View Bot v1] - Made by Plasmonix' if os.name == "nt" else 'clear') 
	print(RED + """
                ██╗   ██╗████████╗    ██╗   ██╗██╗███████╗██╗    ██╗    ██████╗  ██████╗ ████████╗
                ╚██╗ ██╔╝╚══██╔══╝    ██║   ██║██║██╔════╝██║    ██║    ██╔══██╗██╔═══██╗╚══██╔══╝
                 ╚████╔╝    ██║       ██║   ██║██║█████╗  ██║ █╗ ██║    ██████╔╝██║   ██║   ██║   
                  ╚██╔╝     ██║       ╚██╗ ██╔╝██║██╔══╝  ██║███╗██║    ██╔══██╗██║   ██║   ██║   
                   ██║      ██║        ╚████╔╝ ██║███████╗╚███╔███╔╝    ██████╔╝╚██████╔╝   ██║   
                   ╚═╝      ╚═╝         ╚═══╝  ╚═╝╚══════╝ ╚══╝╚══╝     ╚═════╝  ╚═════╝    ╚═╝
  
                                     """ + END + BLUE + """github.com/Plasmonix  Version 1.0 \n""" + END)  
banner()

try :
   url = input(YELLOW + """ [*] Enter video url> """ + END)
   views = int(input(CYAN + """ [*] Enter number of views> """ + END))
   min_watch = int(input(BROWN + """ [*] Enter minimum watchtime (in seconds)> """ + END))
   max_watch = int(input(PURPLE + """ [*] Enter maximum watchtime (in seconds)> """ + END))

except ValueError : 
       print(RED + """ [*] Invalid value """ + END)

def get_proxies(ua):
    proxies = []
    proxies_req = Request('https://www.sslproxies.org/')
    proxies_req.add_header('User-Agent', ua.random)
    proxies_doc = urlopen(proxies_req).read().decode('utf8')
    soup = BeautifulSoup(proxies_doc, 'html.parser')
    proxies_table = soup.find('table', attrs={'class': 'table table-striped table-bordered'})
    for row in proxies_table.tbody.find_all('tr'):
        proxies.append({
            'ip':   row.find_all('td')[0].string,
            'port': row.find_all('td')[1].string})
    return proxies

def random_proxy(proxies):
    return random.choice(proxies)

def load_url(ua, sleep_time, proxy, proxies):
    options = webdriver.ChromeOptions()
    options.add_argument('--proxy-server=%s' %
            (proxy['ip'] + ':' + proxy['port']))
    options.add_argument('user-agent=%s' % ua.random)
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    #browser_driver = path/to/webdriver
    #driver = webdriver.Chrome(executable_path=browser_driver, options=chromeOptions)
    driver = webdriver.Chrome(options=options)
    driver.get(url)
    sleep(sleep_time)
    driver.quit()

if __name__ == "__main__":
    for i in range(views):
        ua = UserAgent()
        proxies = get_proxies(ua)
        sleep_time = random.randint(min_watch,max_watch)
        proxy = random_proxy(proxies)
        load_url(ua, sleep_time, proxy, proxies)
        print(GREEN + """ [*] Adding views  """ + END)
