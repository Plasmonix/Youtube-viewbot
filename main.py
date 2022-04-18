import os,random
from time import sleep
from selenium import webdriver
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

# Credit to Pycenter by billythegoat356
# Github: https://github.com/billythegoat356/pycenter/
# License: https://github.com/billythegoat356/pycenter/blob/main/LICENSE

def center(var:str, space:int=None): # From Pycenter
    if not space:
        space = (os.get_terminal_size().columns - len(var.splitlines()[int(len(var.splitlines())/2)])) / 2
    
    return "\n".join((' ' * int(space)) + var for var in var.splitlines())

class Fore:
    YELLOW = '\033[93m'
    GREEN = '\033[32m'
    RED = '\033[91m'
    CYAN = '\033[36m'
    RESET = '\033[0m' 

proxies = []
    
def banner():
    os.system('cls && title [YT View Bot v2] - Made by Plasmonix' if os.name == "nt" else 'clear') 
    text = '''                          
                     ▓██   ██▓▄▄▄█████▓    ██▒   █▓ ██▓▓█████  █     █░    ▄▄▄▄    ▒█████  ▄▄▄█████▓
                      ▒██  ██▒▓  ██▒ ▓▒   ▓██░   █▒▓██▒▓█   ▀ ▓█░ █ ░█░   ▓█████▄ ▒██▒  ██▒▓  ██▒ ▓▒
                       ▒██ ██░▒ ▓██░ ▒░    ▓██  █▒░▒██▒▒███   ▒█░ █ ░█    ▒██▒ ▄██▒██░  ██▒▒ ▓██░ ▒░
                       ░ ▐██▓░░ ▓██▓ ░      ▒██ █░░░██░▒▓█  ▄ ░█░ █ ░█    ▒██░█▀  ▒██   ██░░ ▓██▓ ░ 
                       ░ ██▒▓░  ▒██▒ ░       ▒▀█░  ░██░░▒████▒░░██▒██▓    ░▓█  ▀█▓░ ████▓▒░  ▒██▒ ░ 
                        ██▒▒▒   ▒ ░░         ░ ▐░  ░▓  ░░ ▒░ ░░ ▓░▒ ▒     ░▒▓███▀▒░ ▒░▒░▒░   ▒ ░░   
                      ▓██ ░▒░     ░          ░ ░░   ▒ ░ ░ ░  ░  ▒ ░ ░     ▒░▒   ░   ░ ▒ ▒░     ░    
                      ▒ ▒ ░░    ░              ░░   ▒ ░   ░     ░   ░      ░    ░ ░ ░ ░ ▒    ░      
                      ░ ░                       ░   ░     ░  ░    ░        ░          ░ ░           
                      ░ ░                      ░                                ░                '''
    faded = ''
    cyan = 100
    for line in text.splitlines():
        faded += (f"\033[38;2;0;255;{cyan}m{line}\033[0m\n")
        if not cyan == 255:
            cyan += 15
            if cyan > 255:
                cyan = 255
    print(center(faded))
    print(center(f'{Fore.YELLOW}\ngithub.com/Plasmonix Version 2.0{Fore.RESET}'))

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
           print(f'[{Fore.RED}!{Fore.RESET}] {Fore.RED}File not found{Fore.RESET}')
           quit()

ua = UserAgent()
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
        print(f'[{Fore.RED}!{Fore.RESET}] {Fore.RED}Failed to scrape proxies{Fore.RESET}')
        quit()

def load_url(ua, sleeptime, proxy):
    options = webdriver.ChromeOptions()
    options.add_argument('--proxy-server=%s' % (proxy['ip'] + ':' + proxy['port']))
    options.add_argument('user-agent=%s' % ua.random)
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    #Uncomment below if you don't have chromedriver.exe in root folder
    #browser_driver = path/to/webdriver
    #driver = webdriver.Chrome(executable_path=browser_driver, options=options)
    driver = webdriver.Chrome(options=options)
    driver.get(url)
    sleep(sleeptime)
    driver.quit()

if __name__ == "__main__":
    banner()
    try:
        url = input(f'[{Fore.CYAN}*{Fore.RESET}] Enter video url> ')
        views = int(input(f'[{Fore.CYAN}*{Fore.RESET}] Enter number of views> '))
        minwatch = int(input(f'[{Fore.CYAN}*{Fore.RESET}] Enter minimum watchtime (in seconds)> '))
        maxwatch = int(input(f'[{Fore.CYAN}*{Fore.RESET}] Enter maximum watchtime (in seconds)> '))
        customproxies = input(f'[{Fore.CYAN}?{Fore.RESET}] Do you want to use custom proxies ? Y/n> ').lower()
        if customproxies == 'y':
            fp = input(f'[{Fore.CYAN}*{Fore.RESET}] Path to proxyfile> ')
            load_proxies()
        elif customproxies == 'n':
            scrape_proxies()
        else:
             print(f'[{Fore.RED}!{Fore.RESET}] {Fore.RED}Please enter a valid choice such as Y or n!{Fore.RESET}')
             quit()
    except ValueError: 
       print(f'[{Fore.RED}!{Fore.RESET}] {Fore.RED}Value must be an integer{Fore.RESET}')
       quit()

    os.system('cls')
    banner()
    for i in range(views):
        sleeptime = random.randint(minwatch,maxwatch)
        proxy = random.choice(proxies)
        load_url(ua, sleeptime, proxy)
