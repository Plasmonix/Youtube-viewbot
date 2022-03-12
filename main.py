import os
import random
from time import sleep
from selenium import webdriver
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

PURPLE = '\033[95m'
CYAN = '\033[36m'
BLUE = '\033[34m'
GREEN = '\033[32m'
YELLOW = '\033[93m'
RED = '\033[91m'
BROWN = "\033[33m"
END = '\033[0m'

def banner():
    os.system('cls && title [YT View Bot v2] - Made by Plasmonix' if os.name == "nt" else 'clear') 
    text = """                          
                     ▓██   ██▓▄▄▄█████▓    ██▒   █▓ ██▓▓█████  █     █░    ▄▄▄▄    ▒█████  ▄▄▄█████▓
                      ▒██  ██▒▓  ██▒ ▓▒   ▓██░   █▒▓██▒▓█   ▀ ▓█░ █ ░█░   ▓█████▄ ▒██▒  ██▒▓  ██▒ ▓▒
                       ▒██ ██░▒ ▓██░ ▒░    ▓██  █▒░▒██▒▒███   ▒█░ █ ░█    ▒██▒ ▄██▒██░  ██▒▒ ▓██░ ▒░
                       ░ ▐██▓░░ ▓██▓ ░      ▒██ █░░░██░▒▓█  ▄ ░█░ █ ░█    ▒██░█▀  ▒██   ██░░ ▓██▓ ░ 
                       ░ ██▒▓░  ▒██▒ ░       ▒▀█░  ░██░░▒████▒░░██▒██▓    ░▓█  ▀█▓░ ████▓▒░  ▒██▒ ░ 
                        ██▒▒▒   ▒ ░░         ░ ▐░  ░▓  ░░ ▒░ ░░ ▓░▒ ▒     ░▒▓███▀▒░ ▒░▒░▒░   ▒ ░░   
                      ▓██ ░▒░     ░          ░ ░░   ▒ ░ ░ ░  ░  ▒ ░ ░     ▒░▒   ░   ░ ▒ ▒░     ░    
                      ▒ ▒ ░░    ░              ░░   ▒ ░   ░     ░   ░      ░    ░ ░ ░ ░ ▒    ░      
                      ░ ░                       ░   ░     ░  ░    ░        ░          ░ ░           
                      ░ ░                      ░                                ░                   
 """
    faded = ""
    blue = 100
    for line in text.splitlines():
        faded += (f"\033[38;2;0;255;{blue}m{line}\033[0m\n")
        if not blue == 255:
            blue += 15
            if blue > 255:
                blue = 255
    print(faded)
    print(YELLOW + "                                       github.com/Plasmonix Version 2.0 \n" + END)
banner()

ua = UserAgent()
proxies = []

def load_proxies():
    try:
        proxyfile = open(fp, "r+").readlines()
        for proxy in proxyfile:
            ip = proxy.split(":")[0]
            port = proxy.split(":")[1]
            proxies.append({
                'ip': ip.rstrip("\n"),
                'port' : port.rstrip("\n")})
    except:
           print(RED + " [!] File not found " + END)
           quit()

def scrape_proxies():
    try:
        proxies_req = Request('https://www.sslproxies.org/')
        proxies_req.add_header('User-Agent', ua.random)
        proxies_doc = urlopen(proxies_req).read().decode('utf8')
        soup = BeautifulSoup(proxies_doc, 'html.parser')
        proxies_table = soup.find('table', attrs={'class': 'table table-striped table-bordered'})
        for row in proxies_table.tbody.find_all('tr'):
            proxies.append({
                    'ip':   row.find_all('td')[0].string,
                    'port': row.find_all('td')[1].string})
    except:
        print(RED + " [!] Failed to scrape proxies " + END)
        quit()

def random_proxy(proxies):
    return random.choice(proxies)

try:
   url = input(BLUE + " [*] Enter video url> " + END)
   views = int(input(CYAN + " [*] Enter number of views> " + END))
   min_watch = int(input(BROWN + " [*] Enter minimum watchtime (in seconds)> " + END))
   max_watch = int(input(PURPLE + " [*] Enter maximum watchtime (in seconds)> " + END))
   choice = input(RED + " [!] Do you want to use custom proxies ? Y/n> " + END).lower()
   if choice == 'y':
       fp = input(YELLOW + " [*] Path to proxyfile> " +END)
       load_proxies()
       proxy = random_proxy(proxies)
   elif choice == 'n':
        scrape_proxies()
        proxy = random_proxy(proxies)
except ValueError: 
       print(RED + " [!] Invalid value" + END)
       quit()

def load_url(ua, sleep_time, proxy):
    options = webdriver.ChromeOptions()
    options.add_argument('--proxy-server=%s' %
            (proxy['ip'] + ':' + proxy['port']))
    options.add_argument('user-agent=%s' % ua.random)
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    #browser_driver = path/to/webdriver
    #driver = webdriver.Chrome(executable_path=browser_driver, options=options)
    driver = webdriver.Chrome(options=options)
    driver.get(url)
    sleep(sleep_time)
    driver.quit()

if __name__ == "__main__":
    for i in range(views):
        sleep_time = random.randint(min_watch,max_watch)
        load_url(ua, sleep_time, proxy)
        print(GREEN + " [*] Adding views " + END)
